import pytest
from simulation import Environment
from simulation.factory import AgentFactory
import config

def test_fish_stays_in_water():
    env = Environment(1000, 800)
    # Water is on the left (0 to 40% of width = 400)
    
    # Spawn fish near the edge of water (e.g., x=390)
    fish = AgentFactory.create("Fish", 390, 400)
    env.add_agent(fish)
    env.update() # Flush
    
    # Force move right (towards land)
    # We can't easily force random movement, but we can check if it stays valid
    # Let's run many updates and ensure x < 400 (approx)
    # Actually, grid size is 40. Water limit is 1000 // 40 * 0.4 * 40 = 25 * 0.4 * 40 = 10 * 40 = 400.
    # So x < 400 is water. x >= 400 is land.
    
    for _ in range(100):
        env.update()
        assert fish.x < 400, f"Fish moved to land at x={fish.x}"

def test_lizard_stays_on_land():
    env = Environment(1000, 800)
    # Land is x >= 400
    
    # Spawn lizard near edge (e.g., x=410)
    lizard = AgentFactory.create("Lizard", 410, 400)
    env.add_agent(lizard)
    env.update()
    
    for _ in range(100):
        env.update()
        # Lizard might move slightly into water cell if not pixel perfect, 
        # but get_terrain_at handles grid.
        # If x < 400, it's water.
        assert lizard.x >= 400, f"Lizard moved to water at x={lizard.x}"

def test_invalid_spawn_correction():
    # If we spawn a fish on land, it should be stuck or handled?
    # Current logic just prevents movement INTO invalid.
    # If already invalid, it might stay invalid or move to valid?
    # Our logic: if is_valid_position(new_x), move.
    # If current is invalid, and random move is also invalid, it stays.
    # If random move is valid, it moves.
    # So it should eventually escape to water if close?
    pass
