# 📐 SYSTEM ARCHITECTURE & VISUAL GUIDE

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER BROWSER                                │
│            http://localhost:8080                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              FRONTEND (HTML/CSS/JS)                   │   │
│  │                                                        │   │
│  │  1. Upload Form                                        │   │
│  │     ├─ Drag & Drop                                    │   │
│  │     └─ File Browser                                   │   │
│  │                                                        │   │
│  │  2. Job Role Selection                                │   │
│  │     └─ Dropdown (10 roles)                            │   │
│  │                                                        │   │
│  │  3. Analyze Button                                    │   │
│  │     └─ Trigger POST /api/analyze                      │   │
│  │                                                        │   │
│  │  4. Results Display                                   │   │
│  │     ├─ File Info                                      │   │
│  │     ├─ ATS Score                                      │   │
│  │     ├─ Charts                                         │   │
│  │     ├─ Skills                                         │   │
│  │     └─ Suggestions                                    │   │
│  │                                                        │   │
│  │  5. Download Report                                   │   │
│  │     └─ Text File (.txt)                               │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                           ↕                                     │
│                    HTTP/JSON (CORS)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND API SERVER                             │
│              (FastAPI - Port 8000)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         FASTAPI APPLICATION (main.py)                 │   │
│  │                                                        │   │
│  │  Endpoints:                                            │   │
│  │  ├─ GET /                    (Info)                   │   │
│  │  ├─ GET /api/health          (Status)                 │   │
│  │  ├─ GET /api/job-roles       (All roles)              │   │
│  │  ├─ GET /api/job-roles/{name}(Role details)           │   │
│  │  ├─ POST /api/analyze        (Main analysis)          │   │
│  │  ├─ POST /api/compare        (Quick compare)          │   │
│  │  ├─ GET /api/results/{id}    (Get results)            │   │
│  │  ├─ GET /api/statistics      (Stats)                  │   │
│  │  └─ GET /api/batch-analyze   (Template)               │   │
│  │                                                        │   │
│  │  Features:                                             │   │
│  │  ├─ CORS Middleware (allow frontend)                  │   │
│  │  ├─ Error Handling                                    │   │
│  │  ├─ Logging                                           │   │
│  │  ├─ Type Hints                                        │   │
│  │  └─ In-Memory Cache                                   │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌────────────────────────────────────────────────────────┐   │
│  │          CORE ANALYSIS MODULES                         │   │
│  │         (Shared Utility Libraries)                     │   │
│  │                                                        │   │
│  │  pdf_extractor.py                                      │   │
│  │  ├─ extract_text_from_pdf()                            │   │
│  │  ├─ get_pdf_info()                                     │   │
│  │  └─ Depends: PyPDF2                                    │   │
│  │                                                        │   │
│  │  skill_analyzer.py                                     │   │
│  │  ├─ extract_skills_from_resume()                       │   │
│  │  ├─ compare_with_job_role()                            │   │
│  │  ├─ get_improvement_suggestions()                      │   │
│  │  └─ Depends: job_roles.py                              │   │
│  │                                                        │   │
│  │  ats_calculator.py                                     │   │
│  │  ├─ calculate_ats_score()  (0-100)                     │   │
│  │  ├─ _check_formatting()    (15% weight)                │   │
│  │  ├─ _check_structure()     (20% weight)                │   │
│  │  ├─ _check_keywords()      (35% weight)                │   │
│  │  ├─ _check_contact_info()  (15% weight)                │   │
│  │  └─ _check_content_quality()(15% weight)               │   │
│  │                                                        │   │
│  │  job_roles.py                                          │   │
│  │  ├─ load_job_roles_data()                              │   │
│  │  ├─ get_default_job_roles()                            │   │
│  │  └─ Depends: data/job_skills.json                      │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                           ↓                                     │
│  ┌────────────────────────────────────────────────────────┐   │
│  │            DATA & CONFIGURATION                        │   │
│  │                                                        │   │
│  │  job_skills.json                                       │   │
│  │  ├─ 10 Job Roles                                       │   │
│  │  ├─ Required Skills (8-10 each)                        │   │
│  │  ├─ Preferred Skills (8+ each)                         │   │
│  │  └─ Salary Ranges                                      │   │
│  │                                                        │   │
│  │  config.py                                             │   │
│  │  ├─ ATS Weights                                        │   │
│  │  ├─ Feature Flags                                      │   │
│  │  └─ Logging Config                                     │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Resume Analysis Process Flow

