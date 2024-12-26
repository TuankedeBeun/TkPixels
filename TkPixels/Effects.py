import numpy as np
from colorsys import hsv_to_rgb
from random import random, choice, randint

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)

    def get_rgb(self):
        if self.beat % 1 == 0:
            rgb = hsv_to_rgb(self.color, 1, 1)
            self.pixels[:] = 255 * np.array(rgb)
        else:
            self.pixels[:,:] = 0

        return self.pixels
    
class Sweep(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.t_scale = randint(3, 5)

        self.direction = getattr(self, 'direction', 'N')
        if self.direction in ('N', 'S'):
            self.xy_index = 1
            self.t_scale = randint(3, 5)
            self.narrowness = randint(2, 30)
        elif self.direction in ('E', 'W'):
            self.xy_index = 0
            self.t_scale = randint(4, 6)
            self.narrowness = randint(2, 20)

        if self.direction in ('N', 'E'):
            self.reversed = False
        elif self.direction in ('S', 'W'):
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
    direction = 'N'

class SweepRight(Sweep):
    direction = 'E'

class SweepDown(Sweep):
    direction = 'S'

class SweepLeft(Sweep):
    direction = 'W'

class SnakeStrip(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.pixel_index = 0
        self.snake_length = randint(4, 20)
        self.pixel_index_increment = int(self.num_pixels / (2 * self.max_beats / self.beat_increment)) + 1
        
        self.strip_nr = getattr(self, 'strip_nr', 0)
        self.direction = getattr(self, 'direction', 'up')
        if self.direction == 'up':
            self.reversed = False
        elif self.direction == 'down':
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
    strip_nr = 0
    direction = 'up'
        
class SnakeStripLeftDown(SnakeStrip):
    strip_nr = 1
    direction = 'down'
    
class SnakeStripRightUp(SnakeStrip):
    strip_nr = 1
    direction = 'up'
        
class SnakeStripRightDown(SnakeStrip):
    strip_nr = 0
    direction = 'down'

class SphericalSweep(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.t_scale = randint(1, 5)
        self.narrowness = randint(10, 100) / self.t_scale
        self.inward = getattr(self, 'inward', True)

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
    inward = True
    
class SphericalSweepOutward(SphericalSweep):
    inward = False

class RetractingSpiral(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        self.rgb = hsv_to_rgb(self.color, 1, 1)
        self.num_rounds = randint(2, 8)
        self.max_spiral_width = randint(5, 25)
        self.line_width = self.max_spiral_width / randint(2, 5)
        self.clockwise = getattr(self, 'clockwise', True)
        self.r = self.pixeldata['coords_spherical'][:, 0]
        self.theta = self.pixeldata['coords_spherical'][:, 1]

    def get_rgb(self):
        # Formula: r(theta, c) = a*theta + c
        # a = spiral_width
        # c = starting_angle
        t_norm = self.beat / self.max_beats
        spiral_width = self.max_spiral_width * (1 - t_norm)
        starting_angle = self.num_rounds * 2 * np.pi * t_norm

        if self.clockwise:
            theta = self.theta + starting_angle
            theta_mod = np.mod(theta, 2 * np.pi)
        else:
            theta = self.theta - starting_angle
            theta_mod = np.mod(2 * np.pi - theta, 2 * np.pi)

        r_mod = np.mod(self.r, spiral_width * 2 * np.pi)

        # Search all LEDs close enough to the spiral
        close_to_spiral = np.abs(r_mod - spiral_width * theta_mod) < self.line_width

        # Create a retracting circle
        retracting_circle = self.r < 8 * spiral_width * 2 * np.pi

        # Combine effects
        I = 255 * close_to_spiral * retracting_circle
        self.pixels = np.outer(I, self.rgb)

        return self.pixels
    
class ClockwiseRetractingSpiral(RetractingSpiral):
    clockwise = True
        
class AnticlockwiseRetractingSpiral(RetractingSpiral):
    clockwise = False

class FlashFade(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        saturation = 0.5 + random() / 2
        self.rgb = hsv_to_rgb(color, saturation, 1)
        self.decay_coef = 4
        self.max_beats = randint(1, 6)

        r = self.pixeldata['coords_spherical'][:, 0]
        r_max = np.max(r)
        self.r_norm = r / r_max + 0.3 # goes from 0.2 to 1.2

    def get_rgb(self):
        t_norm = self.beat / self.max_beats
        I = 255 * np.exp(-self.decay_coef / self.r_norm * t_norm)
        self.pixels = np.outer(I, self.rgb)

        return self.pixels
    
class SectionBuzz(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        self.rgb = hsv_to_rgb(color, 1, 1)
        self.section_ids = self.pixeldata['section_ids']
        self.unique_sections = np.unique(self.section_ids, axis=0)
        self.shuffled = np.random.permutation(self.unique_sections)
        self.section = 0

    def get_rgb(self):

        if (self.beat * 2) % 1 == 0: # do every off-beat

            chosen_section = self.shuffled[self.section]

            on = (self.section_ids == chosen_section)
            on = np.prod(on, axis=1)

            self.pixels = np.outer(255 * on, self.rgb)
            self.section = (self.section + 1) % len(self.shuffled)

        return self.pixels

class SectionPairsSnake(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        self.rgb = hsv_to_rgb(color, 1, 1)
        self.reverse = getattr(self, 'reverse', False)
        self.section_ids = self.pixeldata['section_ids']
        section_pairs = np.array([
            [[0, 0], [1, 2]],
            [[0, 2], [1, 0]],
            [[0, 1], [1, 1]],
            [[0, 3], [1, 3]],
        ])
        self.pair = choice(section_pairs)
        self.snake_length = randint(2,4)

        strip_r = (self.section_ids[:,0] == self.pair[0,0]) * (self.section_ids[:,1] == self.pair[0,1])
        strip_l =(self.section_ids[:,0] == self.pair[1,0]) * (self.section_ids[:,1] == self.pair[1,1])
        series_r = np.cumsum(strip_r)
        series_l = np.cumsum(strip_l)

        if self.reverse:
            series_r = series_r.max() - series_r
            series_l = series_l.max() - series_l

        series_r[series_r == series_r.max()] = 0
        series_l[series_l == series_l.max()] = 0
        series = series_r + series_l

        self.series = (series / self.snake_length).astype(int)

        self.max_beats = self.beat_increment * self.series.max()

    def get_rgb(self):
        index = int(self.beat / self.beat_increment) + 1
        on = self.series == index
        self.pixels = np.outer(255 * on, self.rgb)

        return self.pixels
    
class SectionPairsSnakeUp(SectionPairsSnake):
    reverse = False
    
class SectionPairsSnakeDown(SectionPairsSnake):
    reverse = True

class UnitBuzz(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        self.rgb = hsv_to_rgb(color, 1, 1)
        indices = np.arange(self.num_pixels)
        unit_length = randint(5, 16)
        self.num_units = randint(2, 4)
        self.units = np.floor_divide(indices, unit_length)
        self.unique_units = np.unique(self.units, axis=0)
        self.shuffled_units = np.random.permutation(self.unique_units)
        self.unit_id = 0

    def get_rgb(self):

        if (self.beat * 2) % 1 == 0: # do every off-beat

            start_unit_id = self.num_units * self.unit_id
            chosen_units = self.shuffled_units[start_unit_id : start_unit_id + self.num_units]

            on = np.isin(self.units, chosen_units)

            self.pixels = np.outer(255 * on, self.rgb)
            self.unit_id = (self.unit_id + 1) % int(len(self.shuffled_units) / self.num_units)

        return self.pixels