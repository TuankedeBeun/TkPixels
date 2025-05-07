import numpy as np
from colorsys import hsv_to_rgb
from random import random, choice, randint

class AfterEffect():
    def __init__(self, colors, beat_increment, beat_offset):
        self.colors = colors
        self.max_beats = 16 * randint(1, 4)
        self.beat_increment = beat_increment
        self.beat = beat_offset - 1
    
    def apply(self, pixels, beat_increment=None):
        pass
    
    def increment(self):
        self.beat += self.beat_increment

class BoostColor(AfterEffect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boost_color = choice(self.colors)
        self.max_boost_factor = 0.75 #0.25 + random() * 0.5

        rgb = hsv_to_rgb(self.boost_color, 1, 1)
        print(f'Boost color: {self.boost_color}, RGB: {rgb}')
        print(f'Max boost factor: {self.max_boost_factor}')
        print(f'Max beats: {self.max_beats}')
        
    def apply(self, pixels):

        # gradually increase the boost factor in the first 4 beats, decrease in the last 4 beats and keep it constant in the middle
        if self.beat < 4:
            boost_factor = self.beat / 4 * self.max_boost_factor
        elif self.beat > self.max_beats - 4:
            boost_factor = (self.max_beats - self.beat) / 4 * self.max_boost_factor
        else:
            boost_factor = self.max_boost_factor

        boost_factor = max(0, boost_factor)  # ensure boost factor is not negative

        # convert the boost color to RGB factors
        rgb = hsv_to_rgb(self.boost_color, boost_factor, 1)
        for i in range(3):
            pixels[:, i] = rgb[i] * pixels[:, i]

        return pixels

class DipOnBeat(AfterEffect):
    # This after effect dips the brightness of the pixels on the beat
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_dip_factor = 0.6 + random() * 0.3 # from 0.6 to 0.9
        self.frequency = 2 ** randint(0, 3)
        print(f'Dip on beat: {self.max_dip_factor}, Frequency: {self.frequency}')

    def apply(self, pixels):
        # the dip factor is dependent on how far away we are from the beat
        # the dip factor is max_dip_factor at the beat and 1 exactly in between beats
        # it follows a fourth-order curve: I(t) = ((t*2 - 1)^4 - 1) * max_dip_factor + 1

        t = (self.beat % self.frequency) / self.frequency
        dip_factor = ((t * 2 - 1) ** 6 - 1) * self.max_dip_factor + 1
        brightness = 1 - dip_factor

        # ensure brightness is not negative
        brightness = max(0, brightness)

        # dip the brightness of the pixels
        pixels = np.uint8(pixels * brightness)

        return pixels