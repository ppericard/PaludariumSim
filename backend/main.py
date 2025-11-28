from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

from simulation import Environment, Agent

app = FastAPI()

# Initialize simulation environment
env = Environment(width=100, height=100)

# Add a test agent
test_agent = Agent(x=50, y=50, agent_type="organism")
test_agent.state = {"name": "Test Blob", "color": "#00ff00"}
env.add_agent(test_agent)

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
            # Run simulation step
            env.update()
            
            # Get state and send to client
            state = env.get_state()
            await websocket.send_text(json.dumps(state))
            
            # Control tick rate (e.g., 10 ticks per second)
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
