
from .components import (
    StaticMovement, RandomMovement, TargetedMovement, Growth,
    Photosynthesis, Heterotrophy,
    AsexualReproduction, SexualReproduction
)
import config

# Species Configuration Database
# Defines components and initial parameters for each species.

SPECIES_DB = {
    "Fern": {
        "visual_tag": "plant",
        "components": [
            (StaticMovement, {"speed": 0.0}),
            (Growth, {"growth_rate": 0.01, "max_size": 15.0}),
            (Photosynthesis, {"growth_rate": config.BASE_GROWTH_RATE, "energy": 10.0}),
            (AsexualReproduction, {"cost": 30.0, "threshold": 60.0})
        ],
        "params": {
            "color": "#2ecc71",
            "max_size": 15.0,
            "size": 5.0
        }
    },
    "Frog": {
        "visual_tag": "animal",
        "components": [
            (TargetedMovement, {
                "speed": config.ANIMAL_SPEED,
                "target_criteria": {"has_component": ["Photosynthesis"]}
            }),
            (Growth, {"growth_rate": 0.005, "max_size": 10.0}),
            (Heterotrophy, {"decay_rate": config.ANIMAL_ENERGY_LOSS_RATE, "energy": 80.0}),
            (SexualReproduction, {"cost": 40.0, "threshold": 80.0})
        ],
        "params": {
            "color": "#e74c3c",
            "vision_radius": 100.0,
            "habitat": config.HABITAT_AMPHIBIOUS,
            "size": 4.0
        }
    },
    "Fish": {
        "visual_tag": "animal",
        "components": [
            (TargetedMovement, {
                "speed": config.ANIMAL_SPEED * 1.2,
                "target_criteria": {"has_component": ["Photosynthesis"]}
            }), 
            (Growth, {"growth_rate": 0.005, "max_size": 8.0}),
            (Heterotrophy, {"decay_rate": config.ANIMAL_ENERGY_LOSS_RATE, "energy": 60.0}),
            (SexualReproduction, {"cost": 40.0, "threshold": 80.0})
        ],
        "params": {
            "color": "#f39c12",
            "vision_radius": 80.0,
            "habitat": config.HABITAT_AQUATIC,
            "size": 3.0
        }
    },
    "Lizard": {
        "visual_tag": "animal",
        "components": [
            (TargetedMovement, {
                "speed": config.ANIMAL_SPEED,
                "target_criteria": {"has_component": ["Photosynthesis"]}
            }),
            (Growth, {"growth_rate": 0.005, "max_size": 8.0}),
            (Heterotrophy, {"decay_rate": config.ANIMAL_ENERGY_LOSS_RATE, "energy": 60.0}),
            (SexualReproduction, {"cost": 40.0, "threshold": 80.0})
        ],
        "params": {
            "color": "#8e44ad",
            "vision_radius": 60.0,
            "habitat": config.HABITAT_TERRESTRIAL,
            "size": 3.0
        }
    }
}
