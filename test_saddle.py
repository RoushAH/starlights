import neopixel
import machine
import time

# for pin in range(24,28):
#     np = neopixel.NeoPixel(machine.Pin(pin),66)
#     for pix in range(66):
#         np[pix] = (0,255,255)
#     print(f" Pin {pin}")
#     np.write()
#     input()


def button_handler(pin):
    print(f"Got-ey!! {pin}")


buttons = []
for pin in range(27):
    buttons.append(machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP))
    buttons[pin].irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
    