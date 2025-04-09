import numpy as np
from TkPixels.Effects import *

class EffectSet():
    def __init__(self, name, effects, weights, max_effects, chance_multiplier=1):
        if len(effects) != len(weights):
            raise ValueError("The number of effects is different from the number of weights.")

        self.name = name
        self.effects = effects
        self.max_effects = max_effects
        self.chance_multiplier = chance_multiplier

        # normalize probabilities
        weights = np.array(weights)
        self.effect_weights = weights / weights.sum() 

    def new_effect(self):
        return np.random.choice(self.effects, p = self.effect_weights)
    
class All(EffectSet):
    def __init__(self):
        super().__init__(
            'Everything',
            (
                SphericalSweepOutward, SphericalSweepInward, 
                SweepUp, SweepRight, SweepDown, SweepLeft, 
                SnakeStripLeftUp, SnakeStripLeftDown, SnakeStripRightUp, SnakeStripRightDown, 
                ClockwiseRetractingSpiral, AnticlockwiseRetractingSpiral, 
                FlashFade, 
                SectionBuzz, 
                UnitBuzz,
                SectionPairsSnakeUp, SectionPairsSnakeDown,
                Shower,
                Sparkles,
                CircularPulses,
                CircularWaves
            ),
            (
                8, 8,
                8, 8, 8, 8,
                5, 5, 5, 5,
                3, 3,
                40,
                20,
                10,
                30, 30,
                15,
                10,
                10,
                15
            ),
            8
        )

class Soft(EffectSet):
    def __init__(self):
        super().__init__(
            'Soft',
            (
                SphericalSweepInward, SphericalSweepOutward, 
                SweepRight, SweepUp, SweepDown, SweepLeft,
                Shower
            ),
            (
                12, 12,
                7, 7, 7, 7,
                15
            ),
            8
        )

class Downward(EffectSet):
    def __init__(self):
        super().__init__(
            'Smoothly Downward',
            (
                SweepDown,
                SnakeStripLeftDown, SnakeStripRightDown, 
                SectionPairsSnakeDown,
                Shower
            ),
            (
                20,
                8, 8,
                20,
                25
            ),
            8
        )

class Trippy(EffectSet):
    def __init__(self):
        super().__init__(
            'Trippy',
            (
                FlashFade,
                SphericalSweepOutward, SphericalSweepInward, 
                SweepUp, SweepRight, SweepDown, SweepLeft, 
                SnakeStripLeftUp, SnakeStripLeftDown, SnakeStripRightUp, SnakeStripRightDown, 
                SectionPairsSnakeUp, SectionPairsSnakeDown,
                Shower,
                AnticlockwiseRetractingSpiral,
                CircularPulses,
                CircularWaves
            ),
            (
                25,
                10, 10,
                8, 8, 8, 8,
                10, 10, 10, 10,
                25, 25,
                20,
                6,
                12,
                15
            ),
            12,
            chance_multiplier = 4
        )

class Flashy(EffectSet):
    def __init__(self):
        super().__init__(
            'Flashy & Intense',
            (
                FlashFade,
                ClockwiseRetractingSpiral, 
                SectionBuzz, 
                UnitBuzz, 
                SectionPairsSnakeUp, SectionPairsSnakeDown, 
                Sparkles
            ),
            (
                40,
                5,
                15,
                15,
                20, 20,
                6
            ),
            6
        )

class BeatAndZip(EffectSet):
    def __init__(self):
        super().__init__(
            'Beat & Zip',
            (
                FlashFade, SectionPairsSnakeUp, SectionPairsSnakeDown
            ),
            (
                10, 15, 15
            ),
            5,
            chance_multiplier = 2
        )

class Snakes(EffectSet):
    def __init__(self):
        super().__init__(
            'Snakes',
            (
                SnakeStripLeftDown, SnakeStripLeftUp, SnakeStripRightDown, SnakeStripRightUp,
                SectionPairsSnakeDown, SectionPairsSnakeUp
            ),
            (
                5, 5, 5, 5,
                8, 8
            ),
            15,
            chance_multiplier = 4
        )

class UpUp(EffectSet):
    def __init__(self):
        super().__init__(
            'Up Up',
            (
                SnakeStripLeftUp, SnakeStripRightUp,
                SectionPairsSnakeUp,
                SweepUp
            ),
            (
                12, 12,
                20,
                15
            ),
            10,
            chance_multiplier = 4
        )

class Test(EffectSet):
    def __init__(self):
        super().__init__(
            'Test Set',
            (
                BroadSweepUp, BroadSweepRight, BroadSweepDown, BroadSweepLeft,
                NarrowSweepUp, NarrowSweepRight, NarrowSweepDown, NarrowSweepLeft,
            ),
            (
                10, 10, 10, 10,
                0, 0, 0, 0,
            ),
            10
        )

EffectSets = (All, Soft, Downward, Trippy, Flashy, BeatAndZip, Snakes, UpUp, Test)
