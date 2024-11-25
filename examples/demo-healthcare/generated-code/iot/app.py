import paho.mqtt.client as mqtt
import json
import time

BROKER = "172.45.20.2"
PORT = 1883
TOPIC = "health_data"

client = mqtt.Client()

def simulate_health_data():
    data = {
        "HospitalID": "H001",
        "HospitalName": "General Hospital",
        "PatientID": "P001",
        "PersonalInfo": {
            "FirstName": "John",
            "LastName": "Doe",
            "DOB": "1980-05-15",
            "Gender": "Male",
            "ContactInfo": {
                "Phone": "123-456-7890",
                "Email": "john.doe@example.com",
                "Address": "123 Main St, Cityville"
            }
        },
        "HealthData": {
            "BloodPressure": {
                "Systolic": 120,
                "Diastolic": 80
            },
            "BloodTests": {
                "Hemoglobin": 13.5,
                "Cholesterol": {
                    "Total": 190,
                    "HDL": 50,
                    "LDL": 100
                }
            },
            "HeartRate": 72,
            "OtherMetrics": [
                {
                    "Type": "Glucose",
                    "Value": 90,
                    "Unit": "mg/dL"
                }
            ]
        }
    }
    return json.dumps(data)

client.connect(BROKER, PORT, 60)

while True:
    message = simulate_health_data()
    client.publish(TOPIC, message)
    print(f"Published: {message}")
    time.sleep(10)
