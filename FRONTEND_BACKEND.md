# Frontend & Backend Architecture Documentation

## Overview

The AI Resume Analyzer now uses a modern **Frontend-Backend separated architecture**:

- **Backend**: FastAPI REST API (Python) - runs on `http://localhost:8000`
- **Frontend**: HTML/CSS/JavaScript Single Page Application - runs on `http://localhost:8080` (or any HTTP server)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Frontend (HTML/CSS/JavaScript)                      │  │
│  │  - File Upload                                       │  │
│  │  - Job Role Selection                                │  │
│  │  - Results Display                                   │  │
│  │  - Chart Visualization                               │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │                                              │
└───────────────┼──────────────────────────────────────────────┘
                │ HTTP/JSON
                │
┌───────────────▼──────────────────────────────────────────────┐
│              Backend (FastAPI) - Port 8000                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           REST API Endpoints                         │   │
│  │  POST   /api/analyze         - Analyze resume       │   │
│  │  POST   /api/compare         - Compare with job     │   │
│  │  GET    /api/job-roles       - Get job roles        │   │
│  │  GET    /api/results/{id}    - Get results          │   │
│  │  GET    /api/health          - Health check         │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                               │
│  ┌────────────▼─────────────────────────────────────────┐   │
│  │        Core Analysis Modules                         │   │
│  │  - PDF Extraction (PyPDF2)                          │   │
│  │  - Skill Analysis                                    │   │
│  │  - ATS Calculation                                   │   │
│  │  - Job Role Matching                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Running the Application

### Method 1: Using Startup Scripts (Easiest)

**Windows:**
```bash
run_backend.bat
```

**macOS/Linux:**
```bash
chmod +x run_backend.sh
./run_backend.sh
```

### Method 2: Manual Startup

**Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Start Backend**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Step 3: Serve Frontend**

Option A - Using Python's built-in HTTP server:
```bash
cd frontend
python -m http.server 8080
```

Option B - Using Node.js http-server:
```bash
cd frontend
npx http-server -p 8080
```

Option C - Using any web server (Nginx, Apache, etc.)

**Step 4: Open in Browser**
```
http://localhost:8080
```

## Backend API Endpoints

### 1. Health Check
```
GET /api/health
Response: { status: "healthy", job_roles_loaded: true }
```

### 2. Get Job Roles
```
GET /api/job-roles
Response: { success: true, total_roles: 10, roles: [...] }
```

### 3. Get Job Role Details
```
GET /api/job-roles/{role_name}
Response: { success: true, role_name: "...", required_skills: [...], preferred_skills: [...] }
```

### 4. Analyze Resume
```
POST /api/analyze
Headers: Content-Type: multipart/form-data
Body:
  - file: <PDF file>
  - job_role: "Software Engineer"

Response: {
  success: true,
  result_id: "uuid",
  file_info: {...},
  skills_found: {...},
  ats_score: 75.5,
  ats_status: "Good",
  ats_breakdown: {...},
  ats_feedback: [...],
  job_role_analysis: {...}
}
```

### 5. Compare Skills
```
POST /api/compare
Headers: Content-Type: multipart/form-data
Body:
  - file: <PDF file>
  - job_role: "Data Scientist"

Response: {
  success: true,
  job_role: "...",
  skills_found: 15,
  matched_required: 8,
  total_required: 10,
  required_match_percentage: 80,
  suggestions: [...]
}
```

### 6. Get Analysis Results
```
GET /api/results/{result_id}
Response: <complete analysis result>
```

### 7. Get Statistics
```
GET /api/statistics
Response: { total_analyses: 5, job_roles_available: 10 }
```

## Frontend Features

### File Upload
- Drag & drop PDF files
- Click to browse
- File validation (PDF only, max 10MB)
- Visual feedback

### Job Role Selection
- Dropdown with 10+ job roles
- Dynamically loaded from backend
- Default selection prompt

### Analysis Display
- Real-time progress indicator
- File information display
- ATS score with color coding
- Skill matching metrics
- Interactive charts
- Downloadable reports

## API Response Examples

