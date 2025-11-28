from abc import ABC, abstractmethod
import config

class Equipment(ABC):
    def __init__(self, name: str):
        self.name = name
        self.is_on = True

    @abstractmethod
    def update(self, environment):
        pass

class LightingSystem(Equipment):
    def __init__(self):
        super().__init__("Lighting System")
        self.mode = "always_on" # "cycle" or "always_on"
        self.intensity = 1.0

    def update(self, environment):
        if not self.is_on:
            environment.light_level = config.MIN_LIGHT_LEVEL
            return

        if self.mode == "always_on":
            environment.light_level = config.MAX_LIGHT_LEVEL
        elif self.mode == "cycle":
            # Use existing cycle logic from environment (moved here)
            progress = (environment.time % config.DAY_DURATION_TICKS) / config.DAY_DURATION_TICKS
            
            if progress < config.PHASE_DAWN_START:
                # Night (Early)
                environment.light_level = config.MIN_LIGHT_LEVEL
            elif progress < config.PHASE_DAY_START:
                # Dawn (Transition MIN -> MAX)
                phase_progress = (progress - config.PHASE_DAWN_START) / (config.PHASE_DAY_START - config.PHASE_DAWN_START)
                environment.light_level = config.MIN_LIGHT_LEVEL + phase_progress * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
            elif progress < config.PHASE_DUSK_START:
                # Day (Stable MAX)
                environment.light_level = config.MAX_LIGHT_LEVEL
            elif progress < config.PHASE_NIGHT_START:
                # Dusk (Transition MAX -> MIN)
                phase_progress = (progress - config.PHASE_DUSK_START) / (config.PHASE_NIGHT_START - config.PHASE_DUSK_START)
                environment.light_level = config.MAX_LIGHT_LEVEL - phase_progress * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
            else:
                # Night (Late)
                environment.light_level = config.MIN_LIGHT_LEVEL
