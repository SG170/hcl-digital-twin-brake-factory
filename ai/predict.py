import pickle

# -------------------------------
# Load trained AI model
# -------------------------------
with open("ai/brake_risk_model.pkl", "rb") as file:
    model = pickle.load(file)

# -------------------------------
# Take user input (simulated sensor data)
# -------------------------------
try:
    speed = int(input("Enter speed (km/h): "))
    road = int(input("Enter road (0=Dry, 1=Wet, 2=Ice): "))
except ValueError:
    print("❌ Invalid input. Please enter numeric values.")
    exit()

# -------------------------------
# AI prediction
# -------------------------------
prediction = model.predict([[speed, road]])[0]

# -------------------------------
# Output result
# -------------------------------
print("\n🤖 AI CRASH RISK PREDICTION")
print("--------------------------------")

print(f"Speed          : {speed} km/h")
print(f"Road Condition : {road}")

if prediction == 1:
    print("❌ AI RESULT   : RISK predicted")
else:
    print("✅ AI RESULT   : SAFE predicted")
