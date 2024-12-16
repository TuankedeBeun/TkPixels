from time import sleep, time
from colorsys import hsv_to_rgb
from random import random
from TkPixels.Effects import *

class Controller():
    def __init__(self, board, bpm):
        self.board = board
        self.bpm = bpm
        self.time_per_beat = 60 / self.bpm
        self.time = 0
        self.phrase = 0
        self.bar = 0
        self.beat = 0
        self.beat_increment = 0.25
        self.effects = [Strobe([0.42, 0.83], 16, self.board.num_pixels, self.board.pixeldata)]

    def play(self):
        self.time = time()

        while True:
            num_effects = len(self.effects)
            effect_values = np.zeros((num_effects, self.board.num_pixels, 3))

            # Get individual effects
            for i, effect in enumerate(self.effects):
                effect_value = effect.get_rgb(self.beat)
                effect_values[i,:,:] = effect_value

            # combine effects
            effects_combined = np.sum(effect_values, axis=0, dtype=np.uint8)

            # draw
            self.draw_strips(effects_combined)

            # increment time
            self.increment_beat()

            # check which effects expire
            self.expire_effects()

    def draw_strips(self, vectors):
        for (strip, led), v in zip(self.board.pixeldata['indices'], vectors):
            self.board.strips[strip][led] = tuple(v)
        
        self.board.canvas.update()

    def increment_beat(self):
        self.beat += self.beat_increment
        time_passed = time() - self.time
        time_to_wait = max(0, self.beat_increment * self.time_per_beat - time_passed)
        sleep(time_to_wait)
        self.time = time()

    def expire_effects(self):
        for effect in self.effects:
            if self.beat >= effect.max_beats:
                self.effects.remove(effect)
                del effect