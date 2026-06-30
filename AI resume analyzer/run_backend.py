"""
Startup script for the AI Resume Analyzer Backend

This script starts the FastAPI backend server on http://localhost:8000

Usage: python run_backend.py
"""

import subprocess
import sys
import os
import time

def start_backend():
    """Start the FastAPI backend server."""
    print("=" * 60)
    print("AI Resume Analyzer - Backend Startup")
    print("=" * 60)
    print()
    
    # Check if uvicorn is installed
    try:
        import uvicorn
    except ImportError:
        print("❌ FastAPI/Uvicorn not installed!")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if required modules exist
    try:
        from utils.pdf_extractor import extract_text_from_pdf
        from utils.skill_analyzer import SkillAnalyzer
        from utils.ats_calculator import ATSCalculator
        print("✓ Core modules found")
    except ImportError as e:
        print(f"❌ Error importing core modules: {e}")
        sys.exit(1)
    
    print()
    print("Starting backend server...")
    print()
    print("📍 Backend URL: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 ReDoc: http://localhost:8000/redoc")
    print()
    print("Press CTRL+C to stop the server")
    print()
    print("=" * 60)
    print()
    
    # Start the server
    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nBackend stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_backend()
