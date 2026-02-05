import time

# ----------------------------------
# Simulated V2X message broadcaster
# ----------------------------------
def send_v2x_alert(risk_level):
    print("\n📡 V2X NETWORK STATUS")

    if risk_level == "RISK":
        print("🚨 Risk detected by ECU / AI")
        time.sleep(0.5)

        print("📤 Broadcasting emergency alert...")
        time.sleep(0.5)

        print("🚗→🚗 V2V alert sent to nearby vehicles")
        print("🚦→🚗 V2I alert sent to traffic infrastructure")
        print("⏱️ Average latency: 8 ms")

        return "EMERGENCY_BROADCAST"

    elif risk_level == "SAFE":
        print("✅ No risk detected")
        print("📡 V2X channel idle – monitoring only")

        return "NO_BROADCAST"

    else:
        print("⚠️ Unknown state received")
        print("📡 V2X fallback mode activated")

        return "FALLBACK_MODE"


# ----------------------------------
# Test all possible cases
# ----------------------------------
if __name__ == "__main__":

    test_cases = ["SAFE", "RISK", "UNKNOWN"]

    for case in test_cases:
        print("----------------------------------")
        print(f"Incoming risk status: {case}")
        result = send_v2x_alert(case)
        print(f"V2X ACTION TAKEN: {result}")
