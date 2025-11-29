# Paludarium Simulation

> **Vision**: To create a "bioinformatician's wet dream" — a scientifically accurate, visually stunning, and deeply complex 2D simulation of a paludarium ecosystem.

## Overview

PaludariumSim is a multi-agent simulation where complex behaviors emerge from simple, component-based rules. Unlike traditional simulations with hardcoded "Plant" or "Animal" classes, agents in this system are generic containers defined solely by their composition of **Components** (e.g., `Photosynthesis`, `Locomotion`, `SexualReproduction`).

This architecture allows for:
-   **Emergent Behavior**: Species niches (aquatic, terrestrial, amphibious) emerge naturally from physical constraints and component interactions.
-   **Evolutionary Potential**: Future iterations can mutate component parameters (genome) to drive natural selection.
-   **Scalability**: The backend is decoupled from the visualization, allowing for high-speed headless simulation.

## Architecture

### Backend (Python + FastAPI)
-   **Core Logic**: `backend/simulation/`
    -   **`SimulationRunner`**: Manages the main loop in a background thread, decoupled from network I/O.
    -   **`Environment`**: Holds state (Agents, Terrain, Global Variables). Uses a spatial grid for O(1) neighbor lookups.
    -   **`Agent`**: Generic entity with a list of `Components`.
    -   **`Components`**: Modular logic blocks (e.g., `Growth`, `Heterotrophy`) that define behavior.
-   **API**: `backend/main.py`
    -   **FastAPI**: Serves REST endpoints and static files.
    -   **WebSockets**: Broadcasts state updates at ~10Hz and receives user commands (spawn, pause, speed control).

### Frontend (React + Vite + PixiJS)
-   **Rendering**: **PixiJS** is used for the main simulation canvas to handle thousands of sprites efficiently.
-   **UI**: React components for the Control Panel and Stats Overlay.
-   **State Management**: Custom `useSimulation` hook manages the WebSocket connection and synchronizes state.
-   **Optimization**: `React.memo` and efficient sprite pooling ensure smooth 60fps rendering.

## Getting Started

### Prerequisites
-   Python 3.9+
-   Node.js 16+

### 1. Backend Setup
```bash
cd backend
# Create virtual environment (optional but recommended)
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
```bash
cd frontend
# Install dependencies
npm install

# Run the development server
npm run dev
```
Open `http://localhost:5173` in your browser.

## Project Structure

```
PaludariumSim/
├── backend/
│   ├── simulation/         # Core simulation logic
│   │   ├── components.py   # Behavior modules (Growth, Movement, etc.)
│   │   ├── environment.py  # State container & Spatial Grid
│   │   ├── runner.py       # Main loop manager
│   │   └── factory.py      # Agent creation helper
│   ├── tests/              # Pytest suite
│   ├── main.py             # FastAPI entry point
│   └── config.py           # Central configuration
├── frontend/
│   ├── src/
│   │   ├── components/     # React UI components
│   │   │   └── SimulationCanvas.jsx # PixiJS integration
│   │   ├── hooks/          # Custom hooks (useSimulation)
│   │   └── utils/          # Helpers
│   └── public/             # Static assets
└── ROADMAP.md              # Project goals and status
```

## Contributing

### Testing
All new features must be tested. We use `pytest` for the backend.
```bash
cd backend
python -m pytest
```

### Code Style
-   **Python**: PEP 8.
-   **JavaScript**: Standard React patterns.

## License
MIT
