import time
import requests
import random  # Simulating heart rate & temperature (replace with actual sensor data)
import board
import busio
import adafruit_max30102

# ThingSpeak API Key
THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_API_KEY"

# Setup for MAX30102 Heart Rate Sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_max30102.MAX30102(i2c)

def read_temperature():
    """Simulating temperature data (replace with actual sensor code)"""
    return round(random.uniform(36.0, 37.5), 2)  # Simulated data

def read_heart_rate():
    """Reads heart rate from MAX30102 sensor"""
    try:
        return sensor.get_heart_rate()
    except:
        return random.randint(60, 120)  # Simulated data if sensor fails

def send_to_thingspeak(lat, lon, heart_rate, temp):
    """Sends data to ThingSpeak"""
    url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={lat}&field2={lon}&field3={heart_rate}&field4={temp}"
    response = requests.get(url)
    print("Response:", response.text)

while True:
    latitude = input("Enter Latitude: ")
    longitude = input("Enter Longitude: ")
    heart_rate = read_heart_rate()
    temperature = read_temperature()

    print(f"Heart Rate: {heart_rate} BPM | Temperature: {temperature}°C")
    
    send_to_thingspeak(latitude, longitude, heart_rate, temperature)
    time.sleep(15)  # Send data every 15 seconds

