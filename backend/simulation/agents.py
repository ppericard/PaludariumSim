from typing import Tuple, Dict, Any, List
import uuid

class Agent:
    """
    Generic Agent container.
    Behavior is defined by attached Components.
    """
    def __init__(self, x: int, y: int, species: str):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.alive = True
        self.components: List['Component'] = []
        
        # Generic state dictionary
        self.state: Dict[str, Any] = {
            "species": species,
            "color": "#ffffff", # Default
            "size": 5.0
        }

    def add_component(self, component: 'Component'):
        self.components.append(component)

    def get_component(self, component_type: type):
        for c in self.components:
            if isinstance(c, component_type):
                return c
        return None

    def update(self, environment: 'Environment'):
        """
        Update all components.
        """
        for component in self.components:
            component.update(environment)

    def to_dict(self):
        # Base dict
        data = {
            "id": self.id,
            "type": self.state.get("visual_tag", "unknown"), # For frontend compatibility
            "position": {"x": self.x, "y": self.y},
            "state": self.state.copy(),
            "components": [c.__class__.__name__ for c in self.components]
        }
        return data
