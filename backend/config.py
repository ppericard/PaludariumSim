# Simulation Configuration

# Dimensions
SIMULATION_WIDTH = 1000
SIMULATION_HEIGHT = 800

# Time
TICK_RATE = 5  # Ticks per second (target)

# Environment Defaults
DEFAULT_TEMPERATURE = 25.0  # Celsius
DEFAULT_HUMIDITY = 60.0     # Percentage
DEFAULT_LIGHT_LEVEL = 0.8   # 0.0 to 1.0

# Agent Parameters
HABITAT_AQUATIC = "aquatic"
HABITAT_TERRESTRIAL = "terrestrial"
HABITAT_AMPHIBIOUS = "amphibious"

ANIMAL_SPEED = 2.0
ANIMAL_HUNGER_RATE = 0.1
ANIMAL_ENERGY_LOSS_RATE = 0.05
BASE_GROWTH_RATE = 0.02

# Day/Night Cycle
DAY_DURATION_TICKS = 600 # 60 seconds at 10 ticks/s
MIN_LIGHT_LEVEL = 0.1
MAX_LIGHT_LEVEL = 1.0

# Light Cycle Phases (0.0 to 1.0 of DAY_DURATION_TICKS)
PHASE_DAWN_START = 0.1  # 10%
PHASE_DAY_START = 0.2   # 20%
PHASE_DUSK_START = 0.8  # 80%
PHASE_NIGHT_START = 0.9 # 90%

# Terrain
TERRAIN_GRID_SIZE = 40 # Pixels per cell
TERRAIN_WATER = 0
TERRAIN_SOIL = 1
TERRAIN_ROCK = 2

# Density Control
MAX_NEIGHBORS = 4      # Max neighbors before reproduction stops
NEIGHBOR_RADIUS = 30   # Radius to check for neighbors (pixels)
MIN_SPAWN_DISTANCE = 15 # Min distance for new offspring
# Logging
LOG_LEVEL = "INFO" # DEBUG, INFO, WARNING, ERROR
