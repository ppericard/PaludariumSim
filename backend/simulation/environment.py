from typing import List, Dict
from .agents import Agent
from .equipment import LightingSystem
from .spatial_grid import SpatialGrid
from .factory import AgentFactory
import config
import math
import time

class Environment:
    """
    The central container for the simulation state.

    Holds all agents, the terrain grid, and global variables (time, temperature, etc.).
    Responsible for updating the state each tick.

    Attributes:
        width (int): Simulation width in pixels.
        height (int): Simulation height in pixels.
        agents (List[Agent]): List of active agents.
        spatial_grid (SpatialGrid): Optimization structure for neighbor lookups.
        terrain (List[List[int]]): 2D grid representing terrain types.
        time (int): Cyclic time of day (0-DAY_DURATION_TICKS).
        total_ticks (int): Monotonic tick counter.
    """
    def __init__(self, width: int = config.SIMULATION_WIDTH, height: int = config.SIMULATION_HEIGHT):
        self.width = width
        self.height = height
        self.agents: List[Agent] = []
        self.new_agents: List[Agent] = []
        self.dead_agents: List[str] = []
        
        # Global environment state
        self.temperature = config.DEFAULT_TEMPERATURE
        self.humidity = config.DEFAULT_HUMIDITY
        self.time = 0 
        self.total_ticks = 0
        self.last_tick_duration = 0.0
        self.light_level = config.DEFAULT_LIGHT_LEVEL
        
        # Equipment
        self.equipment = {
            "lights": LightingSystem()
        }
        # Initial update
        self.equipment["lights"].update(self)
        
        # Spatial Grid
        self.spatial_grid = SpatialGrid(self.width, self.height, cell_size=50)

        # Terrain Grid (2D array: [y][x])
        self.grid_width = self.width // config.TERRAIN_GRID_SIZE
        self.grid_height = self.height // config.TERRAIN_GRID_SIZE
        self.terrain = []
        # Stats History
        self.stats_history = []
        self._generate_default_terrain()

    def _populate_default_agents(self):
        """Spawns a default set of agents for testing/demo purposes."""
        import random
        from .factory import AgentFactory
        
        # Spawn 20 Ferns - Scattered
        for _ in range(20):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            agent = AgentFactory.create("Fern", x, y)
            if agent:
                self.agents.append(agent)
                self.spatial_grid.add(agent)

        # Spawn 5 Frogs - Scattered
        for _ in range(5):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            agent = AgentFactory.create("Frog", x, y)
            if agent:
                self.agents.append(agent)
                self.spatial_grid.add(agent)

        # Spawn 5 Fish - Left side (Water)
        water_width = int(self.width * 0.4)
        for _ in range(5):
            x = random.randint(0, water_width - 10)
            y = random.randint(0, self.height)
            agent = AgentFactory.create("Fish", x, y)
            if agent:
                self.agents.append(agent)
                self.spatial_grid.add(agent)

        # Spawn 5 Lizards - Right side (Land)
        for _ in range(5):
            x = random.randint(water_width + 10, self.width)
            y = random.randint(0, self.height)
            agent = AgentFactory.create("Lizard", x, y)
            if agent:
                self.agents.append(agent)
                self.spatial_grid.add(agent)

    def _generate_default_terrain(self):
        """Generates the default terrain (Water on left, Soil on right)."""
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
        """
        Schedule an agent to be added to the simulation.
        
        Args:
            agent (Agent): The agent to add.
        """
        self.new_agents.append(agent)

    def remove_agent(self, agent_id: str):
        """
        Schedule an agent to be removed from the simulation.
        
        Args:
            agent_id (str): The UUID of the agent to remove.
        """
        self.dead_agents.append(agent_id)

    def get_nearby_agents(self, agent: Agent, radius: float) -> List[Agent]:
        """
        Find agents within a certain radius of a target agent.
        
        Args:
            agent (Agent): The center agent.
            radius (float): The search radius.
            
        Returns:
            List[Agent]: A list of nearby agents (excluding the center agent).
        """
        nearby = []
        # Use Spatial Grid for O(1) lookup
        candidates = self.spatial_grid.get_nearby(agent.x, agent.y, radius)
        
        for other in candidates:
            if other.id == agent.id or not other.alive:
                continue
            dist = ((other.x - agent.x)**2 + (other.y - agent.y)**2)**0.5
            if dist <= radius:
                nearby.append(other)
        return nearby

    def get_visible_agents(self, agent: Agent, radius: float) -> List[Agent]:
        """
        Get agents within the vision radius of the given agent.
        
        Args:
            agent (Agent): The observer agent.
            radius (float): The vision radius.
            
        Returns:
            List[Agent]: Visible agents.
        """
        return self.get_nearby_agents(agent, radius)

    def get_terrain_at(self, x: float, y: float) -> int:
        """
        Get the terrain type at the given coordinates.
        
        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            
        Returns:
            int: The terrain type ID (see config.TERRAIN_*).
        """
        grid_x = int(x // config.TERRAIN_GRID_SIZE)
        grid_y = int(y // config.TERRAIN_GRID_SIZE)
        
        # Boundary checks
        if grid_x < 0: grid_x = 0
        if grid_x >= self.grid_width: grid_x = self.grid_width - 1
        if grid_y < 0: grid_y = 0
        if grid_y >= self.grid_height: grid_y = self.grid_height - 1
        
        return self.terrain[grid_y][grid_x]

    def update(self):
        """
        Update the environment state and all agents.
        
        This method:
        1. Updates global variables (time, light).
        2. Updates equipment.
        3. Rebuilds the spatial grid.
        4. Calls update() on all agents.
        5. Processes agent addition/removal buffers.
        6. Records statistics.
        """
        start_time = time.perf_counter()

        # 1. Update global environment (Day/Night Cycle)
        self.time = (self.time + 1) % config.DAY_DURATION_TICKS
        self.total_ticks += 1
        
        # Update Equipment
        for system in self.equipment.values():
            system.update(self)

        # Rebuild Spatial Grid
        self.spatial_grid.clear()
        for agent in self.agents:
            if agent.alive:
                self.spatial_grid.add(agent)

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
            # Use total_ticks for monotonic time to prevent graph looping
            current_stats["time"] = self.total_ticks
            self.stats_history.append(current_stats)
            # Limit history to avoid memory issues
            if len(self.stats_history) > 10000:
                self.stats_history.pop(0)
        
        # End profiling
        self.last_tick_duration = (time.perf_counter() - start_time) * 1000 # ms

    def _calculate_stats(self):
        """Calculates population counts per species."""
        stats = {}
        for agent in self.agents:
            if agent.alive:
                species = agent.state.get("species", "Unknown")
                stats[species] = stats.get(species, 0) + 1
        return stats

    def reset(self):
        """Clear all agents and reset state."""
        self.agents = []
        self.spatial_grid.clear()
        self.dead_agents = []
        self.new_agents = []
        self.time = 0
        self.total_ticks = 0
        self.stats_history = []

    def to_dict(self):
        """Serialize environment state."""
        return {
            "width": self.width,
            "height": self.height,
            "globals": {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "time": self.time,
                "total_ticks": self.total_ticks,
                "light_level": self.light_level
            },
            "equipment": {
                "lights": {
                    "mode": self.equipment["lights"].mode,
                    "intensity": self.equipment["lights"].intensity
                }
            },
            "terrain": self.terrain,
            "agents": [agent.to_dict() for agent in self.agents]
        }

    def from_dict(self, data):
        """Deserialize environment state."""
        self.width = data["width"]
        self.height = data["height"]
        
        # Globals
        self.temperature = data["globals"]["temperature"]
        self.humidity = data["globals"]["humidity"]
        self.time = data["globals"]["time"]
        self.total_ticks = data["globals"]["total_ticks"]
        self.light_level = data["globals"]["light_level"]
        
        # Equipment
        if "equipment" in data:
            self.equipment["lights"].mode = data["equipment"]["lights"]["mode"]
            self.equipment["lights"].intensity = data["equipment"]["lights"]["intensity"]
            
        # Terrain
        self.terrain = data["terrain"]
        
        # Agents
        self.agents = []
        self.spatial_grid.clear()
        
        for agent_data in data["agents"]:
            # Reconstruct using Factory based on species in state
            species = agent_data["state"].get("species")
            if not species:
                # Fallback for old saves if species not present
                if agent_data["type"] == "plant": species = "Fern"
                elif agent_data["type"] == "animal": species = "Frog"
            
            if species:
                agent = AgentFactory.create(species, agent_data["position"]["x"], agent_data["position"]["y"])
                if agent:
                    agent.id = agent_data["id"]
                    # Restore state (overwriting factory defaults)
                    agent.state.update(agent_data["state"])
                    self.agents.append(agent)
                    self.spatial_grid.add(agent)

    def save_to_file(self, filename: str):
        """Save state to a JSON file."""
        import json
        import os
        
        if not os.path.exists("saves"):
            os.makedirs("saves")
            
        filepath = os.path.join("saves", f"{filename}.json")
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f)
            
    def load_from_file(self, filename: str):
        """Load state from a JSON file."""
        import json
        import os
        
        filepath = os.path.join("saves", f"{filename}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                self.from_dict(data)
        else:
            print(f"Save file {filename} not found.")

    def get_state(self):
        """
        Get the current state dict for frontend broadcasting.
        
        Returns:
            Dict: A dictionary containing environment globals, terrain, stats, and agent list.
        """
        # Calculate stats
        stats = self._calculate_stats()
        stats["time"] = self.total_ticks # Use total_ticks for frontend graph

        return {
            "environment": {
                "temperature": self.temperature,
                "humidity": self.humidity,
                "light_level": self.light_level,
                "light_mode": self.equipment["lights"].mode,
                "time": self.time, # Keep cyclic time for day/night rendering
                "total_ticks": self.total_ticks, # Add monotonic time
                "last_tick_duration": self.last_tick_duration,
                "terrain": self.terrain,
                "grid_size": config.TERRAIN_GRID_SIZE,
                "stats": stats
            },
            "agents": [agent.to_dict() for agent in self.agents]
        }
