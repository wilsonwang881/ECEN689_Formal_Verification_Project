"""
Date: 10/19/2021
Description: the code starts a list of vehicle threads.
"""
from vehicle import Vehicle


# Number of vehicles
vehicle_number = 15

# Start a list of threads
thread_list = list()

for i in range(vehicle_number):
    thread_object = Vehicle(id=i, starting_location=None, speed=None, route_completion_status=None)
    thread_list.append(thread_object)
    thread_object.start()

# Wait for threads to terminate
for i, thread_object in enumerate(thread_list):
    thread_object.join()


# TODO: talk to the backend and allow dynamically adjust the number of vehicles injected to the traffic system.