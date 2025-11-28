from typing import Tuple, Dict, Any
import uuid

class Agent:
    def __init__(self, x: int, y: int, agent_type: str):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.agent_type = agent_type  # 'organism', 'equipment', 'environment_modifier'
        self.alive = True
        self.state: Dict[str, Any] = {}

    def update(self, environment: 'Environment'):
        """
        Update agent state based on environment and internal logic.
        Must be implemented by subclasses.
        """
        pass

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.agent_type,
            "position": {"x": self.x, "y": self.y},
            "state": self.state
        }
