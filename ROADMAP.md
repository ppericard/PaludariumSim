# Paludarium Simulation Roadmap

> **Vision**: To create a "bioinformatician's wet dream" — a scientifically accurate, visually stunning, and deeply complex 2D simulation of a paludarium ecosystem.

## 1. Project Status (As of Nov 2025)

The project has successfully graduated from the "Prototype" phase. We have a stable, event-driven architecture with a clear separation of concerns.

### Core Architecture
-   **Backend**: FastAPI (Python) with a decoupled `SimulationRunner` for stable, high-performance ticking.
-   **Frontend**: React + PixiJS (Vite) for high-performance rendering.
-   **Communication**: WebSocket broadcasting state updates at ~10Hz.

### Completed Features (Phase 1: Foundation)
-   [x] **Agent Lifecycle**: Movement, metabolism (hunger/energy), reproduction, death.
-   [x] **Generic Agent System**: Agents are composed of components, not hardcoded classes.
-   [x] **Environmental Physics**:
    -   **Day/Night Cycle**: Realistic solar cycle affecting light levels.
    -   **Terrain System**: Grid-based water/soil/rock layout.
    -   **Variables**: Temperature and humidity affecting agent metabolism.
-   [x] **Data Visualization**:
    -   **Real-time Stats**: Population graph with full history.
    -   **Control Panel**: Spawn agents, toggle modes (Scientific/Zen).
-   [x] **Configuration**: Centralized `config.py` (Backend) and `config.js` (Frontend).

## 2. Technical Debt & Optimization (Completed)

*   [x] **Backend Architecture**: Decoupled simulation loop from WebSocket handler (`SimulationRunner`).
*   [x] **High RAM Usage (Frontend)**: Addressed by limiting stats history in backend.
*   [x] **Profiling Framework**: Implemented profiling decorator/middleware.
*   [x] **Simulation Controls**: Pause, Speed Control (1x, 2x, 5x, Max).
*   [x] **Testing**: Comprehensive environment tests and generic agent tests.

## 3. Roadmap

### Phase 2: Biological Complexity (Current Focus)
The goal is to make the agents feel "alive" and distinct through emergent behavior.

-   [x] **Sensing System**: Agents only "see" within a radius/FOV.
-   [x] **Advanced Species**: Aquatic vs. Terrestrial constraints enforced via components.
-   [x] **Inspector Tool**: Click to view agent stats.
-   [ ] **Complex Interactions**: Predation, symbiosis, territorial behavior.

### Phase 3: The "Bioinformatician's Wet Dream" (Future)
The goal is to enable scientific study and evolution.

-   [ ] **Genetics & Evolution**:
    -   Agents carry a `genome` (float array) modifying component parameters.
    -   Reproduction applies mutation.
    -   Natural selection drives population traits over time.
-   [ ] **Neural Network Brains**:
    -   Replace hardcoded `update()` logic with a simple NN (Inputs: Sensors -> Output: Move Vector).
    -   Trainable via NEAT or simple evolutionary pressure.
-   [ ] **Headless Mode & Data Export**:
    -   Run simulation at max speed (no `sleep`) for data gathering.
    -   Export `stats_history` to CSV/JSON for external analysis (R/Python/Jupyter).
-   [ ] **Chemical Cycles**:
    -   Nitrogen cycle (Waste -> Ammonia -> Nitrite -> Nitrate -> Plants).

## 4. Developer Notes

*   **Config First**: Always check `backend/config.py` before hardcoding values.
*   **Time Handling**: The simulation uses `total_ticks` for monotonic time (graphs) and `time` (0-600) for the cyclic day/night loop.
*   **Generic Architecture**: Do not create new Agent subclasses. Create new **Components** instead.
