
#include <stdio.h>
#include "brake.h"

int apply_brake(int speed_kmh, int road_condition) {
    if (road_condition == ROAD_DRY && speed_kmh <= 120)
        return BRAKE_SAFE;
    if (road_condition == ROAD_WET && speed_kmh <= 90)
        return BRAKE_SAFE;
    if (road_condition == ROAD_ICE && speed_kmh <= 50)
        return BRAKE_SAFE;
    return BRAKE_RISK;
}

int main() {
    int speed_kmh;
    int road_condition;

    printf("Enter speed (km/h): ");
    scanf("%d", &speed_kmh);

    printf("Enter road condition (0=Dry, 1=Wet, 2=Ice): ");
    scanf("%d", &road_condition);

    int result = apply_brake(speed_kmh, road_condition);

    if (result == BRAKE_SAFE)
        printf("ECU RESULT: SAFE\n");
    else
        printf("ECU RESULT: RISK\n");

    return 0;
}
