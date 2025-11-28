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

## Version History

### v1.0.0 (First Fully Working Version)
- **Frontend**:
    -   Upgraded to React 19 and PixiJS v8.
    -   Implemented "Zen Mode" with glassmorphism UI.
    -   Responsive layout with sidebar control panel.
    -   Canvas resized to 1200x800 (centered).
- **Backend**:
    -   Environment resized to 1000x800.
    -   Implemented agent lifecycle (eating, reproduction, death).
    -   Added automated tests for simulation logic.

## Next Steps for Development
1.  **Environment**: Add day/night cycle, temperature/humidity dynamics.
2.  **Advanced AI**: Implement neural networks for agent behavior.


## AI Agent Instructions

This section provides guidelines for AI agents working on the Paludarium Simulation project.

### Project Structure

- **backend/**: FastAPI application.
- **frontend/**: React application with Vite.

### Coding Standards

#### Backend (Python)
- Follow PEP 8 guidelines.
- Use `black` for formatting.
- Use `flake8` for linting.
- Use type hints and check with `mypy`.
- Write unit tests using `pytest`.

#### Frontend (React/JavaScript)
- Use functional components and hooks.
- Use `prettier` for formatting.
- Use `eslint` for linting.
- Write unit tests using `vitest` and `@testing-library/react`.

### Testing Requirements

- **New Features**: All new features must include unit tests.
- **Bug Fixes**: All bug fixes must include a regression test.
- **Coverage**: Aim for high test coverage, especially for core logic.

### Workflow

1.  **Plan**: Create an implementation plan before writing code.
2.  **Implement**: Write code and tests.
3.  **Verify**: Run tests and linting to ensure quality.

### Git Versioning

- **Commit Messages**: Use Conventional Commits (e.g., `feat: add login`, `fix: resolve crash`).
- **Granularity**: Make frequent, atomic commits. Do not bundle unrelated changes. Commit and push regularly to ensure work is saved and shared.
- **Branches**: Use feature branches for new tasks (e.g., `feat/user-auth`).
- **Sync**: Pull latest changes before starting work.
