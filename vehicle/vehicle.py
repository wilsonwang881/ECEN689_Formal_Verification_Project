class Vehicle:
    def __init__(self, starting_location, speed, route_completion_status) -> None:
        self.location = starting_location
        self.speed = speed
        self.route_completion_status = route_completion_status