```
PDF Resume File
      ↓
┌─────────────────────────────────┐
│   1. PDF EXTRACTION             │
│   - PyPDF2 PdfReader            │
│   - Extract text from all pages │
│   - Get metadata                │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│   2. SKILL EXTRACTION           │
│   - Regex pattern matching      │
│   - 100+ skills database        │
│   - Count frequencies           │
│   - Sort by relevance           │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│   3. ATS SCORING (0-100)        │
│   - Formatting check (15%)      │
│   - Structure validation (20%)  │
│   - Keyword analysis (35%)      │
│   - Contact info (15%)          │
│   - Content quality (15%)       │
│   - Generate feedback           │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│   4. JOB ROLE MATCHING          │
│   - Load job role details       │
│   - Compare required skills     │
│   - Compare preferred skills    │
│   - Calculate percentages       │
│   - Generate suggestions        │
└─────────────────────────────────┘
      ↓
┌─────────────────────────────────┐
│   5. RESPONSE GENERATION        │
│   - Compile results             │
│   - Cache in memory             │
│   - Return JSON                 │
│   - Include visualizations      │
└─────────────────────────────────┘
      ↓
JSON Response (Frontend)
```

---

## Frontend Components

```
index.html (Main Page)
│
├── Navigation Bar
│   ├─ Home
│   ├─ Analyzer
│   └─ About
│
├── Home Section
│   ├─ Hero Section
│   └─ 4 Feature Cards
│
├── Analyzer Section
│   │
│   ├─ Upload Area
│   │  ├─ Drag & Drop Zone
│   │  └─ File Input
│   │
│   ├─ Job Role Selection
│   │  └─ Dropdown (populated by API)
│   │
│   ├─ Analyze Button
│   │
│   ├─ Loading Spinner
│   │  └─ Shown during analysis
│   │
│   └─ Results Section (Hidden until analyzed)
│      ├─ File Information Card
│      ├─ ATS Score Card (Color-coded)
│      ├─ ATS Breakdown Card (5 categories)
│      ├─ ATS Feedback Card (List)
│      ├─ Skill Metrics Card
│      ├─ Top Skills Chart (Chart.js)
│      ├─ Matched Skills (Green tags)
│      ├─ Missing Skills (Red tags)
│      ├─ Suggestions Card (Blue list)
│      ├─ Download Report Button
│      └─ Analyze Another Button
│
├── About Section
│   ├─ How It Works
│   ├─ FAQ
│   └─ Job Roles Info
│
└── styles.css (All styling)
    └── app.js (All logic)
```

---

## Backend Request/Response Flow

```
FRONTEND REQUEST
│
├─ Method: POST
├─ URL: http://localhost:8000/api/analyze
├─ Headers: multipart/form-data
│           CORS check
└─ Body:
   ├─ file: resume.pdf (binary)
   └─ job_role: "Software Engineer" (optional)

      ↓

BACKEND PROCESSING
│
├─ Route Handler: /api/analyze
├─ Validation:
│  ├─ File type (PDF only)
│  ├─ File size (< 10 MB)
│  └─ Job role (if specified)
├─ Processing:
│  ├─ Extract PDF → text
│  ├─ Extract skills → list
│  ├─ Calculate ATS → 0-100
│  ├─ Compare job role (if specified)
│  ├─ Generate suggestions
│  └─ Store results (in-memory)
└─ Response Generation

      ↓

BACKEND RESPONSE
│
├─ Status: 200 OK
├─ Headers: application/json
│           Access-Control-Allow-Origin: *
└─ Body: JSON {
     "success": true,
     "result_id": "uuid",
     "file_info": {...},
     "skills_found": {...},
     "ats_score": 78.5,
     "ats_breakdown": {...},
     "ats_feedback": [...],
     "job_role_analysis": {...}
   }

      ↓

FRONTEND DISPLAY
│
├─ Parse JSON response
├─ Validate data
├─ Display file info
├─ Color-code ATS score
├─ Create Chart.js chart
├─ Show skills (tags)
├─ List suggestions
├─ Enable download button
└─ Hide loading spinner
```

