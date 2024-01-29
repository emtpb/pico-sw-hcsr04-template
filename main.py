"""This module is automatically executed when the microcontroller is powered."""
# Import libraries
from machine import Pin
from hcsr04 import HCSR04


# Define your pin connections here
GREEN_PIN = 0

TRIGGER_PIN = 0
ECHO_PIN = 0

# Initialize LED
led_green = Pin(GREEN_PIN, Pin.OUT)

# Initialize distance sensor
sensor = HCSR04(TRIGGER_PIN, ECHO_PIN)

# Your code goes here
# ...
