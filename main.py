import neopixel
import machine
import time
import random

np = neopixel.NeoPixel(machine.Pin(16), 66)
np[0] = (255, 0, 0)
np.write()


def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


def sunrise(np):
    n = np.n
    for i in range(255):
        np.fill((0, i, 0))
        np.write()
        time.sleep_ms(30)
    for i in range(255):
        np.fill((i, 255, i))
        np.write()
        time.sleep_ms(30)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        g = int(pos * 3)
        r = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        g = int(255 - pos * 3)
        r = 0
        b = int(pos * 3)
    else:
        pos -= 170
        g = 0
        r = int(pos * 3)
        b = int(255 - pos * 3)
    return (g, r, b)


def draw_rainbow(np):
    n = np.n
    colour_array = []
    for i in range(n):
        colour_array.append(wheel(int(i * 255 / (n * 1.1))))
    for i in range(n):
        np[i] = colour_array[i]
    np.write()

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = colour_array[j]
        chop = random.randint(1,3)
        np[random.randint(0, n - 1)] = tuple(
            [c // chop for c in colour_array[i % n]]
        )
        np.write()
        time.sleep_ms(random.randint(60,120))
    for j in range(n):
        np[j] = colour_array[j]
    np.write()

draw_rainbow(np)
