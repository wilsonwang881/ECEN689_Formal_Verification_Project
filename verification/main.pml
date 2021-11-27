/*
ECEN 689 Introduction to Formal Verification
Texas A&M University
Date: 2021.11.7

This file serves the purpose of model checking with Spin.

The file is written in Promela syntax.
*/

#include "lock.h"

short NUMBER_OF_VEHICLES = 5;

#define CHANNEL_LENGTH 1

bit mutex = 0;

bit vehicles_reported[NUMBER_OF_VEHICLES];

short number_of_vehicles_reported;

bit traffic_light_reported;

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

MAP_DEF MAP;

typedef DB_CROSSROAD_RECORD_DEF {
    mtype:Traffic_light traffic_lights[4+1];
};

typedef DB_VEHICLE_RECORD_DEF {
    mtype:Road road_segment;
    mtype:Direction direction;
    byte location;
    mtype:speed speed;
    mtype:Route_completion_status route_completion;
};

typedef DB_DEF {
    DB_CROSSROAD_RECORD_DEF crossroad_records[9 + 1];  
    DB_VEHICLE_RECORD_DEF vehicle_records[10];
    short pending_vehicles;
    short vehicle_collisions;
    short u_turns;
    short throughtput;
    short red_light_violations;
};

DB_DEF db;
DB_DEF db_reported;

typedef ALL_CROSSROADS_DEF {
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

byte clock;

// All communication channels are synchronous
chan query_signal_lights = [CHANNEL_LENGTH] of {short, mtype:Crossroads}; // vehicle ID, crossroad name

chan query_signal_lights_return = [CHANNEL_LENGTH] of {short, DB_CROSSROAD_RECORD_DEF}; // vehicle ID, crossroad record

chan set_signal_lights = [1] of {byte, ALL_CROSSROADS_DEF}; // Sender clock, payload

chan set_signal_lights_return = [1] of {byte}; // Receiver clock

chan set_vehicle_status = [1] of {short, DB_VEHICLE_RECORD_DEF, byte}; // vehicle ID, vehicle record, clock

chan set_vehicle_status_return = [1] of {short, byte}; // vehicle ID, clock

chan query_location = [1] of {short, mtype:Road, mtype:Direction, byte}; // vehicle ID, road segment name, direction, location

chan query_location_return = [1] of {short, bit, byte}; // vehicle ID, vehicle present or nots, number of vehicles on that lane

chan add_vehicle = [1] of {short}; // vehicle ID

chan add_vehicle_return = [1] of {short, bit, byte}; // vehicle ID, result of adding vehicles, clock

proctype Backend_query_signal_lights() {

    short query_id;
    mtype:Crossroads query_crossroad;

    mtype:Signal_light_positions i;

    DB_CROSSROAD_RECORD_DEF crossroad_record;

    loop:
    do
    ::  len(query_signal_lights) >= 0 ->
        query_signal_lights?query_id, query_crossroad;

        spin_lock(mutex);

        for(i: 0..EAST) {
            crossroad_record.traffic_lights[i] = db.crossroad_records[query_crossroad].traffic_lights[i];
        }
        

        spin_unlock(mutex);

        return_signal_light_query:
        do
        ::  len(query_signal_lights_return) >= 0 ->
            query_signal_lights_return!query_id, crossroad_record;
            break;
        ::  else ->
            goto return_signal_light_query;       
        od     
    ::  else ->
        goto loop;
    od
}

proctype Backend_set_signal_lights() {

    byte query_clock;
    ALL_CROSSROADS_DEF payload;

    byte i;

    loop:
    do
    ::  len(set_signal_lights) >= 0 ->
        set_signal_lights?query_clock,payload;

        spin_lock(mutex);

        if
        ::  (query_clock == clock) ->

            traffic_light_reported = 1;

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_Z].traffic_lights[i] = payload.crossroad_Z_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_Y].traffic_lights[i] = payload.crossroad_Y_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_X].traffic_lights[i] = payload.crossroad_X_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_W].traffic_lights[i] = payload.crossroad_W_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_V].traffic_lights[i] = payload.crossroad_V_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_U].traffic_lights[i] = payload.crossroad_U_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_D].traffic_lights[i] = payload.crossroad_D_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_C].traffic_lights[i] = payload.crossroad_C_record.traffic_lights[i];
            }

            for(i: 0..EAST) {
                db_reported.crossroad_records[CROSSROAD_B].traffic_lights[i] = payload.crossroad_B_record.traffic_lights[i];
            }

        ::  else ->
            skip;
        fi        

        spin_unlock(mutex);

        set_signal_lights_return!clock; 
    ::  else ->
        goto loop;
    od
}

