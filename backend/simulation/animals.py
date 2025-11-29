from .agents import Agent
import random
import config
import math

class Animal(Agent):
    def __init__(self, x: int, y: int, species: str, habitat: str = config.HABITAT_AMPHIBIOUS):
        super().__init__(x, y, "animal")
        self.species = species
        self.habitat = habitat
        self.state = {
            "hunger": 0.0,
            "energy": 100.0,
            "speed": config.ANIMAL_SPEED,
            "vision_radius": 100.0,
            "color": "#e74c3c",  # Red (Default/Amphibious)
            "habitat": habitat
        }
        
        # Set color based on habitat
        if habitat == config.HABITAT_AQUATIC:
            self.state["color"] = "#3498db" # Blue
        elif habitat == config.HABITAT_TERRESTRIAL:
            self.state["color"] = "#8e44ad" # Purple

    def update(self, environment: 'Environment'):
        # Environment effects
        # Temperature affects speed: Optimal is 25.0. Deviations reduce speed.
        temp_factor = 1.0 - (abs(environment.temperature - 25.0) / 50.0)
        current_speed = self.state["speed"] * max(0.1, temp_factor)

        # Humidity affects energy loss: Low humidity drains energy faster (amphibian-like)
        humidity_factor = 1.0
        if environment.humidity < 40.0:
            humidity_factor = 2.0 # Double energy loss in dry air
            
        # Terrain Constraints
        terrain = environment.get_terrain_at(self.x, self.y)
        terrain_penalty = 1.0
        energy_drain = 1.0
        
        if self.habitat == config.HABITAT_AQUATIC:
            if terrain != config.TERRAIN_WATER:
                terrain_penalty = 0.1 # Stuck on land
                energy_drain = 5.0 # Suffocating
        elif self.habitat == config.HABITAT_TERRESTRIAL:
            if terrain == config.TERRAIN_WATER:
                terrain_penalty = 0.5 # Slow in water
                energy_drain = 5.0 # Drowning
                
        current_speed *= terrain_penalty

        # Behavior Logic
        dx, dy = 0, 0
        target_found = False

        # 1. Check for food if hungry
        if self.state["hunger"] > 20.0:
            visible_agents = environment.get_visible_agents(self, self.state["vision_radius"])
            closest_food = None
            min_dist = float('inf')

            for other in visible_agents:
                if other.agent_type == "plant" and other.alive:
                    dist = ((other.x - self.x)**2 + (other.y - self.y)**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_food = other

            if closest_food:
                # Move towards food
                target_found = True
                angle = math.atan2(closest_food.y - self.y, closest_food.x - self.x)
                dx = math.cos(angle) * current_speed
                dy = math.sin(angle) * current_speed

                # Eat if close enough
                if min_dist <= 5.0:
                    closest_food.alive = False
                    environment.remove_agent(closest_food.id)
                    # Gain energy, reduce hunger
                    self.state["energy"] = min(100.0, self.state["energy"] + 20.0)
                    self.state["hunger"] = max(0.0, self.state["hunger"] - 30.0)

        # 2. Random movement if no target found
        if not target_found:
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
        self.state["energy"] -= config.ANIMAL_ENERGY_LOSS_RATE * humidity_factor * energy_drain

        # Death
        if self.state["hunger"] >= 100.0 or self.state["energy"] <= 0:
            self.alive = False
            environment.remove_agent(self.id)
            return

        # Reproduction
        if self.state["energy"] > 80.0 and self.state["hunger"] < 20.0:
             if random.random() < 0.005: # Low chance
                self.state["energy"] -= 40.0 # Cost of reproduction
                new_animal = Animal(self.x, self.y, self.species)
                environment.add_agent(new_animal)
