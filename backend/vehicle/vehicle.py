"""
Date: 10/19/2021
Description: the code implements vehicles as threads. Each vehicle/thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests
import time
import random

from location_speed_encoding import Crossroads
from location_speed_encoding import Direction
from location_speed_encoding import MAP
from location_speed_encoding import Road
from location_speed_encoding import Route_completion_status
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import Speed
from location_speed_encoding import Traffic_light


polling_interval = 0.8


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
        self.direction = Direction.DIRECTION_LEFT
        self.location = 2
        self.speed = Speed.STOPPED
        self.location_visited = list()
        self.route_completion_status = Route_completion_status.NOT_STARTED
        self.current_time = 0   


    def update_backend(self):        

        payload = {}
        payload["road_segment"] = self.road_segment.value
        payload["direction"] = self.direction.value
        payload["location"] = self.location
        payload["vehicle_speed"] = self.speed.value
        payload["route_completion"] = self.route_completion_status.value
        payload["clock"] = self.current_time

        while True:

            time.sleep(polling_interval)

            response = requests.post("http://127.0.0.1:5000/set_vehicle_status/%d" \
                % (self.id), json=payload)
            
            if int(response.text) == (int(self.current_time) + 2):

                self.current_time = response.text  

                break       


    def crossroad_reached_check(self, last_road_segment, current_road_segment, target_crossroad):
        
        crossroad_list_last_road_segment = list()
        crossroad_list_current_road_segment = list()
        
        if MAP[last_road_segment][Direction.DIRECTION_LEFT] != {}:
            crossroad_list_last_road_segment.append(MAP[last_road_segment][Direction.DIRECTION_LEFT]["crossroad"])

        if MAP[last_road_segment][Direction.DIRECTION_RIGHT] != {}:
            crossroad_list_last_road_segment.append(MAP[last_road_segment][Direction.DIRECTION_RIGHT]["crossroad"])

        if MAP[current_road_segment][Direction.DIRECTION_LEFT] != {}:
            crossroad_list_current_road_segment.append(MAP[last_road_segment][Direction.DIRECTION_LEFT]["crossroad"])

        if MAP[current_road_segment][Direction.DIRECTION_RIGHT] != {}:
            crossroad_list_current_road_segment.append(MAP[last_road_segment][Direction.DIRECTION_RIGHT]["crossroad"])

        for crossroad in crossroad_list_last_road_segment:
            if crossroad in crossroad_list_current_road_segment:
                if crossroad == target_crossroad:
                    return True

        return False

    
    def remove_self_road_segment_from_dict(self, target_to_remove, dict):

        return_dict = {}

        for position_key in dict:

            if position_key != target_to_remove:

                return_dict[position_key] = dict[position_key]

        return return_dict 


    def get_road_segment(self, current_road_segment, current_crossroad):       
        
        if current_road_segment == Road.ROAD_A:
            return {"road_segment": [], "crossroad": {}}     

        for direction in MAP[current_road_segment]:
            
            if MAP[current_road_segment][direction]["crossroad"] != current_crossroad:
                crossroad_to_query = MAP[current_road_segment][direction]["crossroad"]
                road_segment_dict = MAP[crossroad_to_query]
                road_segment_list = list()

                road_segment_dict = self.remove_self_road_segment_from_dict(current_road_segment, road_segment_dict)

                for road_segment_position in road_segment_dict:
                    road_segment_list.append(road_segment_dict[road_segment_position])

                return {"road_segment": road_segment_list, "crossroad": crossroad_to_query}                


    def check_query_direction(self, self_crossroad_position, position_key):

        change_query_direction = False

        if self_crossroad_position == Signal_light_positions.SOUTH:
            if position_key == Signal_light_positions.EAST \
                or position_key == Signal_light_positions.NORTH:
                change_query_direction = False
            else:
                change_query_direction = True
        elif self_crossroad_position == Signal_light_positions.EAST:
            if position_key == Signal_light_positions.WEST \
                or position_key == Signal_light_positions.SOUTH:
                change_query_direction = False
            else:
                change_query_direction = True
        elif self_crossroad_position == Signal_light_positions.NORTH:
            if position_key == Signal_light_positions.SOUTH \
                or position_key == Signal_light_positions.WEST:
                change_query_direction = False
            else:
                change_query_direction = True
        elif self_crossroad_position == Signal_light_positions.WEST:
            if position_key == Signal_light_positions.EAST \
                or position_key == Signal_light_positions.NORTH:
                change_query_direction = False
            else:
                change_query_direction = True        

        return change_query_direction


    def query_vehicle_at_location(self, mode, change_direction, target_road_segment):

        if mode == "query_crossroad":
        
            direction_to_query = self.direction
            position_to_query = 29 - self.location

            if change_direction:  

                position_to_query = self.location          

                if self.direction == Direction.DIRECTION_RIGHT:

                    direction_to_query = Direction.DIRECTION_LEFT

                else:
                    direction_to_query = Direction.DIRECTION_RIGHT

            response = requests.get("http://127.0.0.1:5000/query_location/%d/%d" \
                            % (target_road_segment.value, direction_to_query.value)).json()

            # Return true if vehicle found at that location
            if response == {}:
                
                return False

            for vehicle in response:

                if response[vehicle]["vehicle_location"] == position_to_query:
                    
                    return True

            return False

        elif mode == "query_road_segment":           

            response = requests.get("http://127.0.0.1:5000/query_location/%d/%d" \
                            % (target_road_segment.value, self.direction.value)).json()

            if response == {}:
                
                return False

            if change_direction == False:

                for vehicle in response:                    

                    if self.direction == Direction.DIRECTION_RIGHT:

                        if response[vehicle]["vehicle_location"] == (self.location + 1):
                                
                            return True

                    elif self.direction == Direction.DIRECTION_LEFT:

                        if response[vehicle]["vehicle_location"] == (self.location - 1):
                            
                            return True

            elif change_direction == True:

                for vehicle in response:                    

                    if self.direction == Direction.DIRECTION_RIGHT:

                        if response[vehicle]["vehicle_location"] == (self.location - 1):
                                
                            return True

                    elif self.direction == Direction.DIRECTION_LEFT:

                        if response[vehicle]["vehicle_location"] == (self.location + 1):
                            
                            return True
            
            return False  


    def routing(self, current_crossroad, next_road_segment, target_crossroad):
        
        road_segment_list = list()       
        
        # Generate an exhaustive search of the routes
        step_2_current_crossroad = self.get_road_segment(next_road_segment, current_crossroad)["crossroad"]

        for step_1_road_segment in self.get_road_segment(next_road_segment, current_crossroad)["road_segment"]:            

            step_3_current_crossroad = self.get_road_segment(step_1_road_segment, step_2_current_crossroad)["crossroad"]

            for step_2_road_segment in self.get_road_segment(step_1_road_segment, step_2_current_crossroad)["road_segment"]:

                step_4_current_crossroad = self.get_road_segment(step_2_road_segment, step_3_current_crossroad)["crossroad"]

                for step_3_road_segment in self.get_road_segment(step_2_road_segment, step_3_current_crossroad)["road_segment"]:

                    step_5_current_crossroad = self.get_road_segment(step_3_road_segment, step_4_current_crossroad)["crossroad"]

                    for step_4_road_segment in self.get_road_segment(step_3_road_segment, step_4_current_crossroad)["road_segment"]:

                        step_6_current_crossroad = self.get_road_segment(step_4_road_segment, step_5_current_crossroad)["crossroad"]

                        for step_5_road_segment in self.get_road_segment(step_4_road_segment, step_5_current_crossroad)["road_segment"]:

                            tmpp_road_segment_list = list()        

                            if current_crossroad == target_crossroad:
                                
                                tmpp_road_segment_list = [next_road_segment]

                            elif step_2_current_crossroad == target_crossroad:

                                tmpp_road_segment_list = [next_road_segment, step_1_road_segment]

                            elif step_3_current_crossroad == target_crossroad:

                                tmpp_road_segment_list = [next_road_segment, step_1_road_segment, step_2_road_segment]

                            elif step_4_current_crossroad == target_crossroad:

                                tmpp_road_segment_list = [next_road_segment, step_1_road_segment, step_2_road_segment, step_3_road_segment]

                            elif step_5_current_crossroad == target_crossroad:

                                tmpp_road_segment_list = [next_road_segment, step_1_road_segment, step_2_road_segment, step_3_road_segment, step_4_road_segment]

                            elif step_6_current_crossroad == target_crossroad:

                                tmpp_road_segment_list = [next_road_segment, step_1_road_segment, step_2_road_segment, step_3_road_segment, step_4_road_segment, step_5_road_segment]

                            if len(tmpp_road_segment_list) != 0:
                            
                                road_segment_list.append(tmpp_road_segment_list)       
        
        minimum_route_length = 6

        for route in road_segment_list:

            if len(route) < minimum_route_length:

                minimum_route_length = len(route)                                 

        for route in road_segment_list:

            if len(route) > minimum_route_length:

                road_segment_list.remove(route)              

        if len(road_segment_list) == 1:

            # If only one route available
            # Return the one route            
            return road_segment_list[0]

        elif len(road_segment_list) == 0:

            return road_segment_list
        
        else:

            # If multiple routes available
            # Use a random number generator to pick            
            return road_segment_list[random.randint(0, len(road_segment_list) -1)]


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
                        % (self.id)).json()
                    
                    if response["response"] == "OK":

                        # If permission acquired, set the initial location
                        self.road_segment = Road.ROAD_A
                        self.direction = Direction.DIRECTION_LEFT
                        self.location = 1
                        self.speed = Speed.STOPPED
                        self.location_visited.clear()
                        self.route_completion_status = Route_completion_status.ENROUTE   
                        break

                    else:

                        self.update_backend()                                                                                                                       

            elif self.route_completion_status == Route_completion_status.ENROUTE:

                # If yes, proceed                
                # Make vehicle movement decisions

                if self.road_segment == Road.ROAD_A and self.direction == Direction.DIRECTION_RIGHT:
                    
                    # If moving on the right lane of ROAD_A: the finishing stage

                    if self.location == 1:

                        self.road_segment = Road.ROAD_A
                        self.direction = Direction.DIRECTION_LEFT
                        self.location = 2
                        self.speed = Speed.STOPPED
                        self.location_visited.clear()
                        self.route_completion_status = Route_completion_status.NOT_STARTED                           

                    else:

                        if self.query_vehicle_at_location("query_road_segment", False, self.road_segment):

                            self.speed = Speed.STOPPED                        

                        else:

                            self.speed = Speed.MOVING
                            self.location += 1                        
                    
                elif (self.location != 0 and self.location != 29) \
                    or (self.location == 29 and self.direction == Direction.DIRECTION_LEFT) \
                        or (self.location == 0 and self.direction == Direction.DIRECTION_RIGHT):
                    
                    if self.query_vehicle_at_location("query_road_segment", False, self.road_segment):
                        
                        self.speed = Speed.STOPPED

                    else:
                        
                        self.speed = Speed.MOVING

                        if self.direction == Direction.DIRECTION_LEFT:

                            self.location -= 1

                        elif self.direction == Direction.DIRECTION_RIGHT:

                            self.location += 1
                    
                elif (self.location == 0 \
                    and self.road_segment == Road.ROAD_G \
                        and self.direction == Direction.DIRECTION_LEFT \
                            and len(self.location_visited) == 3) \
                                or (self.location == 29 \
                                    and self.road_segment == Road.ROAD_E \
                                        and self.direction == Direction.DIRECTION_RIGHT \
                                            and len(self.location_visited) == 3):                                    
                    
                    # Waiting to finish the route
                    crossroad_to_query = Crossroads.CROSSROAD_Z

                    direction_to_query = Signal_light_positions.WEST

                    if self.road_segment != Road.ROAD_E:
                        direction_to_query = Signal_light_positions.NORTH
                    
                    # Get the traffic light signal
                    response = requests.get("http://127.0.0.1:5000/query_signal_lights/%d" \
                        % crossroad_to_query.value).json()
                   
                    signal_light = Traffic_light[response[direction_to_query.name]]                    

                    if signal_light == Traffic_light.RED:

                        # If red, do not move
                        self.speed = Speed.STOPPED                            

                    elif signal_light == Traffic_light.GREEN:
                        
                        if self.direction == Direction.DIRECTION_RIGHT:

                            if self.query_vehicle_at_location("query_crossroad", False, Road.ROAD_A):

                                self.speed = Speed.STOPPED

                            else:

                                self.speed = Speed.MOVING
                                self.location = 0
                                self.road_segment = Road.ROAD_A
                                self.direction = Direction.DIRECTION_RIGHT    

                        elif self.direction == Direction.DIRECTION_LEFT:

                            if self.query_vehicle_at_location("query_crossroad", True, Road.ROAD_A):

                                self.speed = Speed.STOPPED      

                            else:

                                self.speed = Speed.MOVING
                                self.location = 0
                                self.road_segment = Road.ROAD_A
                                self.direction = Direction.DIRECTION_RIGHT                                           

                elif self.location == 0 or self.location == 29:
                    
                    # If the vehicle were at the crossroad

                    # Get the right crossroad to query                    
                    crossroad_to_query = MAP[self.road_segment][self.direction]["crossroad"]
                    traffic_light_orientation = MAP[self.road_segment][self.direction]["traffic_light_orientation"]
                                        
                    # Get the traffic light signal
                    response = requests.get("http://127.0.0.1:5000/query_signal_lights/%d" \
                        % crossroad_to_query.value).json()

                    signal_light = Traffic_light[response[traffic_light_orientation.name]]                                                                                                

                    if signal_light == Traffic_light.RED:

                        # If red, do not move
                        self.speed = Speed.STOPPED                            

                    elif signal_light == Traffic_light.GREEN:
                        
                        # If green light, route   
                        # Get the list of road segments to query                                    

                        road_segment_to_query = {}
                        road_segment_to_query_selected = {}     

                        # Dummy value
                        self_crossroad_position = Signal_light_positions.NORTH    

                        for direction in MAP[crossroad_to_query]:

                            if MAP[crossroad_to_query][direction] != self.road_segment:

                                road_segment_to_query[direction] = MAP[crossroad_to_query][direction]
                                road_segment_to_query_selected[direction] = MAP[crossroad_to_query][direction]

                            if MAP[crossroad_to_query][direction] == self.road_segment:

                                self_crossroad_position = direction                                                              

                        for position_key in road_segment_to_query:

                            change_query_direction = self.check_query_direction(self_crossroad_position, position_key)                          

                            query_direction = self.direction

                            if change_query_direction:
                                if self.direction == Direction.DIRECTION_LEFT:
                                    query_direction = Direction.DIRECTION_RIGHT
                                elif self.direction == Direction.DIRECTION_RIGHT:
                                    query_direction = Direction.DIRECTION_LEFT
                           
                            # Ask if any vehicles were at the other side of the crossroad   
                            response = requests.get("http://127.0.0.1:5000/query_location/%d/%d" \
                                % (road_segment_to_query[position_key].value, query_direction.value)).json()                           

                            for vehicle_name in response:

                                if change_query_direction:

                                    if response[vehicle_name]["vehicle_location"] == self.location:
                                       
                                        try:
                                            road_segment_to_query_selected.pop(position_key)

                                            # If the postion_key has been removed once
                                            # Do not remove again
                                            break
                                        except KeyError as e:
                                            print("====================================")
                                            print("response")
                                            print(response)
                                            print("road_segment_to_query")
                                            print(road_segment_to_query)
                                            print("vehicle_%d   %s   " % (self.id, str(road_segment_to_query_selected)))
                                            print("1 vehicle_%d popping %s" % (self.id, vehicle_name))
                                            print(position_key)
                                            print("====================================")
                                   
                                else:

                                    if response[vehicle_name]["vehicle_location"] == (29 - self.location):
                                   
                                        try:
                                            road_segment_to_query_selected.pop(position_key)

                                            # If the postion_key has been removed once
                                            # Do not remove again
                                            break
                                        except KeyError as e:
                                            print("====================================")
                                            print("response")
                                            print(response)
                                            print("road_segment_to_query")
                                            print(road_segment_to_query)
                                            print("vehicle_%d   %s   " % (self.id, str(road_segment_to_query_selected)))
                                            print("2 vehicle_%d popping %s" % (self.id, vehicle_name))
                                            print(position_key)
                                            print("====================================")                                              
                        
                        # Make movement decision
                        if road_segment_to_query_selected == {}:
                            # All other sides of the crossroad have vehicles, stop moving
                            self.speed = Speed.STOPPED

                        elif len(road_segment_to_query_selected) == 1:

                            # If only route is available, take the route
                            self.speed = Speed.MOVING
                            
                            # Should be only one key-value pair
                            # Dummy value
                            road_segment_to_move_to = Road.ROAD_A
                            for position_key in road_segment_to_query_selected:
                                road_segment_to_move_to = road_segment_to_query_selected[position_key]                            

                            # If the vehicle goes past the crossroad
                            # Update the route completion status
                            if crossroad_to_query in MAP["target_crossroad"] and crossroad_to_query not in self.location_visited:

                                self.location_visited.append(crossroad_to_query)
                          
                            # Dummy value
                            position_key_tmpp = Signal_light_positions.EAST

                            for position_key in MAP[crossroad_to_query]:
                                if MAP[crossroad_to_query][position_key] == road_segment_to_move_to:
                                    position_key_tmpp = position_key
                                    break

                            change_query_direction = self.check_query_direction(self_crossroad_position, position_key_tmpp)                          

                            query_direction = self.direction

                            if change_query_direction:
                                if self.direction == Direction.DIRECTION_LEFT:
                                    self.direction = Direction.DIRECTION_RIGHT
                                elif self.direction == Direction.DIRECTION_RIGHT:
                                    self.direction = Direction.DIRECTION_LEFT

                            # Adjust the square index                                
                            if not change_query_direction:
                                self.location = 29 - self.location
                            else:
                                self.location = self.location
                            
                            self.road_segment = road_segment_to_move_to
                            self.speed = Speed.MOVING                                                         

                        else:
                            # If more than one route is available
                            # Need to make routing decision
                            route_candidate = list()   

                            if len(self.location_visited) == 3:

                                for next_road in road_segment_to_query_selected:

                                    # Avoid routing to the visited target crossroads                                
                                    tmpp_route = self.routing(crossroad_to_query, road_segment_to_query_selected[next_road], Crossroads.CROSSROAD_Z)

                                    if tmpp_route != []:
                                        route_candidate.append(tmpp_route)

                            else:

                                for target in MAP["target_crossroad"]:

                                    if target not in self.location_visited:
                                        
                                        for next_road in road_segment_to_query_selected:

                                            # Avoid routing to the visited target crossroads                                
                                            tmpp_route = self.routing(crossroad_to_query, road_segment_to_query_selected[next_road], target)

                                            if tmpp_route != []:
                                                
                                                route_candidate.append(tmpp_route)                                                            
                                    
                            # Choose the shortest route
                            shortest_route_length = 7                            

                            for route in route_candidate:

                                if len(route) < shortest_route_length:

                                    shortest_route_length = len(route)

                            for route in route_candidate:

                                if len(route) > shortest_route_length:

                                    route_candidate.remove(route)

                            route_index = 0

                            if len(route_candidate) > 1:                                

                                route_index = random.randint(0, len(route_candidate) - 1)                                            

                            route_to_be_taken = route_candidate[route_index]                          
                                                    
                            # Dummy value
                            position_key_tmpp = Signal_light_positions.EAST

                            for position_key in MAP[crossroad_to_query]:
                                if MAP[crossroad_to_query][position_key] == route_to_be_taken[0]:
                                    position_key_tmpp = position_key
                                    break

                            change_query_direction = self.check_query_direction(self_crossroad_position, position_key_tmpp)                          

                            query_direction = self.direction

                            if change_query_direction:
                                if self.direction == Direction.DIRECTION_LEFT:
                                    self.direction = Direction.DIRECTION_RIGHT
                                elif self.direction == Direction.DIRECTION_RIGHT:
                                    self.direction = Direction.DIRECTION_LEFT
                                                                   
                            if not change_query_direction:
                                self.location = 29 - self.location
                            else:
                                self.location = self.location
                            
                            self.road_segment = route_to_be_taken[0]
                            self.speed = Speed.MOVING                                                                           

            self.update_backend()            
                                                                                                          
            
        