proctype Backend_set_vehicle_status() {

    short query_id;
    DB_VEHICLE_RECORD_DEF payload;
    byte query_clock;

    short i, j;

    bit number_of_vehicles_finished[31];

    loop:
    do
    ::  len(set_vehicle_status) >= 0 ->
        set_vehicle_status?query_id, payload, query_clock;

        spin_lock(mutex);

        // Update vehicle records
        if
        ::  ((query_clock == clock) && (vehicles_reported[query_id] == 0)) ->

            number_of_vehicles_reported++;
            vehicles_reported[query_id] = 1;

            db_reported.vehicle_records[query_id].road_segment = payload.road_segment;
            db_reported.vehicle_records[query_id].direction = payload.direction;
            db_reported.vehicle_records[query_id].location = payload.location;
            db_reported.vehicle_records[query_id].speed = payload.speed;
            db_reported.vehicle_records[query_id].route_completion = payload.route_completion;
        ::  else ->
            goto return_set_vehicle_status;
        fi

        // Adjust the number of pending vehicles
        if
        ::  ((payload.road_segment == ROAD_A) && (payload.location == 2) && (payload.direction == DIRECTION_LEFT)) ->
            db_reported.pending_vehicles++;
        ::  else ->
            goto return_set_vehicle_status;
        fi

        // If all vehicles and traffic lights have reported, update the database
        if
        ::  ((number_of_vehicles_reported == NUMBER_OF_VEHICLES) && traffic_light_reported) ->

            // Reset report indicators
            number_of_vehicles_reported = 0;

            for(i: 0..(NUMBER_OF_VEHICLES-1)) {
                vehicles_reported[i] = 0;
            }

            traffic_light_reported = 0

            clock = clock + 2;

            // Check collisions
            db_reported.vehicle_collisions = 0;

            for(i: 0..(NUMBER_OF_VEHICLES-1)) {
                
                if
                ::  (db_reported.vehicle_records[i].road_segment != ROAD_A) && \
                    (db_reported.vehicle_records[i].location != 2) ->

                    for(j: 0..(NUMBER_OF_VEHICLES-1)) {                        
                        if
                        ::  (i != j) ->
                            if
                            ::  ((db_reported.vehicle_records[i].road_segment == db_reported.vehicle_records[j].road_segment) && \
                                (db_reported.vehicle_records[i].direction == db_reported.vehicle_records[j].direction) && 
                                (db_reported.vehicle_records[i].location == db_reported.vehicle_records[j].location)) ->
                                db_reported.vehicle_collisions++;
                            ::  else ->
                                skip;
                            fi
                        ::  else ->
                            skip;
                        fi
                    }
                ::  else ->
                    skip;
                fi
            }

            assert(db_reported.vehicle_collisions == 0);

            // Check vehicle U-turn, throughput and traffic light violation
            db_reported.u_turns = 0;
            db_reported.throughtput = 0;
            db_reported.red_light_violations = 0;
            bit has_vehicle_finished = 0;

            for(i: 0..(NUMBER_OF_VEHICLES-1)) {

                // Check U-turn
                if
                ::  ((db.vehicle_records[i].road_segment == db_reported.vehicle_records[i].road_segment) && \
                    (db.vehicle_records[i].location == db_reported.vehicle_records[i].location) && \
                    (db.vehicle_records[i].direction == db_reported.vehicle_records[i].direction) && \
                    (db.vehicle_records[i].road_segment != ROAD_A) && \
                    (db.vehicle_records[i].location != 2)) ->
                    db_reported.u_turns++;
                ::  else ->
                    skip;
                fi

                // Check throughput
                if
                ::  (db_reported.vehicle_records[i].road_segment == ROAD_A && \
                    db_reported.vehicle_records[i].direction == DIRECTION_RIGHT && \
                    db_reported.vehicle_records[i].location == 1) ->
                    has_vehicle_finished = 1;
                ::  else ->
                    skip;
                fi

                // Check traffic light violations
                if
                ::  ((db.vehicle_records[i].location == 0) || \
                    (db.vehicle_records[i].location == 29)) && \
                    ((db.vehicle_records[i].road_segment != ROAD_A) && \
                    (db.vehicle_records[i].direction != DIRECTION_RIGHT)) ->

                    mtype:Crossroads crossroad_to_query = MAP.ROAD_RECORD[db.vehicle_records[i].road_segment].direction_records[db.vehicle_records[i].direction].crossroad;
                    mtype:Signal_light_positions traffic_light_orientation = MAP.ROAD_RECORD[db.vehicle_records[i].road_segment].direction_records[db.vehicle_records[i].direction].traffic_light_orientation;

                    mtype:Traffic_light traffic_light_color = db.crossroad_records[crossroad_to_query].traffic_lights[traffic_light_orientation];

                    if
                    ::  (traffic_light_color == RED) ->
                        if
                        ::  (db_reported.vehicle_records[i].road_segment != db.vehicle_records[i].road_segment) ->
                            db_reported.red_light_violations++;
                        ::  else ->
                            skip;
                        fi
                    ::  else ->
                        skip;
                    fi
                ::  else ->
                    skip;
                fi                                
            }

            // Compute the throughput
            if
            ::  has_vehicle_finished ->
                number_of_vehicles_finished[clock % 30] = 1;
            :: else ->
                number_of_vehicles_finished[clock] = 0;
            fi

            short sum = 0;

            for(i: 0..31) {
                sum = sum + number_of_vehicles_finished[i];
            }

            db_reported.throughtput = sum * 120;

            assert(db_reported.u_turns == 0);
            assert(db_reported.red_light_violations == 0);

            // Commit the changes to the past state storage
            db.pending_vehicles = db_reported.pending_vehicles;
            db.vehicle_collisions = db_reported.vehicle_collisions;
            db.u_turns = db_reported.u_turns;
            db.throughtput = db_reported.throughtput;
            db.red_light_violations = db_reported.red_light_violations;

            for(i: 0..(NUMBER_OF_VEHICLES-1)) {
                db.vehicle_records[i].road_segment = db_reported.vehicle_records[i].road_segment;
                db.vehicle_records[i].direction = db_reported.vehicle_records[i].direction;
                db.vehicle_records[i].location = db_reported.vehicle_records[i].location;
                db.vehicle_records[i].speed = db_reported.vehicle_records[i].speed;
                db.vehicle_records[i].route_completion = db_reported.vehicle_records[i].route_completion;
            }

            for(i: CROSSROAD_B..CROSSROAD_Z) {
                for(j: NORTH..EAST) {
                    db.crossroad_records[i].traffic_lights[j] = db_reported.crossroad_records[i].traffic_lights[j];                     
                }
            }
        ::  else ->
            goto return_set_vehicle_status;
        fi

        return_set_vehicle_status:
        spin_unlock(mutex);
        do
        ::  len(set_vehicle_status_return) >= 0 ->
            set_vehicle_status_return!query_id, clock;                
            break;
        ::  else ->
            goto return_set_vehicle_status;
        od
    ::  else ->
        goto loop;
    od

}

