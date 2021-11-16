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

typedef Road_Direction_Def {
    mtype:Crossroads crossroad;
    mtype:Signal_light_positions traffic_light_orientation;
};

typedef Road_Def {
    Road_Direction_Def direction_left_record;
    Road_Direction_Def direction_right_record;
};

typedef Crossroad_Def {
    mtype:Road EAST_ROAD;
    mtype:Road SOUTH_ROAD;
    mtype:Road WEST_ROAD;
    mtype:Road NORTH_ROAD;
}

typedef Map_Def {
    Road_Def ROAD_A_RECORD;
    Road_Def ROAD_E_RECORD;
    Road_Def ROAD_F_RECORD;
    Road_Def ROAD_G_RECORD;
    Road_Def ROAD_H_RECORD;
    Road_Def ROAD_I_RECORD;
    Road_Def ROAD_J_RECORD;
    Road_Def ROAD_K_RECORD;
    Road_Def ROAD_L_RECORD;
    Road_Def ROAD_M_RECORD;
    Road_Def ROAD_N_RECORD;
    Road_Def ROAD_O_RECORD;
    Road_Def ROAD_P_RECORD;
    Crossroad_Def CROSSROAD_Z_RECORD;
    Crossroad_Def CROSSROAD_X_RECORD;
    Crossroad_Def CROSSROAD_D_RECORD;
    Crossroad_Def CROSSROAD_Y_RECORD;
    Crossroad_Def CROSSROAD_U_RECORD;
    Crossroad_Def CROSSROAD_W_RECORD;
    Crossroad_Def CROSSROAD_B_RECORD;
    Crossroad_Def CROSSROAD_V_RECORD;
    Crossroad_Def CROSSROAD_C_RECORD;
}

mtype:Crossroads target_crossroad[3];

Map_Def MAP;

// All communication channels are synchronous
chan query_signal_lights = [0] of {byte};

chan set_signal_lights = [0] of {byte};

chan query_vehicle_status = [0] of {byte};

chan set_vehicle_status = [0] of {byte};

chan query_road_congestion = [0] of {byte};

chan set_road_congestion = [0] of {byte};

chan query_location = [0] of {byte};

chan add_vehicle = [0] of {short};

proctype Vehicle(short id) {

    short self_id = id;
    printf("Vehicle %d running\n", self_id);
    
}

proctype Traffic_Signal_Control_Master() {

    printf("Traffic light control master running\n");

}

proctype Backend() {

    printf("Backend running\n");

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