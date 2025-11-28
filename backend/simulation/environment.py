from typing import List, Dict
from .agents import Agent
import config

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
        self.light_level = config.DEFAULT_LIGHT_LEVEL

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

    def update(self):
        """
        Update the environment state and all agents.
        """
        # 1. Update global environment (e.g., day/night cycle)
        # TODO: Implement day/night cycle

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
        return {
            "environment": {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "light_level": self.light_level
            },
            "agents": [agent.to_dict() for agent in self.agents]
        }
