import json
from flask import request
from flask import render_template
from flask import jsonify

from app import app
from app import redis_db
from app import current_states
from app import clock
from app import mutex
from app import total_number_of_vehicles
from app import number_of_vehicles_finished
from app import traffic_control_master

from location_speed_encoding import Crossroads
from location_speed_encoding import Direction
from location_speed_encoding import MAP
from location_speed_encoding import Road
from location_speed_encoding import Route_completion_status
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import Speed
from location_speed_encoding import Traffic_light


# Shared variables
reported_vehicles = 0

total_congestion_compute_workers = 12
reported_congestion_compute = 0

vehicle_records = list()
congestion_compute_records = list()

vehicle_timestamp = list()

finished_vehicle_id = 0


def update(mode, id, value):

    # Function to update the database and store temporary records

    global total_number_of_vehicles
    global reported_vehicles
    global total_congestion_compute_workers
    global reported_congestion_compute
    global vehicle_records
    global congestion_compute_records
    global clock    
    global current_states
    global finished_vehicle_id
    global vehicle_timestamp

    if (mode == "vehicle_report") and (id not in vehicle_records): 

        vehicle_timestamp.append(int(value["clock"]))

        reported_vehicles += 1
        vehicle_records.append(id)        

        # Update the current vehicle record
        current_states["vehicle_%d" % id] = value       

        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id] = {}
        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id]["vehicle_location"] = value["location"]
        current_states[Road(value["road_segment"]).name][Direction(value["direction"]).name]["vehicles"]["vehicle_%d" % id]["vehicle_speed"] = value["vehicle_speed"]                       
        current_states["all_vehicles"]["vehicle_%d" % id] = value

        current_states["vehicles"] += 1

        if value["road_segment"] == Road.ROAD_A.value \
            and value["location"] == 2 \
                and value["direction"] == Direction.DIRECTION_LEFT.value:

            current_states["pending_vehicles"] += 1

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
        

    elif (mode == "add_vehicle"):

        # Check if there were any vehicle on road segment A in the previous time slot
        previous_road_A_record = json.loads(redis_db.get(Road.ROAD_A.name))[Direction.DIRECTION_LEFT.name]["vehicles"]

        # Check if there were any vehicle on slot 1 previously
        # Check if there were any vehicle on slot 1 now

        permission_to_add_vehicle = True

        if previous_road_A_record != {}:

            for vehicle in previous_road_A_record:

                if previous_road_A_record[vehicle]["vehicle_location"] == 1:                    
                    
                    permission_to_add_vehicle = False
            
        current_road_A_record = current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]
       
        if current_road_A_record != {}:

            for vehicle in current_road_A_record:

                if current_road_A_record[vehicle]["vehicle_location"] == 1:                    

                    permission_to_add_vehicle = False

        if permission_to_add_vehicle:

            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id] = {}
            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id]["vehicle_location"] = 1
            current_states[Road.ROAD_A.name][Direction.DIRECTION_LEFT.name]["vehicles"]["vehicle_%d" % id]["vehicle_speed"] = Speed.STOPPED.value

            print("A at time %d, vehicle %d added" % (clock, id))

        return permission_to_add_vehicle
    
    # If all threads have reported, update the database
    if (reported_vehicles == total_number_of_vehicles) \
        and (reported_congestion_compute == total_congestion_compute_workers):

        print("Sum of timestamps %d" % sum(vehicle_timestamp))

        if sum(vehicle_timestamp) != (total_number_of_vehicles * clock):
            
            print("Does not equal!")

        vehicle_timestamp.clear()

        reported_vehicles = 0
        reported_congestion_compute = 0    

        if (len(vehicle_records) != total_number_of_vehicles):
            print("error")

        vehicle_records.clear()
        congestion_compute_records.clear()    

        clock += 2
    
        # Check vehicle collision
        collision = 0
        
        for road_segment in Road:

            for direction in Direction:                

                current_road_segment_vehicles = current_states[road_segment.name][direction.name]["vehicles"]

                tmpp_position_list = list()

                for key in current_road_segment_vehicles:

                    if road_segment != Road.ROAD_A and current_road_segment_vehicles[key]["vehicle_location"] != 2:

                        if current_road_segment_vehicles[key]["vehicle_location"] in tmpp_position_list:

                            collision += 1

                            print("Collision")
                            print(road_segment)
                            print(current_road_segment_vehicles[key])
                            print(current_road_segment_vehicles)

                        else:

                            tmpp_position_list.append(current_road_segment_vehicles[key]["vehicle_location"]) 

        current_states["vehicle_collisions"] = collision

        # Check vehicle U-turn, throughput and traffic light violation
        u_turn = 0

        has_vehicle_finished = False

        traffic_light_violation = 0

        for i in range(total_number_of_vehicles):

            past_position = json.loads(redis_db.get("vehicle_%d" % i))
            current_position = current_states["vehicle_%d" % i]

            # Check U-turn
            if past_position["road_segment"] == current_position["road_segment"] \
                and past_position["location"] == current_position["location"] \
                    and past_position["direction"] != current_position["direction"] \
                        and (past_position["road_segment"] != Road.ROAD_A.value and past_position["location"] != 2):

                u_turn += 1

            # Check throughput
            if current_states["vehicle_%d" % i]["road_segment"] == Road.ROAD_A.value \
                and current_states["vehicle_%d" % i]["direction"] == Direction.DIRECTION_RIGHT.value \
                    and current_states["vehicle_%d" % i]["location"] == 1:

                if i != finished_vehicle_id:

                    has_vehicle_finished = True
                    finished_vehicle_id = i

            # Check traffic light violations
            if (past_position["location"] == 0 \
                or past_position["location"] == 29): # \
                    

                crossroad_to_query = Crossroads.CROSSROAD_B
                traffic_light_orientation = Signal_light_positions.EAST
                # Get the right crossroad to query    
                try:                
                    crossroad_to_query = MAP[Road(past_position["road_segment"])][Direction(past_position["direction"])]["crossroad"]
                    traffic_light_orientation = MAP[Road(past_position["road_segment"])][Direction(past_position["direction"])]["traffic_light_orientation"]               
                except:
                    print(crossroad_to_query)
                    print(traffic_light_orientation)
                    print(past_position)
                    print(current_position)

                response = json.loads(redis_db.get(crossroad_to_query.name))

                signal_light = Traffic_light[response[traffic_light_orientation.name]] 

                if signal_light == Traffic_light.RED:

                    # Check if the vehicle moves when the traffic light signal is red
                    if past_position["road_segment"] != current_position["road_segment"]:

                        traffic_light_violation += 1

                        print("vehicle_%d red light violation" % i)
                        print(response)
                        print(past_position)
                        print(current_position)
                
        if has_vehicle_finished:
            
            number_of_vehicles_finished[clock % 120] = 1

        else:

            number_of_vehicles_finished[clock % 120] = 0

        current_states["u_turns"] = u_turn  
        current_states["throughput"] = sum(number_of_vehicles_finished) * 30
        current_states["red_light_violation"] = traffic_light_violation

        # for i in range(total_number_of_vehicles):

        #     db_response = json.loads(redis_db.get("vehicle_%d" % i))                        

        #     print("Vehicle %d: time: %s, road segment: %s, position: %d, status: %s, direction: %s" % (i, clock, Road(db_response["road_segment"]).name, db_response["location"], Speed(db_response["vehicle_speed"]).name, Direction(db_response["direction"]).name))            

        # for crossroad in Crossroads:

        #     print("Crossroad: %s" % crossroad.name)

        #     db_response = json.loads(redis_db.get(crossroad.name))

        #     for orientation in db_response:                

        #         print("orientation: %s, status %s" % (orientation, db_response[orientation]))       

        # Flush Redis DB
        redis_db.flushdb()

                # print("orientation: %s, status %s" % (orientation, db_response[orientation]))
        
        # Flush Redis DB
        redis_db.flushdb()

        for key in current_states:                                

            redis_db.set(key, json.dumps(current_states[key]))

        current_states.clear()                

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

                if signal_light_position in MAP[crossroad]:

                    tmpp_record[signal_light_position.name] = Traffic_light.RED.name
                        
            current_states[crossroad.name] = tmpp_record

        current_states["vehicles"] = 0
        current_states["pending_vehicles"] = total_number_of_vehicles

        for id in range(total_number_of_vehicles):

            current_states["vehicle_%d" % id] = {}
            current_states["vehicle_%d" % id]["road_segment"] = Road.ROAD_A.value
            current_states["vehicle_%d" % id]["direction"] = 2
            current_states["vehicle_%d" % id]["location"] = 2
            current_states["vehicle_%d" % id]["vehicle_speed"] = 2
            current_states["vehicle_%d" % id]["route_completion"] = Route_completion_status.NOT_STARTED.value

        current_states["all_vehicles"] = {}
        current_states["all_traffic_lights"] = {}

        traffic_control_master.run_traffic_light_control()

        print("Database update! Time = %d" % clock)        

    return True
                