proctype Backend_query_location() {

    short query_id;
    mtype:Road query_road;
    mtype:Direction query_direction;
    byte location;

    bit vehicle_presence = 0;

    short i, number_of_vehicles_on_that_lane;

    loop:
    do
    ::  len(query_location) >= 0 ->
        query_location?query_id, query_road, query_direction, location;

        spin_lock(mutex);

        for(i: 0..(NUMBER_OF_VEHICLES-1)) {
            if
            ::  ((db.vehicle_records[i].road_segment == query_road) && \
                (db.vehicle_records[i].direction == query_direction) && \
                (db.vehicle_records[i].location == location)) ->
                vehicle_presence = 1;
            ::  else ->
                skip;
            fi

            number_of_vehicles_on_that_lane = 0;

            if
            ::  ((db.vehicle_records[i].road_segment == query_road) && \
                (db.vehicle_records[i].direction == query_direction)) ->
                number_of_vehicles_on_that_lane++;
            ::  else ->
                skip;
            fi
        }

        spin_unlock(mutex);

        query_location_return!query_id, vehicle_presence, number_of_vehicles_on_that_lane;    
    ::  else ->
        goto loop;    
    od
}

proctype Backend_add_vehicle() {

    short query_id;

    bit vehicle_added = 0;

    short i;

    loop:
    do
    ::  len(add_vehicle) >= 0 ->
        add_vehicle?query_id;

        spin_lock(mutex);

        vehicle_added = 0;

        bit permission_to_add_vehicle = 1;

        // Check if there were any vehicle on road segment A in the previous time slot
        for(i: 0..(NUMBER_OF_VEHICLES-1)) {
            if
            ::  ((db.vehicle_records[i].road_segment == ROAD_A) && \
                (db.vehicle_records[i].direction == DIRECTION_LEFT) && \
                (db.vehicle_records[i].location == 1)) ->
                permission_to_add_vehicle = 0;
            ::  else ->
                skip;
            fi

            if
            ::  ((db_reported.vehicle_records[i].road_segment == ROAD_A) && \
                (db_reported.vehicle_records[i].direction == DIRECTION_LEFT) && \
                (db_reported.vehicle_records[i].location == 1)) ->
                permission_to_add_vehicle = 0;
            ::  else ->
                skip;
            fi
        }

        if
        ::  permission_to_add_vehicle ->
            db_reported.vehicle_records[query_id].road_segment = ROAD_A;
            db_reported.vehicle_records[query_id].direction = DIRECTION_LEFT;
            db_reported.vehicle_records[query_id].location = 1;
            vehicle_added = 1;
        ::  else ->
            vehicle_added = 0;
        fi

        spin_unlock(mutex);

        add_vehicle_return!query_id, vehicle_added, clock;
    ::  else ->
        goto loop;
    od
}

