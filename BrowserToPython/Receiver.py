## Receives a JSON formatted command and uses it to set the colour of some pixels

import machine
import neopixel
import ujson
import sys

# Setup
LED_PIN = 18       # Change this to match your wiring
NUM_PIXELS = 64    # Number of NeoPixels
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_PIXELS)

# Display a grey screen at the start
np.fill((10,10,10))
np.write()

def set_color(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

# Main loop
while True:
    try:
        line = sys.stdin.readline()
        if line:
            data = ujson.loads(line)
            r = int(data.get("r", 0))
            g = int(data.get("g", 0))
            b = int(data.get("b", 0))
            set_color(r, g, b)
    except Exception as e:
        print("Error:", e)

