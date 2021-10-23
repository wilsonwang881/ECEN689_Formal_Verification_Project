from threading import Lock
import json
from flask import request
from app import app
from app import redis_db
from app import current_states
from app import clock
from location_speed_encoding import signal_light_positions
from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.road import Road


# Synchronization construct
mutex = Lock()

# Shared variables
total_vehicles = 15
reported_vehicles = 0

total_congestion_compute_workers = 12
reported_congestion_compute = 0

total_signal_light = 9
reported_signal_light = 0

vehicle_records = list()
congestion_compute_records = list()
signal_light_records = list()


# Function to update the database and store temporary records
def update(mode, id, value):
    global total_vehicles
    global reported_vehicles
    global total_congestion_compute_workers
    global reported_congestion_compute
    global total_signal_light
    global reported_signal_light
    global vehicle_records
    global congestion_compute_records
    global clock

    if (mode == "vehicle_report") and (id not in vehicle_records):
        reported_vehicles += 1
        vehicle_records.append(id)
        current_states[id] = value
    elif (mode == "congestion_compute_report") and (id not in congestion_compute_records):
        reported_congestion_compute += 1
        congestion_compute_records.append(id)
        current_states[Road(id).name] = value
    elif (mode == "signal_lights") and (id not in signal_light_records):
        reported_signal_light += 1
        signal_light_records.append(id)
        current_states[Crossroads(id).name] = value
    
    # If all threads have reported, update the database
    if (reported_vehicles == total_vehicles) \
        and (reported_congestion_compute == total_congestion_compute_workers) \
            and (reported_signal_light == total_signal_light):
        reported_vehicles = 0
        reported_congestion_compute = 0
        reported_signal_light = 0
        vehicle_records.clear()
        congestion_compute_records.clear()
        signal_light_records.clear()

        clock += 2

        for key in current_states:
            redis_db.set(key, json.dumps(current_states[key]))

        print("Reset! Time = %d" % clock)
                

# Test route
@app.route("/")
@app.route("/index")
def index():
    return "Hello world!"


# Route for getting light signals at intersections
@app.route("/query_signal_lights/<int:intersection>")
def query_signal_lights(intersection):
    res = json.loads(redis_db.get(Crossroads(intersection).name))

    return str(res)
    

# Route for setting light signals at intersections
@app.route("/set_signal_lights/<int:intersection>", methods=["POST"])
def set_signal_lights(intersection):
    payload = request.get_json()
    
    mutex.acquire()

    update("signal_lights", intersection, payload)

    mutex.release()

    global clock
    
    return str(clock)


# Route for getting the location of a vehicle
@app.route("/query_vehicle_status/<int:vehicle_id>")
def query_vehicle_location(vehicle_id):
    res = json.loads(redis_db.get(vehicle_id))

    return res


# Route for setting the status of a vehicle
@app.route("/set_vehicle_status/<int:id>/<int:road_segment>/<int:direction>/<int:location>/<int:intersection>/<int:speed>")
def set_vehicle_location(id, road_segment, direction, location, intersection, speed):
    payload = {}
    payload["road_segment"] = road_segment
    payload["direction"] = direction
    payload["location"] = location
    payload["intersection"] = intersection
    payload["speed"] = speed

    mutex.acquire()

    update("vehicle_report", id, payload)

    mutex.release()

    global clock
    
    return str(clock)


# Route for getting the route completion status of a vehicle
@app.route("/query_vehicle_completion/<int:vehicle_id> ")
def query_vehicle_completion(vehicle_id):
    pass


# Route for setting the route completion status of a vehicle
@app.route("/set_vehicle_completion/<int:vehicle_id>")
def set_vehicle_completion(vehicle_id):
    pass


# Route for getting the road congestion status
@app.route("/query_road_congestion/<int:road_id>")
def query_road_congestion(road_id):
    res = json.loads(redis_db.get(Road(road_id).name))
    
    return res


# Route for setting the road congestion status
@app.route("/set_road_congestion/<int:road_id>", methods=["POST"])
def set_road_congestion(road_id):
    payload = request.get_json()

    mutex.acquire()

    update("congestion_compute_report", road_id, payload)

    mutex.release()
    
    global clock
    
    return str(clock)


# Route for getting the vehicles at one location
@app.route("/query_location/<int:road_segment>/<int:direction>/<int:location>/<int:intersection>")
def query_location(location):
    pass


# Route for adding vehicle to the system
@app.route("/add_vehicle/<int:vehicle_id>")
def add_vehicle(vehicle_id):
    pass


# Route for removing vehicle from the system
@app.route("/remove_vehicle/<int:vehicle_id>")
def remove_vehicle(vehicle_id):
    pass