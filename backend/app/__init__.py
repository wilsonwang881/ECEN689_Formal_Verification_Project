from flask import Flask
import redis
import logging
import json
from threading import Lock

from config import Config

from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.direction import Direction
from location_speed_encoding.road import Road
from location_speed_encoding.route_completion_status import Route_completion_status
from location_speed_encoding.signal_light_positions import Signal_light_positions
from location_speed_encoding.traffic_light import Traffic_light


app = Flask(__name__)
app.config.from_object(Config)

# Database connection
redis_db = redis.Redis(
    host=app.config["REDIS_DB_IP"],
    port=app.config["REDIS_DB_PORT"]
)

# Set the logger to only output errors
logger = logging.getLogger(('werkzeug'))
logger.setLevel(logging.ERROR)

# storage for recording the current states of vehicles, crossroads and road segments
current_states = {}

# Number of vehicles, whether enroute or not
total_number_of_vehicles = 100

# Clock
clock = 2

# Synchronization construct
mutex = Lock()

mutex.acquire()

# Flush Redis DB
redis_db.flushdb()

"""
Initialize the road segment->vehicle information in the database
All empty

Initialize the road segment->congestion index information in the database
All 0 (no congestion)

Initialize the (exact) location->vehicle information in the database
All empty
JSON format:
<road_segment_name>: {
    direction_name<clockwise>: {
        "vehicles": {
            <vehicle_name>: {
                "vehicle_location": <vehicle_location>,
                "vehicle_speed": <vehicle_speed>
            }
        },
        "congestion_index": <computed_value>
    },
    direction_name<anti-clockwise>: {
        "vehicles": {
            <vehicle_name>: {
                "vehicle_location": <vehicle_location>,
                "vehicle_speed": <vehicle_speed>
            }
        },
        "congestion_index": <computed_value>
    }
}

Vehicle_location:
on vertical road segments: the top is the 0th position
                           the bottom is the 29th position
on the horizontal road segments: the leftmost is the 0th position
                                 the rightmost is the 29th position
"""
for road_segment in Road:
    tmpp_record = {}
    for direction in Direction:
        tmpp_record[direction.name] = {}
        tmpp_record[direction.name]["vehicles"] = {}
        tmpp_record[direction.name]["congestion_index"] = 0
    redis_db.set(road_segment.name, json.dumps(tmpp_record))
    current_states[road_segment.name] = tmpp_record

"""
# Initialize the crossroad->traffic light information in the database
# All red
JSON format:
<crossroad_name>: {
    <signal_light_position>: <traffic_light_color>,
    ...
}
"""
for crossroad in Crossroads:
    tmpp_record = {}
    for signal_light_position in Signal_light_positions:
        tmpp_record[signal_light_position.name] = Traffic_light.RED.name
    redis_db.set(crossroad.name, json.dumps(tmpp_record))
    current_states[crossroad.name] = tmpp_record

# Record the number of vehicles in the database
# TODO: change the vehicle injection process to one at a time
redis_db.set("vehicles", 0)
current_states["vehicles"] = 0
current_states["pending_vehicles"] = total_number_of_vehicles

for id in range(total_number_of_vehicles):
    current_states["vehicle_%d" % id] = {}
    current_states["vehicle_%d" % id]["road_segment"] = Road.ROAD_A.value
    current_states["vehicle_%d" % id]["direction"] = 2
    current_states["vehicle_%d" % id]["location"] = 2
    current_states["vehicle_%d" % id]["vehicle_speed"] = 2
    current_states["vehicle_%d" % id]["route_completion"] = Route_completion_status.NOT_STARTED.value

    redis_db.set("vehicle_%d" % id, json.dumps(current_states["vehicle_%d" % id]))

# Allow only 1 vehicle to be placed on road segment A
# And have the enroute state
current_states["all_vehicles"] = {}
redis_db.set("all_vehicles", json.dumps(current_states["all_vehicles"]))

current_states_init = current_states

mutex.release()

from app import routes