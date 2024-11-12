import _thread
import os
import machine
from machine import Pin
import network
import time
import ntptime
import neopixel
from webserver import WebServer
import json
import gc
from app_keys import WIFI_SSID, WIFI_PASSWORD
from newsapi import print_news

SYSTEM_VERSION = "24-11-11 - RL0.03.1"

wifi = network.WLAN(network.STA_IF)
RGB = neopixel.NeoPixel(machine.Pin(8), 1)

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
    wifi.active(True)
    if not wifi.isconnected():
        print("Connecting to Wi-Fi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wifi.isconnected():
            ControlRGBLED(B=0)
            time.sleep(1)
            ControlRGBLED(B=64)
    print("Connected to Wi-Fi:", wifi.ifconfig())
    ntptime.settime()
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

def PrintAvailableRAM():
    print("RAM available:", gc.mem_free()/1024/1024, "MB")   
    
# Main program
def main():
    print("SYSTEM VERSION", SYSTEM_VERSION)
    PrintAvailableFlash()
    while True:
        connect_to_wifi()
        PrintAvailableRAM()
        time.sleep(60)  # check wifi connectivity every minute

def task_core1():
    while True:
        
        if wifi.isconnected(): # start webserver only when wifi connection is available
            print("Task 1 started")
            WebServer()
        time.sleep(1)

def task_core0():
    while True:
        print("Task 0 started")
        main()

# Start the second task in a separate thread
_thread.start_new_thread(task_core1, ())

# Run the main task
task_core0()

