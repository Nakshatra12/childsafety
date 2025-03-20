import requests
import time
import random  # Simulating sensor data

# ThingSpeak API Key (Replace with your Write API Key)
THINGSPEAK_API_KEY = "3WGB6MU7A6IDKH9Y"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

while True:
    # Simulated Sensor Data (Replace with real sensor readings)
    temperature = round(random.uniform(36.0, 38.5), 2)  # Example: 36.0°C to 38.5°C
    heart_rate = random.randint(60, 120)  # Example: 60 BPM to 120 BPM

    # Data Payload
    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": temperature,  # Temperature Data
        "field2": heart_rate    # Heart Rate Data
    }

    # Send Data to ThingSpeak
    response = requests.post(THINGSPEAK_URL, data=data)

    if response.status_code == 200:
        print(f"Data sent successfully! Temperature: {temperature}°C, Heart Rate: {heart_rate} BPM")
    else:
        print("Error sending data:", response.status_code, response.text)

    time.sleep(15)  # Wait 15 seconds before next update (ThingSpeak free version limit)
