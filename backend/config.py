# Simulation Configuration

# Dimensions
SIMULATION_WIDTH = 1000
SIMULATION_HEIGHT = 800

# Time
TICK_RATE = 10  # Ticks per second (target)

# Environment Defaults
DEFAULT_TEMPERATURE = 25.0  # Celsius
DEFAULT_HUMIDITY = 60.0     # Percentage
DEFAULT_LIGHT_LEVEL = 0.8   # 0.0 to 1.0

# Agent Parameters
ANIMAL_SPEED = 2.0
ANIMAL_HUNGER_RATE = 0.1
ANIMAL_ENERGY_LOSS_RATE = 0.05
PLANT_GROWTH_RATE = 0.1

# Day/Night Cycle
DAY_DURATION_TICKS = 600 # 60 seconds at 10 ticks/s
MIN_LIGHT_LEVEL = 0.1
MAX_LIGHT_LEVEL = 1.0

# Terrain
TERRAIN_GRID_SIZE = 40 # Pixels per cell
TERRAIN_WATER = 0
TERRAIN_SOIL = 1
TERRAIN_ROCK = 2
