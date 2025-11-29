@echo off
echo ==========================================
echo   Starting Paludarium Simulation
echo ==========================================

:: Start Backend
echo [1/3] Starting Backend Server...
start "Paludarium Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

:: Start Frontend
echo [2/3] Starting Frontend Client...
start "Paludarium Frontend" cmd /k "cd frontend && npm run dev"

:: Open Browser
echo [3/3] Opening Browser in 3 seconds...
timeout /t 3 >nul
start http://localhost:5173

echo.
echo ==========================================
echo   Simulation Started!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5173
echo ==========================================
echo.
echo You can close this window now, or keep it open.
pause
