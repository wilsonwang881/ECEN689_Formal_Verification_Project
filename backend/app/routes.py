from threading import Lock
from app import app


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
def update(mode, id):
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
@app.route("/query_signal_lights/<intersection>")
def query_signal_lights(intersection):
    pass


# Route for setting light signals at intersections
@app.route("/set_signal_lights/<intersection>")
def set_signal_lights(intersection):
    mutex.acquire()

    update("signal_lights", 1)

    mutex.release()
    
    return "OK"


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
    mutex.acquire()

    update("vehicle_report", vehicle_id)

    mutex.release()
    
    return "OK"


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
    mutex.acquire()

    update("congestion_compute_report", road_id)

    mutex.release()
    
    return "OK"


# Route for getting the vehicles at one location
@app.route("/query_location/<location>")
def query_location(location):
    pass