---

## File Upload Process

```
User selects PDF
     ↓
Frontend Validation
├─ Is file PDF? ✓
├─ Size < 10 MB? ✓
└─ Display preview
     ↓
User clicks "Analyze"
     ↓
Frontend prepares FormData
├─ file: File object
└─ job_role: String
     ↓
fetch() POST request
     ↓
Backend receives FormData
     ↓
Save to temporary location
     ↓
Process file
     ↓
Return JSON response
     ↓
Frontend receives response
     ↓
Display results
     ↓
User can download report
```

---

## ATS Score Calculation

```
ATS Score (0-100)
│
├─ Formatting Check (15%)
│  ├─ Check for special characters
│  ├─ Check for table structures
│  ├─ Check line breaks
│  └─ Check font/formatting issues
│
├─ Structure Check (20%)
│  ├─ Check for Resume sections
│  │  ├─ Contact info
│  │  ├─ Experience
│  │  ├─ Education
│  │  ├─ Skills
│  │  └─ Projects/Achievements
│  └─ Validate section order
│
├─ Keywords Check (35%)
│  ├─ Find relevant keywords
│  ├─ Count skill mentions
│  ├─ Check for action verbs
│  │  (Led, Developed, Implemented, etc.)
│  └─ Analyze skill density
│
├─ Contact Info Check (15%)
│  ├─ Find email address
│  ├─ Find phone number
│  ├─ Find location
│  └─ Check LinkedIn/GitHub URLs
│
└─ Content Quality Check (15%)
   ├─ Check word count
   ├─ Check for metrics
   ├─ Check for quantifiable achievements
   └─ Check for relevance
```

---

## Job Role Matching

```
Load Job Role Details
     ↓
Get Required Skills (8-10)
├─ List of must-haves
└─ Weight: 100%
     ↓
Get Preferred Skills (8+)
├─ List of nice-to-haves
└─ Weight: Secondary
     ↓
Match with Found Skills
├─ Compare required
│  └─ Calculate percentage
├─ Compare preferred
│  └─ Calculate percentage
└─ Show matched vs missing
     ↓
Generate Suggestions
├─ Skills to add
├─ Skills to consider
└─ General guidance
     ↓
Display Results
├─ Match percentages
├─ Skill tags (green/red)
└─ Recommendations
```

---

## Technology Integration

```
Browser (Frontend)
    ↓
HTML5 + CSS3 + JavaScript
    ├─ DOM manipulation
    ├─ Fetch API calls
    ├─ Chart.js rendering
    └─ SweetAlert2 notifications
    ↓
HTTP/JSON over Network
    ↓
FastAPI Server (Backend)
    ├─ Request routing
    ├─ CORS handling
    ├─ Error responses
    └─ JSON serialization
    ↓
Core Modules
    ├─ PyPDF2 (PDF reading)
    ├─ Regex (Skill detection)
    ├─ String operations (Analysis)
    ├─ Pandas (Data processing)
    └─ JSON (Data storage)
```

---

## Deployment Architecture

