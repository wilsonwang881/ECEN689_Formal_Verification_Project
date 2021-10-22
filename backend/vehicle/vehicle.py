"""
Date: 10/19/2021
Description: the code implements vehicles as threads. Each vehicle/thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests
import time
from location_speed_encoding.road import Road


polling_interval = 0.5


# Each vehicle in the traffic system is represented by a thread
# Class Vehicle inherits the threading library
# So that the Vehicle objects can make decisions and interact with the traffic system
class Vehicle(threading.Thread):
    def __init__(self, id, starting_location, speed, route_completion_status) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes
        self.id = id
        self.location = starting_location
        self.speed = speed
        self.location_visited = list()
        self.route_completion_status = route_completion_status


    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Vehicle %d running" % (self.id))

        while True:

            # Ask for the congestion map
            for road in Road:
                response = requests.get("http://127.0.0.1:5000/query_road_congestion/%d" % road.value)

            # Ask for traffic light status if visible

            # Make movement decision

            # Update the backend  

            # Update its currrent location

            response = requests.get("http://127.0.0.1:5000/set_vehicle_status/%d/2/2" % self.id)
            response = requests.get("http://127.0.0.1:5000/query_signal_lights/%d" % 1)
            
            time.sleep(polling_interval)
        