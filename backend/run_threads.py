"""
Date: 10/19/2021
Description: the code starts a list of vehicle threads.
"""
from vehicle import Vehicle
from congestion_computation import Congestion_Computation
from traffic_signal_control import Traffic_signal_control_master 

# Number of vehicles
vehicle_number = 15

# Start a list of vehicle threads
vehicle_thread_list = list()

for i in range(vehicle_number):
    thread_object = Vehicle(id=i, starting_location=None, speed=None, route_completion_status=None)
    vehicle_thread_list.append(thread_object)
    thread_object.start()

# Number of road sections
road_segments = 12

# Start a list of threads
congestion_compute_thread_list = list()

for i in range(road_segments):
    thread_object = Congestion_Computation(id=i, road_responsible=None)
    congestion_compute_thread_list.append(thread_object)
    thread_object.start()

# Start the traffic light control master
traffic_control_master = Traffic_signal_control_master()
traffic_control_master.run_traffic_light_control()

# Wait for threads to terminate
for i, thread_object in enumerate(vehicle_thread_list):
    vehicle_thread_list.join()

# Wait for threads to terminate
for i, thread_object in enumerate(congestion_compute_thread_list):
    congestion_compute_thread_list.join()

# TODO: talk to the backend and allow dynamically adjust the number of vehicles injected to the traffic system.