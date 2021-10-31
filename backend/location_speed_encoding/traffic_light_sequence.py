from .crossroads import Crossroads
from .signal_light_positions import Signal_light_positions

traffic_light_direction_sequence = {
    Crossroads.CROSSROAD_Z: [
        Signal_light_positions.WEST,
        Signal_light_positions.EAST,
        Signal_light_positions.EAST,
        Signal_light_positions.NORTH
    ],
    Crossroads.CROSSROAD_X: [
        Signal_light_positions.WEST,        
        Signal_light_positions.EAST,
        Signal_light_positions.WEST,
        Signal_light_positions.EAST,
        Signal_light_positions.NORTH
    ],
    Crossroads.CROSSROAD_D: [
        Signal_light_positions.EAST,
        Signal_light_positions.NORTH
    ],
    Crossroads.CROSSROAD_Y: [
        Signal_light_positions.NORTH,
        Signal_light_positions.SOUTH,
        Signal_light_positions.NORTH,
        Signal_light_positions.SOUTH,
        Signal_light_positions.WEST
    ],
    Crossroads.CROSSROAD_U: [
        Signal_light_positions.NORTH,
        Signal_light_positions.EAST,
        Signal_light_positions.WEST,
        Signal_light_positions.SOUTH
    ],
    Crossroads.CROSSROAD_W: [
        Signal_light_positions.NORTH,
        Signal_light_positions.SOUTH,
        Signal_light_positions.EAST,
        Signal_light_positions.NORTH,
        Signal_light_positions.SOUTH
    ],
    Crossroads.CROSSROAD_B: [
        Signal_light_positions.SOUTH,
        Signal_light_positions.WEST
    ],
    Crossroads.CROSSROAD_V: [
        Signal_light_positions.SOUTH,
        Signal_light_positions.WEST,
        Signal_light_positions.EAST,
        Signal_light_positions.WEST,
        Signal_light_positions.EAST
    ],
    Crossroads.CROSSROAD_C: [
        Signal_light_positions.SOUTH,
        Signal_light_positions.EAST
    ]
}