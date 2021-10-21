"""
    Z=========X=========D
    |         |         |       
    |         |         |       
    |         |         |        
    Y=========U=========W
    |         |         |       
    |         |         |        
    |         |         |       
    B=========V=========C
 """


from enum import Enum

class Crossroads(Enum):
    CROSSROAD_B = 1
    CROSSROAD_C = 2
    CROSSROAD_D = 3
    CROSSROAD_U = 4
    CROSSROAD_V = 5
    CROSSROAD_W = 6
    CROSSROAD_X = 7
    CROSSROAD_Y = 8
    CROSSROAD_Z = 9