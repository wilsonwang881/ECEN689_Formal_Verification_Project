/*
ECEN 689 Introduction to Formal Verification
Texas A&M University
Date: 2021.11.7

This file serves the purpose of model checking with Spin.
All logics from the Python application are included and modeled.
*/

#include "lock.h"

short NUMBER_OF_VEHICLES = 150;

short NUMBER_OF_ROAD_SEGMENTS = 12;

bit mutex = 0;

mtype:Crossroads = {
    CROSSROAD_Z,
    CROSSROAD_Y,
    CROSSROAD_X,
    CROSSROAD_W,
    CROSSROAD_V,
    CROSSROAD_U,
    CROSSROAD_D,
    CROSSROAD_C,
    CROSSROAD_B
}

mtype:Direction = {
    DIRECTION_LEFT,
    DIRECTION_RIGHT
}

mtype:Road = {
    ROAD_P,
    ROAD_O,
    ROAD_N,
    ROAD_M,
    ROAD_L,
    ROAD_K,
    ROAD_J,
    ROAD_I,
    ROAD_H,
    ROAD_G,
    ROAD_F,
    ROAD_E,
    ROAD_A
}

mtype:Route_completion_status = {
    FINISHED,
    ENROUTE,
    NOT_STARTED
}

mtype:Signal_light_positions = {
    EAST,
    WEST,
    SOUTH,
    NORTH
}

mtype:speed = {
    STOPPED,
    MOVING
}

mtype:Traffic_light = {
    GREEN,
    RED
}

typedef MAP_ROAD_DIRECTION_Def {
    mtype:Crossroads crossroad;
    mtype:Signal_light_positions traffic_light_orientation;
};

typedef MAP_ROAD_DEF {
    MAP_ROAD_DIRECTION_Def direction_left_record;
    MAP_ROAD_DIRECTION_Def direction_right_record;
};

typedef MAP_CROSSROAD_DEF {
    mtype:Road EAST_ROAD;
    mtype:Road SOUTH_ROAD;
    mtype:Road WEST_ROAD;
    mtype:Road NORTH_ROAD;
};

typedef MAP_DEF {
    MAP_ROAD_DEF ROAD_A_RECORD;
    MAP_ROAD_DEF ROAD_E_RECORD;
    MAP_ROAD_DEF ROAD_F_RECORD;
    MAP_ROAD_DEF ROAD_G_RECORD;
    MAP_ROAD_DEF ROAD_H_RECORD;
    MAP_ROAD_DEF ROAD_I_RECORD;
    MAP_ROAD_DEF ROAD_J_RECORD;
    MAP_ROAD_DEF ROAD_K_RECORD;
    MAP_ROAD_DEF ROAD_L_RECORD;
    MAP_ROAD_DEF ROAD_M_RECORD;
    MAP_ROAD_DEF ROAD_N_RECORD;
    MAP_ROAD_DEF ROAD_O_RECORD;
    MAP_ROAD_DEF ROAD_P_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_Z_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_X_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_D_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_Y_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_U_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_W_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_B_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_V_RECORD;
    MAP_CROSSROAD_DEF CROSSROAD_C_RECORD;
};

typedef DB_CROSSROAD_RECORD_DEF {
    mtype:Traffic_light east_color;
    mtype:Traffic_light south_color;
    mtype:Traffic_light west_color;
    mtype:Traffic_light north_color;
};

typedef DB_ALL_CROSSROADS_DEF {
    DB_CROSSROAD_RECORD_DEF crossroad_Z_record;
    DB_CROSSROAD_RECORD_DEF crossroad_Y_record;
    DB_CROSSROAD_RECORD_DEF crossroad_X_record;
    DB_CROSSROAD_RECORD_DEF crossroad_W_record;
    DB_CROSSROAD_RECORD_DEF crossroad_V_record;
    DB_CROSSROAD_RECORD_DEF crossroad_U_record;
    DB_CROSSROAD_RECORD_DEF crossroad_D_record;
    DB_CROSSROAD_RECORD_DEF crossroad_C_record;
    DB_CROSSROAD_RECORD_DEF crossroad_B_record;
}

mtype:Crossroads target_crossroad[3];

MAP_DEF MAP;

int clock;

// All communication channels are synchronous
chan query_signal_lights = [0] of {short, mtype:Crossroads}; // vehicle ID, crossroad name

chan query_signal_lights_return = [0] of {short, DB_CROSSROAD_RECORD_DEF}; // vehicle ID, crossroad record

chan set_signal_lights = [0] of {int, DB_ALL_CROSSROADS_DEF}; // Sender clock, payload

chan set_signal_lights_return = [0] of {int}; // Receiver clock

chan query_vehicle_status = [0] of {short, short}; // vehicle ID, vehicle ID (queried one)

chan query_vehicle_status_return = [0] of {byte};

chan set_vehicle_status = [0] of {byte};

chan set_vehicle_status_return = [0] of {byte};

chan query_location = [0] of {byte};

chan query_location_return = [0] of {byte};

chan add_vehicle = [0] of {short};

chan add_vehicle_return = [0] of {short};

proctype Vehicle(short id) {

    short self_id = id;
    printf("Vehicle %d running\n", self_id);
    
}

proctype Traffic_Signal_Control_Master() {

    printf("Traffic light control master running\n");

}

proctype Backend() {

    printf("Backend running\n");

    clock = 0;

    spin_lock(mutex);

    spin_unlock(mutex);

    // byte congestion_index[2];

    // congestion_index[0] = 0;
    // congestion_index[1] = 0;

    // do
    // ::set_road_congestion?congestion_index[0];
    // od

}

init {

    // Initialize target crossroad list
    target_crossroad[0] = CROSSROAD_B;
    target_crossroad[1] = CROSSROAD_C;
    target_crossroad[2] = CROSSROAD_D;

    // Initialize MAP
    

    short id;

    run Backend();

    for (id : 1..NUMBER_OF_VEHICLES) {
        run Vehicle(id);
    }

    run Traffic_Signal_Control_Master();
}