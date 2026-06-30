#!/bin/bash

# AI Resume Analyzer - Backend Startup Script for macOS/Linux

echo ""
echo "========================================"
echo "AI Resume Analyzer - Backend"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Start backend
echo ""
echo "Starting backend server..."
echo ""
echo "Backend URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop"
echo ""

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
