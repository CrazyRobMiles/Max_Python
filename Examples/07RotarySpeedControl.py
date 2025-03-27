## Example 7 flicker 64 pixels using async with a rotary encoder to control draw speed

import uasyncio as asyncio
import machine
import neopixel
import random

class Col:
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (10, 10, 10)
    VIOLET = (127, 0, 155)
    INDIGO = (75, 0, 130)
    ORANGE = (255, 165, 0)

    # Palette definitions as tuples
    RAINBOW = (RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, INDIGO, VIOLET)
    FIRE = (RED, ORANGE, YELLOW)
    COOL = (CYAN, BLUE, MAGENTA)
    MONO = (BLACK, GREY, WHITE)
    
    @staticmethod
    def dim(col):
        return (int(col[0]/20),
                int(col[1]/20),
                int(col[2]/20))
    
    @staticmethod
    def random_from_palette(palette):
        """Pick a random color from the given palette."""
        if not palette:
            return Col.BLACK  # fallback default
        return palette[random.randint(0, len(palette) - 1)]    

# === LED Setup ===
PIXEL_PIN = 18
NUM_PIXELS = 64
np = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), NUM_PIXELS)

# === Shared Variable ===
draw_rate = 1 / 30  # Initial draw interval in seconds (30 FPS)

# === Flicker a pixel at its own color rate (no .write) ===
async def flicker_pixel(index, cols, rate):
    while True:
        for col in cols:
            np[index] = col
            await asyncio.sleep(rate)

# === Shared draw loop ===
async def draw_task():
    global draw_rate
    while True:
        np.write()
        await asyncio.sleep(draw_rate)

# === Rotary encoder polling task (GP13 = A, GP12 = B) ===
async def encoder_task(clk_pin_num=13, dt_pin_num=12):
    global draw_rate
    clk = machine.Pin(clk_pin_num, machine.Pin.IN, machine.Pin.PULL_UP)
    dt = machine.Pin(dt_pin_num, machine.Pin.IN, machine.Pin.PULL_UP)
    
    last_clk = clk.value()
    value = 30  # initial FPS

    while True:
        current_clk = clk.value()

        # Detect falling edge: HIGH → LOW
        if last_clk == 1 and current_clk == 0:
            if dt.value():  # B is HIGH → rotate one way
                value -= 1
            else:           # B is LOW → rotate the other
                value += 1

            value = max(1, min(120, value))  # clamp FPS between 1 and 60
            draw_rate = 1 / value  # convert FPS to seconds

        last_clk = current_clk
        await asyncio.sleep_ms(2)

# === Main program ===
async def main():
    tasks = [
        draw_task(),
        encoder_task()
    ]

    for i in range(NUM_PIXELS):
        delay = random.uniform(0.2,1.0)
        tasks.append(flicker_pixel(i, Col.RAINBOW, delay))

    await asyncio.gather(*tasks)

asyncio.run(main())


