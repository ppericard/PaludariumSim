# AI Agent Instructions

This document provides guidelines for AI agents working on the Paludarium Simulation project.

## Project Structure

- **backend/**: FastAPI application.
- **frontend/**: React application with Vite.

## Coding Standards

### Backend (Python)
- Follow PEP 8 guidelines.
- Use `black` for formatting.
- Use `flake8` for linting.
- Use type hints and check with `mypy`.
- Write unit tests using `pytest`.

### Frontend (React/JavaScript)
- Use functional components and hooks.
- Use `prettier` for formatting.
- Use `eslint` for linting.
- Write unit tests using `vitest` and `@testing-library/react`.

## Testing Requirements

- **New Features**: All new features must include unit tests.
- **Bug Fixes**: All bug fixes must include a regression test.
- **Coverage**: Aim for high test coverage, especially for core logic.

## Workflow

1.  **Plan**: Create an implementation plan before writing code.
2.  **Implement**: Write code and tests.
3.  **Verify**: Run tests and linting to ensure quality.

## Git Versioning

- **Commit Messages**: Use Conventional Commits (e.g., `feat: add login`, `fix: resolve crash`).
- **Granularity**: Make frequent, atomic commits. Do not bundle unrelated changes.
- **Branches**: Use feature branches for new tasks (e.g., `feat/user-auth`).
- **Sync**: Pull latest changes before starting work.
