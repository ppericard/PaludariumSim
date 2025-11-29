import requests
import time
import math

def verify_sensing():
    # 1. Clear simulation (or just restart backend, but we'll assume fresh start or just spawn new)
    # Ideally we'd have a "clear" endpoint, but for now let's just spawn a specific test case.
    
    # We can't easily clear, so we'll rely on spawning far away from others or just checking logic.
    # Better approach: Unit test style by importing classes directly, 
    # BUT we need to test the running system.
    
    # Let's try to spawn an animal and a plant at specific coordinates via WebSocket?
    # The current HTTP API doesn't support spawning specific agents at specific coords.
    # The WebSocket does.
    
    # Actually, let's just write a unit test that imports the backend modules.
    # This avoids the complexity of async websocket testing for now.
    
    try:
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        
        from simulation.environment import Environment
        from simulation.animals import Animal
        from simulation.plants import Plant
        import config
        
        print("Initializing Environment...")
        env = Environment(width=1000, height=1000)
        
        # Setup: Animal at (100, 100), Plant at (150, 100). Distance = 50.
        # Vision radius is 100. Animal should see Plant.
        animal = Animal(100, 100, "TestAnimal")
        animal.state["hunger"] = 50.0 # Make it hungry
        env.add_agent(animal)
        
        plant = Plant(150, 100, "TestPlant")
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
