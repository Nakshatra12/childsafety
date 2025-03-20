import requests
import time
import random
import os
import smbus2  # For I2C LCD communication
from RPi import GPIO  # Raspberry Pi GPIO for LCD

# ThingSpeak API Key (Secure storage recommended)
THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY", "3WGB6MU7A6IDKH9Y")
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# I2C LCD Address (Check with `i2cdetect -y 1` command)
I2C_ADDR = 0x27  
LCD_WIDTH = 16  
bus = smbus2.SMBus(1)

# Function to send commands to LCD
def lcd_send_command(cmd):
    bus.write_byte_data(I2C_ADDR, 0, cmd)
    time.sleep(0.0005)

# Function to send data (characters)
def lcd_send_data(data):
    bus.write_byte_data(I2C_ADDR, 1, data)
    time.sleep(0.0005)

# Function to initialize LCD
def lcd_init():
    lcd_send_command(0x38)  # 2-line mode
    lcd_send_command(0x0C)  # Display on, cursor off
    lcd_send_command(0x01)  # Clear display
    time.sleep(0.002)

# Function to display message on LCD
def lcd_display_message(message, line=1):
    lcd_send_command(0x80 if line == 1 else 0xC0)  # Move to line 1 or 2
    for char in message.ljust(LCD_WIDTH):  # Pad message to fit LCD width
        lcd_send_data(ord(char))

# Initialize LCD
lcd_init()

# Fixed location (Replace with GPS if available)
latitude = "28.7041"
longitude = "77.1025"

def send_data():
    """Reads sensor data, sends to ThingSpeak, and updates LCD display."""
    try:
        # Simulated Sensor Data
        temperature = round(random.uniform(36.0, 40.0), 2)  # Normal: 36.0 - 38.5°C
        heart_rate = random.randint(50, 130)  # Normal: 60 - 120 BPM

        # Determine Alert Message
        alert_msg = ""
        if temperature > 38.5:
            alert_msg = "High Temp!"
        if heart_rate > 120:
            alert_msg = "High HR!"
        if temperature > 38.5 and heart_rate > 120:
            alert_msg = "Emergency!"

        # Send Data to ThingSpeak
        data = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": temperature,
            "field2": heart_rate,
            "field3": latitude,
            "field4": longitude
        }
        response = requests.post(THINGSPEAK_URL, data=data, timeout=10)

        # Display message on LCD
        lcd_display_message(f"T:{temperature}C HR:{heart_rate}", line=1)
        lcd_display_message(alert_msg if alert_msg else "Status: Normal", line=2)

        # Print log
        if response.status_code == 200 and response.text != "0":
            print(f"Data sent! Temp: {temperature}°C, HR: {heart_rate} BPM, Location: ({latitude}, {longitude}), Alert: {alert_msg}")
        else:
            print(f"Failed to send data. Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print("Network Error:", e)
    except Exception as e:
        print("Error:", e)

# Run the loop
while True:
    send_data()
    time.sleep(15)  # 15-second interval (ThingSpeak free limit)
