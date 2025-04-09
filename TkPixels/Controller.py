from time import sleep, time
from random import random, randint
import numpy as np
import csv
from TkPixels.EffectSets import EffectSets, random_effect_set

DATA_PATH = './data/settings.csv'

class Controller():
    def __init__(self, board):
        self.board = board
        
        # set state, bpm, effect_set_nr, brightness, effect_intensity, num_colors
        # It also sets time_per_beat, beat_increment
        self.state = None
        self.bpm = None
        self.time_per_beat = None
        self.beat_increment = None
        self.effect_set_nr = None
        self.brightness = None
        self.effect_intensity = None
        self.chance_effect_per_beat = None
        self.num_colors = None
        print('Loading initial settings')
        self.load_settings()
        print('\nRuntime setting changes:')
        
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
        self.num_effects = 0
        self.effects = []
    
    def load_settings(self):
        
        # open and read settings
        with open(DATA_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            settings = dict(reader)
        
        state = int(settings['state'])
        bpm = float(settings['bpm'])
        effect_set_nr = int(settings['mode'])
        brightness = float(settings['brightness'])
        effect_intensity = float(settings['effect_intensity'])
        num_colors = int(settings['number_of_colors'])

        if state != self.state:
            self.state = state
            print(f'State changed to: {state}')

        if bpm != self.bpm:
            self.bpm = bpm
            self.time_per_beat = 60 / bpm
            self.beat_increment = compute_beat_increment(bpm)
            print(f'BPM changed to: {bpm} (increment {self.beat_increment})')

        if effect_set_nr != self.effect_set_nr:
            self.effect_set_nr = effect_set_nr
            self.effect_set = self.set_effect_set(self.effect_set_nr)
            print(f'Effect set changed to: {effect_set_nr} ({self.effect_set.name})')

        if brightness != self.brightness:
            self.brightness = brightness
            self.board.set_brightness(self.brightness)
            print(f'Brightness changed to: {brightness}')

        if effect_intensity != self.effect_intensity:
            self.effect_intensity = effect_intensity
            self.chance_effect_per_beat = 0.2 + (1 * effect_intensity) # range 0.2 - 1.2
            print(f'Effect intensity changed to: {effect_intensity} (chance/beat {round(self.chance_effect_per_beat, 2)})')

        if num_colors != self.num_colors:
            self.num_colors = num_colors
            print(f'Number of colors changed to: {num_colors}')

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
                
                if self.bar % 32 == 0:
                    self.phrase += 1
                    self.choose_colors()
                    self.set_effect_set(self.effect_set_nr) # Only changes when having effect set shuffle
                    if self.effect_set_nr == 0:
                        print(f'New random effect set: {self.effect_set.name}')

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
            beat_offset = self.beat_increments % 1
            max_beats = randint(4, 16) # TODO: maybe make this dynamic using a settings?
            new_effect_instance = new_effect(self.colors, self.beat_increment, beat_offset, max_beats, self.board.num_pixels, self.board.pixeldata)
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
        if effect_set_nr == 0:
            effect_set = random_effect_set() # Auto shuffle effect sets
        elif effect_set_nr == -1:
            effect_set = EffectSets[0] # Choose the Test Set
        else:
            effect_set = EffectSets[effect_set_nr] # Choose a specific effect set
        return effect_set()

def compute_beat_increment(bpm, increment=1, minimum_ms=30):
    beat_length_ms = 1000 * 60 / bpm
    increment_length_ms = increment * beat_length_ms
    
    if (increment_length_ms / 2) < minimum_ms:
        return increment
    else:
        return compute_beat_increment(bpm, (increment / 2))