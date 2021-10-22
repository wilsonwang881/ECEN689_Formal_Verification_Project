"""
Date: 10/19/2021
Description: the code starts a list of vehicle threads.
"""
from vehicle import Vehicle
from congestion_computation import Congestion_Computation

# Number of vehicles
vehicle_number = 15

# Start a list of threads
thread_list = list()

for i in range(vehicle_number):
    thread_object = Vehicle(id=i, starting_location=None, speed=None, route_completion_status=None)
    thread_list.append(thread_object)
    thread_object.start()

# Number of road sections
road_segments = 12

# Start a list of threads
thread_list = list()

for i in range(road_segments):
    thread_object = Congestion_Computation(id=i, road_responsible=None)
    thread_list.append(thread_object)
    thread_object.start()

# Wait for threads to terminate
for i, thread_object in enumerate(thread_list):
    thread_object.join()

# Wait for threads to terminate
for i, thread_object in enumerate(thread_list):
    thread_object.join()

# TODO: talk to the backend and allow dynamically adjust the number of vehicles injected to the traffic system.