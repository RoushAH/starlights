import network
import socket
import time
import ussl as ssl

# Connect to the Wi-Fi network
ssid = "RET - IOT"
password = "UwolnicMajonez!"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for the connection to complete
while not wlan.isconnected():
    print('Connecting to network...')
    time.sleep(1)

print('Network connected:', wlan.ifconfig())

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
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print('Listening on', addr)

# Load SSL certificates
cert_path = "/cert.der"  # Ensure this matches the upload path
key_path = "/key.der"    # Ensure this matches the upload path
with open(key_path, mode="rb") as k:
    key = k.read()
with open(cert_path, mode="rb") as c:
    cert = c.read()

# Wrap socket with SSL
s = ssl.wrap_socket(s, cert=cert, key=key)

# Function to handle each connection
def handle_connection(conn):
    try:
        request = conn.recv(1024)
        print('Request:')
        print(request)
        conn.send(html)
    except Exception as e:
        print('Connection error:', e)
    finally:
        conn.close()

# Main loop to accept and handle connections
while True:
    try:
        conn, addr = s.accept()
        print('Connection from', addr)
        handle_connection(conn)
    except Exception as e:
        print('Accept error:', e)