# Test route
@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")


# Route for getting light signals at intersections
@app.route("/query_signal_lights/<int:intersection>")
def query_signal_lights(intersection):

    mutex.acquire()

    # res = json.loads(redis_db.get(Crossroads(intersection).name))
    res = traffic_control_master.return_traffic_light_status(Crossroads(intersection).name)

    mutex.release()

    return json.dumps(res)
    

# Route for setting light signals at intersections
@app.route("/set_signal_lights", methods=["POST"])
def set_signal_lights():

    payload = request.get_json()

    global clock

    clock_tmpp = clock
    
    mutex.acquire()

    update("signal_lights", 9, payload)

    mutex.release()
    
    return str(clock_tmpp)


# Route for getting the location of a vehicle
@app.route("/query_vehicle_status/<int:vehicle_id>")
def query_vehicle_location(vehicle_id):    

    if vehicle_id < total_number_of_vehicles:

        mutex.acquire()

        res = json.loads(redis_db.get("vehicle_%d" %vehicle_id))

        mutex.release()

        return jsonify(res)

    else:

        mutex.acquire()

        global clock

        res_vehicle = json.loads(redis_db.get("all_vehicles"))
        res_traffic_light = traffic_control_master.return_all_traffic_light_status() # redis_db.get("all_traffic_lights")
        res_collisions = redis_db.get("vehicle_collisions")
        res_u_turns = redis_db.get("u_turns")
        res_throughtput = redis_db.get("throughput")
        res_red_light_violation = redis_db.get("red_light_violation")

        mutex.release()        

        if res_traffic_light != {}:

            res_vehicle.update(res_traffic_light)        

        res_vehicle["vehicle_collisions"] = int(res_collisions)
        res_vehicle["u_turns"] = int(res_u_turns)
        res_vehicle["throughput"] = int(res_throughtput)
        res_vehicle["red_light_violation"] = int(res_red_light_violation)
        res_vehicle["clock"] = int(clock)

        return jsonify(res_vehicle)


# Route for setting the status of a vehicle
@app.route("/set_vehicle_status/<int:id>", methods=["POST"])
def set_vehicle_location(id):

    payload = request.get_json()

    global clock

    mutex.acquire()    

    # if (int(payload["clock"])) == int(clock):

    update("vehicle_report", id, payload)

    clock_tmpp = clock

    mutex.release()    
    
    return str(clock_tmpp)


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
    
    global clock

    clock_tmpp = clock

    mutex.acquire()

    update("congestion_compute_report", road_id, payload)

    mutex.release()
            
    return str(clock_tmpp)


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

    global clock

    clock_tmpp = clock

    mutex.acquire()

    result = update("add_vehicle", vehicle_id, value=None)

    mutex.release()    

    if result: 

        return {"response": "OK", "clock": str(clock_tmpp)}

    else:

        return {"response": "No", "clock": str(clock_tmpp)}

