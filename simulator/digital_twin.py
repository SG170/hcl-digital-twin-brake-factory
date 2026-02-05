def digital_twin_decision(speed, road):
    if road == 0 and speed <= 120:
        return "SAFE"
    if road == 1 and speed <= 90:
        return "SAFE"
    if road == 2 and speed <= 50:
        return "SAFE"
    return "RISK"

speed = int(input("Enter speed (km/h): "))
road = int(input("Enter road (0=Dry, 1=Wet, 2=Ice): "))

result = digital_twin_decision(speed, road)

print("DIGITAL TWIN RESULT:", result)
