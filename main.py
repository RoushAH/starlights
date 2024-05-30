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


def twinkle_dim(colour):
    g, r, b = colour
    drop = random.randint(55, 75) / 100
    return int(g * drop), int(r * drop), int(b * drop)


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
        chop = random.randint(1, 3)
        rand_pixel = random.randint(0, n - 1)
        np[rand_pixel] = twinkle_dim(colour_array[rand_pixel])
        np.write()
        time.sleep_ms(random.randint(60, 120))
    for j in range(n):
        np[j] = colour_array[j]
    np.write()


# draw_rainbow(np)


def roll_rainbow(np):
    n = np.n
    stime = 30
    colour_array = []
    for i in range(n):
        colour_array.append(wheel(int(i * 255 / n)))
    for i in range(n):
        np[i] = colour_array[i]
    np.write()
    time.sleep_ms(stime)
    for j in range(n * 5):
        for i in range(n):
            np[i] = colour_array[(i + j) % n]
        np.write()
        time.sleep_ms(stime)


# roll_rainbow(np)

def random_fill(np, colour):
    n = np.n
    colour_array = []
    for i in range(n):
        g, r, b = colour
        g += random.randint(-20, 20)
        r += random.randint(-20, 20)
        b += random.randint(-20, 20)
        colour_array.append((g, r, b))
    print(colour_array)
    for i in range(n):
        np[i] = colour_array[i]
    np.write()

def randjust(colour):
    colour += random.randint(-20, 20)
    if colour < 0:
        return 0
    elif colour > 255:
        return 255
    return colour

def living_random(np, colour):
    n = np.n
    colour_array = []
    for i in range(n):
        g, r, b = colour
        g = randjust(g)
        r = randjust(r)
        b = randjust(b)
        colour_array.append((g, r, b))
    print(colour_array)
    for i in range(n):
        np[i] = colour_array[i]
    np.write()
    for i in range(n * 10):
        g, r, b = colour
        g = randjust(g)
        r = randjust(r)
        b = randjust(b)
        rand_pixel = random.randint(0, n - 1)
        np[rand_pixel] = (g, r, b)
        np.write()
        time.sleep_ms(30)

living_random(np, (25, 128, 25))