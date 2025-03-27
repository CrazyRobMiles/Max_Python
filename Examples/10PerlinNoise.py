## Example 10 Draw a perlin noise array using core 1 and render on top of it with core 0

import machine
import neopixel
import uasyncio as asyncio
import _thread
import math
import time

# === Display setup ===
WIDTH=8
HEIGHT = 8
PIXEL_PIN = 18
np = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), WIDTH * HEIGHT)

# === Shared surface ===
surface = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
surface_lock = _thread.allocate_lock()

# === Index mapping (non-serpentine) ===
def index(x, y):
    return y * WIDTH + x

# === Perlin-like noise ===
def hash2d(x, y):
    return ((x * 1836311903) ^ (y * 2971215073)) & 0xFFFFFFFF

def grad(x, y):
    h = hash2d(x, y)
    return ((h & 0xFF) / 255.0) * 2 - 1

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + (b - a) * t

def noise2d(x, y):
    xi = int(x)
    yi = int(y)
    xf = x - xi
    yf = y - yi

    top_left = grad(xi, yi)
    top_right = grad(xi + 1, yi)
    bottom_left = grad(xi, yi + 1)
    bottom_right = grad(xi + 1, yi + 1)

    u = fade(xf)
    v = fade(yf)

    top = lerp(top_left, top_right, u)
    bottom = lerp(bottom_left, bottom_right, u)

    return lerp(top, bottom, v)

def noise_color(value):
    value = (value + 1) / 2  # normalize to 0–1
    return (
        int(128 + 127 * math.sin(value * math.pi)),
        int(128 + 127 * math.sin(value * math.pi + 2)),
        int(128 + 127 * math.sin(value * math.pi + 4))
    )

# === Core 1: Noise surface generator ===
def generate_surface(width, height,noise2d,noise_color):
    t = 0
    scale = 0.15
    speed = 0.05
    global surface
    while True:
        with surface_lock:
            for y in range(height):
                for x in range(width):
                    n = noise2d(x * scale + t, y * scale + t)
                    surface[y][x] = noise_color(n)
        t += speed
        time.sleep(0.03)

# Start Core 1 thread with parameters passed in
_thread.start_new_thread(generate_surface, (WIDTH, HEIGHT,noise2d,noise_color))


# === Core 0: Foreground display with overlay ===
async def draw_task():
    while True:
        with surface_lock:
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    color = surface[y][x]
                    np[index(x, y)] = color
        np.write()
        await asyncio.sleep(1 / 30)

# Run main loop
async def main():
    await draw_task()

asyncio.run(main())


