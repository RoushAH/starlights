import neopixel
import machine
import time
import os
import uasyncio
from phew import server, connect_to_wifi

from battery import batteryPack
import visuals

ssid = 'xxxxxx'
password = 'xxxxxxxxx!'


def pix_write(array, neopixels):
    n = neopixels.n
    for i in range(n):
        neopixels[i] = array[i]
    neopixels.write()


def limit(val):
    if val > 255:
        return 255
    elif val < 0:
        return 0
    else:
        return val


with open("index.html", "r") as f:
    html = f.read()
    try:
        os.remove("log.txt")
    except OSError:
        print("No log file present")
BATTERY_TARGET = "{{INSERT_BATTERY_HERE}}"

np = neopixel.NeoPixel(machine.Pin(16), 66)
battery_pack = batteryPack()

button_queue = [
    visuals.living_random(np.n, (15, 170, 15)),
    visuals.off(np.n),
    visuals.roll_rainbow(np.n),
    visuals.twinkle_rainbow(np.n),
    visuals.living_random(np.n, (185, 22, 45)),
]



last = time.ticks_ms()
pink_btn = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
button_pos = 0
show = button_queue[button_pos]

def button_handler(pin):
    global pink_btn, last, button_pos, show

    if pin is pink_btn:
        if time.ticks_diff(time.ticks_ms(), last) > 500:
            button_pos += 1
            last = time.ticks_ms()
            show = button_queue[button_pos % len(button_queue)]


pink_btn.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)


@server.route("/", methods=["GET"])
def home(request):
    return str(html).replace(BATTERY_TARGET, battery_pack.view_battery())


@server.route("/<command>", methods=["GET"])
def behave(request, command):
    global show, button_pos
    os.remove("log.txt")
    if command == "twinkle_rainbow":
        show = visuals.twinkle_rainbow(np.n)
        button_pos = 0
    elif command == "roll_rainbow":
        show = visuals.roll_rainbow(np.n)
        button_pos = 0
    elif command == "sunrise":
        show = visuals.sunrise(np.n, 3)
        button_pos = 0
    elif command == "demo":
        show = visuals.demo(np.n)
        button_pos = 0
    elif command.startswith("colour"):
        colour = command[command.index("=") + 1:].split(",")
        colour = [limit(int(x)) for x in colour]
        colour = (colour[1], colour[0], colour[2])
        show = visuals.living_random(np.n, colour=colour)
        print(colour)
        button_pos = 0
    elif not command.startswith("fav"):
        show = visuals.off(np.n)
        button_pos = -1
    return str(html).replace(BATTERY_TARGET, battery_pack.view_battery())


@server.catchall()
def catchall(request):
    return "Page not found", 404


async def serve():
    server.run()


async def blinky():
    while True:
        arr, ms = next(show)
        pix_write(arr, np)
        await uasyncio.sleep_ms(ms)


async def mainish():
    uasyncio.create_task(blinky())
    uasyncio.create_task(serve())
    await uasyncio.sleep(10)


if __name__ == "__main__":
    ip = connect_to_wifi(ssid, password)

    print(ip)
    try:
        os.remove("log.txt")
    except OSError:
        print("No log file present")

    time.sleep(5)
    uasyncio.run(mainish())
