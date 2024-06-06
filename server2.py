from phew import server, connect_to_wifi
import machine
import random
import time
import uasyncio
import network


def wordsmith(word):
    word = list(word)
    while True:
        x = word.pop(0)
        yield x
        word.append(x)
        
word = wordsmith("Harriet2021")

led = machine.Pin("LED", machine.Pin.OUT)

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

async def checkStop():
    while True:
        x = input("x to restart, y to stop")
        if x == "x":
            loop.run_forever()
        elif x == "y":
            loop.stop()

async def mainish():
    global wlan
#     uasyncio.create_task(do_display(word))
    blink = uasyncio.create_task(blinkey())
    await uasyncio.sleep(1)
#     loop.stop()
    print("Hello")
    uasyncio.create_task(checkStop())

# server.run(host="starlights_server", port=80)
# time.sleep(10)
wlan = network.WLAN(network.STA_IF)
uasyncio.create_task(mainish())
loop = uasyncio.get_event_loop()
loop.run_forever()
# uasyncio.run(mainish())
