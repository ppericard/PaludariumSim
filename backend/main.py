from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random
import config

from simulation import Environment, Agent, Plant, Animal

app = FastAPI()

# Initialize simulation environment
env = Environment() # Uses defaults from config
env.light_level = config.DEFAULT_LIGHT_LEVEL
target_tps = 10 # Default ticks per second

# Add a test plant
plant = Plant(x=500, y=400, species="Fern")
env.add_agent(plant)

# Add a test animal
frog = Animal(x=550, y=450, species="Dart Frog")
env.add_agent(frog)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Paludarium Simulation API"}

@app.get("/history")
async def get_history():
    return env.stats_history

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global target_tps
    await websocket.accept()
    try:
        while True:
            # Check for incoming messages (non-blocking)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                message = json.loads(data)
                if message.get("type") == "spawn":
                    agent_type = message["payload"]["agent_type"]
                    if agent_type == "plant":
                        new_agent = Plant(x=random.randint(0, config.SIMULATION_WIDTH), y=random.randint(0, config.SIMULATION_HEIGHT), species="Fern")
                    elif agent_type == "animal":
                        new_agent = Animal(x=random.randint(0, config.SIMULATION_WIDTH), y=random.randint(0, config.SIMULATION_HEIGHT), species="Frog")
                    else:
                        continue
                    env.add_agent(new_agent)
                elif message.get("type") == "set_speed":
                    # Update target TPS
                    new_speed = message["payload"]["speed"]
                    # Speed 0 means pause (handled in loop)
                    target_tps = float(new_speed)
                    print(f"Speed set to {target_tps} TPS")
                elif message.get("type") == "set_light_mode":
                    mode = message["payload"]["mode"]
                    if mode in ["cycle", "always_on"]:
                        env.equipment["lights"].mode = mode
                        print(f"Light mode set to {mode}")
                elif message.get("type") == "spawn_batch":
                    agent_type = message["payload"]["type"]
                    count = message["payload"]["count"]
                    print(f"Spawning batch of {count} {agent_type}s")
                    for _ in range(count):
                        if agent_type == "plant":
                            new_agent = Plant(x=random.randint(0, config.SIMULATION_WIDTH), y=random.randint(0, config.SIMULATION_HEIGHT), species="Fern")
                        elif agent_type == "animal":
                            new_agent = Animal(x=random.randint(0, config.SIMULATION_WIDTH), y=random.randint(0, config.SIMULATION_HEIGHT), species="Frog")
                        else:
                            continue
                        env.add_agent(new_agent)
                elif message.get("type") == "save_state":
                    filename = message["payload"].get("filename", "save1")
                    print(f"Saving state to {filename}")
                    env.save_to_file(filename)
                elif message.get("type") == "load_state":
                    filename = message["payload"].get("filename", "save1")
                    print(f"Loading state from {filename}")
                    env.load_from_file(filename)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error processing message: {e}")

            # Run simulation step if not paused
            if target_tps > 0:
                env.update()
            
            # Get state and send to client
            state = env.get_state()
            await websocket.send_text(json.dumps(state))
            
            # Control tick rate
            if target_tps > 0:
                # Calculate sleep time based on target TPS
                sleep_time = 1.0 / target_tps
                await asyncio.sleep(sleep_time)
            else:
                # Paused: wait a bit to avoid CPU spin
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
