import numpy as np
from colorsys import hsv_to_rgb
from random import random, choice, randint

class AfterEffect():
    def __init__(self, colors):
        self.colors = colors
    
    def apply(self):
        pass

class Invert(AfterEffect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def apply(self, beat, pixels):
        if beat % 4 == 0:
            # pixels[:,0] = 255 - pixels[:,0]
            pixels[:,0] = 0
            pixels[:,1] = 0

        return pixels