```
DEVELOPMENT
│
├─ Backend: python -m uvicorn backend.main:app
│           Port: 8000
│           Mode: Reload (dev)
│
└─ Frontend: python -m http.server 8080
             Port: 8080
             Files: index.html, css/, js/

PRODUCTION (Docker)
│
├─ Docker Image
│  ├─ Base: Python 3.9
│  ├─ Install dependencies
│  ├─ Copy backend code
│  └─ Expose port 8000
│
├─ Docker Compose
│  ├─ Backend service
│  ├─ Frontend service (nginx)
│  └─ Networks/Volumes
│
└─ Orchestration: Kubernetes/Docker Swarm

CLOUD DEPLOYMENT
│
├─ Streamlit Cloud
│  └─ Run app.py (Streamlit version)
│
├─ AWS EC2
│  ├─ Backend on EC2 instance
│  ├─ Frontend on S3 + CloudFront
│  └─ RDS for database (optional)
│
├─ Heroku
│  ├─ Procfile defines startup
│  └─ Automatic scaling
│
└─ Kubernetes
   ├─ Backend pod
   ├─ Frontend pod
   ├─ Load balancer
   └─ Auto-scaling
```

---

## Data Flow Example

```
User uploads "john_resume.pdf" for "Software Engineer"

1. Frontend
   └─ FormData: file + job_role

2. Network
   └─ POST /api/analyze

3. Backend Receives
   └─ Extract file to temp

4. PDF Extraction (pdf_extractor.py)
   └─ Output: "Python expert with 5 years JavaScript experience..."

5. Skill Analysis (skill_analyzer.py)
   ├─ Find: Python, JavaScript, SQL, React, Git, etc.
   └─ Extract: {Python: 5, JavaScript: 3, SQL: 2, ...}

6. ATS Calculation (ats_calculator.py)
   └─ Score: 76.5 (Good)

7. Job Matching (skill_analyzer.py)
   ├─ Required match: 7/9 (77%)
   ├─ Preferred match: 4/8 (50%)
   └─ Missing: Java, Linux, Kubernetes

8. Recommendations (skill_analyzer.py)
   ├─ Add: Java, Linux
   ├─ Consider: Kubernetes, CI/CD
   └─ General: "Strong match! Highlight achievements"

9. Response Compilation (main.py)
   └─ JSON with all results

10. Frontend Receives
    ├─ Parse JSON
    ├─ Display results
    ├─ Create chart
    └─ Show suggestions

11. User Views
    ├─ ATS Score: 76.5 (shown with color)
    ├─ Skills Chart: Bars for top skills
    ├─ Match: 77% required, 50% preferred
    └─ Suggestions: Add Java, Linux, etc.

12. User Downloads Report
    └─ Text file with all details
```

---

## Security Measures

```
Backend Security
├─ CORS: Only allow frontend origin
├─ Input Validation
│  ├─ File type check (PDF only)
│  ├─ File size limit (10 MB)
│  └─ Job role validation
├─ Error Handling
│  ├─ Don't expose system errors
│  ├─ Generic error messages
│  └─ Log details server-side
└─ Rate Limiting (can be added)

Frontend Security
├─ Client-side validation
├─ Secure headers (when deployed)
├─ No sensitive data in localStorage
└─ HTTPS (when deployed)

Data Security
├─ No data persistence (in-memory)
├─ No database (local only)
├─ No API keys exposed
└─ Files deleted after processing
```

---

## Performance Optimization

```
Frontend
├─ CDN for Chart.js and SweetAlert2
├─ CSS minified
├─ JS minified
├─ Image optimization
└─ Lazy loading

Backend
├─ In-memory caching
├─ Fast regex patterns
├─ Efficient PDF parsing
├─ Quick JSON serialization
└─ Async processing (optional)

Network
├─ GZIP compression
├─ Connection pooling
├─ Keep-alive headers
└─ Minimal payload size
```

---

This architecture ensures:
✅ Clean separation of concerns
✅ Scalability
✅ Maintainability
✅ Performance
✅ Security
✅ Easy deployment
✅ Extensibility
