import pytest
from simulation import Environment, Plant, Animal
import config

def test_stats_calculation():
    env = Environment()
    
    # Initially 0 agents
    state = env.get_state()
    assert state["environment"]["stats"]["plant"] == 0
    assert state["environment"]["stats"]["animal"] == 0
    
    # Add agents
    env.add_agent(Plant(0, 0, "Fern"))
    env.add_agent(Plant(10, 10, "Fern"))
    env.add_agent(Animal(20, 20, "Frog"))
    
    env.update() # Flush buffers
    
    state = env.get_state()
    assert state["environment"]["stats"]["plant"] == 2
    assert state["environment"]["stats"]["animal"] == 1
    
    # Kill an agent
    env.agents[0].alive = False
    
    state = env.get_state()
    # Stats should reflect alive agents only
    assert state["environment"]["stats"]["plant"] == 1
    assert state["environment"]["stats"]["animal"] == 1
