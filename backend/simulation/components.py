from typing import Dict, Any, Optional, List
import random
import math
import config

class Component:
    """Base class for all agent components."""
    def __init__(self, agent: 'Agent'):
        self.agent = agent

    def update(self, environment: 'Environment'):
        """Update logic for the component."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Return serializable state of the component."""
        return {}

# --- Locomotion Components ---

class Locomotion(Component):
    def __init__(self, agent: 'Agent', speed: float = 1.0):
        super().__init__(agent)
        self.speed = speed
        self.agent.state["speed"] = speed

    def is_valid_position(self, x: float, y: float, environment: 'Environment') -> bool:
        """Check if the position is valid for the agent's habitat."""
        habitat = self.agent.state.get("habitat")
        if not habitat:
            return True # No habitat constraint
            
        terrain_type = environment.get_terrain_at(x, y)
        
        if habitat == config.HABITAT_AQUATIC:
            return terrain_type == config.TERRAIN_WATER
        elif habitat == config.HABITAT_TERRESTRIAL:
            return terrain_type != config.TERRAIN_WATER
        
        return True

    def update(self, environment: 'Environment'):
        # Base update for locomotion (can be overridden)
        pass

class StaticMovement(Locomotion):
    """Agent does not move."""
    def __init__(self, agent: 'Agent', speed: float = 0.0):
        super().__init__(agent, speed)

class RandomMovement(Locomotion):
    """Agent moves randomly."""
    def update(self, environment: 'Environment'):
        dx = random.uniform(-1, 1) * self.speed
        dy = random.uniform(-1, 1) * self.speed
        
        new_x = max(0, min(environment.width, self.agent.x + dx))
        new_y = max(0, min(environment.height, self.agent.y + dy))
        
        if self.is_valid_position(new_x, new_y, environment):
            self.agent.x = new_x
            self.agent.y = new_y

