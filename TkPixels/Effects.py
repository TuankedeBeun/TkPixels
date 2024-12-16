import numpy as np
from colorsys import hsv_to_rgb

class Effect():
    def __init__(self, colors, max_beats, num_pixels, pixel_data, velocity = 1):
        self.colors = colors
        self.beat = 0
        self.max_beats = max_beats
        self.num_pixels = num_pixels
        self.pixel_data = pixel_data
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
    def get_rgb(self, beat):
        if int(beat) % 2 == 0:
            hue = self.colors[0]
            rgb = hsv_to_rgb(hue, 1, 1)
            self.pixels[:] = np.array(rgb)
        else:
            self.pixels[:,:] = 0

        return self.pixels