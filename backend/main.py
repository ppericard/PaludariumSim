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
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error processing message: {e}")

            # Run simulation step
            env.update()
            
            # Get state and send to client
            state = env.get_state()
            await websocket.send_text(json.dumps(state))
            
            # Control tick rate (e.g., 10 ticks per second)
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
