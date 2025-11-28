from typing import List, Dict
from .agents import Agent

class Environment:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.agents: List[Agent] = []
        # Grid for spatial lookups (optional optimization for later)
        # self.grid = [[[] for _ in range(width)] for _ in range(height)]
        
        # Global environment state
        self.temperature = 25.0  # Celsius
        self.humidity = 60.0     # Percentage
        self.light_level = 0.0   # 0.0 to 1.0

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def remove_agent(self, agent_id: str):
        self.agents = [a for a in self.agents if a.id != agent_id]

    def update(self):
        """
        Update the environment state and all agents.
        """
        # 1. Update global environment (e.g., day/night cycle)
        # TODO: Implement day/night cycle

        # 2. Update all agents
        for agent in self.agents:
            agent.update(self)

    def get_state(self):
        return {
            "environment": {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "light_level": self.light_level
            },
            "agents": [agent.to_dict() for agent in self.agents]
        }
