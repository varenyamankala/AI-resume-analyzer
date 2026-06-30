@echo off
REM AI Resume Analyzer - Backend Startup Script for Windows

echo.
echo ========================================
echo AI Resume Analyzer - Backend
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Start backend
echo.
echo Starting backend server...
echo.
echo Backend URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop
echo.

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
