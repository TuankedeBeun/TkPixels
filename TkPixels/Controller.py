from time import sleep, time
from random import random, choice, randint
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
        self.num_colors = 3
        self.colors = [0, 0, 0]
        self.max_effects = 3
        self.num_effects = 1
        self.chance_effect_per_increment = 0.1
        self.possible_effects = (Strobe, StrobeColor, SweepUp, SweepRight, SweepDown, SweepUp)

        self.choose_colors()
        self.effects = [SweepLeft(self.colors, 4, self.board.num_pixels, self.board.pixeldata)]

    def play(self):
        self.time = time()

        while True:
            num_effects = len(self.effects)
            effect_values = np.zeros((num_effects, self.board.num_pixels, 3))

            # Get individual effects
            for i, effect in enumerate(self.effects):
                effect_value = effect.get_rgb()
                effect_values[i,:,:] = effect_value

            # combine effects
            effects_combined = np.sum(effect_values, axis=0, dtype=np.uint8)

            # draw
            self.draw_strips(effects_combined)

            # increment time
            self.increment_beat()

            # check which effects expire
            self.expire_effects()

            # chance to add new effect
            self.add_effect()

    def draw_strips(self, vectors):
        for (strip, led), v in zip(self.board.pixeldata['indices'], vectors):
            self.board.strips[strip][led] = tuple(v)
        
        self.board.canvas.update()

    def increment_beat(self):
        self.beat += self.beat_increment

        for effect in self.effects:
            effect.increment(self.beat_increment)

        time_passed = time() - self.time
        time_to_wait = max(0, self.beat_increment * self.time_per_beat - time_passed)
        sleep(time_to_wait)
        self.time = time()

    def choose_colors(self):
        self.num_colors = randint(3, 5)
        self.colors = [random() for i in range(self.num_colors)]

    def expire_effects(self):
        for i in range(self.num_effects - 1, -1, -1):
            effect = self.effects[i]
            if effect.beat >= effect.max_beats:
                print('deleting effect', effect)
                self.effects.pop(i)
                self.num_effects -= 1
                print('number of effects is', self.num_effects)

    def add_effect(self):
        if self.num_effects < self.max_effects:
            if self.chance_effect_per_increment > random():
                new_effect = choice(self.possible_effects)
                max_beats = randint(4,16)
                new_effect_instance = new_effect(self.colors, max_beats, self.board.num_pixels, self.board.pixeldata)
                self.effects.append(new_effect_instance)
                self.num_effects += 1
                print('added effect', new_effect_instance, 'for', max_beats, 'beats')
                print('number of effects is', self.num_effects)