import sys
import os

def verify_species():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        
        from simulation.environment import Environment
        from simulation.animals import Animal
        import config
        
        print("Initializing Environment...")
        env = Environment(width=1000, height=1000)
        
        # Terrain: Left 40% Water, Right 60% Soil
        water_x = 100
        land_x = 800
        
        print("Testing Aquatic Species (Fish)...")
        fish = Animal(land_x, 500, "TestFish", habitat=config.HABITAT_AQUATIC)
        env.add_agent(fish)
        
        # Step simulation (1st tick adds agent, 2nd tick updates it)
        env.update()
        env.update()
        
        # Fish on land should lose energy fast (5.0 * 0.05 = 0.25 per tick)
        # Normal loss is 0.05
        # Let's check if energy is significantly lower than 100 - 0.05
        
        expected_energy = 100.0 - (config.ANIMAL_ENERGY_LOSS_RATE * 5.0)
        print(f"Fish Energy on Land: {fish.state['energy']} (Expected <= {expected_energy})")
        
        if fish.state["energy"] > expected_energy + 0.01:
            print("FAILURE: Fish did not lose extra energy on land.")
            return False
            
        print("Testing Terrestrial Species (Lizard)...")
        lizard = Animal(water_x, 500, "TestLizard", habitat=config.HABITAT_TERRESTRIAL)
        env.add_agent(lizard)
        
        env.update()
        env.update()
        
        expected_energy_lizard = 100.0 - (config.ANIMAL_ENERGY_LOSS_RATE * 5.0)
        print(f"Lizard Energy in Water: {lizard.state['energy']} (Expected <= {expected_energy_lizard})")
        
        if lizard.state["energy"] > expected_energy_lizard + 0.01:
            print("FAILURE: Lizard did not lose extra energy in water.")
            return False

        print("SUCCESS: Species constraints verified.")
        return True

    except Exception as e:
        print(f"FAILURE: Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if verify_species():
        sys.exit(0)
    else:
        sys.exit(1)
