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

        xy = self.pixeldata['coords_cart'][:,self.xy_index]
        xy_max = np.max(xy)
        self.xy_norm = xy / xy_max # goes from 0 to 1

    def get_rgb(self):
        # I = 255 * (1 - (y - t)^2)
        # I, y, t are the intensity, height and time
        t_norm = self.beat / self.max_beats # goes from 0 to 1

        if self.reversed:
            t_norm = 1 - t_norm

        t_scaled = self.t_scale * (t_norm - 0.5) + 0.5
        I = 255 * (1 - self.narrowness * (self.xy_norm - t_scaled) ** 2)

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

class SnakeStrip(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, strip_nr, direction, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.pixel_index = 0
        self.snake_length = randint(4, 20)
        self.pixel_index_increment = int(self.num_pixels / (2 * max_beats / self.beat_increment)) + 1
        
        self.strip_nr = strip_nr
        if direction == 'up':
            self.reversed = False
        elif direction == 'down':
            self.reversed = True

    def increment(self):
        self.beat += self.beat_increment
        self.pixel_index += self.pixel_index_increment

    def get_rgb(self):
        strip_nr = self.pixeldata['indices'][:, 0] == self.strip_nr
        indices = self.pixeldata['indices'][:, 1]
        on = strip_nr * (self.pixel_index <= indices) * (indices < self.pixel_index + self.snake_length)

        if self.reversed:
            on = np.flip(on)

        self.pixels = np.outer(255 * on, self.rgb)
        return self.pixels
    
class SnakeStripLeftUp(SnakeStrip):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 0, 'up', velocity)
        
class SnakeStripLeftDown(SnakeStrip):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 1, 'down', velocity)
    
class SnakeStripRightUp(SnakeStrip):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 1, 'up', velocity)
        
class SnakeStripRightDown(SnakeStrip):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, 0, 'down', velocity)

class SphericalSweep(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, inward, velocity = 1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.t_scale = randint(1, 5)
        self.narrowness = randint(10, 100) / self.t_scale
        self.inward = inward

        r = self.pixeldata['coords_spherical'][:, 0]
        r_max = np.max(r)
        self.r_norm = r / r_max # goes from 0 to 1
    
    def get_rgb(self):
        t_norm = self.beat / self.max_beats # goes from 0 to 1
        
        if self.inward:
            t_norm = 1 - t_norm
        
        t_scaled = self.t_scale * (t_norm - 0.5) + 0.5

        I = 255 * (1 - self.narrowness * (self.r_norm - t_scaled) ** 2)

        # ensure positive values
        I[I < 0] = 0

        self.pixels = np.outer(I, self.rgb)

        return self.pixels
    
class SphericalSweepInward(SphericalSweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity=1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, True, velocity)
    
class SphericalSweepOutward(SphericalSweep):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity=1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, False, velocity)

class RetractingSpiral(Effect):
    def __init__(self, colors, beat_increment, max_beats, num_pixels, pixeldata, velocity=1):
        super().__init__(colors, beat_increment, max_beats, num_pixels, pixeldata, velocity)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.num_rounds = randint(2, 10)
        self.max_spiral_width = randint(5, 25)
        self.line_width = self.max_spiral_width / randint(2, 5)
        self.r = self.pixeldata['coords_spherical'][:, 0]
        self.theta = self.pixeldata['coords_spherical'][:, 1]

    def get_rgb(self):
        t_norm = self.beat / self.max_beats
        spiral_width = self.max_spiral_width * (1 - t_norm)
        starting_angle = self.num_rounds * 2 * np.pi * t_norm

        r_mod = np.mod(self.r, spiral_width * 2 * np.pi)
        theta_mod = np.mod(self.theta + starting_angle, 2 * np.pi)
        close_to_spiral = np.abs(r_mod - spiral_width * theta_mod) < self.line_width
        retracting_circle = self.r < 8 * spiral_width * 2 * np.pi
        I = 255 * close_to_spiral * retracting_circle

        self.pixels = np.outer(I, self.rgb)

        return self.pixels
