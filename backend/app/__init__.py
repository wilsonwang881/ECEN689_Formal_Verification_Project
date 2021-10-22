from flask import Flask
import redis
import logging
import json
from config import Config
from location_speed_encoding.road import Road
from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.direction import Direction
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

# Record the number of vehicles in the database
# TODO: change the vehicle injection process to one at a time
redis_db.set("vehicles", 0)

from app import routes