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
        # Stats History
        self.stats_history = []

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
        # Calculate progress through the day (0.0 to 1.0)
        progress = (self.time % config.DAY_DURATION_TICKS) / config.DAY_DURATION_TICKS
        
        if progress < config.PHASE_DAWN_START:
            # Night (Early)
            self.light_level = config.MIN_LIGHT_LEVEL
        elif progress < config.PHASE_DAY_START:
            # Dawn (Transition MIN -> MAX)
            phase_progress = (progress - config.PHASE_DAWN_START) / (config.PHASE_DAY_START - config.PHASE_DAWN_START)
            self.light_level = config.MIN_LIGHT_LEVEL + phase_progress * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
        elif progress < config.PHASE_DUSK_START:
            # Day (Stable MAX)
            self.light_level = config.MAX_LIGHT_LEVEL
        elif progress < config.PHASE_NIGHT_START:
            # Dusk (Transition MAX -> MIN)
            phase_progress = (progress - config.PHASE_DUSK_START) / (config.PHASE_NIGHT_START - config.PHASE_DUSK_START)
            self.light_level = config.MAX_LIGHT_LEVEL - phase_progress * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
        else:
            # Night (Late)
            self.light_level = config.MIN_LIGHT_LEVEL

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

        # 4. Record Stats History (Every 10 ticks / 1 second)
        if self.time % 10 == 0:
            current_stats = self._calculate_stats()
            # Add timestamp (ticks) to stats
            current_stats["time"] = self.time
            self.stats_history.append(current_stats)
            # Limit history to avoid memory issues (e.g., last 10000 points = ~2.7 hours)
            if len(self.stats_history) > 10000:
                self.stats_history.pop(0)

    def _calculate_stats(self):
        stats = {"plant": 0, "animal": 0}
        for agent in self.agents:
            if agent.alive:
                stats[agent.agent_type] = stats.get(agent.agent_type, 0) + 1
        return stats

    def get_state(self):
        # Calculate stats
        stats = self._calculate_stats()
        stats["time"] = self.time # Add time to current stats too

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
