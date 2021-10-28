import json
from os import name
from flask import request
from app import app
from app import redis_db
from app import current_states
from app import current_states_init
from app import clock
from app import mutex
from app import total_number_of_vehicles
from location_speed_encoding import Crossroads
from location_speed_encoding import Direction
from location_speed_encoding import Road
from location_speed_encoding import Route_completion_status
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import Speed
from location_speed_encoding import Traffic_light


# Shared variables
total_vehicles = total_number_of_vehicles
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
    global current_states

    if (mode == "vehicle_report") and (id not in vehicle_records):        
        reported_vehicles += 1
        vehicle_records.append(id)        

        # Update the current vehicle record
        current_states["vehicle_%d" % id] = value

        # Get the previous vehicle record
        # original_vehicle_record = json.loads(redis_db.get("vehicle_%d" % id))        

        # Get the previous road segment record 
        # original_road_segment_record = json.loads(redis_db.get(Road(original_vehicle_record["road_segment"]).name))

        # Update the previous road segment record, but in the current record set only
        # Do not commit to the database at this moment

        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id] = {}
        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id]["vehicle_location"] = value["location"]
        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id]["vehicle_speed"] = value["vehicle_speed"]                       

        # Do not update crossroad->vehicle mapping: no such mapping in the database        
        
    elif (mode == "congestion_compute_report") and (id not in congestion_compute_records):        
        reported_congestion_compute += 1
        congestion_compute_records.append(id)
        for key in current_states[Road(id).name]:
            if key == Direction.DIRECTION_RIGHT.name:
                current_states[Road(id).name][Direction.DIRECTION_RIGHT.name]["congestion_index"] = \
                    value[Direction.DIRECTION_RIGHT.name]["congestion_index"]
            elif key == Direction.DIRECTION_LEFT.name:
                current_states[Road(id).name][Direction.DIRECTION_LEFT.name]["congestion_index"] = \
                    value[Direction.DIRECTION_LEFT.name]["congestion_index"]
        
    elif (mode == "signal_lights") and (id not in signal_light_records):        
        reported_signal_light += 1
        signal_light_records.append(id)
        current_states[Crossroads(id).name] = value

    elif mode == "add_vehicle":
        # Check if there were any vehicle on road segment A in the previous time slot
        previous_road_A_record = json.loads(redis_db.get(Road.ROAD_A.name))[Direction.DIRECTION_LEFT.name]["vehicles"]

        # Check if there were any vehicle on slot 1 previously
        # Check if there were any vehicle on slot 1 now

        permission_to_add_vehicle = True
        # print("======%d" % id)
        # print(previous_road_A_record)
        if previous_road_A_record != {}:

            for vehicle in previous_road_A_record:

                if previous_road_A_record[vehicle]["vehicle_location"] == 1:
                    # print("failed A")
                    permission_to_add_vehicle = False

            
        current_road_A_record = current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]
        # print(current_road_A_record)
        if current_road_A_record != {}:

            for vehicle in current_road_A_record:

                if current_road_A_record[vehicle]["vehicle_location"] == 1:
                    # print("failed B")
                    permission_to_add_vehicle = False

        # print("======%d" % id)

        if not permission_to_add_vehicle:

            return False

        else:

            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id] = {}
            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id]["vehicle_location"] = 1
            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id]["vehicle_speed"] = Speed.STOPPED.value

            print("A at time %d, vehicle %d added" % (clock, id))

            return True

    
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

        current_states.clear()
        # current_states = current_states_init.copy()
        # Maybe just use the copy method to copy an initialized dictionary

        for road_segment in Road:
            tmpp_record = {}
            for direction in Direction:
                tmpp_record[direction.name] = {}
                tmpp_record[direction.name]["vehicles"] = {}
                tmpp_record[direction.name]["congestion_index"] = 0            
            current_states[road_segment.name] = tmpp_record

        for crossroad in Crossroads:
            tmpp_record = {}
            for signal_light_position in Signal_light_positions:
                tmpp_record[signal_light_position.name] = Traffic_light.RED.name            
            current_states[crossroad.name] = tmpp_record

        current_states["vehicles"] = 0
        current_states["pending_vehicles"] = total_number_of_vehicles

        for id in range(total_number_of_vehicles):
            current_states["vehicle_%d" % id] = {}
            current_states["vehicle_%d" % id]["road_segment"] = Road.ROAD_A.value
            current_states["vehicle_%d" % id]["direction"] = 0
            current_states["vehicle_%d" % id]["location"] = 1
            current_states["vehicle_%d" % id]["speed"] = 0
            current_states["vehicle_%d" % id]["route_completion"] = Route_completion_status.NOT_STARTED.value

        print("Database update! Time = %d" % clock)

    return True
                

# Test route
@app.route("/")
@app.route("/index")
def index():

    return "Hello world!"


# Route for getting light signals at intersections
@app.route("/query_signal_lights/<int:intersection>")
def query_signal_lights(intersection):

    mutex.acquire()

    res = json.loads(redis_db.get(Crossroads(intersection).name))

    mutex.release()

    return json.dumps(res)
    

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

    mutex.acquire()

    res = json.loads(redis_db.get(vehicle_id))

    mutex.release()

    return res


# Route for setting the status of a vehicle
@app.route("/set_vehicle_status/<int:id>", methods=["POST"])
def set_vehicle_location(id):

    payload = request.get_json()

    mutex.acquire()

    update("vehicle_report", id, payload)

    mutex.release()

    global clock
    
    return str(clock)


# Route for getting the road congestion status
@app.route("/query_road_congestion/<int:road_id>/<int:direction>")
def query_road_congestion(road_id, direction):

    mutex.acquire()

    res = json.loads(redis_db.get(Road(road_id).name))

    mutex.release()
    
    return str(res[Direction(direction).name]["congestion_index"])


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
@app.route("/query_location/<int:road_id>/<int:direction>")
def query_location(road_id, direction):

    mutex.acquire()

    res = json.loads(redis_db.get(Road(road_id).name))

    mutex.release()

    return res[Direction(direction).name]["vehicles"]


# Route for adding vehicle to the system
@app.route("/add_vehicle/<int:vehicle_id>")
def add_vehicle(vehicle_id):

    mutex.acquire()

    result = update("add_vehicle", vehicle_id, value=None)

    mutex.release()

    global clock

    if result: 

        return {"response": "OK", "clock": str(clock)}

    else:

        return {"response": "No", "clock": str(clock)}


# Route for removing vehicle from the system
@app.route("/remove_vehicle/<int:vehicle_id>")
def remove_vehicle(vehicle_id):

    pass