## Table of Contents

- [Table of Contents](#table-of-contents)
- [Map](#map)
- [Goal](#goal)
- [Constraints](#constraints)
- [Structure](#structure)
- [Technology Stack](#technology-stack)
- [Environment Setup](#environment-setup)
- [Location Encoding](#location-encoding)
- [Database](#database)
  - [Road Segment Record](#road-segment-record)
  - [Traffic Light Record](#traffic-light-record)
  - [Vehicle Record](#vehicle-record)
  - [Number of Vehicles](#number-of-vehicles)
  - [Database Structure](#database-structure)
- [Backend Workflow](#backend-workflow)
- [Vehicle Workflow](#vehicle-workflow)
- [Congestion Computation Workflow](#congestion-computation-workflow)
- [Traffic Light Control Workflow](#traffic-light-control-workflow)
- [Unit Test Workflow](#unit-test-workflow)
- [Tutorials](#tutorials)


## Map

```
====A Z =======E======= X =======F======= D
     | |               | |               | |
     | |               | |               | |
     | |               | |               | |
      G                 H                 I
     | |               | |               | |
     | |               | |               | | 
     | |               | |               | | 
      Y =======J======= U =======K======= W
     | |               | |               | |
     | |               | |               | |
     | |               | |               | |
      L                 M                 N
     | |               | |               | |
     | |               | |               | | 
     | |               | |               | | 
      B =======O======= V =======P======= C
```

Each vehicle must start from A, visit B, C, D in any order and leave at A.

A is not a crossroad. B, C and D are crossroads.

Each road segment has two lanes running in different directions.

Traffic signals are either red or green.


## Goal

Design and verify a simple traffic system.

All vehicles on the map start and finish at the same position.

All vehicles have the same constraints.

The infrastructure group develop the traffic light control system.

The vehicle group simulate the vehicles in the traffic system.

The congestion information is shared across all vehicles.

Maximize the number of vehicles completing the route per unit time.


## Constraints

Each road segment is divided into 30 slots.

Each vehicle can move one slot at a time.

At any time instant, the same slot should have one vehicle. Otherwise, a collision happens.

Vehicles stop at a red signal and cannot make right turn.

Between two consecutive time steps, one vehicle can cross the road intersection.

At any time step, at the same intersection, only one signal can be green.

Vehicles at the intersection can see others at the intersection as well.

Vehicles have limited visibility along the same direction.

Vehicles can only move in the correct direction of the lane.

No U-turn.

Vehicles cannot move if another vehicle were immediately ahead of it.


## Structure

The code is divided into 3 groups: vehicle, backend and database.

Bonus part: a single page web application for viewing the traffic in real time.

The files are organized as the follows:

```
ECEN689_Formal_Verification_Project\    ----------> Root directory
    backend\    ----------------------------------> Python Flask backend
        app\
            __init__.py
            routes.py
        congestion_computation\    ---------------> Threaded computation
            __init__.py
            congestion_computation.py            
        location_speed_encoding\    --------------> Location and speed representation
            __init__.py
            crossroads.py
            direction.py
            map.py
            road.py
            route_completion_status.py
            signal_light_positions.py
            speed.py
            traffic_lights.py
        trafic_signal_control\    ----------------> Single thread signal light control
            __init__.py
            traffic_signal_control_master.py
        vehicle\    ------------------------------> One vehicle object per thread
            __init__.py
            vehicle.py  
        .flaskenv    -----------------------------> Python flask environment variables
        backend.py
        config.py
        run_threads.py    ------------------------> Start vehicle and congestion computation
    unit_tests\    -------------------------------> Automated tests    
    .gitignore 
    README.md
    requirements.txt    --------------------------> Python library requirements
```


## Technology Stack

Python + Flask + Redis + HTML + JavaScript + CSS


## Environment Setup

Ensure **Python 3** and **virtualenv** is installed.

For the first time setup, clone the code, change into the root directory of the code folder, then run:

``python3 -m venv venv``

``source venv/bin/activate``

``pip install -r requirements.txt``

Install [Redis](https://redis.io/topics/quickstart). Remember to copy **redis-server** and **redis-cli** to ``/usr/local/bin/``.

Once the environemt is setup, anytime one wants to activate the virtual environemnt, run:

``source venv/bin/activate``

To start the backend, change directory to **backend**, then run:

``flask run``

To start vehicle and congestion threads, change directory to **backend**, then run:

``python run_threads.py``

Remember to start **Redis** with:

``redis-server``

The connection information such as **port number** is shown in the terminal.


## Location Encoding

Each road segment has a name.

Each road segment has two lanes: in clockwise or anti-clockwise direction.

Encoding order: road segment -> lane direction -> square position.

Square position:

```
     29                   0  
     ======================
0  | |                    
   | |                   
   | |                
   | |                 
   | |                 
   | |                
   | |                
29 | |                
```

When a vehicle is moving from square 0 to square 29 on the same road segment, the vehicle is said to be on the right lane.

When a vehicle is moving from square 29 to square 0 on the same road segment, the vehicle is said to be on the left lane.


## Database

All records are in JSON format.


### Road Segment Record

```
<road_segment_name>: {
    direction_name<right>: {
        "vehicles": {
            <vehicle_name>: {
                "vehicle_location": <vehicle_location>,
                "vehicle_speed": <vehicle_speed>
            }
        },
        "congestion_index": <computed_value>
    },
    direction_name<left>: {
        "vehicles": {
            <vehicle_name>: {
                "vehicle_location": <vehicle_location>,
                "vehicle_speed": <vehicle_speed>
            }
        },
        "congestion_index": <computed_value>
    }
}
```


### Traffic Light Record

```
JSON format:
<crossroad_name>: {
    <signal_light_position>: <traffic_light_color>,
    ...
}
```


### Vehicle Record

```
<vehicle_name>: {
    "road_segment": <road_segment_name>,
    "direction": <direction_name>,
    "location": <location_on_the_segment>,
    "speed": <speed>,
    "route_completion": <yes_no_not_started>
}
```

### Number of Vehicles

```
"vehicles": <number_of_vehicles_in_the_system>,
"pending_vehicles": <number_of_vehicles_waiting_to_enter_the_system>
```


### Database Structure

**Redis** is primarily a key-value pair database system. Compared with any SQL based database system such as **MySQL**, which has a strict on the structure, ** Redis** allows more flexibility. The content in **Redis** used by the project is listed below.


```
"ROAD_A": <road_segment_record>,
"ROAD_B": <road_segment_record>,
"ROAD_C": <road_segment_record>,
"ROAD_D": <road_segment_record>,
...
...
"CROSSROAD_A": <traffic_light_record>,
"CROSSROAD_B": <traffic_light_record>,
"CROSSROAD_C": <traffic_light_record>,
"CROSSROAD_D": <traffic_light_record>,
...
...
"VEHICLE_1": <vehicle_record>,
"VEHICLE_2": <vehicle_record>,
"VEHICLE_3": <vehicle_record>,
"VEHICLE_4": <vehicle_record>,
...
...
"vehicles": <number_of_vehicles_in_the_system>,
"pending_vehicles": <number_of_vehicles_waiting_to_enter_the_system>
```


## Backend Workflow

The backend uses Python Flask as the framework and implements the following APIs:

| Route                                                                       
|--------------------------------------------------------------|
| ``/query_signal_light/<intersection>``                       |
| ``/set_signal_light/<intersection>``                         | 
| ``/query_vehicle_status/<vehicle_id>``                       | 
| ``/set_vehicle_status/<vehicle_id>``                         | 
| ``/query_road_congestion/<road_id>/<direction>``             | 
| ``/set_road_congestion/<road_id>``                           |
| ``/query_location/<road_id>/<direction>``                    |
| ``/add_vehicle/<vehicle_id>``                                |
| ``/remove_vehicle/<vehicle_id>``                             |

Threads report updated information with HTTP POST method. The payload is in JSON format, as shown in [Database](#database).

The route names are fairly self-explanatory. The ``/query_location`` route is used to get the vehicle records at any road segment.

If any vehicle thread or congestion computation thread queries the backend, the backend will query the database and return the information.

If any thread sends the updated information to the backend, the backend will temporarily hold the information until all threads have reported. After all the information is gathered, the backend will temporarily block all requests, update the database then resume operation.

To ensure data consistency, all operations to the database are protected with mutex, including queries.

The backend responses to the requests sent by the threads with the current timestamp. If the threads receive timestamps that are different from their own ones, the threads then know their requests have been fullfilled and can move to the next decision making process.


## Vehicle Workflow

Each vehicle is a single thread:

1. Ask for permission to enter the map.
2. If permission granted, start on road segment A.
3. If not, retry.
4. Ask for the congestion map.
5. Ask for traffic light status if at the crossroad.
6. Ask for whether there are any vehicles ahead.
7. Make movement decision.
8. Send the movement decision to the backend.
9. Once the backend has acknowledged the update, go to the next iteration.
10. The vehicle resets its location and route completion status and restarts.

The number of vehicles can be changed.


## Congestion Computation Workflow

Each congestion computation thread is responsible for one road segment, not the whole road:

1. Ask for vehicles on the road at give location.
2. Update the local road segment data.
3. Compute the congestion index.
4. Send the updated congestion index to the backend.
5. Once the backend has acknowledged the update, go to the next iteration.
6. The thread terminates only with manual exit of the program.

The number of congestion computation threads is fixed, because the map does not change. The number of road segments is fixed.

Formula to calculate the congestion index:

1. Once a vehicle shows up on the road segment, put the car and the timestamp into an array.
2. Sum up the difference between the current time and the timestamp for each vehicle.
3. Divide the sum by the number of vehicles.
4. Once the vehicle leaves the road segment, remove the record from the array.


## Traffic Light Control Workflow

One single thread exists for doing traffic light control.

1. Ask for road congestion information.
2. Check where there are any vehicles at the cross roads.
3. Make decision on changing the traffic lights.
4. Send the updated traffic light status to the backend.
5. Wait for the backend to acknowledge, go to the next iteration.
6. The thread terminates only with manual exit of the program.


## Unit Test Workflow


## Tutorials

[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

[Flask's Documentation](https://flask.palletsprojects.com/en/2.0.x/)

[Python - Multithreaded Programming](https://www.tutorialspoint.com/python/python_multithreading.htm).

[Object-Oriented Programming (OOP) in Python 3](https://realpython.com/python3-object-oriented-programming/)