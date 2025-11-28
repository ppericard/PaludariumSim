from typing import List, Dict
from .agents import Agent
import config
import math

class Environment:
    def __init__(self, width: int = config.SIMULATION_WIDTH, height: int = config.SIMULATION_HEIGHT):
        self.width = width
        self.height = height
        self.agents: List[Agent] = []
        self.new_agents: List[Agent] = []
        self.dead_agents: List[str] = []
        
        # Global environment state
        self.temperature = config.DEFAULT_TEMPERATURE
        self.humidity = config.DEFAULT_HUMIDITY
        self.time = 0 # Ticks since start
        self._update_light_level()
        
        # Terrain Grid (2D array: [y][x])
        self.grid_width = self.width // config.TERRAIN_GRID_SIZE
        self.grid_height = self.height // config.TERRAIN_GRID_SIZE
        self.terrain = []
        self._generate_default_terrain()

    def _generate_default_terrain(self):
        # Default: Shoreline (Left 40% Water, Right 60% Soil)
        water_limit = int(self.grid_width * 0.4)
        
        for y in range(self.grid_height):
            row = []
            for x in range(self.grid_width):
                if x < water_limit:
                    row.append(config.TERRAIN_WATER)
                else:
                    row.append(config.TERRAIN_SOIL)
            self.terrain.append(row)

    def add_agent(self, agent: Agent):
        self.new_agents.append(agent)

    def remove_agent(self, agent_id: str):
        self.dead_agents.append(agent_id)

    def get_nearby_agents(self, agent: Agent, radius: float) -> List[Agent]:
        nearby = []
        for other in self.agents:
            if other.id == agent.id or not other.alive:
                continue
            dist = ((other.x - agent.x)**2 + (other.y - agent.y)**2)**0.5
            if dist <= radius:
                nearby.append(other)
        return nearby

    def _update_light_level(self):
        # Calculate light level: Sine wave from -1 to 1, mapped to Min/Max
        # 0 = Dawn, 0.25 = Noon, 0.5 = Dusk, 0.75 = Midnight (approx)
        cycle_progress = (self.time / config.DAY_DURATION_TICKS) * 2 * math.pi
        # Shift so it starts at dawn (sin is 0)
        sine_val = math.sin(cycle_progress - math.pi / 2) 
        # Map [-1, 1] to [MIN, MAX]
        normalized = (sine_val + 1) / 2 # [0, 1]
        self.light_level = config.MIN_LIGHT_LEVEL + normalized * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)

    def update(self):
        """
        Update the environment state and all agents.
        """
        # 1. Update global environment (Day/Night Cycle)
        self.time = (self.time + 1) % config.DAY_DURATION_TICKS
        self._update_light_level()

        # 2. Update all agents
        for agent in self.agents:
            if agent.alive:
                agent.update(self)

        # 3. Process buffers
        # Remove dead agents
        if self.dead_agents:
            self.agents = [a for a in self.agents if a.id not in self.dead_agents]
            self.dead_agents = []
        
        # Add new agents
        if self.new_agents:
            self.agents.extend(self.new_agents)
            self.new_agents = []

    def get_state(self):
        # Calculate stats
        stats = {"plant": 0, "animal": 0}
        for agent in self.agents:
            if agent.alive:
                stats[agent.agent_type] = stats.get(agent.agent_type, 0) + 1

        return {
            "environment": {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "light_level": self.light_level,
                "time": self.time,
                "terrain": self.terrain,
                "grid_size": config.TERRAIN_GRID_SIZE,
                "stats": stats
            },
            "agents": [agent.to_dict() for agent in self.agents]
        }
