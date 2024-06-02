import network
import socket
import time
from machine import Pin
import uasyncio

ssid = 'BT-89CP3S'
password = '7mdJXHmCRyAQ3J'
LED = Pin('LED', Pin.OUT)

state = False

last = time.ticks_ms()

def wordsmith(word):
    word = list(word)
    while True:
        x = word.pop(0)
        yield x
        word.append(x)

pink_btn = Pin(4, Pin.IN, Pin.PULL_UP)
program_pos = 0

def button_handler(pin):
    global pink_btn, last
    global program_pos

    if pin is pink_btn:
        if time.ticks_diff(time.ticks_ms(), last) > 500:
            program_pos += 1
            last = time.ticks_ms()
            print(program_pos)

pink_btn.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

# HTML template for the webpage
def webpage(state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>Led Control</h2>
            <form action="./twinkle_rainbow">
                <input type="submit" value="Twinkling Rainbow" />
            </form>
            <br>
            <form action="./roll_rainbow">
                <input type="submit" value="Rolling Rainbow" />
            </form>
            <p>LED state: {state}</p>
        </body>
        </html>
        """
    return str(html)

class Server:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        network.hostname("HelloHarriet")
        self.job = "do"
        self.led = LED
    
    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        
        # Wait for Wi-Fi connection
        connection_timeout = 10
        while connection_timeout > 0:
            if self.wlan.status() >= 3:
                break
            connection_timeout -= 1
            print('Waiting for Wi-Fi connection...')
            time.sleep(1)

        # Check if connection is successful
        if self.wlan.status() != 3:
            raise RuntimeError('Failed to establish a network connection')
        else:
            print('Connection successful!')
            network_info = self.wlan.ifconfig()
            print('IP address:', network_info[0])

    def listen(self):
        global state

        # Set up socket and start listening
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen()

        # Main loop to listen for connections
        while True:
            try:
                if state:
                    self.led.value(1)
                else:
                    self.led.value(0)
                conn, addr = s.accept()
                print('Got a connection from', addr)

                # Receive and parse the request
                request = conn.recv(1024)
                request = str(request)
                # print('Request content = %s' % request)

                try:
                    request = request.split()[1]
                    print('Request:', request)
                except IndexError:
                    pass

                # Process the request and update variables
                if request == '/twinkle_rainbow?':
                    print("twinkle_rainbow")
                    state = True
                elif request == '/roll_rainbow?':
                    print("roll_rainbow")
                    state = True
                else:
                    state = False

                # Generate HTML response
                response = webpage(state)

                # Send the HTTP response and close the connection
                conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                conn.send(response)
                conn.close()

            except OSError as e:
                conn.close()

word = wordsmith("Harriet2021")
async def do_display(iterable):
    while True:
        print(next(word))
        await uasyncio.sleep_ms(5)

async def blinkey():
    while True:
        LED.value(1)
        await uasyncio.sleep_ms(50)
        LED.value(0)
        await uasyncio.sleep_ms(150)

async def mainish():
    uasyncio.create_task(do_display(word))
    uasyncio.create_task(blinkey())
    await uasyncio.sleep(100)
    
if __name__ == "__main__":
    test_server = Server()
    test_server.connect()
    uasyncio.run(mainish())
    test_server.listen()