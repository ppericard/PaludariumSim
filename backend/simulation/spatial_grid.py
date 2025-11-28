from typing import List, Dict, Tuple, Set
from .agents import Agent

class SpatialGrid:
    def __init__(self, width: int, height: int, cell_size: int = 50):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List[Agent]] = {}

    def _get_cell_coords(self, x: float, y: float) -> Tuple[int, int]:
        return int(x // self.cell_size), int(y // self.cell_size)

    def clear(self):
        self.grid.clear()

    def add(self, agent: Agent):
        cell_coords = self._get_cell_coords(agent.x, agent.y)
        if cell_coords not in self.grid:
            self.grid[cell_coords] = []
        self.grid[cell_coords].append(agent)

    def get_nearby(self, x: float, y: float, radius: float) -> List[Agent]:
        """
        Get agents from the cell containing (x, y) and its neighbors.
        Note: This returns a superset of agents within radius. 
        Precise distance checks should still be performed on this result.
        """
        center_cell_x, center_cell_y = self._get_cell_coords(x, y)
        # Check 3x3 grid of cells around the agent
        # Radius might span multiple cells if it's large, but we assume radius <= cell_size for efficiency
        # If radius > cell_size, we might need to check more cells. 
        # For now, we assume cell_size (50) is > max sensing radius (usually ~5-20).
        
        nearby_agents = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell_coords = (center_cell_x + dx, center_cell_y + dy)
                if cell_coords in self.grid:
                    nearby_agents.extend(self.grid[cell_coords])
                    
        return nearby_agents
