# Contributing to Paludarium Simulation

## Setup

1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    ```

## Running Tests

- **Backend**:
    ```bash
    cd backend
    pytest
    ```

- **Frontend**:
    ```bash
    cd frontend
    npm test
    ```

## Linting & Formatting

- **Backend**:
    ```bash
    cd backend
    black .
    flake8 .
    mypy .
    ```

- **Frontend**:
    ```bash
    cd frontend
    npm run lint
    npm run format
    ```
