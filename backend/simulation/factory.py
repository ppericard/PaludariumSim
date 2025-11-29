from typing import Optional
from .agents import Agent
from .species_config import SPECIES_DB
from logger import setup_logger

logger = setup_logger("Factory")

class AgentFactory:
    @staticmethod
    def create(species_name: str, x: float, y: float) -> Optional[Agent]:
        """
        Creates an agent of the given species at (x, y).
        """
        if species_name not in SPECIES_DB:
            logger.warning(f"Unknown species: {species_name}")
            return None
            
        config = SPECIES_DB[species_name]
        
        # Create base agent
        agent = Agent(x, y, species_name)
        
        # Initialize state from params
        agent.state.update(config["params"])
        
        # Add components
        for component_cls, kwargs in config["components"]:
            agent.add_component(component_cls(agent, **kwargs))
            
        return agent
