import _thread
import os
import machine
from machine import Pin
import network
import time
import neopixel
import mrequests as requests
from webserver import WebServer
import json
import gc
from app_keys import WIFI_SSID, WIFI_PASSWORD, NEWSAPI_KEY, OPENWEATHERMAP_KEY

SYSTEM_VERSION = "24-11-07 - RL0.01.0"

RGB = neopixel.NeoPixel(machine.Pin(48), 1)
# Set RGB LED
R_old = 0
G_old = 0
B_old = 0

# Led Control Pin
def ControlRGBLED(R=None, G=None, B=None):
    global R_old, G_old, B_old
    if R is not None:
        R_old = R
    if G is not None:
        G_old = G
    if B is not None:
        B_old = B
    RGB[0] = (R_old, G_old, B_old)
    RGB.write()

# Connect to Wi-Fi
def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("Connecting to Wi-Fi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            ControlRGBLED(B=0)
            time.sleep(1)
            ControlRGBLED(B=64)
    print("Connected to Wi-Fi:", wifi.ifconfig())
    ControlRGBLED(B=64)

def PrintAvailableFlash():
    # Get filesystem statistics
    statvfs = os.statvfs('/')
    # Calculate total and available space
    total_flash_size = statvfs[0] * statvfs[2]  # total size in bytes
    available_flash_size = statvfs[0] * statvfs[3]  # available space in bytes
    # Convert bytes to a more readable unit (e.g., MB)
    total_flash_size_mb = total_flash_size / (1024 * 1024)
    available_flash_size_mb = available_flash_size / (1024 * 1024)
    print("Total Flash Size: {:.2f} MB".format(total_flash_size_mb))
    print("Available Flash Size: {:.2f} MB".format(available_flash_size_mb))


# Fetch news data
def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
    try:
        response = requests.get(url,headers={"User-Agent": "Zissis"})
        if response.status_code == 200:
            news_data = response.json()
            response.close()
            return news_data.get("articles", [])
        else:
            print("Failed to fetch news:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Print news to serial
def print_news():
    ControlRGBLED(G=64)
    articles = fetch_news()
    print("\nLatest News Headlines:\n")
    for i, article in enumerate(articles[:5]):  # Limit to 5 headlines for simplicity
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        print(f"{i + 1}. {title}\n   {description}\n")
    ControlRGBLED(G=0)

def print_available_RAM():
    print("RAM available:", gc.mem_free()/1024/1024, "MB")
    
    
# Main program
def main():
    print("SYSTEM VERSION", SYSTEM_VERSION)
    PrintAvailableFlash()
    connect_to_wifi()
    while True:
        print_available_RAM()
        print_news()
        time.sleep(600)  # Fetch news every 10 minutes

def task_core1():
    while True:
        time.sleep(5)  # Wait 5 seconds to start the server - should wait for connection
        print("Core 1 started")
        WebServer()

def task_core0():
    while True:
        print("Core 0 started")
        main()

# Start the second task in a separate thread, which will run on the second core
_thread.start_new_thread(task_core1, ())

# Run the main task on the main core
task_core0()
