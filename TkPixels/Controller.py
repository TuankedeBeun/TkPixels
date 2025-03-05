from time import sleep, time
from random import random, randint
import numpy as np
import csv
from TkPixels.EffectSets import EffectSets

DATA_PATH = './data/settings.csv'

class Controller():
    def __init__(self, board):
        self.board = board
        
        # set state, bpm, effect_set_nr, brightness, effect_intensity, num_colors
        # It also sets time_per_beat, beat_increment
        self.load_settings()
        
        # determine time properties
        self.time = 0
        self.phrase = 0
        self.bar = 0
        self.beat = 0
        self.beat_increments = 0
        
        # color settings
        self.colors = [0, 0, 0]
        self.choose_colors()
        
        # effect settings
        self.max_effects = 0
        self.chance_effect_per_beat = 0.0
        self.num_effects = 0
        self.effects = []
        
        self.effect_set = self.set_effect_set(self.effect_set_nr)
    
    def load_settings(self):
        
        with open(DATA_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            settings = dict(reader)
        
        self.state = int(settings['state'])
        self.bpm = float(settings['bpm'])
        self.effect_set_nr = int(settings['mode'])
        self.brightness = float(settings['brightness'])
        effect_intensity = float(settings['effect_intensity'])
        self.num_colors = int(settings['number_of_colors'])
        
        # adjust BPM settings
        self.time_per_beat = 60 / self.bpm
        if self.bpm < 125:
            self.beat_increment = 0.0625
        else:
            self.beat_increment = 0.125
            
        # adjust effect instensity
        self.chance_effect_per_beat = 0.2 + (1 * effect_intensity) # range 0.2 - 1.2
        
        print(settings)

    def play(self):
        self.time = time()

        while True:
            effect_values = np.zeros((self.num_effects, self.board.num_pixels, 3))

            # get individual effects
            for i, effect in enumerate(self.effects):
                effect_value = effect.get_rgb()
                effect_values[i,:,:] = effect_value

            # combine effects
            effects_combined = np.sum(effect_values, axis=0, dtype=int)
            effects_combined[effects_combined > 255] = 255

            # draw
            self.draw_strips(effects_combined)

            # increment time
            self.increment_beat()

            # check which effects expire
            self.expire_effects()

            # chance to add new effect
            if self.state:
                self.add_effect()

    def draw_strips(self, vectors):
        for (strip, led), v in zip(self.board.pixeldata['indices'], vectors):
            self.board.strips[strip][led] = tuple(v)
        
        self.board.update()

    def increment_beat(self):
        self.beat_increments += self.beat_increment

        if self.beat_increments - self.beat > 0.98:
            self.beat += 1
            self.beat_increments = round(self.beat_increments)

            if self.beat % 4 == 0:
                self.bar += 1
                self.load_settings()
                self.board.set_brightness(self.brightness)
                self.effect_set = self.set_effect_set(self.effect_set_nr)
                
                if self.bar % 32 == 0:
                    self.phrase += 1
                    self.choose_colors()

        for effect in self.effects:
            effect.increment()

        time_passed = time() - self.time
        time_to_wait = max(0, self.beat_increment * self.time_per_beat - time_passed)
        # print('time to sleep:', time_to_wait)
        sleep(time_to_wait)
        self.time = time()

    def choose_colors(self):
        self.colors = [random() for i in range(self.num_colors)]

    def expire_effects(self):
        for i in range(self.num_effects - 1, -1, -1):
            effect = self.effects[i]
            if effect.beat >= effect.max_beats:
                self.effects.pop(i)
                self.num_effects -= 1

    def add_effect(self):

        if self.num_effects >= self.effect_set.max_effects:
            return
        
        chance_per_increment = self.beat_increment * self.chance_effect_per_beat * self.effect_set.chance_multiplier
        if chance_per_increment > random():
            new_effect = self.effect_set.new_effect()
            max_beats = randint(4, 16)
            new_effect_instance = new_effect(self.colors, self.beat_increment, max_beats, self.board.num_pixels, self.board.pixeldata)
            self.effects.append(new_effect_instance)
            self.num_effects += 1

    def random_effect_set(self):
        possible_sets = list(range(7))
        weights = [1, 3, 5, 2, 3, 2, 2]
        sum_weights = sum(weights)
        weights = [i/sum_weights for i in weights]

        effect_set_nr = np.random.choice(possible_sets, p = weights)
        print('effect set', effect_set_nr)
        return effect_set_nr

    def set_effect_set(self, effect_set_nr):
        effect_set = EffectSets[effect_set_nr]
        return effect_set()