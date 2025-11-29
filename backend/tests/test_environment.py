import pytest
from simulation import Environment
from simulation.factory import AgentFactory
import config

def test_environment_initialization():
    env = Environment(100, 100)
    assert env.width == 100
    assert env.height == 100
    assert len(env.agents) == 0
    assert env.time == 0
    assert env.total_ticks == 0

def test_add_remove_agent():
    env = Environment(100, 100)
    agent = AgentFactory.create("Fern", 50, 50)
    
    env.add_agent(agent)
    # Agents are added in update() from new_agents buffer
    assert len(env.agents) == 0
    assert len(env.new_agents) == 1
    
    env.update()
    assert len(env.agents) == 1
    assert len(env.new_agents) == 0
    
    env.remove_agent(agent.id)
    # Agents are removed in update() from dead_agents buffer
    assert len(env.agents) == 1 # Still there until update
    assert len(env.dead_agents) == 1
    
    env.update()
    assert len(env.agents) == 0
    assert len(env.dead_agents) == 0

def test_reset():
    env = Environment(100, 100)
    agent = AgentFactory.create("Fern", 50, 50)
    env.add_agent(agent)
    env.update()
    
    assert len(env.agents) == 1
    
    env.reset()
    assert len(env.agents) == 0
    assert env.total_ticks == 0
    assert env.time == 0
    assert len(env.stats_history) == 0

def test_stats_history_limit():
    env = Environment(100, 100)
    # Mock stats history limit to small number for testing if possible, 
    # or just fill it up (might be slow).
    # Instead, we can manually append to stats_history and call update to trigger the check.
    
    # Fill with 10001 items
    env.stats_history = [{"time": i} for i in range(10001)]
    
    # Force update to trigger stats recording (every 10 ticks)
    env.time = 9 # Next tick will be 10
    env.update()
    
    # Should be capped at 10000 (popped one, added one -> wait, logic is > 10000 pop. 
    # If we have 10001, add 1 -> 10002, pop 1 -> 10001. 
    # The logic in environment.py is:
    # self.stats_history.append(current_stats)
    # if len(self.stats_history) > 10000: self.stats_history.pop(0)
    # So it maintains max 10000.
    
    # Let's re-verify logic:
    # If I have 10000 items. Append 1 -> 10001. Pop 1 -> 10000. Correct.
    
    # So if we start with 10000 items.
    env.stats_history = [{"time": i} for i in range(10000)]
    env.time = 9
    env.update()
    
    assert len(env.stats_history) == 10000
    assert env.stats_history[-1]["time"] == env.total_ticks
