## Example 12 - make lots of dots

import random
import machine
import neopixel

# Sprite base class
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
WIDTH = 8
HEIGHT = 8
np = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), NUM_PIXELS)

class Sprite:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col

    def random_pos(self):
        self.x = random.randint(0,WIDTH-1)
        self.y = random.randint(0,HEIGHT-1)

class Dot(Sprite):
    def draw(self):
        p = self.x + 8*self.y
        np[p]=self.col

class Block(Sprite):
    def __init__(self, x, y, width, height, col):
        super().__init__(x, y, col)
        self.width = width
        self.height = height

def draw(self):
    x0 = int(self.x - self.width // 2)
    y0 = int(self.y - self.height // 2)
    for dy in range(self.height):
        for dx in range(self.width):
            px = x0 + dx
            py = y0 + dy
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                index = py * WIDTH + px
                np[index] = self.col

sprites = []

for p in range(0,10):
    s = Dot

d = Dot(0,0,Col.RED)
d.draw()
b = Block(x=4,y=4,
          width=2,height=3,
          col=Col.BLUE)
b.draw()
np.write()
