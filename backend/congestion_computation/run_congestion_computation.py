"""
Date: 10/19/2021
Description: the code implements congestion computation as threads. Each thread can talk to the backend via HTTP requests and make decisions.
"""
import threading
import requests


from congestion_computation import Congestion_Computation


# Number of road sections
vehicle_number = 12

# Start a list of threads
thread_list = list()

for i in range(vehicle_number):
    thread_object = Congestion_Computation(id=i, road_responsible=None)
    thread_list.append(thread_object)
    thread_object.start()

# Wait for threads to terminate
for i, thread_object in enumerate(thread_list):
    thread_object.join()


# TODO: talk to the backend and allow dynamically adjust the number of vehicles injected to the traffic system.