import numpy as np
from colorsys import hsv_to_rgb
from random import random, choice, randint

class Effect():
    def __init__(self, colors, beat_increment, beat_offset, max_beats, num_pixels, pixeldata, velocity = 1):
        self.colors = colors
        self.beat = 0
        self.beat_increment = beat_increment
        self.beat_offset = beat_offset
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
        self.max_beats = randint(4,7)

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
        brightness = getattr(self, 'brightness')
        self.rgb = hsv_to_rgb(self.color, 1, brightness)
        self.narrowness = getattr(self, 'narrowness')
        self.t_scale = getattr(self, 't_scale')

        self.direction = getattr(self, 'direction')
        if self.direction in ('N', 'S'):
            self.xy_index = 1
            xy = self.pixeldata['coords_cart'][:,self.xy_index]
            xy_max = np.max(xy)
            self.xy_norm = xy / xy_max # goes from 0 to 1
            self.narrowness *= 2
        elif self.direction in ('E', 'W'):
            self.xy_index = 0
            xy = self.pixeldata['coords_cart'][:,self.xy_index]
            xy_max = np.max(xy)
            self.xy_norm = ((xy / xy_max) + 1) / 2 # goes from 0 to 1

        if self.direction in ('N', 'E'):
            self.reversed = False
        elif self.direction in ('S', 'W'):
            self.reversed = True
        
    def get_rgb(self):
        return self.get_rgb_of_beat(self.beat)

    def get_rgb_of_beat(self, beat, binary=False):
        # I = 255 * (1 - (y - t)^2)
        # I, y, t are the intensity, height and time
        t_norm = 1.2 * (beat / self.max_beats) - 0.1 # goes from -0.1 to 1.1

        if self.reversed:
            t_norm = 1 - t_norm

        if self.direction in ('E', 'W'):
            t_norm = 2 * (t_norm - 0.5) # goes from -1.2 to 1.2 (in contrast to -0.1 to 1.1 for N and S)

        t_scaled = self.t_scale * t_norm
        I = 255 * (1 - self.narrowness * (self.xy_norm - t_scaled) ** 2)

        # ensure positive values
        I[I < 0] = 0

        # optionally make binary
        if binary:
            I[I > 0] = 255
            I = I.astype(np.uint8)

        self.pixels = np.outer(I, self.rgb)

        return self.pixels
    
class BroadSweep(Sweep):
    brightness = 0.25 + 0.5 * random()
    narrowness = randint(6, 12)
    t_scale = 1 + 1 * random() # between 1 and 2

class NarrowSweep(Sweep):
    brightness = 1
    narrowness = 400
    t_scale = 1.5 + 1.5 * random() # between 2 and 4

class NarrowSweeps(NarrowSweep):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_beats = randint(4, 8)
        self.number_of_sweeps = randint(3, 8)
        self.sweep_interval = randint(1, 2)
        self.beat = self.beat_offset - self.number_of_sweeps / self.sweep_interval
    
    def get_rgb(self):
        individual_sweeps = np.zeros((self.number_of_sweeps, self.num_pixels, 3), dtype=np.uint8)

        # get the individual sweeps
        for i in range(self.number_of_sweeps):
            beat = self.beat + i / self.sweep_interval # each next sweep is delayed by beat divided by the sweep interval
            individual_sweeps[i] = self.get_rgb_of_beat(beat, binary=True)
        
        # sum the individual sweeps
        combined_sweeps = np.sum(individual_sweeps, axis=0, dtype=np.uint8)

        return combined_sweeps
    
class BroadSweepUp(BroadSweep):
    direction = 'N'

class BroadSweepRight(BroadSweep):
    direction = 'E'

class BroadSweepDown(BroadSweep):
    direction = 'S'

class BroadSweepLeft(BroadSweep):
    direction = 'W'

class NarrowSweepsUp(NarrowSweeps):
    direction = 'N'

class NarrowSweepsRight(NarrowSweeps):
    direction = 'E'

class NarrowSweepsDown(NarrowSweeps):
    direction = 'S'

class NarrowSweepsLeft(NarrowSweeps):
    direction = 'W'

