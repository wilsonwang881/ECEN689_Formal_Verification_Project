## Table of Contents

- [Table of Contents](#table-of-contents)
- [Map](#map)
- [Goal](#goal)
- [Structure](#structure)
- [Technology Stack](#technology-stack)
- [Environment Setup](#environment-setup)
- [Location Encoding](#location-encoding)
- [Road Segment Record](#road-segment-record)
- [Backend Workflow](#backend-workflow)
- [Vehicle Workflow](#vehicle-workflow)
- [Congestion Computation Workflow](#congestion-computation-workflow)
- [Traffic Light Control Workflow](#traffic-light-control-workflow)
- [Unit Test Workflow](#unit-test-workflow)
- [Tutorials](#tutorials)


## Map

```
====A  ==============  ============== D
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              || 
       ==============  ==============  
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              ||
     ||              ||              || 
     B ==============  ============== C
```
Each vehicle must start from A, visit B, C, D in any order and leave at A.
A is not a crossroad.
B, C and D are crossroads.


## Goal

Design and verify a simple traffic system.

All vehicles on the map start and finish at the same position.

All vehicles have the same constraints.

The infrastructure group develop the traffic light control system.

The vehicle group simulate the vehicles in the traffic system.

The congestion information is shared across all vehicles.


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
            congestion_computation.py
            run_congestion_computation.py
        location_speed_encoding\    --------------> Location and speed representation
            __init__.py
            crossroads.py
            direction.py
            road.py
            signal_light_positions.py
            speed.py
            traffic_lights.py
        trafic_signal_control\    ----------------> Single thread signal light control
            traffic_signal_control_master.py
        vehicle\    ------------------------------> One vehicle object per thread
            vehicle.py
            run_vehicle_threads.py    
        .flaskenv    -----------------------------> Python flask environment variables
        backend.py
        config.py
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

Then run:

``flask run``

to start the backend.

Remember to start **Redis** with:

``redis-server``

The connection information such as **port number** is shown in the terminal.

To start congestion computation, vehicles and traffic signal control, make sure the virtual environment is activated before starting the corresponding scripts.


## Location Encoding

Each road segment has a name.

Each road segment has two lanes: in clockwise or anti-clockwise direction.

If the road segment is vertical, the 0th position is on the top.

If the road segment is horizontal, the 0th position is the leftmost one.

Encoding order: road segment -> lane direction -> square position.


## Road Segment Record

In JSON format:

```
{<road_segment_name>: 
    [
        {
        "direction": direction_name<clockwise>,
        "vehicles": {
                  <vehicle_name>: <vehicle_location>,
                  ...
                  },
        "congestion_index": <computed_value>
        },
        {
        "direction": direction_name<anticlockwise>,
        "vehicles": {
                  <vehicle_name>: <vehicle_location>,
                  ...
                  },
        "congestion_index": <computed_value>
        }
    ]
}
```


## Backend Workflow

The backend uses Python Flask as the framework and implements the following APIs:

| Route                                        |
|----------------------------------------------|
| ``/query_signal_light/<intersection>``           |
| ``/set_signal_light/<intersection>/<signal>``             |
| ``/query_vehicle_status/<vehicle_id>``         | 
| ``/set_vehicle_status/<vehicle_id>/<location>/<speed>`` | 
| ``/query_vehicle_completion/<vehicle_id>``       | 
| ``/set_vehicle_completion/<vehicle_id>``         | 
| ``/query_road_congestion/<road_id>``             | 
| ``/set_road_congestion/<road_id>/<index>``        |
| ``/query_location/<location>``                   |

The route names are fairly self-explanatory. The ``/query_location`` route is used to get the vehicle at one location if any.

If any vehicle thread or congestion computation thread queries the backend, the backend will query the database and return the information.

If any thread sends the updated information to the backend, the backend will temporarily hold the information until all threads have reported. After all the information is gathered, the backend will temporarily block all requests, update the database then resume operation.


## Vehicle Workflow

Each vehicle is a single thread:

1. Ask for congestion map.
2. Ask for traffic light status if at the crossroad.
3. Ask for whether there are any vehicles ahead.
4. Make movement decision.
5. Send the movement decision to the backend.
6. Once the backend has acknowledged the update, go to the next iteration.
7. The thread terminates until all locations (B, C and D) are visited.

The vehicle threads are started by ``vehicle_threads_start_script.py``.

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

[Python - Multithreaded Programming](https://www.tutorialspoint.com/python/python_multithreading.htm).

[Object-Oriented Programming (OOP) in Python 3](https://realpython.com/python3-object-oriented-programming/)