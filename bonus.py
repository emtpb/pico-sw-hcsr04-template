"""Show distance on a website accessible via the Pico's access point."""
# Import libraries
from machine import Pin
import network
import socket

from hcsr04 import HCSR04


# Define your pin connections here
GREEN_PIN = 0

TRIGGER_PIN = 0
ECHO_PIN = 0

# Initialize LED
led_green = Pin(GREEN_PIN, Pin.OUT)

# Initialize distance sensor
sensor = HCSR04(TRIGGER_PIN, ECHO_PIN)

# Set up WiFi Access Point
wap = network.WLAN(network.AP_IF)

# Set WiFi name and password (min. 8 characters)
# If you change the config, please perform a power reset
wap.config(ssid="", password="")
wap.active(True)

# Print network configuration
print(wap.ifconfig())

# Import HTML file
with open("index.html", "r", encoding="utf-8") as file:
    HTML = file.read()

# Open socket
print("Starting server")
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
soc = socket.socket()
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(addr)
soc.listen(1)
print("Server listening at: ", addr)
print()
print("Press Ctrl + C to exit")
print()

while True:
    # Enter your if-elif-else block here and adapt response accordingly
    # You can set two variables in the HTML code: background color and distance
    # For example:
    RESPONSE = HTML % ("pink", 42)

    try:
        conn, addr = soc.accept()
        print("Request received from: ", addr)
        request = conn.recv(1024)
        print("Request: ", request)

        # Send HTTP header
        conn.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        # Send actual content
        conn.send(RESPONSE)
        conn.close()
        print("Response has been sent")
        print()
    except OSError:
        print("An error occurred, exiting...")
        break
    except KeyboardInterrupt:
        break

soc.close()
print("Server terminated")
