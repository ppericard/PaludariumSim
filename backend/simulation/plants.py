from .agents import Agent
import random
import config
import math
from typing import Optional

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

        # Try to reproduce
        new_plant = self.reproduce(environment)
        if new_plant:
            environment.add_agent(new_plant)

    def reproduce(self, environment: 'Environment') -> Optional['Plant']:
        # Density Check: Don't reproduce if too crowded
        neighbors = environment.get_nearby_agents(self, config.PLANT_NEIGHBOR_RADIUS)
        plant_neighbors = [n for n in neighbors if n.agent_type == "plant"]
        
        if len(plant_neighbors) >= config.PLANT_MAX_NEIGHBORS:
            return None
        
        # Reproduction logic
        # Only reproduce if mature and lucky
        if self.state["size"] >= self.state["max_size"] * 0.8 and random.random() < 0.05:
            # Create offspring
            # Ensure it's at least MIN_SPAWN_DISTANCE away
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(config.PLANT_MIN_SPAWN_DISTANCE, config.PLANT_NEIGHBOR_RADIUS)
            
            new_x = max(0, min(environment.width, self.x + math.cos(angle) * distance))
            new_y = max(0, min(environment.height, self.y + math.sin(angle) * distance))
            
            return Plant(new_x, new_y, self.species)
            
        return None
