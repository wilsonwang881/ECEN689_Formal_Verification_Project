"""
Date: 10/19/2021
Description: the code implements congestion calculation as threads. Each thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests
import time
from location_speed_encoding.direction import Direction


polling_interval = 0.5


class Congestion_Computation(threading.Thread):
    def __init__(self, id, road_responsible) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes
        self.id = id
        self.road_responsible = road_responsible
        self.vehicle_list = {}
        self.current_time = 0

    
    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Cogestion computation worker %d running" % (self.id))

        while True:

            # Get a list of vehicles on the road

            # Update local record

            # Calculate the congestion

            # Send the updated congestion information back to the backend
            for direction in Direction:
                response = requests.get("http://127.0.0.1:5000/set_road_congestion/%d/%d/0" % (self.id, direction.value))
            
            time.sleep(polling_interval)