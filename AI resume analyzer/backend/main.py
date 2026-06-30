"""
FastAPI Backend Server for AI Resume Analyzer

This is the REST API backend for the AI Resume Analyzer application.
It handles PDF uploads, resume analysis, skill matching, and ATS scoring.

Run with: uvicorn backend.main:app --reload
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import os
from typing import Optional
from datetime import datetime
import json
import uuid

# Import application modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.pdf_extractor import extract_text_from_pdf, get_pdf_info
from utils.skill_analyzer import SkillAnalyzer
from utils.ats_calculator import ATSCalculator
from utils.job_roles import load_job_roles_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="REST API for analyzing resumes against job requirements",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load job roles data
try:
    job_roles_data = load_job_roles_data()
    logger.info("Job roles data loaded successfully")
except Exception as e:
    logger.error(f"Error loading job roles data: {e}")
    job_roles_data = {}

# Initialize analyzers
skill_analyzer = SkillAnalyzer(job_roles_data) if job_roles_data else None
ats_calculator = ATSCalculator()

# In-memory storage for analysis results (in production, use database)
analysis_results = {}


@app.on_event("startup")
async def startup_event():
    """Event handler for application startup."""
    logger.info("AI Resume Analyzer Backend Starting...")
    logger.info(f"Loaded {len(job_roles_data)} job roles")


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "AI Resume Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "job_roles": "/api/job-roles",
            "analyze": "/api/analyze",
            "results": "/api/results/{result_id}"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "job_roles_loaded": len(job_roles_data) > 0
    }


@app.get("/api/job-roles")
async def get_job_roles():
    """Get list of all available job roles with details."""
    try:
        roles = []
        for role_name, role_data in job_roles_data.items():
            roles.append({
                "name": role_name,
                "description": role_data.get("description", ""),
                "salary_range": role_data.get("salary_range", ""),
                "required_skills_count": len(role_data.get("required_skills", [])),
                "preferred_skills_count": len(role_data.get("preferred_skills", []))
            })
        
        return {
            "success": True,
            "total_roles": len(roles),
            "roles": sorted(roles, key=lambda x: x["name"])
        }
    except Exception as e:
        logger.error(f"Error retrieving job roles: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving job roles")


@app.get("/api/job-roles/{role_name}")
async def get_job_role_details(role_name: str):
    """Get detailed information about a specific job role."""
    try:
        if role_name not in job_roles_data:
            raise HTTPException(
                status_code=404,
                detail=f"Job role '{role_name}' not found"
            )
        
        role_data = job_roles_data[role_name]
        return {
            "success": True,
            "role_name": role_name,
            "description": role_data.get("description", ""),
            "salary_range": role_data.get("salary_range", ""),
            "required_skills": role_data.get("required_skills", []),
            "preferred_skills": role_data.get("preferred_skills", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving job role details: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving job role details")


@app.post("/api/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_role: str = None,
    background_tasks: BackgroundTasks = None
):
    """
    Analyze a resume PDF file.
    
    Parameters:
    - file: PDF resume file
    - job_role: Target job role for comparison (optional)
    
    Returns:
    - Analysis results with skill matching and ATS score
    """
    result_id = str(uuid.uuid4())
    
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Extract PDF text
        logger.info(f"Extracting text from {file.filename}")
        # Read file bytes (async operation - must be awaited)
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)
        resume_info = get_pdf_info(pdf_bytes, file.filename)
        
        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. Ensure it's a text-based PDF."
            )
        
        # Extract skills
        found_skills = skill_analyzer.extract_skills_from_resume(resume_text)
        
        # Calculate ATS score
        ats_result = ats_calculator.calculate_ats_score(resume_text, found_skills)
        
        # Prepare response data
        response_data = {
            "success": True,
            "result_id": result_id,
            "file_info": {
                "filename": file.filename,
                "pages": resume_info.get("num_pages", 0),
                "size_mb": round(resume_info.get("file_size", 0) / (1024 * 1024), 2)
            },
            "skills_found": {
                "total": len(found_skills),
                "top_skills": dict(sorted(found_skills.items(), key=lambda x: x[1], reverse=True)[:10])
            },
            "ats_score": ats_result["ats_score"],
            "ats_status": ats_result["status"],
            "ats_breakdown": {
                k: v["score"] for k, v in ats_result["breakdown"].items()
            },
            "ats_feedback": ats_result["feedback"]
        }
        
        # If job role provided, add skill comparison
        if job_role and job_role in job_roles_data:
            comparison_data = skill_analyzer.compare_with_job_role(found_skills, job_role)
            suggestions = skill_analyzer.get_improvement_suggestions(comparison_data)
            
            response_data["job_role_analysis"] = {
                "job_role": job_role,
                "salary_range": comparison_data["salary_range"],
                "job_description": comparison_data["job_description"],
                "matched_required_skills": comparison_data["matched_required_skills"],
                "missing_required_skills": comparison_data["missing_required_skills"],
                "matched_required_count": comparison_data["matched_required_count"],
                "total_required_skills": comparison_data["total_required_skills"],
                "required_match_percentage": comparison_data["required_match_percentage"],
                "matched_preferred_skills": comparison_data["matched_preferred_skills"],
                "missing_preferred_skills": comparison_data["missing_preferred_skills"],
                "matched_preferred_count": comparison_data["matched_preferred_count"],
                "total_preferred_skills": comparison_data["total_preferred_skills"],
                "preferred_match_percentage": comparison_data["preferred_match_percentage"],
                "suggestions": suggestions
            }
        
        # Store results for later retrieval
        analysis_results[result_id] = response_data
        
        logger.info(f"Analysis completed for result_id: {result_id}")
        
        return response_data
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing resume: {str(e)}"
        )


@app.get("/api/results/{result_id}")
async def get_analysis_results(result_id: str):
    """Retrieve previously analyzed results."""
    try:
        if result_id not in analysis_results:
            raise HTTPException(
                status_code=404,
                detail=f"Results with ID '{result_id}' not found"
            )
        
        return analysis_results[result_id]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving results: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving results")


@app.post("/api/compare")
async def compare_skills(
    file: UploadFile = File(...),
    job_role: str = None
):
    """
    Quick endpoint to compare resume with a job role.
    """
    if not job_role:
        raise HTTPException(status_code=400, detail="job_role parameter required")
    
    if job_role not in job_roles_data:
        raise HTTPException(
            status_code=404,
            detail=f"Job role '{job_role}' not found"
        )
    
    try:
        resume_text = extract_text_from_pdf(file)
        found_skills = skill_analyzer.extract_skills_from_resume(resume_text)
        comparison_data = skill_analyzer.compare_with_job_role(found_skills, job_role)
        suggestions = skill_analyzer.get_improvement_suggestions(comparison_data)
        
        return {
            "success": True,
            "job_role": job_role,
            "skills_found": len(found_skills),
            "matched_required": comparison_data["matched_required_count"],
            "total_required": comparison_data["total_required_skills"],
            "required_match_percentage": comparison_data["required_match_percentage"],
            "matched_preferred": comparison_data["matched_preferred_count"],
            "total_preferred": comparison_data["total_preferred_skills"],
            "preferred_match_percentage": comparison_data["preferred_match_percentage"],
            "suggestions": suggestions,
            "matched_required_skills": comparison_data["matched_required_skills"],
            "missing_required_skills": comparison_data["missing_required_skills"][:5]  # Top 5
        }
    except Exception as e:
        logger.error(f"Error in skill comparison: {e}")
        raise HTTPException(status_code=500, detail="Error comparing skills")


@app.get("/api/statistics")
async def get_statistics():
    """Get API statistics."""
    return {
        "total_analyses": len(analysis_results),
        "job_roles_available": len(job_roles_data),
        "api_version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/batch-analyze")
async def batch_analyze(job_role: str):
    """Get batch analysis template for a job role."""
    if job_role not in job_roles_data:
        raise HTTPException(status_code=404, detail="Job role not found")
    
    role_data = job_roles_data[job_role]
    
    return {
        "success": True,
        "template": {
            "job_role": job_role,
            "required_skills": role_data.get("required_skills", []),
            "preferred_skills": role_data.get("preferred_skills", []),
            "description": role_data.get("description", ""),
            "salary_range": role_data.get("salary_range", "")
        }
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
