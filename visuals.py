import random
import time


def demo(n):
    while True:
        out_array = [(0, 0, 0) for _ in range(n)]
        yield out_array, 25
        # runner
        for i in range(4 * n):
            out_array = [(0, 0, 0) for _ in range(n)]
            out_array[i % n] = (255, 255, 255)
            yield out_array, 25

        # rainbow_runner
        for i in range(4 * n):
            out_array = [(0, 0, 0) for _ in range(n)]
            out_array[i % n] = wheel(i)
            yield out_array, 40

        # bouncer
        for i in range(4 * n):
            out_array = [(0, 0, 128) for _ in range(n)]
            if (i // n) % 2 == 0:
                out_array[i % n] = (0, 0, 0)
            else:
                out_array[n - 1 - (i % n)] = (0, 0, 0)
            yield out_array, 60

        # fader
        for i in range(4):
            for j in range(256):
                out_array = [(j, j, j) for _ in range(n)]
                yield out_array, 2
            for j in range(256):
                out_array = [(255 - j, 255 - j, 255 - j) for _ in range(n)]
                yield out_array, 2


def demo_old(np):
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


def sunrise(n, mins):
    step = int(mins * 60 * (1000 / 455))
    for r in range(245):
        out_array = [(0, r, 0) for _ in range(n)]
        yield out_array, step
    for gb in range(210):
        out_array = [(gb, 245, gb) for _ in range(n)]
        yield out_array, step
    out_array = [(210, 245, 210) for _ in range(n)]
    while True:
        g = randjust(210)
        r = randjust(245)
        b = randjust(210)
        rand_pix = random.randint(0, n - 1)
        out_array[rand_pix] = (g, r, b)
        yield out_array, 20


def twinkle_dim(colour):
    g, r, b = colour
    drop = random.randint(65, 85) / 100
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
    return g, r, b


def twinkle_rainbow(n):
    colour_array = []
    for i in range(n):
        colour_array.append(wheel(int(i * 255 / (n * 1.1))))
    yield colour_array, random.randint(60, 120)
    old_pix = 0
    while True:
        rand_pix = random.randint(0, n - 1)
        colour_array[rand_pix] = twinkle_dim(colour_array[rand_pix])
        colour_array[old_pix] = wheel(int(old_pix * 255 / (n * 1.1)))
        yield colour_array, random.randint(60, 120)
        old_pix = rand_pix


def roll_rainbow(n):
    colour_list = []
    for i in range(n):
        colour_list.append(wheel(int(i * 255 / n)))
    while True:
        yield colour_list, 40
        x = colour_list.pop(0)
        colour_list.append(x)


def randjust(colour):
    colour += random.randint(-20, 20)
    if colour < 0:
        return 0
    elif colour > 255:
        return 255
    return colour


def off(n):
    colour_array = [(0, 0, 0) for _ in range(n)]
    while True:
        yield None, 500


def living_random(n, colour):
    colour_array = []
    for i in range(n):
        g, r, b = colour
        g = randjust(g)
        r = randjust(r)
        b = randjust(b)
        colour_array.append((g, r, b))
    yield colour_array, 30
    while True:
        g, r, b = colour
        g = randjust(g)
        r = randjust(r)
        b = randjust(b)
        rand_pix = random.randint(0, n - 1)
        colour_array[rand_pix] = (g, r, b)
        yield colour_array, 30



def sunrise_filter(grb, num):
    # Tries to simulate a sunrise by first showing reds, then fading in greens and blues
    # Based on 500 `brightsteps`
    rgb = [grb[1], grb[0], grb[2]]
    if num < 200:
        # red only
        rgb = [min(num,rgb[1]), 0, 0]
    elif num < 350:
        # finish red, fade in green
        rgb = [min(num,rgb[0]), min(num-200,rgb[1]), 0]
    else:
        #finish green, bring blue in quick
        blue_min = int((num-350)/150*255)
        rgb = [min(num,rgb[0]), min(num-200,rgb[1]), min(blue_min, rgb[2])]
    return (rgb[1],rgb[0],rgb[2])


def fade_in(gen, mins):
    # Use a provided generator and fade in to its behaviour
    i = 1
    # calculate `brightstep` length in millis, set current timer to 0
    brightstep = mins * 60 * 2
    t = 0
    while i < 500:
        vals, millis = next(gen)
        news = []
        for val in vals:
            news.append(sunrise_filter(val, i))
        # compute current time and check to see if we've ticked a brightstep
        t += millis
        if t > brightstep * i:
            i+= 1
        yield news, millis
    while True:
        yield next(gen)