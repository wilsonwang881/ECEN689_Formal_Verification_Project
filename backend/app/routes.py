from app import app


# Test route
@app.route("/")
@app.route("/index")
def index():
    return "Hello world!"


# Routes for getting light signals at intersections
@app.route("/query_signal_lights")
def query_signal_lights():
    pass


# Routes for getting the location of a vehicle
@app.route("/query_vehicle_location")
def query_vehicle_location():
    pass


# Routes for setting the location of a vehicle
@app.route("/set_vehicle_location")
def set_vehicle_location():
    pass


# Routes for getting the speed of a vehicle
@app.route("/query_vehicle_speed")
def query_vehicle_speed():
    pass


# Routes for setting the speed of a vehicle
@app.route("/set_vehicle_speed")
def set_vehicle_speed():
    pass


# Routes for getting the route completion status of a vehicle
@app.route("/query_vehicle_completion")
def query_vehicle_completion():
    pass


# Routes for setting the route completion status of a vehicle
@app.route("/set_vehicle_completion")
def set_vehicle_completion():
    pass