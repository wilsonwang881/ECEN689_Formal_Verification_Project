from threading import Lock
import json
from app import app
from app import redis_db
from app import current_states
from app import clock
from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.road import Road


# Synchronization construct
mutex = Lock()

# Shared variables
total_vehicles = 15
reported_vehicles = 0

total_congestion_compute_workers = 12
reported_congestion_compute = 0

vehicle_records = list()
congestion_compute_records = list()

time = 0


# Function to update the database and store temporary records
def update(mode, id, value):
    global total_vehicles
    global reported_vehicles
    global total_congestion_compute_workers
    global reported_congestion_compute
    global vehicle_records
    global congestion_compute_records
    global time

    if (mode == "vehicle_report") and (id not in vehicle_records):
        reported_vehicles += 1
        vehicle_records.append(id)
    elif (mode == "congestion_compute_report") and (id not in congestion_compute_records):
        reported_congestion_compute += 1
        congestion_compute_records.append(id)
    
    if (reported_vehicles == total_vehicles) and (reported_congestion_compute == total_congestion_compute_workers):
        reported_vehicles = 0
        reported_congestion_compute = 0
        vehicle_records.clear()
        congestion_compute_records.clear()
        time += 2
        print("Reset! Time = %d" % time)
        # Update the database
        

# Test route
@app.route("/")
@app.route("/index")
def index():
    return "Hello world!"


# Route for getting light signals at intersections
@app.route("/query_signal_lights/<int:intersection>")
def query_signal_lights(intersection):
    res = json.loads(redis_db.get(Crossroads(intersection).name))

    return res
    

# Route for setting light signals at intersections
@app.route("/set_signal_lights/<int:intersection>/<int:direction>/<int:signal>")
def set_signal_lights(intersection, signal):
    mutex.acquire()

    update("signal_lights", intersection, [signal])

    mutex.release()

    global time
    
    return str(time)


# Route for getting the location of a vehicle
@app.route("/query_vehicle_status/<int:vehicle_id>")
def query_vehicle_location(vehicle_id):
    res = json.loads(redis_db.get(vehicle_id))

    return res


# Route for setting the status of a vehicle
@app.route("/set_vehicle_status/<int:id>/<int:road_segment>/<int:direction>/<int:location>/<int:intersection>/<int:speed>/<int:timestamp>")
def set_vehicle_location(id, road_segment, direction, location, intersection, speed, timestamp):
    mutex.acquire()

    update("vehicle_report", id, [location, speed])

    mutex.release()

    global time
    
    return str(time)


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
@app.route("/set_road_congestion/<int:road_id>/<int:direction_1>/<index_1>/<int:direction_2>/<index_2>/<int:timestamp>")
def set_road_congestion(road_id, direction_1, index_1, direction_2, index_2, timestamp):
    mutex.acquire()

    update("congestion_compute_report", road_id, [index_1])

    mutex.release()
    
    global time
    
    return str(time)


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