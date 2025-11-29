import pytest
from simulation import Environment
from simulation.factory import AgentFactory
from simulation.components import AsexualReproduction
import config
from unittest.mock import patch

def test_density_control():
    env = Environment(1000, 800)
    
    # Create a central agent (using Fern as it has AsexualReproduction)
    center_agent = AgentFactory.create("Fern", 500, 400)
    center_agent.state["size"] = 20.0 
    center_agent.state["energy"] = 100.0 # Full energy
    env.add_agent(center_agent)
    
    # Surround it with MAX_NEIGHBORS agents of the same species
    # Radius is NEIGHBOR_RADIUS (30). Place them close (dist 10).
    for i in range(config.MAX_NEIGHBORS):
        neighbor = AgentFactory.create("Fern", 500 + 10, 400)
        env.add_agent(neighbor)
        
    env.update() # Flush new_agents to self.agents
    env.update() # Rebuild spatial grid with new agents
    
    # Verify neighbors count
    neighbors = env.get_nearby_agents(center_agent, config.NEIGHBOR_RADIUS)
    same_species = [n for n in neighbors if n.state.get("species") == center_agent.state.get("species")]
    assert len(same_species) == config.MAX_NEIGHBORS
    
    # Try to reproduce - should fail due to density
    initial_count = len(env.agents)
    
    # Mock random to ensure it tries to reproduce (chance is 0.01)
    with patch('random.random', return_value=0.0):
        env.update()
        
    # Should NOT have spawned a new agent
    assert len(env.agents) == initial_count
    # Energy should NOT have decreased (cost is 30)
    assert center_agent.state["energy"] == 100.0

def test_reproduction_success_when_uncrowded():
    env = Environment(1000, 800)
    center_agent = AgentFactory.create("Fern", 500, 400)
    center_agent.state["energy"] = 100.0
    env.add_agent(center_agent)
    env.update()
    
    initial_count = len(env.agents)
    
    # Mock random to ensure reproduction
    with patch('random.random', return_value=0.0):
        env.update()
        
    # Should have spawned
    assert len(env.agents) == initial_count + 1
    # Energy should have decreased
    assert center_agent.state["energy"] < 100.0
