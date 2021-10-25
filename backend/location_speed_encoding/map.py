from .crossroads import Crossroads
from .direction import Direction
from .road import Road
from .signal_light_positions import Signal_light_positions


MAP = {
    Road.ROAD_A: {
        Direction.DIRECTION_LEFT: {            
            "crossroad": Crossroads.CROSSROAD_Z,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {}
    },
    Road.ROAD_E: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_X,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_Z,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Road.ROAD_F: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_D,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_X,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Road.ROAD_G: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_Z,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_Y,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_H: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_X,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_U,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_I: {       
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_D,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
         Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_W,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_J: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_U,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_Y,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Road.ROAD_K: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_W,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_U,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Road.ROAD_L: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_Y,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_B,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_M: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_U,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_V,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_N: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_W,
            "traffic_light_orientation": Signal_light_positions.NORTH
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_C,
            "traffic_light_orientation": Signal_light_positions.SOUTH
        }
    },
    Road.ROAD_O: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_V,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_B,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Road.ROAD_P: {
        Direction.DIRECTION_LEFT: {
            "crossroad": Crossroads.CROSSROAD_C,
            "traffic_light_orientation": Signal_light_positions.EAST
        },
        Direction.DIRECTION_RIGHT: {
            "crossroad": Crossroads.CROSSROAD_V,
            "traffic_light_orientation": Signal_light_positions.WEST
        }
    },
    Crossroads.CROSSROAD_Z: [
        Road.ROAD_A,
        Road.ROAD_E,
        Road.ROAD_G
    ],
    Crossroads.CROSSROAD_X: [
        Road.ROAD_E,
        Road.ROAD_F,
        Road.ROAD_H
    ],
    Crossroads.CROSSROAD_D: [
        Road.ROAD_F,
        Road.ROAD_I
    ],
    Crossroads.CROSSROAD_Y: [
        Road.ROAD_G,
        Road.ROAD_J,
        Road.ROAD_L
    ],
    Crossroads.CROSSROAD_U: [
        Road.ROAD_H,
        Road.ROAD_I,
        Road.ROAD_J,
        Road.ROAD_M
    ],
    Crossroads.CROSSROAD_W: [
        Road.ROAD_I,
        Road.ROAD_K,
        Road.ROAD_N
    ],
    Crossroads.CROSSROAD_B: [
        Road.ROAD_L,
        Road.ROAD_O
    ],
    Crossroads.CROSSROAD_V: [
        Road.ROAD_M,
        Road.ROAD_O,
        Road.ROAD_P
    ],
    Crossroads.CROSSROAD_C: [
        Road.ROAD_N,
        Road.ROAD_P
    ]
}
