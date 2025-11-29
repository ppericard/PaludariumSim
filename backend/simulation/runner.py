import asyncio
import time
import logging
from typing import Optional, Dict, Any
from .environment import Environment
import config

logger = logging.getLogger("SimulationRunner")

class SimulationRunner:
    """
    Manages the main simulation loop in a separate asyncio Task.

    This class decouples the simulation logic from the WebSocket connection,
    ensuring the simulation continues running even if clients disconnect.
    It handles the tick rate (TPS) and synchronization.

    Attributes:
        environment (Environment): The simulation environment instance.
        target_tps (float): The target ticks per second.
        actual_tps (float): The measured ticks per second.
        is_running (bool): Whether the simulation loop is active.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationRunner, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.environment = Environment()
        self.target_tps = 10.0
        self.actual_tps = 0.0
        self.is_running = False
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    def start(self):
        """
        Start the simulation loop if not already running.
        
        Creates a new asyncio Task for the loop.
        """
        if self._task is None or self._task.done():
            self._stop_event.clear()
            self.is_running = True
            self._task = asyncio.create_task(self._loop())
            logger.info("Simulation loop started.")

    def stop(self):
        """
        Stop the simulation loop.
        
        Signals the loop to exit and cancels the task.
        """
        self.is_running = False
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            logger.info("Simulation loop stopped.")

    async def _loop(self):
        """
        The main simulation loop.
        
        Updates the environment and sleeps to maintain the target TPS.
        Calculates the actual TPS for telemetry.
        """
        logger.info("Entering simulation loop.")
        try:
            while not self._stop_event.is_set():
                loop_start = time.perf_counter()

                if self.target_tps > 0:
                    # Update environment
                    try:
                        self.environment.update()
                    except Exception as e:
                        logger.error(f"Error in simulation update: {e}")
                        import traceback
                        logger.error(traceback.format_exc())

                    # Calculate sleep time
                    compute_end = time.perf_counter()
                    compute_duration = compute_end - loop_start
                    
                    target_frame_time = 1.0 / self.target_tps
                    sleep_time = target_frame_time - compute_duration
                    
                    if sleep_time > 0:
                        await asyncio.sleep(sleep_time)
                    else:
                        await asyncio.sleep(0) # Yield control
                else:
                    # Paused
                    await asyncio.sleep(0.1)

                # Calculate Actual TPS
                loop_end = time.perf_counter()
                total_duration = loop_end - loop_start
                self.actual_tps = 1.0 / total_duration if total_duration > 0 else 0.0

        except asyncio.CancelledError:
            logger.info("Simulation loop cancelled.")
        except Exception as e:
            logger.error(f"Simulation loop crashed: {e}")
        finally:
            self.is_running = False

    def set_speed(self, tps: float):
        """
        Set the target ticks per second.

        Args:
            tps (float): The new target TPS.
        """
        self.target_tps = float(tps)
        logger.info(f"Target TPS set to {self.target_tps}")

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the simulation.

        Returns:
            Dict[str, Any]: A dictionary containing environment and agent data,
            plus telemetry (actual_tps, target_tps).
        """
        state = self.environment.get_state()
        state["environment"]["actual_tps"] = self.actual_tps
        state["environment"]["target_tps"] = self.target_tps
        return state
