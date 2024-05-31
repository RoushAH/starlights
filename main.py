import neopixel
import machine
import time
import random

import visuals


def pix_write(array, neopixels):
    n = neopixels.n
    for i in range(n):
        neopixels[i] = array[i]
    neopixels.write()


if __name__ == "__main__":
    np = neopixel.NeoPixel(machine.Pin(16), 66)
    shows = []
    this_show = visuals.sunrise(np.n)
    shows.append(this_show)
    this_show = visuals.twinkle_rainbow(np.n)
    shows.append(this_show)
    this_show = visuals.living_random(np.n, (20, 127, 15))
    shows.append(this_show)
    this_show = visuals.roll_rainbow(np.n)
    shows.append(this_show)

    last = time.ticks_ms()

    pink_btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
    program_pos = 0

    def button_handler(pin):
        global pink_btn, last
        global program_pos

        if pin is pink_btn:
            if time.ticks_diff(time.ticks_ms(), last) > 500:
                program_pos += 1
                last = time.ticks_ms()

    pink_btn.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

    # Master Loop
    while True:
        arr, ms = next(shows[program_pos % len(shows)])
        pix_write(arr, np)
        time.sleep_ms(ms)
