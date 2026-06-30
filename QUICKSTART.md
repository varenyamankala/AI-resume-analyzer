# Quick Start Guide for AI Resume Analyzer

## Installation (5 minutes)

### 1. Navigate to the project directory
```bash
cd "AI Resume Analyzer"
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Key Features

✅ Upload PDF resume
✅ Compare against 10+ job roles
✅ Get ATS score (0-100)
✅ View skill matching analysis
✅ Get improvement recommendations
✅ Download analysis report
✅ Interactive visualizations

## Usage

1. Upload your PDF resume
2. Select a job role
3. Click "Analyze Resume"
4. Review results in tabs:
   - Skill Analysis
   - ATS Score
   - Recommendations
   - Report

## Deployment Options

### Free: Streamlit Cloud
- Push to GitHub
- Go to https://streamlit.io/cloud
- Deploy with one click
- URL: `https://[username]-[app-name].streamlit.app`

### Free: Docker + GitHub Actions
- See Docker section in README.md

### Paid: AWS EC2
- See AWS section in README.md

## Troubleshooting

**"Module not found" error**
```bash
pip install -r requirements.txt
```

**PDF won't extract**
- Use text-based PDF (not scanned image)
- Try online PDF converter first

**Slow performance**
- Check internet connection
- Clear browser cache (Ctrl+Shift+Del)

## File Structure
```
├── app.py              # Main app
├── requirements.txt    # Dependencies
├── README.md          # Full documentation
├── QUICKSTART.md      # This file
├── utils/
│   ├── pdf_extractor.py
│   ├── skill_analyzer.py
│   ├── ats_calculator.py
│   └── job_roles.py
├── components/
│   ├── ui.py
│   └── charts.py
└── data/
    └── job_skills.json
```

## Next Steps

1. ✅ Run the app and try it with your resume
2. ✅ Customize job roles in `data/job_skills.json`
3. ✅ Deploy to Streamlit Cloud for sharing
4. ✅ Share feedback and improvements

## Support

- Check README.md for detailed documentation
- Review code comments for technical details
- Check FAQ section in the app

---

**Happy resume analyzing!** 🚀
