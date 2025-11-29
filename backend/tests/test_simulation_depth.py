import pytest
from simulation import Environment
from simulation.factory import AgentFactory
from unittest.mock import patch

def test_animal_eating():
    env = Environment(100, 100)
    plant = AgentFactory.create("Fern", 50, 50)
    animal = AgentFactory.create("Frog", 50, 50)
    
    # Set initial state
    animal.state["hunger"] = 50.0
    animal.state["energy"] = 50.0
    
    env.add_agent(plant)
    env.add_agent(animal)
    
    # Flush buffers
    env.update()
    
    # Run update for interaction
    env.update()
    
    # Check results
    assert not plant.alive
    assert len(env.agents) == 1
    assert env.agents[0].id == animal.id
    
    # Check animal state
    assert animal.state["hunger"] < 50.0 # Hunger decreased
    assert animal.state["energy"] > 50.0 # Energy increased

def test_animal_death():
    env = Environment(100, 100)
    animal = AgentFactory.create("Frog", 50, 50)
    
    # Set fatal state
    animal.state["hunger"] = 100.0
    
    env.add_agent(animal)
    env.update() # Flush buffer
    env.update() # Run logic
    
    assert not animal.alive
    assert len(env.agents) == 0

def test_animal_reproduction():
    import simulation.factory
    env = Environment(100, 100)
    animal = simulation.factory.AgentFactory.create("Frog", 50, 50)
    
    # Set fertile state
    animal.state["energy"] = 90.0
    animal.state["hunger"] = 10.0
    
    env.add_agent(animal)
    env.update() # Flush buffer
    
    # Mock random to return 0.0 (always reproduce)
    with patch('random.random', return_value=0.0):
        env.update()
        
    assert len(env.agents) == 2
    # Check energy cost (40.0) + tick cost (approx 0.05)
    assert animal.state["energy"] < 90.0 - 40.0

def test_plant_reproduction():
    from simulation.factory import AgentFactory
    env = Environment(100, 100)
    plant = AgentFactory.create("Fern", 50, 50)
    plant.state["size"] = plant.state["max_size"] # Mature
    plant.state["energy"] = 100.0 # Full energy
    
    env.add_agent(plant)
    env.update() # Flush buffer
    
    # Mock random to return 0.0 (always reproduce)
    with patch('random.random', return_value=0.0):
        env.update()
        
    assert len(env.agents) == 2
