## Example 5 flicker 64 pixels using async

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

PIXEL_PIN = 18
NUM_PIXELS = 64
np = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), NUM_PIXELS)

async def flicker_pixel(index, cols, delay):
    while True:
        for col in cols:
            np[index] = col
            np.write()
            await asyncio.sleep(delay)

async def main():
    tasks = []
    for i in range(NUM_PIXELS):
        delay = random.uniform(0.2,1.0)
        tasks.append(flicker_pixel(i, Col.RAINBOW, delay))
    await asyncio.gather(*tasks)

asyncio.run(main())


