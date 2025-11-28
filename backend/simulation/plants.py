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
            
            # Update visual size/radius if we were tracking it explicitly
            # For now, size is just a state variable