class SnakeStrip(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_beats = randint(3, 6)
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
        brightness = 0.25 + 0.5 * random()
        self.rgb = hsv_to_rgb(self.color, 1, brightness)
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
        self.num_rounds = randint(4, 9)
        self.max_spiral_width = randint(8, 25)
        self.line_width = self.max_spiral_width / randint(4, 6)
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
        self.decay_coef = 6
        self.max_beats = randint(2, 4)
        self.beat = self.beat_offset - 1

        r = self.pixeldata['coords_spherical'][:, 0]
        r_max = np.max(r)
        self.r_norm = r / r_max + 0.1 # goes from 0.1 to 1.1

    def get_rgb(self):
        # wait until the beat offset has passsed
        if self.beat < 0:
            return self.pixels
        
        t_norm = self.beat / self.max_beats
        I = 255 * np.exp(-self.decay_coef / self.r_norm * t_norm)
        self.pixels = np.outer(I, self.rgb)

        return self.pixels

class FlashFadeSlow(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        saturation = random() / 2
        self.rgb = hsv_to_rgb(color, saturation, 1)
        self.decay_coef = 0.5
        self.max_beats = randint(10, 20)
        self.beat = self.beat_offset - 1

        r = self.pixeldata['coords_spherical'][:, 0]
        r_max = np.max(r)
        self.r_norm = r / r_max + 0.1 # goes from 0.1 to 1.1

    def get_rgb(self):        
        t_norm = (self.beat / self.max_beats - 0.2) * 7 # goes from -1.4 to 5.6
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
        self.beat = self.beat_offset - 1

    def get_rgb(self):

        if self.beat % 1 == 0: # do every beat

            chosen_section = self.shuffled[self.section]

            on = (self.section_ids == chosen_section)
            on = np.prod(on, axis=1)

            self.pixels = np.outer(255 * on, self.rgb)
            self.section = (self.section + 1) % len(self.shuffled)

        return self.pixels

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
        self.beat = self.beat_offset - 1

    def get_rgb(self):

        if (self.beat * 2) % 1 == 0: # do every off-beat

            start_unit_id = self.num_units * self.unit_id
            chosen_units = self.shuffled_units[start_unit_id : start_unit_id + self.num_units]

            on = np.isin(self.units, chosen_units)

            self.pixels = np.outer(255 * on, self.rgb)
            self.unit_id = (self.unit_id + 1) % int(len(self.shuffled_units) / self.num_units)

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

class Shower(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        saturation = 0.5 + random() / 2
        self.rgb = hsv_to_rgb(color, saturation, 1)
        self.x = self.pixeldata['coords_cart'][:,0]
        self.y = self.pixeldata['coords_cart'][:,1]

        self.drop_speed = randint(32, 50) # cm / beat
        self.drop_width = randint(25, 100) / self.drop_speed
        self.fade = 7 / self.drop_speed # which is "a" in the formulas below
        self.fade_norm = np.exp(-1 / self.fade) / self.fade # normalization coefficient for "a"

        self.x_min = int(self.x.min())
        self.x_max = int(self.x.max())
        self.y_max = self.y.max()

        self.drop_coords = np.array([[randint(self.x_min, self.x_max), self.y_max]])

    def get_rgb(self):
        # Using formula for a single droplet:
        # I = ye^(-ay) * e^-x^2
        # which needs to be normalized
        # dI/dy = e^-ay - ay*e^-ay = 0
        # 1 = ay => y = 1/a
        # I(1/a) = 1/a*e(-1/a)

        num_drops = len(self.drop_coords)
        drop_intensities = np.zeros((num_drops, self.num_pixels))

        for i, drop in enumerate(self.drop_coords):
            x = self.x - drop[0]
            y = self.y - drop[1]
            drop_intensity = np.exp(-(x**2 / self.drop_width)) * y * np.exp(-self.fade * y) / self.fade_norm
            drop_intensity[drop_intensity < 0] = 0

            drop_intensities[i] = drop_intensity

        summed_intensities = 255 * np.sum(drop_intensities, axis=0)
        self.pixels = np.outer(summed_intensities, self.rgb)

        # lower drops
        self.drop_coords[:,1] -= self.drop_speed * self.beat_increment

        # generate new droplets
        if (self.beat * 2) % 1 == 0: # do every off-beat
            beats_left = self.max_beats - self.beat
            if ((beats_left - 1) * self.drop_speed > self.y_max):
                new_drop = np.array([[randint(self.x_min, self.x_max), self.y_max]])
                self.drop_coords = np.append(self.drop_coords, new_drop, axis=0)

        return self.pixels
        
class Sparkles(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = choice(self.colors)
        saturation = random()
        self.rgb = hsv_to_rgb(color, saturation, 1)
        self.indices = np.arange(self.num_pixels)
        self.num_sparkles = randint(10, 25)
        self.on_count = randint(1, 7) / 2
        self.off_count = 0
        self.beat = self.beat_offset - 1

    def get_rgb(self):

        if (self.beat * 8) % 1 == 0: # sparkle frequency is 8 per beat
            if self.on_count > 0:
                indices_sparkles = np.random.choice(self.indices, self.num_sparkles, replace=False)
                on = np.isin(self.indices, indices_sparkles)
                self.pixels = np.outer(255 * on, self.rgb)

                if (self.beat * 2) % 1 == 0:
                    self.on_count -= 0.5

                    if self.on_count == 0:
                        self.off_count = randint(1, 7) / 2

            elif self.off_count > 0:
                self.pixels = np.zeros((self.num_pixels, 3), dtype=np.uint8)

                if (self.beat * 2) % 1 == 0:
                    self.off_count -= 0.5

                    # when the off count has finished, determine the new on duration
                    if self.off_count == 0:
                        self.on_count = randint(1, 4) / 2

        return self.pixels

class CircularPulses(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        saturation = 0.5 + 0.5 * random()
        self.rgb = hsv_to_rgb(self.color, saturation, 1)
        self.frequency = 1
        self.drop_radius = randint(30, 70)
        self.circle_width = 3
        self.drop_speed = 2 * self.drop_radius
        self.beat -= self.beat_offset
        
        self.x = self.pixeldata['coords_cart'][:,0]
        self.y = self.pixeldata['coords_cart'][:,1]
        self.xlim = (int(min(self.x)), int(max(self.x)))
        self.ylim = (int(min(self.y)), int(max(self.y)))

        self.drop_coords = np.array([[randint(*self.xlim), randint(*self.ylim), 5 * self.drop_radius]], dtype=float) # coords in x, y, z

    
    def get_rgb(self):
        # Using formula for a single droplet (falling elongated sphere):
        # a pixel is ON if it is within the droplet radius + circle width and outside the droplet radius
        # d < r + w and d > r
        # d = V(dx^2 + dy^2 + dz^2) = V((x_drop - x)^2 + (y_drop - y)^2 + z_drop^2)

        num_drops = len(self.drop_coords)
        droplets_on = np.zeros((num_drops + 1, self.num_pixels))
        for i, drop in enumerate(self.drop_coords):
            dx = drop[0] - self.x
            dy = drop[1] - self.y
            dz = drop[2]
            d = np.sqrt(dx**2 + dy**2 + (0.25 * dz)**2)
            droplet_on = (d < self.drop_radius + self.circle_width) * (d > self.drop_radius)
            droplets_on[i] = droplet_on
        
        combined_droplets = 255 * np.max(droplets_on, axis=0)
        self.pixels = np.outer(combined_droplets, self.rgb)

        # lower drops
        self.drop_coords[:,2] -= self.drop_speed * self.beat_increment

        # remove old droplets
        condition = self.drop_coords[:, 2] > -5 * self.drop_radius
        self.drop_coords = self.drop_coords[condition, :]
        
        # generate new droplets
        if (self.beat * self.frequency) % 4 == 0: # do every off-beat
            beats_left = self.max_beats - self.beat
            if beats_left > 1:
                new_drop = np.array([[randint(*self.xlim), randint(*self.ylim), 5 * self.drop_radius]]) # choose new point, 1 radius above the strip
                self.drop_coords = np.append(self.drop_coords, new_drop, axis=0)

        return self.pixels
    
class CircularWaves(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = choice(self.colors)
        saturation = 0.5 + 0.5 * random()
        self.rgb = hsv_to_rgb(self.color, saturation, 1)
        self.frequency = randint(1, 4) # number of drops generated per beat
        self.max_radius = randint(70, 140)
        self.circle_width = 7
        self.wave_speed = randint(15, 35)
        self.beat -= self.beat_offset
        
        self.x = self.pixeldata['coords_cart'][:,0]
        self.y = self.pixeldata['coords_cart'][:,1]
        self.xlim = (int(min(self.x)), int(max(self.x)))
        self.ylim = (int(min(self.y)), int(max(self.y)))

        self.wave_coords = np.array([[randint(*self.xlim), randint(*self.ylim), 0]], dtype=float) # coords in x, y, z

    
    def get_rgb(self):
        # Using formula for a single droplet:
        # a pixel is ON if it is within the droplet radius + circle width and outside the droplet radius

        num_waves = len(self.wave_coords)
        wave_intensities = np.zeros((num_waves + 1, self.num_pixels))
        for i, wave in enumerate(self.wave_coords):
            dx = wave[0] - self.x
            dy = wave[1] - self.y
            r = wave[2]
            d = np.sqrt(dx**2 + dy**2)
            wave_on = (d < r + self.circle_width) * (d > r)
            wave_intensity = 255 * (1 - r / self.max_radius) * wave_on
            wave_intensities[i] = wave_intensity
        
        combined_waves = np.max(wave_intensities, axis=0)
        self.pixels = np.outer(combined_waves, self.rgb)

        # increase the wave sizes
        self.wave_coords[:,2] += self.wave_speed * self.beat_increment

        # remove old waves
        condition = self.wave_coords[:, 2] < self.max_radius
        self.wave_coords = self.wave_coords[condition, :]
        
        # generate new waves
        if (self.beat * self.frequency) % 4 == 0: # do every off-beat
            beats_left = self.max_beats - self.beat
            if beats_left > 1:
                new_wave = np.array([[randint(*self.xlim), randint(*self.ylim), 0]]) # choose new point
                self.wave_coords = np.append(self.wave_coords, new_wave, axis=0)

        return self.pixels
    
class Nova(Effect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_beats = randint(2, 3)
        self.color = choice(self.colors)

        r = self.pixeldata['coords_spherical'][:, 0]
        r_max = np.max(r)
        self.r_norm = r / r_max # goes from 0 to 1

        r_scale = 0.75 + 0.25 * random()
        self.r_1 = 0.25 * r_scale # radius of the light circle at t_1
        self.r_2a = 0.07 # radius of the dark circle at t_1
        self.r_2b = 0.12 * r_scale # radius of the dark circle at t_2

        self.t_1 = 0.4 # time until light circle grows
        self.t_2 = 0.5 # time when dark circle grows
    
    def get_rgb(self):
        # Concept:
        # 1. light circle grows until t_1
        # 2. dark circle grows until t_2
        # 3. light and dark circles both grow until the dark circle is fully grown 

        t_norm = self.beat / self.max_beats # goes from 0 to 1

        if (t_norm < self.t_1):
            t_scaled = t_norm / self.t_1
            r_light = self.r_1 * (t_scaled ** 2)
            on = self.r_norm < r_light
        
        elif (t_norm < self.t_2):
            t_scaled = (t_norm - self.t_1) / (self.t_2 - self.t_1)
            light = self.r_norm < self.r_1
            r_dark = self.r_2a + (self.r_2b - self.r_2a) * (t_scaled ** 2)
            dark = self.r_norm < r_dark
            on = light * (1 - dark)
        
        else:
            t_scaled = (t_norm - self.t_2) / (1 - self.t_2)
            r_light = self.r_1 + 2 * (1 - self.r_1) * (t_scaled ** 1.5) # light circle grows faster than the dark circle
            light = self.r_norm < r_light
            r_dark = self.r_2b + (1 - self.r_2b) * (t_scaled ** 2)
            dark = self.r_norm < r_dark
            on = light * (1 - dark)

        rgb = hsv_to_rgb(self.color, t_norm**2, 1) # the saturation increases with time
        self.pixels = 255 * np.outer(on, rgb)

        return self.pixels
    