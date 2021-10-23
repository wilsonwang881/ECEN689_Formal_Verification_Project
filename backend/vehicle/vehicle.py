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
from location_speed_encoding.traffic_light import Traffic_light


polling_interval = 0.4


# Each vehicle in the traffic system is represented by a thread
# Class Vehicle inherits the threading library
# So that the Vehicle objects can make decisions and interact with the traffic system
class Vehicle(threading.Thread):
    def __init__(self, id, starting_location, speed, route_completion_status) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes
        self.id = id
        self.road_segment = 0
        self.direction = 0
        self.location = 0
        self.intersection = 0
        self.speed = 0
        self.route_completion = Route_completion_status.NOT_STARTED
        self.location_visited = list()
        self.route_completion_status = route_completion_status
        self.current_time = 0                


    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Vehicle %d running" % (self.id))

        while True:

            # Ask for the congestion map
            for road in Road:
                for direction in Direction:
                    response = requests.get("http://127.0.0.1:5000/query_road_congestion/%d/%d" \
                        % (road.value, direction.value))

            # Ask for traffic light status if visible
            for crossroad in Crossroads:
                response = requests.get("http://127.0.0.1:5000/query_signal_lights/%d" \
                    % crossroad.value)

            # Make movement decision
            payload = {}
            payload["road_segment"] = self.road_segment
            payload["direction"] = self.direction
            payload["location"] = self.location
            payload["intersection"] = self.intersection
            payload["speed"] = self.speed
            payload["route_completion"] = self.route_completion.name


            # Update the backend
            while True:
                response = requests.post("http://127.0.0.1:5000/set_vehicle_status/%d" \
                    % (self.id), json=payload)
                
                if response.text != self.current_time:
                    self.current_time = response.text
                    break
                else:
                    time.sleep(polling_interval)

            # Update its currrent location            
            
        