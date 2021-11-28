/*
ECEN 689 Introduction to Formal Verification
Texas A&M University
Date: 2021.11.7

This file serves the purpose of model checking with Spin.

The file is written in Promela syntax.
*/

#include "lock.h"

short NUMBER_OF_VEHICLES = 4;

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

proctype get_road_segment(chan get_road_segment_return; byte current_road_segment; byte current_crossroad) {
    
    if
    ::  current_road_segment == ROAD_A ->
        get_road_segment_return!0, ROAD_A, ROAD_A, ROAD_A, current_crossroad;

    ::  else ->

        byte i, j;

        for(i: DIRECTION_RIGHT..DIRECTION_LEFT) {
            if
            ::  MAP.ROAD_RECORD[current_road_segment].direction_records[i].crossroad != current_crossroad ->

                mtype:Crossroads crossroad_to_query = MAP.ROAD_RECORD[current_road_segment].direction_records[i].crossroad;

                mtype:Road road_segment_list[3];

                j = 0;

                for(i: NORTH..EAST) {
                    if
                    ::  MAP.CROSSROAD_RECORD[crossroad_to_query].road_records[i] != current_road_segment ->
                        road_segment_list[j] = MAP.CROSSROAD_RECORD[crossroad_to_query].road_records[i];
                        j++;
                    ::  else ->
                        skip;
                    fi
                }

                get_road_segment_return!j, road_segment_list[0], road_segment_list[1], road_segment_list[2], crossroad_to_query;

            ::  else ->
                skip;
            fi
        }
    fi
   
}

proctype routing(chan routing_return; byte current_crossroad; byte next_road_segment; byte target_crossroad) {

    byte minimum_route_length = 6;
    byte tmpp_minimum_route_length = 6;

    mtype:Road next_road_segment_to_take;

    byte step_2_current_crossroad;
    byte step_3_current_crossroad;
    byte step_4_current_crossroad;
    byte step_5_current_crossroad;
    byte step_6_current_crossroad;

    byte number_of_step_1_road_segment;
    byte number_of_step_2_road_segment;
    byte number_of_step_3_road_segment;
    byte number_of_step_4_road_segment;
    byte number_of_step_5_road_segment;

    byte list_of_step_1_road_segment[3];
    byte list_of_step_2_road_segment[3];
    byte list_of_step_3_road_segment[3];
    byte list_of_step_4_road_segment[3];
    byte list_of_step_5_road_segment[3];

    byte i_1;
    byte i_2;
    byte i_3;
    byte i_4;
    byte i_5;

    chan return_get_road_segment = [0] of {short, mtype:Road, mtype:Road, mtype:Road, mtype:Crossroads};

    run get_road_segment(return_get_road_segment, next_road_segment, current_crossroad);
    return_get_road_segment?number_of_step_1_road_segment, list_of_step_1_road_segment[0], list_of_step_1_road_segment[1], list_of_step_1_road_segment[2], step_2_current_crossroad;

    for(i_1: 0..number_of_step_1_road_segment) {

        run get_road_segment(return_get_road_segment, list_of_step_1_road_segment[i_1], step_2_current_crossroad);
        return_get_road_segment?number_of_step_2_road_segment, list_of_step_2_road_segment[0], list_of_step_2_road_segment[1], list_of_step_2_road_segment[2], step_3_current_crossroad;

        for(i_2: 0..number_of_step_2_road_segment) {

            run get_road_segment(return_get_road_segment, list_of_step_2_road_segment[i_2], step_3_current_crossroad);
            return_get_road_segment?number_of_step_3_road_segment, list_of_step_3_road_segment[0], list_of_step_3_road_segment[1], list_of_step_3_road_segment[2], step_4_current_crossroad;

            for(i_3: 0..number_of_step_3_road_segment) {

                run get_road_segment(return_get_road_segment, list_of_step_3_road_segment[i_2], step_4_current_crossroad);
                return_get_road_segment?number_of_step_4_road_segment, list_of_step_4_road_segment[0], list_of_step_4_road_segment[1], list_of_step_4_road_segment[2], step_5_current_crossroad;

                for(i_4: 0..number_of_step_4_road_segment) {

                    run get_road_segment(return_get_road_segment, list_of_step_4_road_segment[i_2], step_5_current_crossroad);
                    return_get_road_segment?number_of_step_5_road_segment, list_of_step_5_road_segment[0], list_of_step_5_road_segment[1], list_of_step_5_road_segment[2], step_6_current_crossroad;

                    for(i_5: 0..number_of_step_5_road_segment) {

                        if
                        ::  current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 1;
                            next_road_segment_to_take = next_road_segment;
                        ::  step_2_current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 2;
                            next_road_segment_to_take = next_road_segment;
                        ::  step_3_current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 3;
                            next_road_segment_to_take = next_road_segment;
                        ::  step_4_current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 4;
                            next_road_segment_to_take = next_road_segment;
                        ::  step_5_current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 5;
                            next_road_segment_to_take = next_road_segment;
                        ::  step_6_current_crossroad == target_crossroad ->
                            tmpp_minimum_route_length = 6;
                            next_road_segment_to_take = next_road_segment;
                        ::  else->
                            skip;
                        fi

                        if
                        ::  tmpp_minimum_route_length < minimum_route_length ->
                            minimum_route_length = tmpp_minimum_route_length;
                        ::  else ->
                            skip;
                        fi
                    }
                }
            }            
        }
    }

    routing_return!minimum_route_length;
}

