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
                BroadSweepUp, BroadSweepRight, BroadSweepDown, BroadSweepLeft,
                NarrowSweepsUp, NarrowSweepsRight, NarrowSweepsDown, NarrowSweepsLeft,
                SnakeStripLeftUp, SnakeStripLeftDown, SnakeStripRightUp, SnakeStripRightDown, 
                ClockwiseRetractingSpiral, AnticlockwiseRetractingSpiral, 
                FlashFade,
                FlashFadeSlow,
                SectionBuzz, 
                UnitBuzz,
                SectionPairsSnakeUp, SectionPairsSnakeDown,
                Shower,
                Sparkles,
                CircularPulses, CircularWaves,
                Nova,
                GraphSnake, GraphSectionBuzz, GraphNodeBuzz, GraphSectionSnake,
                GraphLightning
            ),
            (
                8, 8,
                8, 8, 8, 8,
                5, 5, 5, 5,
                5, 5, 5, 5,
                3, 3,
                40,
                3,
                20,
                10,
                30, 30,
                15,
                10,
                10, 15,
                20,
                30, 15, 15, 20,
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
                BroadSweepUp, BroadSweepRight, BroadSweepDown, BroadSweepLeft, 
                Shower,
                CircularWaves
            ),
            (
                12, 12,
                7, 7, 7, 7,
                12,
                10
            ),
            8
        )

class Downward(EffectSet):
    def __init__(self):
        super().__init__(
            'Smoothly Downward',
            (
                BroadSweepDown,
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
                FlashFadeSlow,
                SphericalSweepOutward, SphericalSweepInward, 
                BroadSweepUp, BroadSweepRight, BroadSweepDown, BroadSweepLeft, 
                SnakeStripLeftUp, SnakeStripLeftDown, SnakeStripRightUp, SnakeStripRightDown, 
                SectionPairsSnakeUp, SectionPairsSnakeDown,
                GraphSnake, GraphSectionSnake,
                Shower,
                AnticlockwiseRetractingSpiral,
                CircularPulses,
                CircularWaves,
                Nova
            ),
            (
                25,
                2,
                10, 10,
                8, 8, 8, 8,
                10, 10, 10, 10,
                25, 25,
                30, 10,
                20,
                6,
                12,
                15,
                10
            ),
            12,
            chance_multiplier = 4
        )

class IntenseMoving(EffectSet):
    def __init__(self):
        super().__init__(
            'Intense Moves',
            (
                FlashFade,
                FlashFadeSlow,
                NarrowSweepsUp, NarrowSweepsRight, NarrowSweepsDown, NarrowSweepsLeft,
                ClockwiseRetractingSpiral, AnticlockwiseRetractingSpiral,
                SectionPairsSnakeUp, SectionPairsSnakeDown, 
                CircularPulses,
                Nova,
                GraphSectionSnake
            ),
            (
                40,
                2,
                4, 4, 4, 4,
                3, 3,
                20, 20,
                6,
                10,
                15
            ),
            5,
            chance_multiplier = 0.8
        )

class IntenseFlashing(EffectSet):
    def __init__(self):
        super().__init__(
            'Intense Flashes',
            (
                FlashFade,
                FlashFadeSlow,
                SectionBuzz, UnitBuzz,
                GraphSectionBuzz, GraphNodeBuzz,
                Sparkles,
                GraphLightning
            ),
            (
                40,
                2,
                12, 12,
                12, 12,
                8,
                10
            ),
            5,
            chance_multiplier = 0.8
        )

class BeatAndZip(EffectSet):
    def __init__(self):
        super().__init__(
            'Beat & Zip',
            (
                FlashFade, FlashFadeSlow,
                SectionPairsSnakeUp, SectionPairsSnakeDown,
                GraphLightning
            ),
            (
                20, 1,
                30, 30,
                10
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
                SectionPairsSnakeDown, SectionPairsSnakeUp,
                NarrowSweepsUp, NarrowSweepsRight, NarrowSweepsDown, NarrowSweepsLeft,
                GraphSnake
            ),
            (
                5, 5, 5, 5,
                8, 8,
                1, 1, 1, 1,
                30
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
                BroadSweepUp,
                NarrowSweepsUp
            ),
            (
                12, 12,
                20,
                15,
                3
            ),
            10,
            chance_multiplier = 2
        )

class CirclesAndShower(EffectSet):
    def __init__(self):
        super().__init__(
            'Circles & Shower',
            (
                CircularWaves,
                SphericalSweepOutward,
                Shower,
                Nova,
                GraphSnake
            ),
            (
                10,
                15,
                8,
                3,
                5
            ),
            5,
            chance_multiplier = 0.6
        )

class Test(EffectSet):
    def __init__(self):
        super().__init__(
            'Test Set',
            (
                GraphSectionBuzz,
                SectionBuzz,
                GraphSectionSnake,
                GraphNodeBuzz,
                GraphLightning
            ),
            (
                0,
                0,
                0,
                0,
                10
            ),
            1,
            chance_multiplier = 1
        )
    
def random_effect_set():
    effect_set_weights = np.array(EffectSetWeights) / sum(EffectSetWeights)
    return np.random.choice(EffectSets, p = effect_set_weights)

EffectSets = (Test, Soft, Downward, Trippy, IntenseMoving, IntenseFlashing, BeatAndZip, Snakes, UpUp, CirclesAndShower, All)
EffectSetWeights = (0, 2, 1, 1, 2, 2, 1, 1, 1, 1)