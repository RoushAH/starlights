import network
import time

# Replace these with your actual network credentials

SSID = "RET - IOT"
PASSWORD = "UwolnicMajonez!"
HOSTNAME = 'your_hostname'

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Set the hostname
wlan.config(dhcp_hostname=HOSTNAME)

# Connect to the Wi-Fi network
wlan.connect(SSID, PASSWORD)

# Wait for connection
while not wlan.isconnected():
    print('Connecting to network...')
    time.sleep(1)

# Print network details
print('Connected to network')
print('IP address:', wlan.ifconfig()[0])
