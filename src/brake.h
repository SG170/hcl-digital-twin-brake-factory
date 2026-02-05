#ifndef BRAKE_H
#define BRAKE_H

// Road condition definitions
#define ROAD_DRY  0
#define ROAD_WET  1
#define ROAD_ICE  2

// Brake decision output
#define BRAKE_SAFE 1
#define BRAKE_RISK 0

// Core brake ECU logic
int apply_brake(int speed_kmh, int road_condition);

#endif
