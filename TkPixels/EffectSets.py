import numpy as np
from TkPixels.Effects import *
from TkPixels.AfterEffects import *

class EffectSet():
    def __init__(self, name, effects, weights, max_effects, chance_multiplier=1, after_effects=None):
        if len(effects) != len(weights):
            raise ValueError("The number of effects is different from the number of weights.")

        self.name = name
        self.effects = effects
        self.after_effects = [after_effects] if isinstance(after_effects, Effect) else after_effects
        self.max_effects = max_effects
        self.chance_multiplier = chance_multiplier

        # normalize probabilities
        weights = np.array(weights)
        self.effect_weights = weights / weights.sum() 

    def new_effect(self):
        return np.random.choice(self.effects, p = self.effect_weights)
    
    def new_after_effect(self):
        if self.after_effects is None:
            return None
        
        elif len(self.after_effects) == 1:
            return self.after_effects[0]
        
        return np.random.choice(self.after_effects)

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
            6,
            after_effects = (BoostColor, DipOnBeat, Blurr)
        )

class Soft(EffectSet):
    def __init__(self):
        super().__init__(
            'Soft',
            (
                SphericalSweepInward, SphericalSweepOutward, 
                BroadSweepUp, BroadSweepRight, BroadSweepDown, BroadSweepLeft, 
                Shower,
                CircularWaves,
                GraphSnake
            ),
            (
                12, 12,
                7, 7, 7, 7,
                5,
                1,
                10
            ),
            8,
            chance_multiplier = 1.2,
            after_effects = (BoostColor, DipOnBeat)
        )

class Downward(EffectSet):
    def __init__(self):
        super().__init__(
            'Smoothly Downward',
            (
                BroadSweepDown,
                SnakeStripLeftDown, SnakeStripRightDown,
                NarrowSweepsDown,
                SectionPairsSnakeDown,
                Shower
            ),
            (
                20,
                8, 8,
                5,
                20,
                15
            ),
            8,
            after_effects = (BoostColor,)
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
                1,
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
            chance_multiplier = 1.5,
            after_effects = (BoostColor, DipOnBeat, Blurr)
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
            chance_multiplier = 1.2,
            after_effects = (DipOnBeat,)
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
            chance_multiplier = 0.9,
            after_effects = (DipOnBeat, Blurr)
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
                30, 1,
                50, 50,
                8
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
                GraphSnake
            ),
            (
                5, 5, 5, 5,
                8, 8,
                35
            ),
            15,
            chance_multiplier = 3,
            after_effects = (BoostColor, Blurr)
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
                20, 20,
                30,
                15,
                3
            ),
            10,
            chance_multiplier = 2.5,
            after_effects = (BoostColor, DipOnBeat, Blurr)
        )

class CirclesAndShower(EffectSet):
    def __init__(self):
        super().__init__(
            'Circles & Shower',
            (
                CircularWaves,
                SphericalSweepOutward,
                Shower,
                Nova
            ),
            (
                8,
                15,
                8,
                3
            ),
            3,
            chance_multiplier = 2,
            after_effects = (BoostColor, Blurr)
        )

class Test(EffectSet):
    def __init__(self): 
        super().__init__(
            'Test Set',
            (
                GraphSnake,
                GraphSectionBuzz,
                GraphSectionSnake,
                GraphNodeBuzz,
                GraphLightning
            ),
            (
                10,
                10,
                10,
                10,
                10,
            ),
            3,
            chance_multiplier = 1
        )
    
def random_effect_set():
    effect_set_weights = np.array(EffectSetWeights) / sum(EffectSetWeights)
    return np.random.choice(EffectSets, p = effect_set_weights)

EffectSets = (Test, Soft, Downward, Trippy, IntenseMoving, IntenseFlashing, BeatAndZip, Snakes, UpUp, CirclesAndShower, All)
EffectSetWeights = (0, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1)
