# Set the real time clock of the raspberry pi pico w using ntp

# Imports
import ntptime
import time
import network
import socket
import sys
import os
import wifi_info     # The SSID and WIFI password
    
# Replace with your own SSID and WIFI password
ssid = wifi_info.ssid
wifi_password = wifi_info.wifi_password
my_ip_addr = '192.168.0.22'

# Please see https://docs.micropython.org/en/latest/library/network.WLAN.html
# Try to connect to WIFI
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Specify the IP address
wlan.ifconfig((my_ip_addr, '255.255.255.0', '192.168.0.1', '8.8.8.8'))

# Connect
wlan.connect(ssid, wifi_password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')    
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    # Connection to wireless LAN failed
    print('Connection failed')    
    sys.exit()    
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
# Try to set the real time clock with the NTP server    
try:
    ntptime.settime()
except:
    print("Could not set time")
    sys.exit()

# Set the offset from UTC
UTC_OFFSET = -4 * 60 * 60
# Get the local time
temp = time.localtime(time.time() + UTC_OFFSET)
