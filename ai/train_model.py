import pickle
from sklearn.tree import DecisionTreeClassifier

# ----------------------------------------
# Training data (synthetic, hackathon-safe)
# ----------------------------------------
# Features: [speed_kmh, road_condition]
# Label: 0 = SAFE, 1 = RISK

X = [
    [60, 0],    # Dry, low speed
    [100, 0],   # Dry, high speed
    [80, 1],    # Wet, moderate speed
    [120, 1],   # Wet, high speed
    [40, 2],    # Ice, low speed
    [70, 2]     # Ice, risky speed
]

y = [
    0,  # SAFE
    0,  # SAFE
    0,  # SAFE
    1,  # RISK
    0,  # SAFE
    1   # RISK
]

# ----------------------------------------
# Train AI model
# ----------------------------------------
model = DecisionTreeClassifier()
model.fit(X, y)

# ----------------------------------------
# Save trained model
# ----------------------------------------
with open("ai/brake_risk_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ AI MODEL TRAINED & SAVED")
