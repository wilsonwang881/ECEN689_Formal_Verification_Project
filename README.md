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

Remember to start **Redis** with:

``redis-server``

The connection information such as **port number** is shown in the terminal.


## APIs


