from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random

from simulation import Environment, Agent, Plant, Animal

app = FastAPI()

# Initialize simulation environment
env = Environment(width=100, height=100)
env.light_level = 0.8  # Simulate bright light

# Add a test plant
plant = Plant(x=30, y=70, species="Fern")
env.add_agent(plant)

# Add a test animal
frog = Animal(x=50, y=50, species="Dart Frog")
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
                        new_agent = Plant(x=random.randint(0, 100), y=random.randint(0, 100), species="Fern")
                    elif agent_type == "animal":
                        new_agent = Animal(x=random.randint(0, 100), y=random.randint(0, 100), species="Frog")
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
