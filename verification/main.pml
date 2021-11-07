/*
ECEN 689 Introduction to Formal Verification
Texas A&M University
Date: 2021.11.7

This file serves the purpose of model checking with Spin.
All logics from the Python application are included and modeled.
*/

#include "lock.h"

short NUMBER_OF_VEHICLES = 150;

byte NUMBER_OF_ROAD_SEGMENTS = 12;

// All communication channels are synchronous
chan query_signal_lights = [0] of {byte};

chan set_signal_lights = [0] of {byte};

chan query_vehicle_status = [0] of {byte};

chan set_vehicle_status = [0] of {byte};

chan query_road_congestion = [0] of {byte};

chan set_road_congestion = [0] of {byte};

chan query_location = [0] of {byte};

chan add_vehicle = [0] of {short};

proctype Congestion_Computation(short crossroad_id) {

    short self_id = crossroad_id;
    printf("Congestion computation worker %d running\n", self_id);

}

proctype Vehicle(short id) {

    short self_id = id;
    printf("Vehicle %d running\n", self_id);
    
}

proctype Traffic_Signal_Control_Master() {

    printf("Traffic light control master running\n");

}

proctype Backend() {

    printf("Backend running\n");

}

// Start all threads
init {

    short id;

    run Backend();

    for (id : 1..NUMBER_OF_VEHICLES) {
        run Vehicle(id);
    }

    for (id : 1..NUMBER_OF_ROAD_SEGMENTS) {
        run Congestion_Computation(id);
    }

    run Traffic_Signal_Control_Master();
    
}