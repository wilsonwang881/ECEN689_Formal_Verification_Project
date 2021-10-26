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
    Crossroads.CROSSROAD_Z: {
        Signal_light_positions.WEST: Road.ROAD_A,
        Signal_light_positions.EAST: Road.ROAD_E,
        Signal_light_positions.SOUTH: Road.ROAD_G
    },
    Crossroads.CROSSROAD_X: {
        Signal_light_positions.WEST: Road.ROAD_E,
        Signal_light_positions.EAST: Road.ROAD_F,
        Signal_light_positions.SOUTH: Road.ROAD_H
    },
    Crossroads.CROSSROAD_D: {
        Signal_light_positions.WEST: Road.ROAD_F,
        Signal_light_positions.SOUTH: Road.ROAD_I
    },
    Crossroads.CROSSROAD_Y: {
        Signal_light_positions.NORTH: Road.ROAD_G,
        Signal_light_positions.EAST: Road.ROAD_J,
        Signal_light_positions.SOUTH: Road.ROAD_L
    },
    Crossroads.CROSSROAD_U: {
        Signal_light_positions.NORTH: Road.ROAD_H,
        Signal_light_positions.EAST: Road.ROAD_K,
        Signal_light_positions.WEST: Road.ROAD_J,
        Signal_light_positions.SOUTH: Road.ROAD_M
    },
    Crossroads.CROSSROAD_W: {
        Signal_light_positions.NORTH: Road.ROAD_I,
        Signal_light_positions.WEST: Road.ROAD_K,
        Signal_light_positions.SOUTH: Road.ROAD_N
    },
    Crossroads.CROSSROAD_B: {
        Signal_light_positions.NORTH: Road.ROAD_L,
        Signal_light_positions.EAST: Road.ROAD_O
    },
    Crossroads.CROSSROAD_V: {
        Signal_light_positions.NORTH: Road.ROAD_M,
        Signal_light_positions.WEST: Road.ROAD_O,
        Signal_light_positions.EAST: Road.ROAD_P
    },
    Crossroads.CROSSROAD_C: {
        Signal_light_positions.NORTH: Road.ROAD_N,
        Signal_light_positions.WEST: Road.ROAD_P
    }
}
