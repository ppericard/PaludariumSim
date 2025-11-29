# Paludarium Simulation Roadmap

> **Vision**: To create a "bioinformatician's wet dream" — a scientifically accurate, visually stunning, and deeply complex 2D simulation of a paludarium ecosystem.

## 1. Project Status (As of Nov 2025)

The project has successfully graduated from the "Prototype" phase. We have a stable, event-driven architecture with a clear separation of concerns.

### Core Architecture
-   **Backend**: FastAPI (Python) handling simulation logic, physics, and state management.
    -   *Key Components*: `Environment` (state container), `Agent` (base class), `Plant`/`Animal` (implementations).
    -   *Communication*: WebSocket broadcasting state updates at ~10Hz.
-   **Frontend**: React + PixiJS (Vite) for high-performance rendering.
    -   *Key Components*: `SimulationCanvas` (PixiJS stage), `ControlPanel` (UI), `StatsPanel` (Recharts).

### Completed Features (Phase 1: Foundation)
-   [x] **Agent Lifecycle**: Movement, metabolism (hunger/energy), reproduction, death.
-   [x] **Environmental Physics**:
    -   **Day/Night Cycle**: Realistic solar cycle affecting light levels.
    -   **Terrain System**: Grid-based water/soil/rock layout.
    -   **Variables**: Temperature and humidity affecting agent metabolism.
-   [x] **Data Visualization**:
    -   **Real-time Stats**: Population graph with full history (monotonic time tracking).
    -   **Control Panel**: Spawn agents, toggle modes (Scientific/Zen).
-   [x] **Configuration**: Centralized `config.py` (Backend) and `config.js` (Frontend).

## 2. Known Issues & Technical Debt

*   **Client-side RAM Usage**: The frontend memory usage grows over time.
    *   *Suspect*: `StatsPanel` history array growing indefinitely or PixiJS texture/container not being garbage collected properly.
    *   *Action*: Implement data downsampling for the graph and verify PixiJS resource disposal.
*   **Type Safety**: Python backend has some type hints, but coverage is incomplete.
    *   *Action*: Run `mypy` and strict type checking on `simulation/` modules.
*   **Testing**: Basic unit tests exist (`tests/`), but complex interactions (e.g., "do animals actually die of hunger?") need integration tests.

## 3. Technical Debt & Optimization (Completed)

*   [x] **High RAM Usage (Frontend)**:
    -   Addressed by limiting stats history in backend.
*   [x] **Profiling Framework**:
    -   **Backend**: Implement a profiling decorator/middleware to measure tick execution time and memory usage.
    -   **Frontend**: Monitor render time and FPS.
*   [x] **Simulation Controls & Telemetry**:
    -   Display "Total Ticks" and "Average Tick Time (last 10s)" in Control Panel.
    -   Implement Speed Control (Pause, 1x, 2x, 5x, Max).

## 3. Roadmap

### Phase 2: Biological Complexity (Completed)
The goal is to make the agents feel "alive" and distinct.

-   [x] **Sensing System**:
    -   Agents currently know global state. They should only "see" within a radius/FOV.
    -   Implement `get_visible_agents(agent)` in backend.
-   [x] **Advanced Species**:
    -   **Aquatic vs. Terrestrial**: Enforce terrain constraints (fish die on land, frogs swim).
    -   **Traits**: Speed, size, and color should vary by individual.
-   [x] **Inspector Tool**:
    -   Clicking an agent in the frontend should show its specific stats (Age, Hunger, Energy, ID) in the sidebar.

### Phase 3: The "Bioinformatician's Wet Dream" (Future)
The goal is to enable scientific study and evolution.

-   [ ] **Genetics & Evolution**:
    -   Agents carry a `genome` (e.g., float array).
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

## 4. Developer Notes (For the Next Agent)

*   **Config First**: Always check `backend/config.py` before hardcoding values.
*   **Time Handling**: The simulation uses `total_ticks` for monotonic time (graphs) and `time` (0-600) for the cyclic day/night loop. Do not confuse them.
*   **Imports**: Be careful with circular imports in Python (`Environment` needs `Agent`, `Agent` needs `Environment` for type hints). Use `TYPE_CHECKING`.
*   **Frontend Imports**: Always use **named imports** for config (`import { config } from '../config'`), NOT default imports. We crashed the app once doing this wrong.
