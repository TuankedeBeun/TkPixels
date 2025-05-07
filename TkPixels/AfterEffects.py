import numpy as np
from colorsys import hsv_to_rgb
from random import random, choice, randint

class AfterEffect():
    def __init__(self, colors, beat_increment):
        self.colors = colors
        self.max_beats = 16 * randint(1, 4)
        self.beat_increment = beat_increment
        self.beat = 0
    
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