### Successful Analysis Response
```json
{
  "success": true,
  "result_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "file_info": {
    "filename": "resume.pdf",
    "pages": 2,
    "size_mb": 0.45
  },
  "skills_found": {
    "total": 18,
    "top_skills": {
      "Python": 3,
      "JavaScript": 2,
      "SQL": 2
    }
  },
  "ats_score": 78.5,
  "ats_status": "Good - Your resume has decent ATS compatibility",
  "ats_breakdown": {
    "formatting": 85,
    "structure": 80,
    "keywords": 72,
    "contact": 90,
    "content": 68
  },
  "ats_feedback": [
    "✓ Good formatting - minimal special characters",
    "✓ Good text structure with proper line breaks",
    "✓ Email address found",
    "✓ Phone number found"
  ],
  "job_role_analysis": {
    "job_role": "Software Engineer",
    "salary_range": "$100,000 - $180,000",
    "matched_required_skills": ["Python", "JavaScript", "SQL", "Git", "REST API"],
    "missing_required_skills": ["Java", "Linux"],
    "matched_required_count": 5,
    "total_required_skills": 9,
    "required_match_percentage": 55.56,
    "matched_preferred_skills": ["Docker", "AWS"],
    "missing_preferred_skills": ["Kubernetes", "CI/CD"],
    "matched_preferred_count": 2,
    "total_preferred_skills": 8,
    "preferred_match_percentage": 25,
    "suggestions": [
      "Add experience with: Java, Linux, Kubernetes",
      "Consider adding: CI/CD, Microservices",
      "You have a moderate match. Focus on acquiring the missing required skills."
    ]
  }
}
```

## Frontend File Structure

```
frontend/
├── index.html              # Main HTML page
├── assets/
│   ├── css/
│   │   └── styles.css      # All CSS styles
│   └── js/
│       └── app.js          # Frontend JavaScript logic
```

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **PyPDF2**: PDF text extraction
- **Python**: Core language

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Grid/Flexbox
- **Vanilla JavaScript**: No dependencies required
- **Chart.js**: Chart visualization
- **SweetAlert2**: User notifications

## Configuration

### Backend Configuration

Edit `config.py`:
```python
# ATS Score Weights
ATS_WEIGHTS = {
    "formatting": 0.15,
    "structure": 0.20,
    "keywords": 0.35,      # Highest weight on keywords
    "contact": 0.15,
    "content": 0.15
}
```

### Frontend Configuration

Edit `frontend/assets/js/app.js`:
```javascript
// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';
```

## Error Handling

### Backend Errors
- 400: Bad request (invalid file, missing parameters)
- 404: Resource not found (job role doesn't exist)
- 500: Internal server error

### Frontend Errors
- File validation errors
- Network errors
- API timeout
- Analysis failures

All errors display user-friendly messages using SweetAlert2.

## Performance Considerations

- **File Upload**: Max 10MB per file
- **Analysis Time**: 2-5 seconds per resume
- **Results Caching**: Results stored in memory
- **CORS**: Enabled for cross-origin requests

## Deployment

### Local Development
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Frontend
cd frontend && python -m http.server 8080
```

### Production
See main README.md for production deployment guides:
- Docker
- Kubernetes
- AWS
- Heroku
- Streamlit Cloud

## Troubleshooting

### Backend won't start
```
Error: Connection refused on port 8000
Solution: Port already in use. Kill process or use different port.
```

### Frontend can't reach backend
```
Error: CORS error or network error
Solution: Ensure backend is running on http://localhost:8000
```

### PDF extraction fails
```
Error: No text extracted from PDF
Solution: Ensure PDF is text-based, not scanned image
```

## API Testing

### Using curl
```bash
# Get job roles
curl http://localhost:8000/api/job-roles

# Health check
curl http://localhost:8000/api/health

# Analyze resume
curl -X POST -F "file=@resume.pdf" -F "job_role=Software Engineer" \
     http://localhost:8000/api/analyze
```

### Using Postman
1. Import API collection from backend/main.py
2. Set base URL: http://localhost:8000/api
3. Test endpoints

### Using Swagger UI
Visit: http://localhost:8000/docs

## Next Steps

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 8080
3. ✅ Test with sample resume
4. ✅ Deploy to production

---

**Version**: 1.0.0
**Status**: Production Ready ✅