class TargetedMovement(Locomotion):
    """Agent moves towards a target satisfying criteria."""
    def __init__(self, agent: 'Agent', speed: float = 1.0, target_criteria: Dict[str, Any] = None):
        super().__init__(agent, speed)
        self.target_criteria = target_criteria or {}

    def update(self, environment: 'Environment'):
        # Check hunger
        hunger = self.agent.state.get("hunger", 0)
        vision_radius = self.agent.state.get("vision_radius", 100)
        
        target = None
        if hunger > 20:
            visible = environment.get_visible_agents(self.agent, vision_radius)
            min_dist = float('inf')
            
            for other in visible:
                if not other.alive: continue
                
                # Check criteria
                match = True
                for key, value in self.target_criteria.items():
                    # Check state
                    if key in other.state:
                        if other.state[key] != value:
                            match = False
                            break
                    # Check components (by class name string for now, or use a tag)
                    elif key == "has_component":
                        # Value is a list of component names
                        for comp_name in value:
                            has_it = False
                            for c in other.components:
                                if c.__class__.__name__ == comp_name:
                                    has_it = True
                                    break
                            if not has_it:
                                match = False
                                break
                    else:
                        match = False # Key not found
                        break
                
                if match:
                    dist = ((other.x - self.agent.x)**2 + (other.y - self.agent.y)**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        target = other
        
        dx, dy = 0, 0
        if target:
            angle = math.atan2(target.y - self.agent.y, target.x - self.agent.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            
            # Eat if close (and valid move)
            if min_dist <= 5.0:
                target.alive = False
                environment.remove_agent(target.id)
                self.agent.state["energy"] = min(100.0, self.agent.state.get("energy", 0) + 20.0)
                self.agent.state["hunger"] = max(0.0, self.agent.state.get("hunger", 0) - 30.0)
                return # Stop moving this tick if ate
        else:
            # Random wander
            dx = random.uniform(-1, 1) * self.speed
            dy = random.uniform(-1, 1) * self.speed

        new_x = max(0, min(environment.width, self.agent.x + dx))
        new_y = max(0, min(environment.height, self.agent.y + dy))
        
        if self.is_valid_position(new_x, new_y, environment):
            self.agent.x = new_x
            self.agent.y = new_y

class Growth(Component):
    """Handles physical growth of the agent."""
    def __init__(self, agent: 'Agent', growth_rate: float = 0.01, max_size: float = 20.0, energy_cost: float = 0.0):
        super().__init__(agent)
        self.growth_rate = growth_rate
        self.max_size = max_size
        self.energy_cost = energy_cost
        # Ensure initial size is set if not present
        if "size" not in self.agent.state:
            self.agent.state["size"] = 1.0

    def update(self, environment: 'Environment'):
        current_size = self.agent.state["size"]
        if current_size < self.max_size:
            # Check if we have enough energy (if there's a cost)
            if self.energy_cost > 0 and self.agent.state.get("energy", 0) < self.energy_cost:
                return

            # Apply growth
            growth_amount = self.growth_rate
            
            # If energy cost is 0, we might want to scale growth by energy available (optional, but keeping simple for now)
            # Or we can make growth dependent on energy surplus like before?
            # For now, linear growth up to max size.
            
            self.agent.state["size"] = min(self.max_size, current_size + growth_amount)
            
            if self.energy_cost > 0:
                self.agent.state["energy"] -= self.energy_cost

# --- Metabolism Components ---

class Metabolism(Component):
    def __init__(self, agent: 'Agent', energy: float = 100.0, max_energy: float = 100.0):
        super().__init__(agent)
        self.agent.state["energy"] = energy
        self.agent.state["max_energy"] = max_energy

class Photosynthesis(Metabolism):
    """Gains energy from light."""
    def __init__(self, agent: 'Agent', growth_rate: float = 0.1, energy: float = 100.0, max_energy: float = 100.0):
        super().__init__(agent, energy, max_energy)
        self.growth_rate = growth_rate
        self.agent.state["size"] = self.agent.state.get("size", 5.0) # Default size

    def update(self, environment: 'Environment'):
        if environment.light_level > 0.3:
            gain = self.growth_rate * environment.light_level
            self.agent.state["energy"] = min(self.agent.state["max_energy"], self.agent.state["energy"] + gain)

class Heterotrophy(Metabolism):
    """Loses energy over time, needs to eat (handled by Interaction/Movement for now)."""
    def __init__(self, agent: 'Agent', decay_rate: float = 0.1, energy: float = 100.0, max_energy: float = 100.0):
        super().__init__(agent, energy, max_energy)
        self.decay_rate = decay_rate
        self.agent.state["hunger"] = 0.0

    def update(self, environment: 'Environment'):
        self.agent.state["energy"] -= self.decay_rate
        self.agent.state["hunger"] += self.decay_rate
        
        if self.agent.state["energy"] <= 0 or self.agent.state["hunger"] >= 100:
            self.agent.alive = False
            environment.remove_agent(self.agent.id)

# --- Reproduction Components ---

class Reproduction(Component):
    def __init__(self, agent: 'Agent', cost: float = 30.0, threshold: float = 80.0):
        super().__init__(agent)
        self.cost = cost
        self.threshold = threshold

class AsexualReproduction(Reproduction):
    def update(self, environment: 'Environment'):
        if self.agent.state["energy"] > self.threshold:
             # Density Check: Don't reproduce if crowded
             import config
             neighbors = environment.get_nearby_agents(self.agent, config.NEIGHBOR_RADIUS)
             same_species_neighbors = [n for n in neighbors if n.state.get("species") == self.agent.state.get("species")]
             
             if len(same_species_neighbors) >= config.MAX_NEIGHBORS:
                 return # Too crowded, save energy

             if random.random() < 0.01: # Chance to reproduce
                self.agent.state["energy"] -= self.cost
                
                # Local import to avoid circular dependency
                from .factory import AgentFactory
                
                species = self.agent.state.get("species", "Unknown")
                
                # Spawn nearby, but respect size to avoid overlap
                size = self.agent.state.get("size", 5.0)
                # Spawn at 3x to 5x the radius distance
                min_dist = size * 3.0
                max_dist = size * 5.0
                
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(min_dist, max_dist)
                new_x = max(0, min(environment.width, self.agent.x + math.cos(angle) * dist))
                new_y = max(0, min(environment.height, self.agent.y + math.sin(angle) * dist))
                
                new_agent = AgentFactory.create(species, new_x, new_y)
                environment.add_agent(new_agent)

class SexualReproduction(Reproduction):
    def update(self, environment: 'Environment'):
         if self.agent.state["energy"] > self.threshold and self.agent.state.get("hunger", 0) < 20:
             if random.random() < 0.005:
                self.agent.state["energy"] -= self.cost
                
                from .factory import AgentFactory
                
                species = self.agent.state.get("species", "Unknown")
                new_agent = AgentFactory.create(species, self.agent.x, self.agent.y)
                environment.add_agent(new_agent)
