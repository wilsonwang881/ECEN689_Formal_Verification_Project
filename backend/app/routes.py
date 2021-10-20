from app import app


# Test route
@app.route("/")
@app.route("/index")
def index():
    return "Hello world!"


# Route for getting light signals at intersections
@app.route("/query_signal_lights/<intersection>")
def query_signal_lights(intersection):
    pass


# Route for setting light signals at intersections
@app.route("/set_signal_lights/<intersection>")
def set_signal_lights(intersection):
    pass


# Route for getting the location of a vehicle
@app.route("/query_vehicle_location/<vehicle_id>")
def query_vehicle_location(vehicle_id):
    pass


# Route for setting the location of a vehicle
@app.route("/set_vehicle_location/<vehicle_id>/<location>")
def set_vehicle_location(vehicle_id, location):
    pass


# Route for getting the speed of a vehicle
@app.route("/query_vehicle_speed/<vehicle_id>")
def query_vehicle_speed(vehicle_id):
    pass


# Route for setting the speed of a vehicle
@app.route("/set_vehicle_speed/<vehicle_id>/<speed>")
def set_vehicle_speed(vehicle_id, speed):
    pass


# Route for getting the route completion status of a vehicle
@app.route("/query_vehicle_completion/<vehicle_id> ")
def query_vehicle_completion(vehicle_id):
    pass


# Route for setting the route completion status of a vehicle
@app.route("/set_vehicle_completion/<vehicle_id>")
def set_vehicle_completion(vehicle_id):
    pass


# Route for getting the road congestion status
@app.route("/query_road_congestion/<road_id>")
def query_road_congestion(road_id):
    pass


# Route for setting the road congestion status
@app.route("/set_road_congestion/<road_id>/<index>")
def set_road_congestion(road_id, index):
    pass


# Route for getting the vehicles at one location
@app.route("/query_location/<location>")
def query_location(location):
    pass