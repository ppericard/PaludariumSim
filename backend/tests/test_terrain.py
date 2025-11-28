import pytest
from simulation import Environment
import config

def test_terrain_initialization():
    env = Environment(width=100, height=100)
    # With grid size 40, we expect 2x2 grid (100//40 = 2)
    # Wait, 100 // 40 = 2.
    
    # Let's use standard size to test default generation
    env = Environment()
    
    assert len(env.terrain) == env.grid_height
    assert len(env.terrain[0]) == env.grid_width
    
    # Test Shoreline layout
    # Left 40% should be Water (0)
    # Right 60% should be Soil (1)
    
    water_limit = int(env.grid_width * 0.4)
    
    # Check a row
    row = env.terrain[10]
    assert row[0] == config.TERRAIN_WATER
    assert row[water_limit - 1] == config.TERRAIN_WATER
    assert row[water_limit] == config.TERRAIN_SOIL
    assert row[-1] == config.TERRAIN_SOIL
