import numpy as np
from colorsys import hsv_to_rgb
from random import choice, randint

class Effect():
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        self.colors = colors
        self.beat = 0
        self.beat_increment = beat_increment
        self.max_beats = max_beats
        self.num_pixels = num_pixels
        self.pixeldata = pixeldata
        self.pixels = np.zeros((self.num_pixels, 3), dtype=np.uint8)

    def get_rgb(self):
        return self.pixels
    
    def increment(self):
        self.beat += self.beat_increment

class Strobe(Effect):
    def get_rgb(self):
        if self.beat % 1.25 == 0:
            self.pixels[:,:] = 255
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class StrobeColor(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)

    def get_rgb(self):
        if self.beat % 1 == 0:
            rgb = hsv_to_rgb(self.color, 1, 1)
            self.pixels[:] = 255 * np.array(rgb)
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class Sweep(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, direction, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.t_scale = randint(3, 5)

        if direction in ('N', 'S'):
            self.xy_index = 1
            self.t_scale = randint(3, 5)
            self.narrowness = randint(2, 30)
        elif direction in ('E', 'W'):
            self.xy_index = 0
            self.t_scale = randint(4, 6)
            self.narrowness = randint(2, 20)

        if direction in ('N', 'E'):
            self.reversed = False
        elif direction in ('S', 'W'):
            self.reversed = True

        self.xy_max = np.max(self.pixeldata['coords_cart'][:, self.xy_index])

    def get_rgb(self):
        # I = 255 * (1 - (y - t)^2)
        # I, y, t are the intensity, height and time
        xy = self.pixeldata['coords_cart'][:,self.xy_index]
        xy_norm = xy / self.xy_max # goes from 0 to 1
        t_norm = self.beat / self.max_beats # goes from 0 to 1

        if self.reversed:
            t_norm = 1 - t_norm

        t_scaled = self.t_scale * (t_norm - 0.5) + 0.5
        I = 255 * (1 - self.narrowness * (xy_norm - t_scaled) ** 2)

        # ensure positive values
        I[I < 0] = 0

        self.pixels = np.outer(I, self.rgb)

        return self.pixels
    
class SweepUp(Sweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 'N', velocity)

class SweepRight(Sweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 'E', velocity)

class SweepDown(Sweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 'S', velocity)

class SweepLeft(Sweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 'W', velocity)

class SweepStrip(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.pixel_index = 0
        self.snake_length = randint(1, 7)
        self.pixel_index_increment = int(self.num_pixels / (2 * max_beats / self.beat_increment)) + 1
        print(self.pixel_index_increment)

    def increment(self):
        self.beat += self.beat_increment
        self.pixel_index += self.pixel_index_increment

    def get_rgb(self):
        indices = self.pixeldata['indices'][:, 1]
        on = (self.pixel_index <= indices) * (indices < self.pixel_index + self.snake_length)
        self.pixels = np.outer(255 * on, self.rgb)
        return self.pixels
