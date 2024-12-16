import numpy as np
from colorsys import hsv_to_rgb
from random import choice

class Effect():
    def __init__(self, colors, max_beats, num_pixels, pixeldata, velocity = 1):
        self.colors = colors
        self.beat = 0
        self.max_beats = max_beats
        self.num_pixels = num_pixels
        self.pixeldata = pixeldata
        self.pixels = np.zeros((self.num_pixels, 3), dtype=np.uint8)

    def get_rgb(self, beat):
        return self.pixels

class Strobe(Effect):
    def get_rgb(self, beat):
        if int(beat) % 2 == 0:
            self.pixels[:,:] = 255
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class StrobeColor(Effect):
    def __init__(self, colors, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, max_beats, num_pixels, pixeldata, velocity = 1)
        self.color = choice(self.colors)

    def get_rgb(self, beat):
        if int(beat) % 3 == 0:
            hue = self.color
            rgb = hsv_to_rgb(hue, 1, 1)
            self.pixels[:] = np.array(rgb)
        else:
            self.pixels[:,:] = 0

        return self.pixels