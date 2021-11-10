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
                    
                    exist_car1 = 0
                
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (8,1)).json() #road L, right lane

                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 29:#bottom
                            
                     	    exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0

                    exist_car2 = 0
                    
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (11,1)).json() #road O, right lane
                    
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0
                    
                    if num1 > num2:
                    
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                        
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.WEST.name] = Traffic_light.RED.name
                        
                    else:
                    
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.WEST.name] = Traffic_light.GREEN.name
                        
                        self.traffic_lights[Crossroads.CROSSROAD_B.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                        
                elif crossroad == Crossroads.CROSSROAD_C:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (12,2)).json() #road P, left lane
                   
                    exist_car1 = 0
                    
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0

                    exist_car2 = 0

                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (10,1)).json() #road N, right lane
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 29:#bottom
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0
                   
                    if num1 > num2:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.SOUTH.name] = Traffic_light.RED.name
                       
                    else:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.SOUTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_C.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name

                elif crossroad == Crossroads.CROSSROAD_D:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (2,2)).json() #road F, left lane
                   
                    exist_car1 = 0
                    
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0

                    exist_car2 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (5,2)).json() #road I, left lane
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0
                   
                    if num1 > num2:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.EAST.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.NORTH.name] = Traffic_light.RED.name
                       
                    else:
                   
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.NORTH.name] = Traffic_light.GREEN.name
                       
                        self.traffic_lights[Crossroads.CROSSROAD_D.name][Signal_light_positions.EAST.name] = Traffic_light.RED.name                        

                elif crossroad == Crossroads.CROSSROAD_U:
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (4,1)).json() #road H, right lane
                   
                    exist_car1 = 0
                    
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 29:#bottom
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0

                    exist_car2 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (6,2)).json() #road J, left lane
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0
                        
                    exist_car3 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (7,1)).json() #road K, right lane
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0

                    response4 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (9,2)).json() #road M, left lane
                    
                    exist_car4 = 0
                   
                    for vehicle in response4:
                        
                        if response4[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car4 = 1
                            
                    if exist_car4 == 1:
                    
                        num4 = len(response4)
                        
                    else:
                        
                        num4 = 0

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
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (9,1)).json() #road V, right lane
                   
                    exist_car1 = 0
                   
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 29:#bottom
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (11,2)).json() #road O, left lane
                   
                    exist_car2 = 0
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (12,1)).json() #road P, right lane
                   
                    exist_car3 = 0
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0

                    num1 = round(0.5*num1)

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
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (5,1)).json() #road I, right lane
                   
                    exist_car1 = 0
                   
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 29:#bottom
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (7,2)).json() #road K, left lane
                   
                    exist_car2 = 0
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (10,2)).json() #road N, left lane
                   
                    exist_car3 = 0
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0
 
                    num2 = round(0.5*num2)

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
               
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (1,2)).json() #road E, left lane
                   
                    exist_car2 = 0
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (2,1)).json() #road F, right lane
                   
                    exist_car3 = 0
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0

                    response4 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (4,2)).json() #road H, left lane
                   
                    exist_car4 = 0
                   
                    for vehicle in response4:
                        
                        if response4[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car4 = 1
                            
                    if exist_car4 == 1:
                    
                        num4 = len(response2)
                        
                    else:
                        
                        num4 = 0

                    num4 = round(0.5*num4)

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
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (3,1)).json() #road G, right lane
                   
                    exist_car1 = 0
                   
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 29:#bottom
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        num1 = len(response1)
                        
                    else:
                        
                        num1 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (6,1)).json() #road J, right lane
                   
                    exist_car2 = 0
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (8,2)).json()  #road L, left lane
                   
                    exist_car3 = 0
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0
 
                    num2 = round(0.5*num2)

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
               
                    response1 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (0,2)).json() #road A, left lane
                   
                    for vehicle in response1:
                        
                        if response1[vehicle]["vehicle_location"] == 0:#right
                            
                            exist_car1 = 1
                            
                    if exist_car1 == 1:
                    
                        if response1[vehicle]["vehicle_location"] == 1:
                            
                            num1 = 20 # Remove the car at the base, and assume 1 slot for 10 cars in road A
                            
                        else:
                            
                            num1 = 10
                        
                    else:
                        
                        num1 = 0
                   
                    response2 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (1,1)).json() #road E, right lane
                   
                    exist_car2 = 0
                   
                    for vehicle in response2:
                        
                        if response2[vehicle]["vehicle_location"] == 29:#left
                            
                            exist_car2 = 1
                            
                    if exist_car2 == 1:
                    
                        num2 = len(response2)
                        
                    else:
                        
                        num2 = 0

                    response3 = requests.get("http://127.0.0.1:5000/query_location/%d/%d" % (3,2)).json() #road G, left lane
                   
                    exist_car3 = 0
                   
                    for vehicle in response3:
                        
                        if response3[vehicle]["vehicle_location"] == 0:#top
                            
                            exist_car3 = 1
                            
                    if exist_car3 == 1:
                    
                        num3 = len(response3)
                        
                    else:
                        
                        num3 = 0

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



