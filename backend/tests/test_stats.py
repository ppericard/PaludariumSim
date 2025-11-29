import pytest
from simulation import Environment
from simulation.factory import AgentFactory
import config

def test_stats_calculation():
    env = Environment()
    
    # Initially 0 agents
    state = env.get_state()
    # Stats should be empty or have 0 for known species if initialized, 
    # but our logic builds it dynamically from agents.
    # So it should be empty or contain only keys for present agents.
    # Let's check if it's empty or 0.
    stats = state["environment"]["stats"]
    assert len(stats) == 0 or all(v == 0 for v in stats.values())
    
    # Add agents
    env.add_agent(AgentFactory.create("Fern", 0, 0))
    env.add_agent(AgentFactory.create("Fern", 10, 10))
    env.add_agent(AgentFactory.create("Frog", 20, 20))
    
    env.update() # Flush buffers
    
    state = env.get_state()
    stats = state["environment"]["stats"]
    assert stats["Fern"] == 2
    assert stats["Frog"] == 1
    
    # Kill an agent
    env.agents[0].alive = False
    
    state = env.get_state()
    stats = state["environment"]["stats"]
    # Stats should reflect alive agents only
    # Note: agents[0] is the first Fern
    assert stats["Fern"] == 1
    assert stats["Frog"] == 1
