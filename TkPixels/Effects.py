import numpy as np
from colorsys import hsv_to_rgb
from random import choice, randint

class Effect():
    def __init__(self, colors, max_beats, num_pixels, pixeldata, velocity = 1):
        self.colors = colors
        self.beat = 0
        self.max_beats = max_beats
        self.num_pixels = num_pixels
        self.pixeldata = pixeldata
        self.pixels = np.zeros((self.num_pixels, 3), dtype=np.uint8)

    def get_rgb(self):
        return self.pixels
    
    def increment(self, beat_increment):
        self.beat += beat_increment

class Strobe(Effect):
    def get_rgb(self):
        if self.beat % 1.25 == 0:
            self.pixels[:,:] = 255
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class StrobeColor(Effect):
    def __init__(self, colors, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)

    def get_rgb(self):
        if self.beat % 1 == 0:
            rgb = hsv_to_rgb(self.color, 1, 1)
            self.pixels[:] = 255 * np.array(rgb)
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class SweepUp(Effect):
    def __init__(self, colors, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.t_scale = randint(3, 5)
        self.width = randint(2, 30)
        self.y_max = np.max(self.pixeldata['coords_cart'][:,1])

    def get_rgb(self):
        # I = 255 * (1 - (y - t)^2)
        # I, y, t are the intensity, height and time
        y = self.pixeldata['coords_cart'][:,1]
        y_norm = y / self.y_max # goes from 0 to 1
        t_norm = self.beat / self.max_beats # goes from 0 to 1
        t_scaled = self.t_scale * (t_norm - 0.5) + 0.5
        I = 255 * (1 - self.width * (y_norm - t_scaled) ** 2)

        # ensure positive values
        I[I < 0] = 0

        rgb = hsv_to_rgb(self.color, 1, 1)
        pixels = np.outer(I, np.array(rgb))
        self.pixels = pixels

        return self.pixels

        
