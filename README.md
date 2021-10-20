# ECEN689 Formal Verification Project

## Goal

Design and verify a simple traffic system.

All vehicles on the map start and finish at the same position.

All vehicles have the same constraints.

The infrastructure group develop the traffic light control system.

The vehicle group simulate the vehicles in the traffic system.

## Structure

The code is divided into 3 groups: vehicle, backend and database.

Bonus part: a single page web application for viewing the traffic in real time.

The files are organized as the follows:

```
ECEN689_Formal_Verification_Project\    ------> Root directory
    backend\    ------------------------------> Python Flask backend
        backend.py
        app\
            __init__.py
            routes.py
    congestion_computation\    ---------------> Threaded computation
        congestion_computation.py
        run_congestion_computation.py
    trafic_signal_control\    ----------------> Single thread signal light control
        traffic_signal_control_master.py
    unit_tests\    ---------------------------> Automated tests
    vehicle\    ------------------------------> One vehicle object per thread
        vehicle.py
        vehicle_threads_start_script.py
    .flaskenv    -----------------------------> Python flask environment variables
    .gitignore 
    README.md
    requirements.txt    ----------------------> Python library requirements
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


## APIs


## Tutorials

[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.

[Python - Multithreaded Programming](https://www.tutorialspoint.com/python/python_multithreading.htm).

[Object-Oriented Programming (OOP) in Python 3](https://realpython.com/python3-object-oriented-programming/)