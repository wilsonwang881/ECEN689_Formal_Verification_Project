from location_speed_encoding import Crossroads
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import traffic_light_direction_sequence
from location_speed_encoding import Traffic_light


polling_interval = 1.0


class Traffic_signal_control_master:
    def __init__(self) -> None:

        self.traffic_lights = {}
        self.signal_timer = 0
        self.green_position = Signal_light_positions.NORTH
        self.timer = 0

        for crossroad in Crossroads:

            self.traffic_lights[crossroad.name] = {}

            for signal_light_position in Signal_light_positions:

                if signal_light_position in traffic_light_direction_sequence[crossroad]:

                    self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name

    def return_traffic_light_status(self, crossroad):

        return self.traffic_lights[crossroad]

    def return_all_traffic_light_status(self):

        return self.traffic_lights

    def run_traffic_light_control(self):                    

        if self.timer >= 12:
            
            self.timer = 0
        
        for crossroad in Crossroads:

            number_of_signals = len(traffic_light_direction_sequence[crossroad])

            for signal_light_position in Signal_light_positions:

                if signal_light_position in traffic_light_direction_sequence[crossroad]:

                    if signal_light_position == traffic_light_direction_sequence[crossroad][self.timer % number_of_signals]:

                        self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.GREEN.name

                    else:

                        self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name  

            # print(crossroad)
            # print(self.traffic_lights[crossroad.name])  

        self.timer += 1      
                       
