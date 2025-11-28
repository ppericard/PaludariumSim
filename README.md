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

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Status
**Current Phase**: Phase 2 (Biological Complexity)
See [ROADMAP.md](./ROADMAP.md) for the detailed project vision, completed features, and future plans.

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

### v1.0.0 (Foundation)
- **Frontend**: React 19 + PixiJS v8, Glassmorphism UI, Stats Panel.
- **Backend**: FastAPI, WebSocket state sync, Day/Night Cycle, Terrain System.
- **Simulation**: Basic agent lifecycle, monotonic time tracking.

## Next Steps
See [ROADMAP.md](./ROADMAP.md) for the full list.
1.  **Sensing System**: Agents reacting to local environment.
2.  **Advanced Species**: Aquatic vs Terrestrial traits.


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
