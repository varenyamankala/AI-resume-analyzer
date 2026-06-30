# 🚀 QUICK REFERENCE CARD

## STARTUP COMMANDS

### Backend (Required First)
```bash
python run_backend.py
# Runs on: http://localhost:8000
# Status: http://localhost:8000/api/health
```

### Frontend (Required Second)
```bash
cd frontend
python -m http.server 8080
# Access: http://localhost:8080
```

### Alternative Startup
```bash
# Windows
run_backend.bat

# macOS/Linux
./run_backend.sh
```

---

## API ENDPOINTS

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check server status |
| `/api/job-roles` | GET | List all job roles |
| `/api/job-roles/{name}` | GET | Get job role details |
| `/api/analyze` | POST | Analyze resume |
| `/api/compare` | POST | Quick skill compare |
| `/api/results/{id}` | GET | Retrieve results |
| `/api/statistics` | GET | API statistics |

---

## FILE LOCATIONS

```
backend/main.py          - FastAPI server
frontend/index.html      - Web page
frontend/assets/js/app.js - JavaScript
frontend/assets/css/styles.css - CSS

utils/pdf_extractor.py   - PDF processing
utils/skill_analyzer.py  - Skill analysis
utils/ats_calculator.py  - ATS scoring
data/job_skills.json     - Job roles database
```

---

## CONFIGURATION

```
config.py                - Settings
requirements.txt         - Dependencies
data/job_skills.json     - Job roles
```

---

## TESTING

```bash
# Test all endpoints
python test_api.py

# Expected: All 6 tests pass ✓
```

---

## DOCUMENTATION

- **README.md** - Complete guide
- **QUICKSTART.md** - 5 min setup
- **FRONTEND_BACKEND.md** - Architecture
- **IMPLEMENTATION_GUIDE.md** - Details
- **DEPLOYMENT_CHECKLIST.md** - Pre-deploy

---

## BROWSER PORTS

```
Frontend: http://localhost:8080
Backend API: http://localhost:8000
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
```

---

## KEY FEATURES

✓ PDF upload & extraction
✓ Skill analysis (100+ skills)
✓ Job role matching (10 roles)
✓ ATS scoring (0-100)
✓ Smart recommendations
✓ Interactive charts
✓ Report download
✓ Mobile responsive

---

## JOB ROLES

1. Software Engineer
2. Data Scientist
3. Full Stack Developer
4. DevOps Engineer
5. Cloud Architect
6. Mobile Developer
7. Frontend Developer
8. Backend Developer
9. QA Engineer
10. Product Manager

---

## TECH STACK

**Backend**: FastAPI, Uvicorn, PyPDF2, Pandas
**Frontend**: HTML5, CSS3, JavaScript, Chart.js
**Python**: 3.8+

---

## TROUBLESHOOTING

**Port in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

**CORS error?**
- Backend has CORS enabled
- Check both services running
- Check URLs are correct

**PDF won't extract?**
- Use text-based PDF (not image)
- Try different PDF
- Check file size < 10MB

---

## DEPLOYMENT

**Docker:**
```bash
docker-compose up --build
```

**Streamlit:**
```bash
streamlit run app.py
```

---

## USEFUL COMMANDS

```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python -m uvicorn backend.main:app --reload

# Run tests
python test_api.py

# View swagger docs
# http://localhost:8000/docs

# Start frontend
cd frontend && python -m http.server 8080
```

---

## SUPPORT

- Check documentation files
- Review inline code comments
- Test with sample resume
- Check browser console (F12)
- Check terminal output

---

**Status**: ✅ Ready to Use
**Version**: 2.0.0
**Time to Setup**: ~5 minutes
