import neopixel
import machine
import time
import os
import uasyncio
from phew import server, connect_to_wifi
import urequests
import secrets

import visuals

network_number = 1
ssid, password = secrets.wifis[network_number]
BUTTON_RESET_MILLIS = 750
starting_light_level = 3


def pix_write(array, neopixels):
    # Take an array and the neopixel object, write to the object
    n = neopixels.n
    for i in range(n):
        neopixels[i] = array[i]
    neopixels.write()


def limit(val):
    # Force a value to be between 0 - 255
    if val > 255:
        return 255
    elif val < 0:
        return 0
    else:
        return val


with open("index.html", "r") as f:
    # Load the webpage, and nuke the goddamn log
    html = f.read()
    try:
        os.remove("log.txt")
    except OSError:
        print("No log file present")

np = neopixel.NeoPixel(machine.Pin(27), 66)
empty_colour_array = [(0, 0, 0) for _ in range(np.n)]  # Turn them off

# the order of programs to run when Harriet presses the button
button_queue = [
    visuals.living_random(np.n, (15, 170, 15)),
    visuals.off(np.n),
    visuals.roll_rainbow(np.n),
    visuals.twinkle_rainbow(np.n),
    visuals.living_random(np.n, (185, 22, 45)),
]

last = time.ticks_ms()
pink_btn = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
button_pos = 0
show = button_queue[button_pos]


def button_handler(pin):
    # define how to manage the button press
    global pink_btn, last, button_pos, show

    if pin is pink_btn:
        if time.ticks_diff(time.ticks_ms(), last) > BUTTON_RESET_MILLIS:
            button_pos += 1
            button_pos %= len(button_queue)
            last = time.ticks_ms()
            show = button_queue[button_pos]


pink_btn.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)


@server.route("/", methods=["GET"])
def home(request):
    """ If home is requested, return home"""
    return str(html)

@server.route("/update", methods=["GET"])
def update(request):
    """ Do the updates from Github repo"""
    with open("manifest.txt", "r") as f:
        manifest = f.read()
    manifest = manifest.split("\n")
    target = "https://raw.githubusercontent.com/RoushAH/starlights/main/"
    for file in manifest:
        result = urequests.get(target + file)
        print(f"GREAT SUCCESS {file}") if result.status_code == 200 else print(f"Whomp, whomp, {file}")
        if result.status_code == 200:
            with open(file, "w") as f:
                f.write(result.text)

    return str(html)



@server.route("/<command>", methods=["GET"])
def behave(request, command):
    """ Really bad version of FLASK here, to handle requests to change program """
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
    elif command == "fade_in":
        show = visuals.fade_in(visuals.twinkle_rainbow(np.n), 3)
        button_pos = 3
    elif command == "fade_out":
        show = visuals.fade_out(show, 3)
        button_pos = -1
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
    return str(html)


@server.catchall()
def catchall(request):
    # 404'd!
    return "Page not found", 404


async def serve():
    server.run()


async def blinky():
    blank = False
    # Checks to see if you've blanked out the pixels
    while True:
        arr, ms = next(show)
        # a show returns an array of colours, written as GRB tuples,
        # and a number of millis to wait until the next time to pull
        if arr is None and not blank:
            # blank the pixels
            arr = empty_colour_array
            pix_write(arr, np)
            #             print(arr)
            blank = True
        elif arr is None:
            pass
        else:
            # Grab the next version of the array from the visuals library, then write it
            pix_write(arr, np)
            #             print(arr)
            blank = False
        await uasyncio.sleep_ms(ms)


async def mainish():
    # I don't know why this works, but it does
    # Create the two tasks, then await sleep. The tasks wil have begun before it awakens
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
