from .agents import Agent
import random
import config

class Animal(Agent):
    def __init__(self, x: int, y: int, species: str):
        super().__init__(x, y, "animal")
        self.species = species
        self.state = {
            "hunger": 0.0,
            "energy": 100.0,
            "speed": config.ANIMAL_SPEED,
            "color": "#e74c3c"  # Red
        }

    def update(self, environment: 'Environment'):
        # Environment effects
        # Temperature affects speed: Optimal is 25.0. Deviations reduce speed.
        temp_factor = 1.0 - (abs(environment.temperature - 25.0) / 50.0)
        current_speed = self.state["speed"] * max(0.1, temp_factor)

        # Humidity affects energy loss: Low humidity drains energy faster (amphibian-like)
        humidity_factor = 1.0
        if environment.humidity < 40.0:
            humidity_factor = 2.0 # Double energy loss in dry air

        # Basic random movement
        # TODO: Add collision detection and bounds checking
        dx = random.uniform(-1, 1) * current_speed
        dy = random.uniform(-1, 1) * current_speed
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Keep within bounds
        if 0 <= new_x <= environment.width:
            self.x = new_x
        if 0 <= new_y <= environment.height:
            self.y = new_y
            
        # Increase hunger, decrease energy
        self.state["hunger"] += config.ANIMAL_HUNGER_RATE
        self.state["energy"] -= config.ANIMAL_ENERGY_LOSS_RATE * humidity_factor

        # Death
        if self.state["hunger"] >= 100.0 or self.state["energy"] <= 0:
            self.alive = False
            environment.remove_agent(self.id)
            return

        # Eating (Plants)
        # Simple herbivore logic for now
        nearby = environment.get_nearby_agents(self, radius=5.0)
        for other in nearby:
            if other.agent_type == "plant" and other.alive:
                # Eat the plant
                other.alive = False
                environment.remove_agent(other.id)
                
                # Gain energy, reduce hunger
                self.state["energy"] = min(100.0, self.state["energy"] + 20.0)
                self.state["hunger"] = max(0.0, self.state["hunger"] - 30.0)
                break # Eat one per tick

        # Reproduction
        if self.state["energy"] > 80.0 and self.state["hunger"] < 20.0:
             if random.random() < 0.005: # Low chance
                self.state["energy"] -= 40.0 # Cost of reproduction
                new_animal = Animal(self.x, self.y, self.species)
                environment.add_agent(new_animal)
