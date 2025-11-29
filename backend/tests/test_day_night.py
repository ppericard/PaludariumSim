import pytest
from simulation import Environment
import config

def test_day_night_cycle():
    env = Environment()
    # Set mode to cycle for testing
    env.equipment["lights"].mode = "cycle"
    
    # Initial state (Time 0) -> Night (Early)
    # Progress 0.0 < 0.1 (DAWN_START) -> MIN_LIGHT_LEVEL
    env.equipment["lights"].update(env)
    assert env.light_level == config.MIN_LIGHT_LEVEL
    
    # Advance to Dawn (Progress 0.15)
    # 0.15 is halfway between 0.1 and 0.2 -> 50% light
    env.time = int(config.DAY_DURATION_TICKS * 0.15)
    env.equipment["lights"].update(env)
    expected_light = config.MIN_LIGHT_LEVEL + 0.5 * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
    assert abs(env.light_level - expected_light) < 0.01
    
    # Advance to Day (Progress 0.5)
    # 0.2 < 0.5 < 0.8 -> MAX_LIGHT_LEVEL
    env.time = int(config.DAY_DURATION_TICKS * 0.5)
    env.equipment["lights"].update(env)
    assert env.light_level == config.MAX_LIGHT_LEVEL
    
    # Advance to Dusk (Progress 0.85)
    # 0.85 is halfway between 0.8 and 0.9 -> 50% light
    env.time = int(config.DAY_DURATION_TICKS * 0.85)
    env.equipment["lights"].update(env)
    expected_light = config.MAX_LIGHT_LEVEL - 0.5 * (config.MAX_LIGHT_LEVEL - config.MIN_LIGHT_LEVEL)
    assert abs(env.light_level - expected_light) < 0.01
    
    # Advance to Night (Late) (Progress 0.95)
    # 0.95 > 0.9 -> MIN_LIGHT_LEVEL
    env.time = int(config.DAY_DURATION_TICKS * 0.95)
    env.equipment["lights"].update(env)
    assert env.light_level == config.MIN_LIGHT_LEVEL
