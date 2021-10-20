"""
Date: 10/19/2021
Description: the code implements congestion calculation as threads. Each thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests


class Congestion_Computation_Worker(threading.Thread):
    def __init__(self, id, road_responsible) -> None:
        # Needed for using the threading library
        threading.Thread.__init__(self)

        # Set the object attributes
        self.id = id
        self.road_responsible = road_responsible

    
    # Inherited from the threading library
    # The thread runs this function when it starts
    def run(self):
        print("Cogestion computation work %d running" % (self.id))

        # Get a list of vehicles on the road

        # Update local record

        # Calculate the congestion

        # Send the updated congestion information back to the backend