proctype Vehicle(short id) {

    chan return_routing = [0] of {byte};

    DB_VEHICLE_RECORD_DEF self;

    self.road_segment = ROAD_A;
    self.direction = DIRECTION_LEFT;
    self.location = 2;
    self.speed = STOPPED;
    self.route_completion = NOT_STARTED;

    mtype:Crossroads location_visited[4];
    byte total_number_location_visited = 0;

    short i, j;

    for(i: 0..3) {
        location_visited[i] = 0;
    }

    byte current_time = 0;

    mtype:Crossroads crossroad_query_targt = CROSSROAD_Z;

    DB_CROSSROAD_RECORD_DEF crossroad_lights;

    bit added;

    byte received_clock;

    bit vehicle_present_or_not;

    byte number_of_vehicles_on_that_lane;

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
    ::  else ->
        goto update_backend;  
    od

    query_backend:
    do
    // Try to join the map
    ::  self.route_completion == NOT_STARTED ->
        do
        ::  len(add_vehicle) >= 0 ->
            add_vehicle!id;
            add_vehicle_return??eval(id), added, received_clock;
            if
            ::  added ->
                self.road_segment = ROAD_A;
                self.direction = DIRECTION_LEFT;
                self.location = 1;
                self.speed = STOPPED;
                self.route_completion = ENROUTE;
                for(i: 0..3) {
                    location_visited[i] = 0;
                }
                total_number_location_visited = 0;
            ::  else ->
                goto update_backend;
            fi
        ::  else ->
            goto update_backend;
        od

    // Already in the map
    ::  self.route_completion == ENROUTE ->

        if
        // Finishing stage
        ::  self.road_segment == ROAD_A && self.direction == DIRECTION_RIGHT ->
            if
            ::  self.location == 1 ->
                self.road_segment = ROAD_A;
                self.direction = DIRECTION_LEFT;
                self.location = 2;
                self.speed = STOPPED;
                for(i: 0..3) {
                    location_visited[i] = 0;
                }
                total_number_location_visited = 0;
                self.route_completion = NOT_STARTED;
            ::  else ->
                query_road_A_location_1:
                do
                ::  len(query_location) >= 0 ->
                    query_location!id, ROAD_A, DIRECTION_RIGHT, 1;
                    query_location_return??eval(id), vehicle_present_or_not, number_of_vehicles_on_that_lane;

                    if
                    ::  vehicle_present_or_not ->
                        self.speed = STOPPED;
                        break;
                    ::  else ->
                        self.speed = MOVING;
                        self.location++;
                        break;
                    fi
                ::  else ->
                    goto query_road_A_location_1;
                od                
            fi
            goto update_backend;

        // Vehicle moving without checking traffic lights
        ::  (self.location != 0 && \
            self.location != 29) || \
            (self.location == 29 && \
            self.direction == DIRECTION_LEFT) || \
            (self.location == 0 && \
            self.direction == DIRECTION_RIGHT) ->

            // Determine the exact location to check
            byte location_to_query;

            if
            ::  self.direction == DIRECTION_RIGHT ->
                location_to_query = self.location + 1;
            ::  else ->
                location_to_query = self.location - 1;
            fi

            // check with the backend
            check_location_no_traffic_lights:
            do
            ::  len(query_location) >= 0 ->
                query_location!id, self.road_segment, self.direction, location_to_query;
                query_location_return??eval(id), vehicle_present_or_not, number_of_vehicles_on_that_lane;
                break;
            ::  else ->
                goto check_location_no_traffic_lights;
            od

            if
            ::  vehicle_present_or_not ->
                self.speed = STOPPED;
            ::  else ->
                self.location = location_to_query;
            fi

            goto query_backend;

        // Waiting to finish the route around crossroad Z
        :: (self.location ==  0 && \
            self.road_segment == ROAD_G && \
            self.direction == DIRECTION_LEFT && \
            total_number_location_visited == 3) || \
            (self.location ==  29 && \
            self.road_segment == ROAD_E && \
            self.direction == DIRECTION_RIGHT && \
            total_number_location_visited == 3)            

            check_traffic_light_at_crossroad_z:
            do
            ::  len(query_signal_lights) >= 0 ->
                query_signal_lights!id, CROSSROAD_Z;
                query_signal_lights_return??eval(id), crossroad_lights; 
            ::  else ->
                goto check_traffic_light_at_crossroad_z;
            od

            mtype:Traffic_light traffic_light_at_crossroad_z;

            if
            ::  self.road_segment == ROAD_E ->
                traffic_light_at_crossroad_z = crossroad_lights.traffic_lights[3];
            ::  else ->
                traffic_light_at_crossroad_z = crossroad_lights.traffic_lights[1];
            fi

            if
            ::  traffic_light_at_crossroad_z == RED ->
                self.speed = STOPPED;
            ::  else ->

                check_location_near_crossroad_z:
                do
                ::  len(query_location) >= 0 ->
                    query_location!id, ROAD_A, DIRECTION_RIGHT, 0;
                    query_location_return??eval(id), vehicle_present_or_not, number_of_vehicles_on_that_lane;
                    break;
                ::  else ->
                    goto check_location_near_crossroad_z;
                od
            fi

            if
            ::  vehicle_present_or_not ->
                self.speed = STOPPED;
            ::  else ->
                self.speed = MOVING;
                self.location = 0;
                self.road_segment = ROAD_A;
                self.direction = DIRECTION_RIGHT;
            fi

            goto query_backend;

        // ::  else ->
        //     skip;

        // At crossroads, need to check traffic lights
        // ::  self.location == 0 || \
        //     self.location == 29 ->
        ::  else ->

            crossroad_query_targt = MAP.ROAD_RECORD[self.road_segment].direction_records[self.direction].crossroad;
            mtype:Signal_light_positions traffic_light_orientation = MAP.ROAD_RECORD[self.road_segment].direction_records[self.direction].traffic_light_orientation;

            check_traffic_light_at_crossroad:
            do
            ::  len(query_signal_lights) >= 0 ->
                query_signal_lights!id, crossroad_query_targt;
                query_signal_lights_return??eval(id), crossroad_lights; 
            ::  else ->
                goto check_traffic_light_at_crossroad;
            od

            mtype:Traffic_light traffic_light_at_crossroad = crossroad_lights.traffic_lights[traffic_light_orientation];

            if
            ::  traffic_light_at_crossroad == RED ->
                self.speed = STOPPED;
            ::  else ->            

                bit road_segment_to_query_enable[3];

                for(i: 0..2) {
                    road_segment_to_query_enable[i] = 0;
                }                

                mtype:Signal_light_positions road_segment_to_query_key_direction[3];
                mtype:Road road_segment_to_query_val_road_segment[3];

                byte road_segment_to_query_number = 0;
                byte available_road_segment_to_query_number = 0;

                mtype:Signal_light_positions self_crossroad_position = NORTH;

                for(i: NORTH..EAST) {
                    if
                    ::  MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] != 0 && \
                        MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] != self.road_segment ->
                        road_segment_to_query_enable[road_segment_to_query_number] = 1;
                        road_segment_to_query_key_direction[road_segment_to_query_number] = i;
                        road_segment_to_query_val_road_segment[road_segment_to_query_number] = MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i];
                        road_segment_to_query_number++;
                        available_road_segment_to_query_number++;
                    ::  else ->
                        skip;
                    fi
                    
                    if
                    ::  MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] != 0 && \
                        MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] == self.road_segment ->
                        self_crossroad_position = i;
                    ::  else ->
                        skip;
                    fi
                }

                road_segment_to_query_number--;
                available_road_segment_to_query_number--;

                bit change_query_direction = 0;

                for(i: 0..road_segment_to_query_number) {                    

                    mtype:Signal_light_positions position_key = road_segment_to_query_key_direction[i];

                    if
                    ::  self_crossroad_position == SOUTH ->
                        if
                        ::  position_key == EAST || \
                            position_key == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == EAST ->
                        if
                        ::  position_key == WEST || \
                            position_key == SOUTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == NORTH ->
                        if
                        ::  position_key == SOUTH || \
                            position_key == WEST ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  else ->
                        if
                        ::  position_key == EAST || \
                            position_key == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    fi

                    mtype:Direction query_direction = self.direction;
                    
                    byte target_query_location = self.location;

                    if
                    ::  change_query_direction ->
                        if
                        ::  self.direction == DIRECTION_LEFT ->
                            query_direction = DIRECTION_RIGHT;
                        ::  else ->
                            query_direction = DIRECTION_LEFT;
                        fi
                    ::  else ->
                        target_query_location = 29 - self.location;
                    fi

                    // Check whether there are vehicles on other sides of the crossroad
                    check_vehicles_on_other_sides_of_crossroad:
                    do
                    ::  len(query_location) >= 0 ->
                        query_location!id, road_segment_to_query_val_road_segment[i], query_direction, target_query_location;
                        query_location_return??eval(id), vehicle_present_or_not, number_of_vehicles_on_that_lane;
                        break;
                    ::  else ->
                        goto check_vehicles_on_other_sides_of_crossroad;
                    od

                    if
                    ::  vehicle_present_or_not ->
                        available_road_segment_to_query_number--;
                        road_segment_to_query_enable[i] = 0;
                    ::  else ->
                        skip;
                    fi
                }

                if
                // All other sides of the crossroad have vehicles, stop
                ::  available_road_segment_to_query_number == 0 ->
                    self.speed = STOPPED;
                // Only one side of the crossroad has space to move to, move
                ::  available_road_segment_to_query_number == 1 ->
                    
                    self.speed = MOVING;

                    mtype:Road road_segment_to_move_to;

                    for(i: 0..2) {
                        if
                        ::  road_segment_to_query_enable[i] == 1 ->
                            road_segment_to_move_to = road_segment_to_query_val_road_segment[i];
                            break;
                        ::  else ->
                            skip;
                        fi
                    }

                    // Check if the vehicle will move past one of the target crossroads

                    bit found_in_target_crossroad = 0;
                
                    for(i: 0..3) {
                        if
                        ::  crossroad_query_targt == location_visited[i] ->
                            found_in_target_crossroad = 1;
                            break;
                        ::  else ->
                            skip
                        fi
                    }

                    if
                    ::  found_in_target_crossroad == 0 ->
                        for(i: 0..2) {
                            if
                            ::  crossroad_query_targt == MAP.target_crossroad[i] ->
                                found_in_target_crossroad = 1;
                                location_visited[total_number_location_visited] = 1;
                                total_number_location_visited++;
                                break;
                            ::  else ->
                                skip;
                            fi
                        }
                    ::  else ->
                        skip;
                    fi

                    // Decide if change lane direction and self direction
                    mtype:Signal_light_positions position_key_tmpp;

                    for(i: NORTH..EAST) {
                        if
                        ::  MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] == road_segment_to_move_to ->
                            position_key_tmpp = i;
                            break;
                        ::  else ->
                            skip;
                        fi
                    }

                    if
                    ::  self_crossroad_position == SOUTH ->
                        if
                        ::  position_key_tmpp == EAST || \
                            position_key_tmpp == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == EAST ->
                        if
                        ::  position_key_tmpp == WEST || \
                            position_key_tmpp == SOUTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == NORTH ->
                        if
                        ::  position_key_tmpp == SOUTH || \
                            position_key_tmpp == WEST ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  else ->
                        if
                        ::  position_key_tmpp == EAST || \
                            position_key_tmpp == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    fi

                    if
                    ::  change_query_direction ->
                        if
                        ::  self.direction == DIRECTION_LEFT ->
                            self.direction = DIRECTION_RIGHT;
                        ::  else ->
                            self.direction = DIRECTION_LEFT;
                        fi
                    ::  else ->
                        self.location = 29 - self.location;
                    fi

                    self.road_segment = road_segment_to_move_to

                // If the vehicle can move to more than one side of the crossroad
                ::  else ->                    

                    byte shortest_route_length = 7;

                    byte road_segment_path_length[3];

                    byte path_length_tmpp;

                    if 
                    // Vehicle has visited all target crossroads, route to crossroad Z
                    ::  total_number_location_visited == 3 ->

                        for(i: 0..2) {

                            if
                            ::  road_segment_to_query_enable[i] ->
                                run routing(return_routing, crossroad_query_targt, road_segment_to_query_val_road_segment[i], CROSSROAD_Z);
                                return_routing?path_length_tmpp;
                                road_segment_path_length[i] = path_length_tmpp;
                            ::  else ->
                                road_segment_path_length[i] = 7;
                            fi
                        }

                    // Vehicle has not yet visited all target crossroads
                    ::  else ->

                        for(i: 0..2) {

                            bit found = 0;

                            for(j: 0..total_number_location_visited) {

                                if
                                ::  location_visited[j] == MAP.target_crossroad[i] ->
                                    found = 1;
                                ::  else ->
                                    skip;
                                fi
                            }

                            if
                            ::  found == 0 ->                                

                                for(j: 0..3) {

                                    if
                                    ::  road_segment_to_query_enable[j] ->
                                        run routing(return_routing, crossroad_query_targt, road_segment_to_query_val_road_segment[j], MAP.target_crossroad[i]);
                                        return_routing?path_length_tmpp;
                                    
                                        if
                                        ::  path_length_tmpp < road_segment_path_length[j] ->
                                            road_segment_path_length[i] = path_length_tmpp;
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
                    fi

                    for(i: 0..3) {
                        
                        if
                        ::  road_segment_to_query_enable[j] ->

                            if
                            ::  road_segment_path_length[i] < shortest_route_length ->
                                shortest_route_length = road_segment_path_length[i];
                            ::  else ->
                                skip;
                            fi

                        ::  else ->
                            skip;
                        fi
                    }

                    mtype:Road next_road;

                    if
                    ::  road_segment_to_query_enable[0] && \
                        road_segment_path_length[0] == shortest_route_length ->
                        next_road = road_segment_to_query_val_road_segment[0];
                    ::  road_segment_to_query_enable[1] && \
                        road_segment_path_length[1] == shortest_route_length ->
                        next_road = road_segment_to_query_val_road_segment[1];
                    ::  road_segment_to_query_enable[2] && \
                        road_segment_path_length[2] == shortest_route_length ->
                        next_road = road_segment_to_query_val_road_segment[2];
                    ::  else ->
                        skip;
                    fi

                    found_in_target_crossroad = 0;
                
                    for(i: 0..3) {
                        if
                        ::  crossroad_query_targt == location_visited[i] ->
                            found_in_target_crossroad = 1;
                            break;
                        ::  else ->
                            skip
                        fi
                    }

                    if
                    ::  found_in_target_crossroad == 0 ->
                        for(i: 0..2) {
                            if
                            ::  crossroad_query_targt == MAP.target_crossroad[i] ->
                                found_in_target_crossroad = 1;
                                location_visited[total_number_location_visited] = 1;
                                total_number_location_visited++;
                                break;
                            ::  else ->
                                skip;
                            fi
                        }
                    ::  else ->
                        skip;
                    fi

                    // Decide if change lane direction and self direction

                    for(i: NORTH..EAST) {
                        if
                        ::  MAP.CROSSROAD_RECORD[crossroad_query_targt].road_records[i] == next_road ->
                            position_key_tmpp = i;
                            break;
                        ::  else ->
                            skip;
                        fi
                    }

                    if
                    ::  self_crossroad_position == SOUTH ->
                        if
                        ::  position_key_tmpp == EAST || \
                            position_key_tmpp == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == EAST ->
                        if
                        ::  position_key_tmpp == WEST || \
                            position_key_tmpp == SOUTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  self_crossroad_position == NORTH ->
                        if
                        ::  position_key_tmpp == SOUTH || \
                            position_key_tmpp == WEST ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    ::  else ->
                        if
                        ::  position_key_tmpp == EAST || \
                            position_key_tmpp == NORTH ->
                            change_query_direction = 0;
                        ::  else ->
                            change_query_direction = 1;
                        fi
                    fi

                    if
                    ::  change_query_direction ->
                        if
                        ::  self.direction == DIRECTION_LEFT ->
                            self.direction = DIRECTION_RIGHT;
                        ::  else ->
                            self.direction = DIRECTION_LEFT;
                        fi
                    ::  else ->
                        self.location = 29 - self.location;
                    fi

                    self.road_segment = road_segment_to_move_to;
                    
                fi
            fi

            goto query_backend;
                
        fi

    ::  else ->
        goto query_backend;

    od
}

proctype traffic_light_get_vehicle_location(chan res; byte road; byte lane_direction; byte location_to_query) {

    short id = NUMBER_OF_VEHICLES + 1;

    bit vehicle_present_or_not;
    short number_of_vehicles_on_that_lane;

    query:
    do
    ::  len(query_location) >= 0 ->
        query_location!id, road, lane_direction, location_to_query;
        query_location_return??eval(id), vehicle_present_or_not, number_of_vehicles_on_that_lane;
        break;
    ::  else ->
        goto query;
    od

    res!vehicle_present_or_not, number_of_vehicles_on_that_lane;
}

proctype Traffic_Signal_Control_Master() {

    chan query_return = [0] of {bit, short};

    bit exist_car1;
    bit exist_car2;
    bit exist_car3
    bit exist_car4;

    short number_of_vehicles_on_that_lane;

    ALL_CROSSROADS_DEF self_traffic_light_records;
    ALL_CROSSROADS_DEF received_traffic_light_records

    byte i;

    for(i: 0..4) {
        self_traffic_light_records.crossroad_Z_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_Y_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_X_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_W_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_V_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_U_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_D_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_C_record.traffic_lights[i] = RED;
        self_traffic_light_records.crossroad_B_record.traffic_lights[i] = RED;
    }

    byte self_clock;   
    byte received_clock;

    decision_making_state:  
    do
    ::  true ->

        byte num1 = 0;
        byte num2 = 0;
        byte num3 = 0;
        byte num4 = 0;

        exist_car1 = 0;
        exist_car2 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_L, DIRECTION_RIGHT, 29);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_O, DIRECTION_RIGHT, 29);
        query_return?exist_car2, num2;

        if
        ::  num1 >= num2 ->
            self_traffic_light_records.crossroad_B_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_B_record.traffic_lights[WEST] = RED;
        ::  else ->
            self_traffic_light_records.crossroad_B_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_B_record.traffic_lights[SOUTH] = RED;
        fi

        exist_car1 = 0;
        exist_car2 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_P, DIRECTION_LEFT, 0);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_N, DIRECTION_RIGHT, 29);
        query_return?exist_car2, num2;

        if
        ::  num1 >= num2 ->
            self_traffic_light_records.crossroad_C_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_C_record.traffic_lights[SOUTH] = RED;
        ::  else ->
            self_traffic_light_records.crossroad_C_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_C_record.traffic_lights[EAST] = RED;
        fi

        exist_car1 = 0;
        exist_car2 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_F, DIRECTION_LEFT, 0);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_I, DIRECTION_LEFT, 0);
        query_return?exist_car2, num2;

        if
        ::  num1 >= num2 ->
            self_traffic_light_records.crossroad_D_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_D_record.traffic_lights[NORTH] = RED;
        ::  else ->
            self_traffic_light_records.crossroad_D_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_D_record.traffic_lights[EAST] = RED;
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;
        exist_car4 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_H, DIRECTION_RIGHT, 29);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_J, DIRECTION_LEFT, 0);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_K, DIRECTION_RIGHT, 29);
        query_return?exist_car3, num3;

        run traffic_light_get_vehicle_location(query_return, ROAD_M, DIRECTION_LEFT, 0);
        query_return?exist_car4, num4;

        if
        ::  num1 >= num2 && \
            num1 >= num3 && \
            num1 >= num4 ->
            self_traffic_light_records.crossroad_U_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_U_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[WEST] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[EAST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 && \
            num2 >= num4 ->
            self_traffic_light_records.crossroad_U_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_U_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[SOUTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[WEST] = RED;
        ::  num3 >= num1 && \
            num3 >= num2 && \
            num3 >= num4 ->
            self_traffic_light_records.crossroad_U_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_U_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[SOUTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[EAST] = RED;
        ::  else ->
            self_traffic_light_records.crossroad_U_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_U_record.traffic_lights[EAST] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[SOUTH] = RED;
            self_traffic_light_records.crossroad_U_record.traffic_lights[WEST] = RED;
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_M, DIRECTION_RIGHT, 29);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_O, DIRECTION_LEFT, 0);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_P, DIRECTION_RIGHT, 29);
        query_return?exist_car3, num3;

        if
        ::  num1 >= num2 && \
            num1 >= num3 ->
            self_traffic_light_records.crossroad_V_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_V_record.traffic_lights[WEST] = RED;
            self_traffic_light_records.crossroad_V_record.traffic_lights[EAST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 ->
            self_traffic_light_records.crossroad_V_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_V_record.traffic_lights[SOUTH] = RED;
            self_traffic_light_records.crossroad_V_record.traffic_lights[WEST] = RED;        
        ::  else ->
            self_traffic_light_records.crossroad_V_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_V_record.traffic_lights[SOUTH] = RED;
            self_traffic_light_records.crossroad_V_record.traffic_lights[EAST] = RED;         
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_I, DIRECTION_RIGHT, 29);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_K, DIRECTION_LEFT, 0);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_N, DIRECTION_LEFT, 0);
        query_return?exist_car3, num3;

        if
        ::  num1 >= num2 && \
            num1 >= num3 ->
            self_traffic_light_records.crossroad_W_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_W_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_W_record.traffic_lights[EAST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 ->
            self_traffic_light_records.crossroad_W_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_W_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_W_record.traffic_lights[SOUTH] = RED;        
        ::  else ->
            self_traffic_light_records.crossroad_W_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_W_record.traffic_lights[EAST] = RED;
            self_traffic_light_records.crossroad_W_record.traffic_lights[SOUTH] = RED;         
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_E, DIRECTION_LEFT, 0);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_F, DIRECTION_RIGHT, 29);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_H, DIRECTION_LEFT, 0);
        query_return?exist_car3, num3;

        if
        ::  num1 >= num2 && \
            num1 >= num3 ->
            self_traffic_light_records.crossroad_X_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_X_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_X_record.traffic_lights[WEST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 ->
            self_traffic_light_records.crossroad_X_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_X_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_X_record.traffic_lights[EAST] = RED;        
        ::  else ->
            self_traffic_light_records.crossroad_X_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_X_record.traffic_lights[EAST] = RED;
            self_traffic_light_records.crossroad_X_record.traffic_lights[WEST] = RED;        
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_G, DIRECTION_RIGHT, 29);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_J, DIRECTION_RIGHT, 29);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_L, DIRECTION_LEFT, 0);
        query_return?exist_car3, num3;

        if
        ::  num1 >= num2 && \
            num1 >= num3 ->
            self_traffic_light_records.crossroad_Y_record.traffic_lights[SOUTH] = GREEN;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[WEST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 ->
            self_traffic_light_records.crossroad_Y_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[SOUTH] = RED;        
        ::  else ->
            self_traffic_light_records.crossroad_Y_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[WEST] = RED;
            self_traffic_light_records.crossroad_Y_record.traffic_lights[SOUTH] = RED;  
        fi

        exist_car1 = 0;
        exist_car2 = 0;
        exist_car3 = 0;

        run traffic_light_get_vehicle_location(query_return, ROAD_A, DIRECTION_LEFT, 0);
        query_return?exist_car1, num1;

        run traffic_light_get_vehicle_location(query_return, ROAD_E, DIRECTION_RIGHT, 29);
        query_return?exist_car2, num2;

        run traffic_light_get_vehicle_location(query_return, ROAD_G, DIRECTION_LEFT, 0);
        query_return?exist_car3, num3;

        if
        ::  num1 >= num2 && \
            num1 >= num3 ->
            self_traffic_light_records.crossroad_Z_record.traffic_lights[EAST] = GREEN;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[WEST] = RED;
        ::  num2 >= num1 && \
            num2 >= num3 ->
            self_traffic_light_records.crossroad_Z_record.traffic_lights[WEST] = GREEN;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[NORTH] = RED;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[EAST] = RED;        
        ::  else ->
            self_traffic_light_records.crossroad_Z_record.traffic_lights[NORTH] = GREEN;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[EAST] = RED;
            self_traffic_light_records.crossroad_Z_record.traffic_lights[WEST] = RED;       
        fi
        
        goto backend_reporting_state;
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