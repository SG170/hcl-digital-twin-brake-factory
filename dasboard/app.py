import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
import time

from core.decision_engine import final_decision
from hil.hil_mock import hil_brake_response
# -------------------------------
# Car Icon Configuration
# -------------------------------


# -------------------------------
# Page config
# -------------------------------
st.markdown(
    """
    <style>
    /* Full page background */
    .stApp {
        background-color: #E3F2FD;  /* Light tech blue */
    }

    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #0D47A1;
    }

    /* Normal text */
    p, span, label {
        color: #0D47A1;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="Digital Twin Brake Safety",
    layout="centered"
)




st.title(" Digital Twin Brake Safety Dashboard")
st.caption("What-If scenario based brake safety simulation using Digital Twin")

# -------------------------------
# WHAT-IF SCENARIO SIMULATOR
# -------------------------------
st.header(" What-If Scenario Simulator")

scenario = st.selectbox(
    "Select Driving Scenario",
    [
        "Custom",
        "City Driving",
        "Highway Cruising",
        "Emergency Braking",
        "Snowstorm / Ice Road"
    ]
)

speed = 80
road = "Dry"

if scenario == "City Driving":
    speed = 40
    road = "Dry"
elif scenario == "Highway Cruising":
    speed = 120
    road = "Dry"
elif scenario == "Emergency Braking":
    speed = 130
    road = "Wet"
elif scenario == "Snowstorm / Ice Road":
    speed = 60
    road = "Ice"

import time
# -------------------------------
# Scenario Base Locations
# -------------------------------
scenario_locations = {
    "City Driving": [12.9716, 77.5946],        # Bengaluru
    "Highway Cruising": [12.9000, 77.5000],
    "Emergency Braking": [28.7041, 77.1025],   # Delhi
    "Snowstorm / Ice Road": [46.8182, 8.2275], # Alps
    "Custom": [12.9716, 77.5946]
}

lat, lon = scenario_locations[scenario]

# -------------------------------
# 3D Driving Scenario View (Red Dot Simulation)
# -------------------------------
st.divider()
st.header(" 3D Driving Scenario View")

simulate = st.button("▶ Start Driving Simulation")

# Generate path based on speed & road
def generate_path(lat, lon, speed, road):
    step = speed / 500000
    road_factor = {"Dry": 1.0, "Wet": 0.6, "Ice": 0.3}[road]
    steps = int(25 * road_factor)
    return [{"lat": lat, "lon": lon + i * step} for i in range(steps)]

path = generate_path(lat, lon, speed, road)
map_slot = st.empty()

if simulate:
    for point in path:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=[point],
            get_position="[lon, lat]",
            get_color="[255, 0, 0]",
            get_radius=150
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(
                latitude=point["lat"],
                longitude=point["lon"],
                zoom=14,
                pitch=50
            ),
            map_style="road"
        )

        map_slot.pydeck_chart(deck)
        time.sleep(max(0.05, 1 - speed / 150))
else:
    static_layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": lat, "lon": lon}],
        get_position="[lon, lat]",
        get_color="[255, 0, 0]",
        get_radius=150
    )

    deck = pdk.Deck(
        layers=[static_layer],
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=14,
            pitch=50
        ),
        map_style="road"
    )

    st.pydeck_chart(deck)

st.caption("Red dot represents vehicle position moving based on speed and road friction")

# -------------------------------
# VEHICLE INPUTS (AUTO-FILLED)
# -------------------------------
st.divider()
st.header(" Vehicle Inputs")

speed = st.slider("Vehicle Speed (km/h)", 0, 150, speed)
road = st.selectbox(
    "Road Condition",
    ["Dry", "Wet", "Ice"],
    index=["Dry", "Wet", "Ice"].index(road)
)

road_map = {"Dry": 0, "Wet": 1, "Ice": 2}
road_val = road_map[road]

# -------------------------------
# DIGITAL TWIN LOGIC
# -------------------------------
def digital_twin(speed, road):
    if road == 0 and speed <= 120:
        return "SAFE", "Dry road within safe speed"
    if road == 1 and speed <= 90:
        return "SAFE", "Wet road within safe speed"
    if road == 2 and speed <= 50:
        return "SAFE", "Ice road within safe speed"
    return "RISK", "Speed exceeds safe threshold for this road condition"

dt_result, dt_reason = digital_twin(speed, road_val)

# -------------------------------
# RISK SCORE
# -------------------------------
def calculate_risk_score(speed, road):
    speed_risk = (speed / 150) * 70
    road_risk = {0: 10, 1: 20, 2: 30}[road]
    return min(int(speed_risk + road_risk), 100)

risk_score = calculate_risk_score(speed, road_val)

# -------------------------------
# FIDELITY SCORE
# -------------------------------
def calculate_fidelity_score(dt_result, risk_score, scenario):
    rule_confidence = 1.0 if dt_result == "SAFE" else 0.85
    ai_confidence = 1 - (risk_score / 100)
    scenario_realism = {
        "City Driving": 0.95,
        "Highway Cruising": 0.9,
        "Emergency Braking": 0.85,
        "Snowstorm / Ice Road": 0.8,
        "Custom": 0.75
    }.get(scenario, 0.75)

    hil_confidence = 0.8

    fidelity = (
        0.3 * rule_confidence +
        0.3 * ai_confidence +
        0.2 * scenario_realism +
        0.2 * hil_confidence
    )

    return int(fidelity * 100)

fidelity_score = calculate_fidelity_score(dt_result, risk_score, scenario)
# -------------------------------
# RISK SCORE
# -------------------------------
# -------------------------------
# Risk vs Speed Visualization
# -------------------------------
st.divider()
st.header(" Risk vs Speed Analysis")

speed_range = list(range(0, 151, 10))
risk_values = [calculate_risk_score(s, road_val) for s in speed_range]

risk_df = pd.DataFrame({
    "Speed (km/h)": speed_range,
    "Risk Score (%)": risk_values
})

risk_chart = alt.Chart(risk_df).mark_line(
    point=True,
    interpolate="monotone"
).encode(
    x=alt.X("Speed (km/h)", title="Vehicle Speed"),
    y=alt.Y("Risk Score (%)", title="Risk Score"),
    tooltip=["Speed (km/h)", "Risk Score (%)"]
).properties(
    title=f"Risk Growth with Speed on {road} Road"
)

st.altair_chart(risk_chart, use_container_width=True)

st.caption(
    "This graph shows how braking risk increases as speed rises "
    "under the selected road condition."
)


# -------------------------------
# HARDWARE-IN-THE-LOOP (MOCK)
# -------------------------------
st.divider()
st.header(" Hardware-in-the-Loop (Mock ECU)")

hil_data = hil_brake_response(speed, road)

st.metric("Total ECU Latency", f"{hil_data['total_latency_ms']} ms")
st.metric("Brake Efficiency", f"{hil_data['brake_efficiency'] * 100:.1f}%")

with st.expander(" HIL Signal Breakdown"):
    st.write(hil_data)

# -------------------------------
# FINAL SAFETY DECISION (FUSION)
# -------------------------------
final_status, final_reason = final_decision(risk_score, fidelity_score)

st.divider()
st.header("🚦 Final Safety Decision (Fusion Engine)")

if final_status == "SAFE":
    st.success("FINAL DECISION: SAFE")
else:
    st.error("FINAL DECISION: UNSAFE")

st.caption(final_reason)

# -------------------------------
# PRODUCTION READINESS
# -------------------------------
st.divider()
st.subheader(" Production Readiness Indicator")

if final_status == "SAFE" and fidelity_score >= 85:
    st.success(" READY FOR HARDWARE DEPLOYMENT")
elif final_status == "SAFE":
    st.warning(" SAFE BUT REQUIRES HARDWARE VALIDATION")
else:
    st.error(" NOT SAFE FOR DEPLOYMENT")
st.subheader(" Release Gate Checklist")

gate_results = {
    "Digital Twin Validation": dt_result == "SAFE",
    "Risk Score < 70%": risk_score < 70,
    "Simulation Fidelity ≥ 80%": fidelity_score >= 80,
    "HIL Signals Verified": hil_data["brake_efficiency"] > 0.6,
    "Decision Fusion Passed": final_status == "SAFE"
}

for gate, passed in gate_results.items():
    if passed:
        st.success(f" {gate}")
    else:
        st.error(f" {gate}")

