import requests
import json
import time

from location_speed_encoding import Crossroads
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import traffic_light_direction_sequence
from location_speed_encoding import Traffic_light


polling_interval = 0.2


class Traffic_signal_control_master:
    def __init__(self) -> None:
        self.current_time = 0
        self.traffic_lights = {}
        self.signal_timer = 0
        self.green_position = Signal_light_positions.NORTH
        self.timer = 0

        for crossroad in Crossroads:

            self.traffic_lights[crossroad.name] = {}

            for signal_light_position in Signal_light_positions:

                self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name

    def run_traffic_light_control(self):
        
        print("Traffic light control master running")

        while True:    

            self.timer += 1

            if self.timer >= 19:
                
                self.timer = 0
            
            for crossroad in Crossroads:

                number_of_signals = len(traffic_light_direction_sequence[crossroad])

                for signal_light_position in Signal_light_positions:

                    if signal_light_position == traffic_light_direction_sequence[crossroad][self.timer % number_of_signals]:

                        self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.GREEN.name

                    else:

                        self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name          
            
            # Send the updated traffic light signals to the backend
            while True:
                for crossroad in Crossroads:
                    response = requests.post("http://127.0.0.1:5000/set_signal_lights/%d" % crossroad.value, \
                        json=self.traffic_lights[crossroad.name])

                if response.text != self.current_time:
                    self.current_time = response.text
                    break
                else:
                    time.sleep(polling_interval)



