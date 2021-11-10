import requests
import json
import time

from location_speed_encoding import Crossroads
from location_speed_encoding import Signal_light_positions
from location_speed_encoding import traffic_light_direction_sequence
from location_speed_encoding import Traffic_light


polling_interval = 1.0


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

            if self.timer >= 60:
                
                self.timer = 0
            
            for crossroad in Crossroads:

                number_of_signals = len(traffic_light_direction_sequence[crossroad])

                
                if crossroad == Crossroads.CROSSROAD_B:
                
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (8,1))
                    
                    num1 = len(response1.json())
                    
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (11,1))
                    
                    num2 = len(response2.json())
                    
                    if num1 > num2:
                    
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                        
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                    else:
                    
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                        
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                elif crossroad == Crossroads.CROSSROAD_C:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (12,2))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (10,1))
                   
                    num2 = len(response2.json())
                   
                    if num1 > num2:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                       
                    else:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                elif crossroad == Crossroads.CROSSROAD_D:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (2,2))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (5,2))
                   
                    num2 = len(response2.json())
                   
                    if num1 > num2:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name
                       
                    else:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name                        

                elif crossroad == Crossroads.CROSSROAD_U:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (4,1))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (6,2))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (7,1))
                   
                    num3 = len(response3.json())

                    response4 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (9,2))
                   
                    num4 = len(response4.json())

                    maxcar = max(num1, num2, num3, num4)
                   
                    if num1 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue
                       
                    elif num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue

                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue

                    elif num4 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue

                elif crossroad == Crossroads.CROSSROAD_V:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (9,1))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (11,2))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (12,1))
                   
                    num3 = len(response3.json())

                    num1 = 2*num1

                    maxcar = max(num1, num2, num3)
                   
                    if num1 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue
                       
                    elif num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue

                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_V.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue


                elif crossroad == Crossroads.CROSSROAD_W:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (5,1))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (7,2))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (10,2))
                   
                    num3 = len(response3.json())
 
                    num2 = 2*num2

                    maxcar = max(num1, num2, num3)
                   
                    if num1 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue
                       
                    elif num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                        continue


                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_W.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                        continue


                elif crossroad == Crossroads.CROSSROAD_X:
               
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (1,2))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (2,1))
                   
                    num3 = len(response3.json())

                    response4 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (4,2))
                   
                    num4 = len(response4.json())

                    num4 = 2*num4

                    maxcar = max(num2, num3, num4)
                   
                       
                    if num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue

                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue

                    elif num4 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_X.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue


                elif crossroad == Crossroads.CROSSROAD_Y:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (3,1))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (6,1))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (8,2))
                   
                    num3 = len(response3.json())
 
                    num2 = 2*num2

                    maxcar = max(num1, num2, num3)
                   
                    if num1 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue
                       
                    elif num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                        continue


                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_Y.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                        continue


                elif crossroad == Crossroads.CROSSROAD_Z:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (0,2))
                   
                    num1 = len(response1.json())
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (1,1))
                   
                    num2 = len(response2.json())

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (3,2))
                   
                    num3 = len(response3.json())

                    maxcar = max(num1, num2, num3)
                   
                    if num1 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue
                       
                    elif num2 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_Z.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name
                        
                        continue


                    elif num3 == maxcar:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                        self.traffic_lights[Crossroads.CROSSROAD_U.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                        continue

                else:

                    for signal_light_position in Signal_light_positions:

                        if signal_light_position == traffic_light_direction_sequence[crossroad][self.timer % number_of_signals]:

                            self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.GREEN.name

                        else:

                            self.traffic_lights[crossroad.name][signal_light_position.name] = Traffic_light.RED.name    

            self.timer += 1      
            
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



