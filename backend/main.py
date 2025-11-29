from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import random
import config
import time
from logger import setup_logger

from simulation.runner import SimulationRunner
from simulation.factory import AgentFactory

# Setup Logger
logger = setup_logger("Main")

app = FastAPI()

# Initialize SimulationRunner
runner = SimulationRunner()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Simulation Runner...")
    runner.start()
    # Populate default agents if empty
    if not runner.environment.agents:
        runner.environment._populate_default_agents()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stopping Simulation Runner...")
    runner.stop()

@app.get("/")
async def root():
    return {"message": "Paludarium Simulation API"}

@app.get("/api/stats")
async def get_stats():
    return {"agent_count": len(runner.environment.agents)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_info = f"{websocket.client.host}:{websocket.client.port}"
    logger.info(f"Client connected: {client_info}")
    
    last_heartbeat = time.time()
    HEARTBEAT_INTERVAL = 5.0
    
    # Reader Task Function
    async def listen_for_messages():
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "pong":
                    pass 
                    
                elif message.get("type") == "spawn":
                    agent_type = message["payload"]["agent_type"]
                    species_map = {
                        "plant": "Fern",
                        "animal": "Frog",
                        "Fish": "Fish",
                        "Lizard": "Lizard"
                    }
                    species = species_map.get(agent_type, "Fern")
                    new_agent = AgentFactory.create(
                        species, 
                        random.randint(0, config.SIMULATION_WIDTH), 
                        random.randint(0, config.SIMULATION_HEIGHT)
                    )
                    if new_agent:
                        runner.environment.add_agent(new_agent)
                        logger.info(f"Spawned {species} via WebSocket")
                        
                elif message.get("type") == "set_speed":
                    new_speed = message["payload"]["speed"]
                    runner.set_speed(new_speed)
                    
                elif message.get("type") == "set_light_mode":
                    mode = message["payload"]["mode"]
                    if mode in ["cycle", "always_on"]:
                        runner.environment.equipment["lights"].mode = mode
                        logger.info(f"Light mode set to {mode}")
                        
                elif message.get("type") == "spawn_batch":
                    agent_type = message["payload"]["type"]
                    count = message["payload"]["count"]
                    species_map = {
                        "plant": "Fern",
                        "animal": "Frog",
                        "Fish": "Fish",
                        "Lizard": "Lizard"
                    }
                    species = species_map.get(agent_type, "Fern")
                    logger.info(f"Spawning batch of {count} {species}s")
                    for _ in range(count):
                        new_agent = AgentFactory.create(
                            species,
                            random.randint(0, config.SIMULATION_WIDTH),
                            random.randint(0, config.SIMULATION_HEIGHT)
                        )
                        if new_agent:
                            runner.environment.add_agent(new_agent)
                            
                elif message.get("type") == "save_state":
                    filename = message["payload"].get("filename", "save1")
                    logger.info(f"Saving state to {filename}")
                    runner.environment.save_to_file(filename)
                    
                elif message.get("type") == "load_state":
                    filename = message["payload"].get("filename", "save1")
                    logger.info(f"Loading state from {filename}")
                    runner.environment.load_from_file(filename)
                    
                elif message.get("type") == "reset":
                    logger.info("Resetting simulation")
                    runner.environment.reset()
                    
        except Exception as e:
            if "disconnect" not in str(e).lower() and "closed" not in str(e).lower():
                logger.error(f"Reader error: {e}")

    # Start Reader Task
    reader_task = asyncio.create_task(listen_for_messages())

    try:
        while True:
            # Check if reader is done (connection closed)
            if reader_task.done():
                break

            # Send Heartbeat
            if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                try:
                    await websocket.send_text(json.dumps({"type": "heartbeat", "timestamp": time.time()}))
                    last_heartbeat = time.time()
                except Exception:
                    break

            # Broadcast State
            try:
                state = runner.get_state()
                await websocket.send_text(json.dumps(state))
            except Exception as e:
                if "disconnect" in str(e).lower() or "closed" in str(e).lower():
                    break
                logger.error(f"Broadcast error: {e}")
                await asyncio.sleep(1.0)
                
            # Throttle broadcast rate (e.g., 10Hz or 20Hz independent of simulation TPS)
            await asyncio.sleep(0.05) # 20 FPS broadcast

    except Exception as e:
        logger.info(f"Client disconnected: {client_info} ({e})")
    finally:
        reader_task.cancel()
        logger.info(f"Connection handler finished for {client_info}")

