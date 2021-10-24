"""
Date: 10/19/2021
Description: the code implements congestion calculation as threads. Each thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests
import time
from location_speed_encoding import Crossroads
from location_speed_encoding import Direction
from location_speed_encoding import Road
from location_speed_encoding import Signal_light_positions


polling_interval = 0.4


class Congestion_Computation(threading.Thread):
    def __init__(self, road_responsible) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes        
        self.road_segment = Road(road_responsible)
        self.congestion_index_clockwise = 0
        self.congestion_index_anticlockwise = 0
        self.vehicle_list_clockwise = {}
        self.vehicle_list_anticlockwise = {}
        self.current_time = 0

    
    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Cogestion computation worker %d running" % (self.road_segment.value))

        while True:

            # TODO: change the congestion computation to: average vehicle speed

            # Get a list of vehicles on the road            
            for direction in Direction:
                response = requests.get("http://127.0.0.1:5000/query_location/%d/%d/%d" \
                    % (self.road_segment.value, direction.value, 0))

                if direction == Direction.DIRECTION_CLOCKWISE:
                    self.vehicle_list_clockwise = response.json()
                else:
                    self.vehicle_list_anticlockwise = response.json()

            # Update local record
            self.congestion_index_clockwise = len(self.vehicle_list_clockwise)
            self.congestion_index_anticlockwise = len(self.vehicle_list_anticlockwise)                        
            
            # Calculate the congestion

            # Send the updated congestion information back to the backend
            payload = {}
            payload[Direction.DIRECTION_CLOCKWISE.name] = {}
            payload[Direction.DIRECTION_CLOCKWISE.name]["congestion_index"] = self.congestion_index_clockwise
            payload[Direction.DIRECTION_ANTICLOCKWISE.name] = {}
            payload[Direction.DIRECTION_ANTICLOCKWISE.name]["congestion_index"] = self.congestion_index_anticlockwise

            while True:
                # for direction in Direction:
                response = requests.post("http://127.0.0.1:5000/set_road_congestion/%d" % \
                    (self.road_segment.value), json=payload)

                if response.text != self.current_time:
                    self.current_time = response.text
                    break
                else:                    
                    time.sleep(polling_interval)
            
            
            
            