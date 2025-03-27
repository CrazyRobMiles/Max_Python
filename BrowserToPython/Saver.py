## Loads a colour from a file on startup and stores the colour when it is changed

import machine
import neopixel
import ujson
import sys
import os

# Setup
LED_PIN = 0        # Adjust as needed
NUM_PIXELS = 8
COLOR_FILE = "color.json"

np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_PIXELS)

def set_color(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

def save_color_to_file(r, g, b):
    try:
        with open(COLOR_FILE, "w") as f:
            ujson.dump({"r": r, "g": g, "b": b}, f)
    except Exception as e:
        print("Failed to save color:", e)

def load_color_from_file():
    if COLOR_FILE in os.listdir():
        try:
            with open(COLOR_FILE, "r") as f:
                data = ujson.load(f)
                r = int(data.get("r", 0))
                g = int(data.get("g", 0))
                b = int(data.get("b", 0))
                set_color(r, g, b)
                print("Loaded saved color")
        except Exception as e:
            print("Failed to load color:", e)

# On startup, load saved color if available
load_color_from_file()

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
            save_color_to_file(r, g, b)
    except Exception as e:
        print("Error:", e)
