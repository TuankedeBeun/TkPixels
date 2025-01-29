import board
import neopixel
from time import sleep

max_brightness = 0.5
Npixels = 240
pixels = neopixel.NeoPixel(board.D18, Npixels, brightness=1, auto_write=False)

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(Npixels):
            pixel_index = (i * 256 // Npixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        sleep(wait)
        
Ncycles = 5
for cycle in range(1, Ncycles + 1):
    intensity = cycle/Ncycles
    pixels.brightness = intensity/max_brightness
    rainbow_cycle(0.0001)

for cycle in range(1, Ncycles + 1):
    intensity = 1 - cycle/Ncycles
    pixels.brightness = intensity/max_brightness
    rainbow_cycle(0.0001)
    
pixels.fill((0,0,0))
