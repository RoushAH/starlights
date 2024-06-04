import neopixel
import machine
import time
import random
import network
import os
import uasyncio
from phew import server, connect_to_wifi

import visuals

ssid1 = 'BT-89CP3S'
ssid = "RET - IOT"
password1 = '7mdJXHmCRyAQ3J'
password = "UwolnicMajonez!"


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

np = neopixel.NeoPixel(machine.Pin(16), 66)
# option1
button_queue = []

this_show = visuals.living_random(np.n, (20, 127, 15))
button_queue.append(this_show)
this_show = visuals.off(np.n)
button_queue.append(this_show)
this_show = visuals.living_random(np.n, (220, 227, 215))
button_queue.append(this_show)

# option 2
# button_queue = [
#     visuals.living_random(np.n, (20, 127, 15)),
#     visuals.off(np.n),
#     visuals.living_random(np.n, (220, 227, 215)),
# ]

show = button_queue[0]

last = time.ticks_ms()
pink_btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
button_pos = 0


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
    return str(html)


@server.route("/<command>", methods=["GET"])
def command(request, command):
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
        button_pos = 1
    return str(html)


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
