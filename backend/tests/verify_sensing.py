import requests
import time
import math

def verify_sensing():
    try:
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        
        from simulation.environment import Environment
        from simulation.factory import AgentFactory
        import config
        
        print("Initializing Environment...")
        env = Environment(width=1000, height=1000)
        
        # Setup: Animal at (100, 100), Plant at (150, 100). Distance = 50.
        # Vision radius is 100. Animal should see Plant.
        animal = AgentFactory.create("Frog", 100, 100) # Use Frog as generic animal
        animal.state["hunger"] = 50.0 # Make it hungry
        env.add_agent(animal)
        
        plant = AgentFactory.create("Fern", 150, 100)
        env.add_agent(plant)
        
        # Force update to populate grid
        env.update()
        
        print(f"Initial Animal Pos: ({animal.x}, {animal.y})")
        print(f"Plant Pos: ({plant.x}, {plant.y})")
        
        # Step simulation
        print("Stepping simulation...")
        env.update()
        
        print(f"New Animal Pos: ({animal.x}, {animal.y})")
        
        # Check if moved towards plant (x should increase)
        if animal.x > 100:
            print("SUCCESS: Animal moved towards plant.")
            return True
        else:
            print("FAILURE: Animal did not move towards plant.")
            return False
            
    except Exception as e:
        print(f"FAILURE: Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if verify_sensing():
        import sys
        sys.exit(0)
    else:
        import sys
        sys.exit(1)
