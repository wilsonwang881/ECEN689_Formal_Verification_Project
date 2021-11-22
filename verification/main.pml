/*
ECEN 689 Introduction to Formal Verification
Texas A&M University
Date: 2021.11.7

This file serves the purpose of model checking with Spin.

The file is written in Promela syntax.
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
    MAP_ROAD_DIRECTION_Def direction_records[2+1];
};

typedef MAP_CROSSROAD_DEF {
    mtype:Road road_records[4+1];
};

typedef MAP_DEF {
    MAP_ROAD_DEF ROAD_RECORD[13+1];
    MAP_CROSSROAD_DEF CROSSROAD_RECORD[9+1];
    mtype:Crossroads target_crossroad[3];
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
};

typedef DB_VEHICLE_RECORD_DEF {
    short vehicle_id;
    mtype:Road road_segment;
    mtype:Direction direction;
    byte location;
    mtype:speed speed;
    mtype:Route_completion_status route_completion;
};

typedef DB_ROAD_ONE_SIDE_SEGMENT_RECORD_DEF {
    DB_VEHICLE_RECORD_DEF vehicle_record[30];
};

typedef DB_ROAD_SEGMENT_RECORD_DEF {
    DB_ROAD_ONE_SIDE_SEGMENT_RECORD_DEF left_lane_vehicle_record;
    DB_ROAD_ONE_SIDE_SEGMENT_RECORD_DEF right_lane_vehicle_record;
};

MAP_DEF MAP;

int clock;

// All communication channels are synchronous
chan query_signal_lights = [0] of {short, mtype:Crossroads}; // vehicle ID, crossroad name

chan query_signal_lights_return = [0] of {short, DB_CROSSROAD_RECORD_DEF}; // vehicle ID, crossroad record

chan set_signal_lights = [0] of {int, DB_ALL_CROSSROADS_DEF}; // Sender clock, payload

chan set_signal_lights_return = [0] of {int}; // Receiver clock

chan set_vehicle_status = [0] of {short, DB_VEHICLE_RECORD_DEF, int}; // vehicle ID, vehicle record, clock

chan set_vehicle_status_return = [0] of {short, int}; // vehicle ID, clock

chan query_location = [0] of {short, mtype:Road, mtype:Direction, byte}; // vehicle ID, road segment name, direction, location

chan query_location_return = [0] of {short, bit, DB_VEHICLE_RECORD_DEF}; // vehicle ID, vehicle present or not, vehicle record if any

chan add_vehicle = [0] of {short}; // vehicle ID

chan add_vehicle_return = [0] of {short, bit, int}; // vehicle ID, result of adding vehicles, clock

proctype Vehicle(short id) {

    DB_VEHICLE_RECORD_DEF self;
    self.vehicle_id = id;

    bit location_visited[4];
    int current_time = 0;

    printf("Vehicle %d running\n", self.vehicle_id);
    
}

proctype Traffic_Signal_Control_Master() {

    printf("Traffic light control master running\n");

}

proctype Backend() {

    printf("Backend running\n");

    clock = 0;

    spin_lock(mutex);

    spin_unlock(mutex);

}

init {    

    // Initialize MAP and the target crossroad list
    MAP.ROAD_RECORD[ROAD_A].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_Z;
    MAP.ROAD_RECORD[ROAD_A].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;

    MAP.ROAD_RECORD[ROAD_E].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_X;
    MAP.ROAD_RECORD[ROAD_E].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_E].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_Z;
    MAP.ROAD_RECORD[ROAD_E].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.ROAD_RECORD[ROAD_F].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_D;
    MAP.ROAD_RECORD[ROAD_F].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_F].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_X;
    MAP.ROAD_RECORD[ROAD_F].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.ROAD_RECORD[ROAD_G].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_Z;
    MAP.ROAD_RECORD[ROAD_G].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_G].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_Y;
    MAP.ROAD_RECORD[ROAD_G].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_H].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_X;
    MAP.ROAD_RECORD[ROAD_H].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_H].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_U;
    MAP.ROAD_RECORD[ROAD_H].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_I].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_D;
    MAP.ROAD_RECORD[ROAD_I].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_I].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_W;
    MAP.ROAD_RECORD[ROAD_I].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_J].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_U;
    MAP.ROAD_RECORD[ROAD_J].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_J].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_Y;
    MAP.ROAD_RECORD[ROAD_J].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.ROAD_RECORD[ROAD_K].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_W;
    MAP.ROAD_RECORD[ROAD_K].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_K].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_U;
    MAP.ROAD_RECORD[ROAD_K].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.ROAD_RECORD[ROAD_L].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_Y;
    MAP.ROAD_RECORD[ROAD_L].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_L].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_B;
    MAP.ROAD_RECORD[ROAD_L].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_M].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_U;
    MAP.ROAD_RECORD[ROAD_M].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_M].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_V;
    MAP.ROAD_RECORD[ROAD_M].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_N].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_W;
    MAP.ROAD_RECORD[ROAD_N].direction_records[DIRECTION_LEFT].traffic_light_orientation = NORTH;
    MAP.ROAD_RECORD[ROAD_N].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_C;
    MAP.ROAD_RECORD[ROAD_N].direction_records[DIRECTION_RIGHT].traffic_light_orientation = SOUTH;

    MAP.ROAD_RECORD[ROAD_O].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_V;
    MAP.ROAD_RECORD[ROAD_O].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_O].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_B;
    MAP.ROAD_RECORD[ROAD_O].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.ROAD_RECORD[ROAD_P].direction_records[DIRECTION_LEFT].crossroad = CROSSROAD_C;
    MAP.ROAD_RECORD[ROAD_P].direction_records[DIRECTION_LEFT].traffic_light_orientation = EAST;
    MAP.ROAD_RECORD[ROAD_P].direction_records[DIRECTION_RIGHT].crossroad = CROSSROAD_V;
    MAP.ROAD_RECORD[ROAD_P].direction_records[DIRECTION_RIGHT].traffic_light_orientation = WEST;

    MAP.CROSSROAD_RECORD[CROSSROAD_Z].road_records[WEST] = ROAD_A;
    MAP.CROSSROAD_RECORD[CROSSROAD_Z].road_records[EAST] = ROAD_E;
    MAP.CROSSROAD_RECORD[CROSSROAD_Z].road_records[SOUTH] = ROAD_G;

    MAP.CROSSROAD_RECORD[CROSSROAD_X].road_records[WEST] = ROAD_E;
    MAP.CROSSROAD_RECORD[CROSSROAD_X].road_records[EAST] = ROAD_F;
    MAP.CROSSROAD_RECORD[CROSSROAD_X].road_records[SOUTH] = ROAD_H;

    MAP.CROSSROAD_RECORD[CROSSROAD_D].road_records[WEST] = ROAD_F;
    MAP.CROSSROAD_RECORD[CROSSROAD_D].road_records[SOUTH] = ROAD_I;
    
    MAP.CROSSROAD_RECORD[CROSSROAD_Y].road_records[NORTH] = ROAD_G;
    MAP.CROSSROAD_RECORD[CROSSROAD_Y].road_records[EAST] = ROAD_J;
    MAP.CROSSROAD_RECORD[CROSSROAD_Y].road_records[SOUTH] = ROAD_L;
    
    MAP.CROSSROAD_RECORD[CROSSROAD_U].road_records[NORTH] = ROAD_H;
    MAP.CROSSROAD_RECORD[CROSSROAD_U].road_records[EAST] = ROAD_K;
    MAP.CROSSROAD_RECORD[CROSSROAD_U].road_records[WEST] = ROAD_J;
    MAP.CROSSROAD_RECORD[CROSSROAD_U].road_records[SOUTH] = ROAD_M;

    MAP.CROSSROAD_RECORD[CROSSROAD_W].road_records[NORTH] = ROAD_I;
    MAP.CROSSROAD_RECORD[CROSSROAD_W].road_records[WEST] = ROAD_K;
    MAP.CROSSROAD_RECORD[CROSSROAD_W].road_records[SOUTH] = ROAD_N;

    MAP.CROSSROAD_RECORD[CROSSROAD_B].road_records[NORTH] = ROAD_L;
    MAP.CROSSROAD_RECORD[CROSSROAD_B].road_records[EAST] = ROAD_O;

    MAP.CROSSROAD_RECORD[CROSSROAD_V].road_records[NORTH] = ROAD_M;
    MAP.CROSSROAD_RECORD[CROSSROAD_V].road_records[WEST] = ROAD_O;
    MAP.CROSSROAD_RECORD[CROSSROAD_V].road_records[EAST] = ROAD_P;
    
    MAP.CROSSROAD_RECORD[CROSSROAD_C].road_records[NORTH] = ROAD_N;
    MAP.CROSSROAD_RECORD[CROSSROAD_C].road_records[WEST] = ROAD_P;    
            
    MAP.target_crossroad[0] = CROSSROAD_B;
    MAP.target_crossroad[1] = CROSSROAD_C;
    MAP.target_crossroad[2] = CROSSROAD_D;
    short id;

    run Backend();

    for (id : 1..NUMBER_OF_VEHICLES) {
        run Vehicle(id);
    }

    run Traffic_Signal_Control_Master();
}