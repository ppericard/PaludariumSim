from .agents import Agent
import random
import config

class Plant(Agent):
    def __init__(self, x: int, y: int, species: str):
        super().__init__(x, y, "plant")
        self.species = species
        self.state = {
            "size": 5.0,
            "max_size": 20.0,
            "growth_rate": config.PLANT_GROWTH_RATE,
            "color": "#2ecc71"  # Green
        }

    def update(self, environment: 'Environment'):
        # Growth depends on light
        if self.state["size"] < self.state["max_size"]:
            # Only grow if there is enough light (e.g., > 0.3)
            if environment.light_level > 0.3:
                # Growth scales with light intensity
                growth = self.state["growth_rate"] * environment.light_level
                self.state["size"] += growth

        # Reproduction
        rnd = random.random()
        if self.state["size"] >= self.state["max_size"] * 0.8:
            if rnd < 0.01:  # 1% chance per tick if mature
                # Spawn new plant nearby
                offset_x = random.uniform(-10, 10)
                offset_y = random.uniform(-10, 10)
                new_x = max(0, min(environment.width, self.x + offset_x))
                new_y = max(0, min(environment.height, self.y + offset_y))
                
                new_plant = Plant(new_x, new_y, self.species)
                environment.add_agent(new_plant)
