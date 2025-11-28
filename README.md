# Paludarium Simulation

A realistic 2D Paludarium simulation with a Multi-Agent System backend.

## Architecture
- **Frontend**: React (Vite)
- **Backend**: Python (FastAPI)

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Current Status
- **Backend**: 
    - FastAPI server running on `localhost:8000`.
    - WebSocket endpoint `/ws` broadcasts simulation state.
    - Simulation Engine: `Environment` class manages `Agent`s.
    - Agents implemented: `Plant` (growth), `Animal` (movement, hunger).
- **Frontend**: 
    - React + Vite running on `localhost:5173`.
    - PixiJS rendering in `SimulationCanvas.jsx`.
    - Real-time updates via WebSocket.

## Project Structure
```
PaludariumSim/
├── backend/
│   ├── simulation/      # Core logic (Agents, Environment)
│   ├── main.py          # FastAPI app & WebSocket loop
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/components/  # React components (SimulationCanvas)
│   └── package.json     # Node dependencies
└── README.md
```

## Next Steps for Development
1.  **UI/UX**: Implement the "Zen" vs "Scientific" modes. Add controls to spawn agents.
2.  **Simulation Depth**: Add more complex interactions (eating, reproduction, death).
3.  **Environment**: Add day/night cycle, temperature/humidity dynamics.

