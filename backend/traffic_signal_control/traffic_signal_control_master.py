import requests
import json
import time
from location_speed_encoding.crossroads import Crossroads
from location_speed_encoding.signal_light_positions import Signal_light_positions
from location_speed_encoding.traffic_light import Traffic_light


polling_interval = 0.4


class Traffic_signal_control_master:
    def __init__(self) -> None:
        self.current_time = 0
        self.traffic_lights = {}
        self.signal_timer = 0
        self.green_position = Signal_light_positions.NORTH

        for crossroad in Crossroads:
            self.traffic_lights[crossroad.name] = {}
            for signal_light_position in Signal_light_positions:
                self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name

    def run_traffic_light_control(self):
        print("Traffic light control master running")

        while True:    
            # Update traffic light signals
            self.signal_timer += 1

            if self.signal_timer > 2:
                self.signal_timer = 0

            if self.signal_timer == 0:
                # Change signal
                for crossroad in Crossroads:
                    for signal_light_position in Signal_light_positions:
                        if signal_light_position == self.green_position:
                            self.traffic_lights[crossroad.name][self.green_position.name] = Traffic_light.GREEN.name
                        else:
                            self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name

                # Change green light position
                if self.green_position == Signal_light_positions.NORTH:
                    print("Changing signal lights from %s to %s" % (Signal_light_positions.NORTH.name, Signal_light_positions.WEST.name))
                    self.green_position = Signal_light_positions.WEST
                elif self.green_position == Signal_light_positions.WEST:
                    print("Changing signal lights from %s to %s" % (Signal_light_positions.WEST.name, Signal_light_positions.SOUTH.name))
                    self.green_position = Signal_light_positions.SOUTH
                elif self.green_position == Signal_light_positions.SOUTH:
                    print("Changing signal lights from %s to %s" % (Signal_light_positions.SOUTH.name, Signal_light_positions.EAST.name))
                    self.green_position = Signal_light_positions.EAST
                elif self.green_position == Signal_light_positions.EAST:
                    print("Changing signal lights from %s to %s" % (Signal_light_positions.EAST.name, Signal_light_positions.NORTH.name))
                    self.green_position = Signal_light_positions.NORTH
            
            
            # Send the updated traffic light signals to the backend
            while True:
                for crossroad in Crossroads:
                    response = requests.post("http://127.0.0.1:5000/set_signal_lights/%d" % crossroad.value, \
                        data=json.dumps(self.traffic_lights[crossroad.name]))

                if response.text != self.current_time:
                    self.current_time = response.text
                    break
                else:
                    time.sleep(polling_interval)



