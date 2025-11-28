from .agents import Agent
import random

class Animal(Agent):
    def __init__(self, x: int, y: int, species: str):
        super().__init__(x, y, "animal")
        self.species = species
        self.state = {
            "hunger": 0.0,
            "energy": 100.0,
            "speed": 2.0,
            "color": "#e74c3c"  # Red
        }

    def update(self, environment: 'Environment'):
        # Basic random movement
        # TODO: Add collision detection and bounds checking
        dx = random.uniform(-1, 1) * self.state["speed"]
        dy = random.uniform(-1, 1) * self.state["speed"]
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Keep within bounds
        if 0 <= new_x <= environment.width:
            self.x = new_x
        if 0 <= new_y <= environment.height:
            self.y = new_y
            
        # Increase hunger, decrease energy
        self.state["hunger"] += 0.1
        self.state["energy"] -= 0.05
