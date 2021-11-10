"""
Date: 10/19/2021
Description: the code starts a list of vehicle threads.
"""

from vehicle import Vehicle
from congestion_computation import Congestion_Computation
from location_speed_encoding import Road

# Number of vehicles
vehicle_number = 130

# Start a list of vehicle threads
vehicle_thread_list = list()

for i in range(vehicle_number):
    thread_object = Vehicle(id=i)
    vehicle_thread_list.append(thread_object)
    thread_object.start()

# Number of road sections
road_segments = 12

# Start a list of threads
congestion_compute_thread_list = list()

for road in Road:
    if road != Road.ROAD_A:
        thread_object = Congestion_Computation(road.value)
        congestion_compute_thread_list.append(thread_object)
        thread_object.start()

# Wait for threads to terminate
for thread_object in vehicle_thread_list:
    thread_object.join()

# Wait for threads to terminate
for thread_object in congestion_compute_thread_list:
    thread_object.join()
