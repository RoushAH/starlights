import network
import time
import socket
import machine
import ssl

# Replace these with your actual network credentials

SSID = "RET - IOT"
PASSWORD = "UwolnicMajonez!"
HOSTNAME = 'your_hostname'

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the Wi-Fi network
wlan.connect(SSID, PASSWORD)

# Wait for connection
while not wlan.isconnected():
    print('Connecting to network...')
    time.sleep(1)

# Print network details
print('Connected to network')
print('IP address:', wlan.ifconfig()[0])

# Define the HTML response
html = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Hello, World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
"""

# Create a socket and listen for connections
addr = socket.getaddrinfo('0.0.0.0', 443)[0][-1]
s = socket.socket()
# s = ssl.wrap_socket(s)
s.bind(addr)
s.listen(5)
print('Listening on', addr)
t = ssl.wrap_socket(s)

# Function to handle each connection
def handle_connection(conn):
    request = conn.recv(1024)
    print('Request:')
    print(request)
    conn.sendall(html)
    conn.close()

# Main loop to accept and handle connections
while True:
    conn, addr = t.accept()
    print('Connection from', addr)
    handle_connection(conn)
