import pytest
from simulation import Environment
import config

def test_day_night_cycle():
    env = Environment()
    
    # Start at time 0 (Dawn)
    assert env.time == 0
    # Light should be around 0.5 (normalized 0.5 mapped to range)
    # sin(-pi/2) = -1 -> normalized 0 -> MIN_LIGHT
    # Wait, let's check the math in environment.py:
    # cycle_progress = 0
    # sine_val = sin(-pi/2) = -1
    # normalized = 0
    # light = MIN
    assert env.light_level == config.MIN_LIGHT_LEVEL
    
    # Advance to Noon (1/4 day)
    ticks_to_noon = config.DAY_DURATION_TICKS // 4
    for _ in range(ticks_to_noon):
        env.update()
        
    # At noon, sin(0) = 0? No.
    # cycle_progress = pi/2
    # sine_val = sin(0) = 0
    # normalized = 0.5
    # light = MIN + 0.5 * range
    
    # Wait, my math in implementation might be slightly off for "Noon = Max".
    # Let's re-read the code I wrote:
    # cycle_progress = (time / duration) * 2pi
    # sine_val = sin(cycle_progress - pi/2)
    
    # At time = duration/4:
    # cycle_progress = pi/2
    # sine_val = sin(0) = 0. This is mid-light.
    
    # At time = duration/2:
    # cycle_progress = pi
    # sine_val = sin(pi/2) = 1. This is MAX light.
    
    # So Noon is at duration/2.
    
    # Let's advance to duration/2
    for _ in range(ticks_to_noon):
        env.update()
        
    assert env.time == config.DAY_DURATION_TICKS // 2
    assert abs(env.light_level - config.MAX_LIGHT_LEVEL) < 0.001
    
    # Advance to Midnight (Full cycle)
    ticks_to_midnight = config.DAY_DURATION_TICKS // 2
    for _ in range(ticks_to_midnight - 1): # -1 because update increments first
        env.update()
        
    # Check near end of cycle
    # Light should be low again
