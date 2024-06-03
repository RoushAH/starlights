from phew import server, connect_to_wifi
import machine
import random
import time
import uasyncio

ssid1 = 'BT-89CP3S'
ssid = "RET - IOT"
password1 = '7mdJXHmCRyAQ3J'
password = "UwolnicMajonez!"

ip = connect_to_wifi(ssid,password)

print(ip)

# page = open("index.html","r")
# html= page.read()
# page.close()
html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico PHEW Server</h1>
            <h2>Led Control</h2>
            <form action="./twinkle_rainbow">
                <input type="submit" value="Twinkling Rainbow" />
            </form>
            <br>
            <form action="./roll_rainbow">
                <input type="submit" value="Rolling Rainbow" />
            </form>
            <br>
            <form action="./on">
                <input type="submit" value="LED On" />
            </form>
            <br>
            <form action="./off">
                <input type="submit" value="LED Off" />
            </form>
            <p>LED state: {state}</p>
        </body>
        </html>
        """


def wordsmith(word):
    word = list(word)
    while True:
        x = word.pop(0)
        yield x
        word.append(x)
        
word = wordsmith("Harriet2021")

led = machine.Pin("LED", machine.Pin.OUT)

@server.route("/", methods=["GET"])
def home(request):
    return str(html)

@server.route("/<command>", methods=["GET"])
def command(request, command):
    global word
    if command == "on":
        led.on()
    elif command == "off":
        led.off()
    elif not command.startswith("fav") :
        word = wordsmith(command)
    return str(html)

@server.catchall()
def catchall(request):
    return "Page not found", 404

async def serve():
    server.run()

async def do_display(iterable):
    while True:
        print(next(word))
        await uasyncio.sleep_ms(50)

async def blinkey():
    while True:
        led.value(1)
        await uasyncio.sleep_ms(50)
        led.value(0)
        await uasyncio.sleep_ms(150)

async def mainish():
    uasyncio.create_task(serve())
    uasyncio.create_task(do_display(word))
    uasyncio.create_task(blinkey())
    await uasyncio.sleep(10)

# server.run(host="starlights_server", port=80)
time.sleep(10)
uasyncio.run(mainish())
