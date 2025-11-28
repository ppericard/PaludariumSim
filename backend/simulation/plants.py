from .agents import Agent
import random

class Plant(Agent):
    def __init__(self, x: int, y: int, species: str):
        super().__init__(x, y, "plant")
        self.species = species
        self.state = {
            "size": 1.0,
            "growth_rate": 0.1,
            "max_size": 10.0,
            "color": "#2ecc71"  # Green
        }

    def update(self, environment: 'Environment'):
        # Basic growth logic
        if self.state["size"] < self.state["max_size"]:
            # Growth depends on light and humidity (simplified)
            growth_factor = environment.light_level * (environment.humidity / 100.0)
            # Base growth if conditions are decent, even if simple
            if growth_factor == 0: growth_factor = 0.5 # Fallback for now until env is fully dynamic
            
            self.state["size"] += self.state["growth_rate"] * growth_factor
            
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
