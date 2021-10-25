"""
Date: 10/19/2021
Description: the code implements vehicles as threads. Each vehicle/thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests
import time


from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.direction import Direction
from location_speed_encoding.road import Road
from location_speed_encoding.route_completion_status import Route_completion_status
from location_speed_encoding.signal_light_positions import Signal_light_positions
from location_speed_encoding.speed import Speed
from location_speed_encoding.traffic_light import Traffic_light


polling_interval = 0.4


# Each vehicle in the traffic system is represented by a thread
# Class Vehicle inherits the threading library
# So that the Vehicle objects can make decisions and interact with the traffic system
class Vehicle(threading.Thread):
    def __init__(self, id) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes
        self.id = id
        self.road_segment = Road.ROAD_A
        self.previous_road_segment = Road.ROAD_A
        self.direction = Direction.DIRECTION_CLOCKWISE
        self.location = 0
        self.speed = Speed.STOPPED
        self.location_visited = list()
        self.route_completion_status = Route_completion_status.NOT_STARTED
        self.current_time = 0                
        self.target_crossroad = [Crossroads.CROSSROAD_B, Crossroads.CROSSROAD_C, Crossroads.CROSSROAD_D]


    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Vehicle %d running" % (self.id))

        while True:

            # Check if the vehicle is in the traffic system            
            if self.route_completion_status == Route_completion_status.NOT_STARTED:
                # If not, request permission to enter
                # Also update its location with dummy value                
                while True:
                    response = requests.get("http://127.0.0.1:5000/add_vehicle/%d" \
                        % (self.id))
                    
                    if response.text == "OK":
                        # If permission acquired, set the initial location
                        self.road_segment = Road.ROAD_A
                        self.direction = Direction.DIRECTION_CLOCKWISE
                        self.location = 0
                        self.speed = Speed.STOPPED
                        self.location_visited.clear()
                        self.route_completion_status = Route_completion_status.ENROUTE                        

                    payload = {}
                    payload["road_segment"] = self.road_segment.value
                    payload["direction"] = self.direction.value
                    payload["location"] = self.location
                    payload["vehicle_speed"] = self.speed.value
                    payload["route_completion"] = self.route_completion_status.value

                    response = requests.post("http://127.0.0.1:5000/set_vehicle_status/%d" \
                        % (self.id), json=payload)
                    
                    if response.text != self.current_time:
                        self.current_time = response.text
                        break                                                     
                    
                    time.sleep(polling_interval)

            elif self.route_completion == Route_completion_status.FINISHED:
            # If the vehicle just finished the route
            # Reset its status to NOT_STARTED
                while True:
                    self.road_segment = Road.ROAD_A
                    self.direction = Direction.DIRECTION_CLOCKWISE
                    self.location = 0
                    self.speed = Speed.STOPPED
                    self.location_visited.clear()
                    self.route_completion_status = Route_completion_status.NOT_STARTED

                    payload = {}
                    payload["road_segment"] = self.road_segment.value
                    payload["direction"] = self.direction.value
                    payload["location"] = self.location
                    payload["vehicle_speed"] = self.speed.value
                    payload["route_completion"] = self.route_completion_status.value

                    response = requests.post("http://127.0.0.1:5000/set_vehicle_status/%d" \
                        % (self.id), json=payload)
                    
                    if response.text != self.current_time:
                        self.current_time = response.text
                        break                                                     
                    
                    time.sleep(polling_interval)

            elif self.route_completion == Route_completion_status.ENROUTE:
            # If yes, proceed                
                # Make vehicle movement decisions
                if self.location != 0 and self.location != 29:
                # If not at any crossroad
                    response = requests.get("http://127.0.0.1:5000/query_location/%d/%d" \
                        % (self.road_segment.value, self.direction.value)).json()

                    # Handle cases when the vehicle is moving clockwise or anticlockwise
                    # Check whether any other vehicle is immediately before the vehicle itself
                    for key in response:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            if response[key]["vehicle_location"] == self.location + 1:
                                self.speed = Speed.STOPPED
                            else:
                                self.speed = Speed.MOVING
                                self.location += 1
                        elif self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            if response[key] == self.location - 1:
                                self.speed = Speed.STOPPED
                            else:
                                self.speed = Speed.MOVING
                                self.location -= 1
                    
                elif self.location == 0 or self.location == 29:
                    # If the vehicle were at the crossroad

                    # Ask for traffic light status if visible
                    crossroad_to_query = Crossroads.CROSSROAD_Z
                    traffic_light_orientation = Signal_light_positions.EAST

                    if self.road_segment == Road.ROAD_A:
                        crossroad_to_query = Crossroads.CROSSROAD_Z
                        traffic_light_orientation = Signal_light_positions.EAST
                    elif self.road_segment == Road.ROAD_E:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_X
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_Z
                            traffic_light_orientation = Signal_light_positions.WEST
                    elif self.road_segment == Road.ROAD_F:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_D
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_X
                            traffic_light_orientation = Signal_light_positions.WEST
                    elif self.road_segment == Road.ROAD_G:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_Z
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_Y
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_H:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_X
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_U
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_I:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_D
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_W
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_J:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_U
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_Y
                            traffic_light_orientation = Signal_light_positions.WEST
                    elif self.road_segment == Road.ROAD_K:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_W
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_U
                            traffic_light_orientation = Signal_light_positions.WEST
                    elif self.road_segment == Road.ROAD_L:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_Y
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_B
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_M:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_U
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_V
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_N:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_W
                            traffic_light_orientation = Signal_light_positions.NORTH
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_C
                            traffic_light_orientation = Signal_light_positions.SOUTH
                    elif self.road_segment == Road.ROAD_O:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_V
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_B
                            traffic_light_orientation = Signal_light_positions.WEST
                    elif self.road_segment == Road.ROAD_P:
                        if self.direction == Direction.DIRECTION_CLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_C
                            traffic_light_orientation = Signal_light_positions.EAST
                        if self.direction == Direction.DIRECTION_ANTICLOCKWISE:
                            crossroad_to_query = Crossroads.CROSSROAD_V
                            traffic_light_orientation = Signal_light_positions.WEST
                    
                    response = requests.get("http://127.0.0.1:5000/query_signal_lights/%d" \
                        % crossroad_to_query.value).json()

                    signal_light = Traffic_light(response[traffic_light_orientation.name])                                                                                                

                    if signal_light == Traffic_light.GREEN:
                    # If green light, move into the cross                        
                        self.speed = Speed.MOVING
                        self.previous_road_segment = self.road_segment
                        self.intersection = crossroad_to_query
                        
                        # TODO Check whether there is any vehicle in the crossroad

                    elif signal_light == Traffic_light.RED:
                    # If not, do not move
                        self.speed = Speed.STOPPED
                        self.previous_road_segment = self.road_segment
                            
                else:
                    # If the vehicle were in the crossroad
                    # Update the route completion status                   

                     # Ask for the congestion map
                    for road in Road:
                        for direction in Direction:
                            response = requests.get("http://127.0.0.1:5000/query_road_congestion/%d/%d" \
                                % (road.value, direction.value))                    

                    # Make movement decision      

                    pass         

                # Update the backend
                payload = {}
                payload["road_segment"] = self.road_segment.value
                payload["direction"] = self.direction.value
                payload["location"] = self.location
                payload["intersection"] = self.intersection.value
                payload["vehicle_speed"] = self.speed
                payload["route_completion"] = self.route_completion_status.value


                # Update the backend
                while True:
                    response = requests.post("http://127.0.0.1:5000/set_vehicle_status/%d" \
                        % (self.id), json=payload)
                    
                    if response.text != self.current_time:
                        self.current_time = response.text
                        break
                    else:
                        time.sleep(polling_interval)
            
        