proctype Vehicle(short id) {

    DB_VEHICLE_RECORD_DEF self;

    self.road_segment = ROAD_A;
    self.direction = DIRECTION_LEFT;
    self.location = 2;
    self.speed = STOPPED;
    self.route_completion = NOT_STARTED;

    bit location_visited[4];

    short i;

    for(i: 0..3) {
        location_visited[i] = 0;
    }

    byte current_time = 0;

    mtype:Crossroads crossroad_query_targt = CROSSROAD_Z;

    DB_CROSSROAD_RECORD_DEF crossroad_lights;

    byte received_clock;

    update_backend:
    do
    ::  len(set_vehicle_status) >= 0 ->
        set_vehicle_status!id, self, current_time;
        set_vehicle_status_return??eval(id), received_clock;

        if
        ::  received_clock == (current_time + 2) ->
            current_time = received_clock;
            goto query_backend; 
        ::  else ->
            goto update_backend;  
        fi        
    :: goto update_backend;  
    od

    query_backend:
    do
    ::  len(query_signal_lights) >= 0 ->
        query_signal_lights!id,crossroad_query_targt;
        query_signal_lights_return??eval(id),crossroad_lights;  
        goto update_backend;
    ::  else ->
        goto query_backend;        
    od
}

proctype Traffic_Signal_Control_Master() {

    ALL_CROSSROADS_DEF self_traffic_light_records;
    ALL_CROSSROADS_DEF received_traffic_light_records

    byte self_clock;   
    byte received_clock;

    decision_making_state:  
    do
    ::  goto backend_reporting_state;
    od
    
    backend_reporting_state:
    do
    ::  len(set_signal_lights) >= 0 ->
        set_signal_lights!self_clock,self_traffic_light_records;
        set_signal_lights_return?received_clock;

        if
        ::  (received_clock == (self_clock + 2)) ->
            self_clock = received_clock
            goto decision_making_state; 
        ::  else ->
            goto backend_reporting_state;
        fi
    ::  else ->
        goto backend_reporting_state;
    od
}

init {    

    // Initialize the MAP and the target crossroad list
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

    // Initialize both db(past state) and db_reported(current state)
    int i, j, k;

    // Initialize crossroad records
    // Iteration order: crossroad -> orientation
    for(i: CROSSROAD_B..CROSSROAD_Z) {
        for(j: NORTH..EAST) {
            db.crossroad_records[i].traffic_lights[j] = RED;
            db_reported.crossroad_records[i].traffic_lights[j] = RED;
        }
    }

    // Initialize vehicle records
    for(i: 0..(NUMBER_OF_VEHICLES-1)) {
        db.vehicle_records[i].road_segment = ROAD_A;
        db.vehicle_records[i].direction = DIRECTION_LEFT;
        db.vehicle_records[i].location = 2;
        db.vehicle_records[i].speed = STOPPED;
        db.vehicle_records[i].route_completion = NOT_STARTED;

        db_reported.vehicle_records[i].road_segment = ROAD_A;
        db_reported.vehicle_records[i].direction = DIRECTION_LEFT;
        db_reported.vehicle_records[i].location = 2;
        db_reported.vehicle_records[i].speed = STOPPED;
        db_reported.vehicle_records[i].route_completion = NOT_STARTED;

        vehicles_reported[i] = 0;
    }

    number_of_vehicles_reported = 0;

    traffic_light_reported = 0;

    // Set statistics    
    db.pending_vehicles = NUMBER_OF_VEHICLES;
    db.vehicle_collisions = 0;
    db.u_turns = 0;
    db.throughtput = 0;
    db.red_light_violations = 0;
    
    db_reported.pending_vehicles = NUMBER_OF_VEHICLES;
    db_reported.vehicle_collisions = 0;
    db_reported.u_turns = 0;
    db_reported.throughtput = 0;
    db_reported.red_light_violations = 0;

    // Set the clock
    clock = 2;

    short id;

    mutex = 0;

    atomic {
        run Backend_query_signal_lights();
        run Backend_set_signal_lights();
        run Backend_set_vehicle_status();
        run Backend_query_location();
        run Backend_add_vehicle();
    }
    

    run Traffic_Signal_Control_Master();

    atomic {
        for (id: 0..(NUMBER_OF_VEHICLES-1)) {
            run Vehicle(id);
        }
    }        
}