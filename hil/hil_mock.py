import time
import random

def hil_brake_response(speed, road_condition):
    """
    Simulates hardware brake ECU behavior
    """

    # Sensor latency (ms)
    sensor_delay = random.uniform(5, 15)

    # ECU processing time (ms)
    ecu_delay = random.uniform(8, 20)

    # Actuator response delay (ms)
    actuator_delay = random.uniform(10, 25)

    total_latency = sensor_delay + ecu_delay + actuator_delay

    # Simulated braking effectiveness
    friction_map = {
        "Dry": 0.9,
        "Wet": 0.7,
        "Ice": 0.4
    }

    brake_efficiency = friction_map[road_condition] * (1 - speed / 200)

    return {
        "sensor_delay_ms": round(sensor_delay, 2),
        "ecu_delay_ms": round(ecu_delay, 2),
        "actuator_delay_ms": round(actuator_delay, 2),
        "total_latency_ms": round(total_latency, 2),
        "brake_efficiency": round(brake_efficiency, 2)
    }
