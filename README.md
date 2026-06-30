# AI Resume Analyzer 🎯

A powerful Streamlit-based web application that analyzes resumes using AI and machine learning. Users can upload their PDF resumes, compare them against job requirements, get an ATS (Applicant Tracking System) score, and receive actionable recommendations for improvement.

## Features ✨

- **📤 PDF Resume Upload**: Upload and process resume files in PDF format
- **📊 Skill Analysis**: Extract and analyze skills from your resume
- **🎯 Job Role Comparison**: Compare your skills with 10+ professional job roles
- **📈 Skill Match Score**: Visual representation of required vs. preferred skills match
- **📋 ATS Score**: Calculate resume compatibility with Applicant Tracking Systems
- **💡 Smart Recommendations**: Get personalized suggestions to improve your resume
- **📊 Visual Analytics**: Interactive charts and gauges for easy understanding
- **📄 Report Generation**: Download detailed analysis reports
- **🎨 Clean UI**: Modern, intuitive user interface with Streamlit

## Supported Job Roles 💼

The application supports analysis for the following job roles:
1. **Software Engineer** - $100,000 - $180,000
2. **Data Scientist** - $110,000 - $190,000
3. **Full Stack Developer** - $95,000 - $160,000
4. **DevOps Engineer** - $105,000 - $175,000
5. **Cloud Architect** - $120,000 - $200,000
6. **Mobile Developer** - $95,000 - $170,000
7. **Frontend Developer** - $90,000 - $155,000
8. **Backend Developer** - $95,000 - $170,000
9. **QA Engineer** - $80,000 - $140,000
10. **Product Manager** - $110,000 - $190,000

## Project Structure 📁

```
AI-Resume-Analyzer/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation (this file)
│
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py      # PDF text extraction using PyPDF2
│   ├── skill_analyzer.py     # Skill extraction and job matching
│   ├── ats_calculator.py     # ATS score calculation
│   └── job_roles.py          # Job roles database loader
│
├── components/
│   ├── __init__.py
│   ├── ui.py                 # Reusable UI components
│   └── charts.py             # Plotly chart generation
│
└── data/
    └── job_skills.json       # Job roles and required skills database
```

## Installation 🔧

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download the Repository

```bash
# If cloning from git
git clone https://github.com/yourusername/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

# Or navigate to the project directory if you have the files
cd "AI Resume Analyzer"
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage 🚀

### Running Locally

1. **Activate the virtual environment** (if not already active):
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Access the application**:
   - The app will open in your default browser at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL manually

4. **Using the Application**:
   - Upload your resume in PDF format
   - Select a target job role from the dropdown
   - Click "Analyze Resume" to generate insights
   - Review skill matching, ATS score, and recommendations
   - Download your analysis report

## Deployment 🌐

### Deploying on Streamlit Cloud (Free & Easy)

1. **Prepare Your Repository**:
   - Ensure your project is on GitHub (public or private)
   - Make sure all files are properly committed

2. **Deploy on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch, and main file (`app.py`)
   - Click "Deploy"
   - Streamlit will automatically deploy your app

3. **Access Your App**:
   - Your app will be available at: `https://[your-username]-[app-name].streamlit.app`

### Deploying on AWS (EC2)

1. **Launch an EC2 Instance**:
   ```bash
   # Choose Amazon Linux 2 or Ubuntu
   # Use at least t2.micro for free tier eligibility
   ```

2. **Connect and Setup**:
   ```bash
   # SSH into your instance
   ssh -i your-key.pem ec2-user@your-instance-ip
   
   # Update system
   sudo yum update -y  # For Amazon Linux
   # or
   sudo apt update && sudo apt upgrade -y  # For Ubuntu
   
   # Install Python and pip
   sudo yum install python3 python3-pip -y  # For Amazon Linux
   # or
   sudo apt install python3 python3-pip -y  # For Ubuntu
   ```

3. **Clone Repository and Install**:
   ```bash
   git clone https://github.com/yourusername/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
   pip install -r requirements.txt
   ```

4. **Run with Systemd**:
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/resume-analyzer.service
   ```
   
   Add this content:
   ```ini
   [Unit]
   Description=AI Resume Analyzer
   After=network.target
   
   [Service]
   Type=simple
   User=ec2-user
   WorkingDirectory=/home/ec2-user/AI-Resume-Analyzer
   ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   ```bash
   # Enable and start service
   sudo systemctl daemon-reload
   sudo systemctl enable resume-analyzer
   sudo systemctl start resume-analyzer
   
   # Check status
   sudo systemctl status resume-analyzer
   ```

5. **Configure Security Group**:
   - Allow inbound traffic on port 8501 (TCP)
   - Access your app at: `http://your-instance-ip:8501`

### Deploying on Heroku

1. **Install Heroku CLI**:
   ```bash
   # Visit https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Create Procfile**:
   ```bash
   echo "web: streamlit run --server.port=\$PORT --server.address=0.0.0.0 app.py" > Procfile
   ```

4. **Create setup.sh**:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@example.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   port = \$PORT\n\
   enableCORS = false\n\
   " > ~/.streamlit/config.toml
   ```

5. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Deploying on Docker

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**:
   ```bash
   docker build -t resume-analyzer .
   docker run -p 8501:8501 resume-analyzer
   ```

3. **Push to Docker Hub**:
   ```bash
   docker tag resume-analyzer yourusername/resume-analyzer
   docker push yourusername/resume-analyzer
   ```

## How It Works 🔍

### 1. PDF Text Extraction
- Uses PyPDF2 to extract text from uploaded PDF resumes
- Handles multi-page documents
- Cleans and processes extracted text

### 2. Skill Analysis
- Extracts skills using keyword matching against a comprehensive skill database
- Compares found skills with job role requirements
- Calculates match percentages for both required and preferred skills

### 3. ATS Score Calculation
- **Formatting**: Checks for clean formatting and proper structure
- **Structure**: Validates presence of standard resume sections
- **Keywords**: Analyzes skill and keyword density
- **Contact Info**: Verifies presence of email and phone number
- **Content Quality**: Evaluates content length and quantifiable metrics

### 4. Recommendations
- Generates personalized improvement suggestions based on analysis
- Prioritizes adding missing required skills
- Considers skill match percentage when making recommendations

## Configuration 🎨

### Customizing Job Roles

Edit `data/job_skills.json` to add or modify job roles:

```json
{
    "Your Job Title": {
        "description": "Job description",
        "salary_range": "$X - $Y",
        "required_skills": ["Skill1", "Skill2", ...],
        "preferred_skills": ["Skill1", "Skill2", ...]
    }
}
```

### Adjusting ATS Score Weights

Edit the weights in `utils/ats_calculator.py`:

```python
weights = {
    "formatting": 0.15,      # Formatting weight
    "structure": 0.20,       # Structure weight
    "keywords": 0.35,        # Keywords weight (highest)
    "contact": 0.15,         # Contact info weight
    "content": 0.15          # Content quality weight
}
```

## Technologies Used 🛠️

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web application framework |
| **PyPDF2** | PDF text extraction |
| **Plotly** | Interactive data visualization |
| **Pandas** | Data processing |
| **Python** | Core language |

## API Reference 📚

### PDF Extractor
```python
from utils.pdf_extractor import extract_text_from_pdf

# Extract text from PDF
resume_text = extract_text_from_pdf(uploaded_file)
```

### Skill Analyzer
```python
from utils.skill_analyzer import SkillAnalyzer

# Initialize
analyzer = SkillAnalyzer(job_roles_data)

# Extract skills
skills = analyzer.extract_skills_from_resume(resume_text)

# Compare with job
comparison = analyzer.compare_with_job_role(skills, "Software Engineer")

# Get suggestions
suggestions = analyzer.get_improvement_suggestions(comparison)
```

### ATS Calculator
```python
from utils.ats_calculator import ATSCalculator

# Calculate score
calculator = ATSCalculator()
result = calculator.calculate_ats_score(resume_text, found_skills)
```

## Troubleshooting 🐛

### Issue: "Module not found" error
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: PDF extraction fails
**Solution**: 
- Ensure PDF is text-based (not scanned image)
- Try converting PDF with an online tool
- Check file is not corrupted

### Issue: App runs slowly
**Solution**:
- Check internet connection
- Clear browser cache
- Restart the application

### Issue: "ModuleNotFoundError: No module named 'utils'"
**Solution**: Ensure you're running the app from the project root directory

## Best Practices 💡

1. **Resume Format**: Use standard fonts (Arial, Calibri, Times New Roman)
2. **Skill Listing**: Explicitly list skills in your resume
3. **Keywords**: Include relevant industry keywords
4. **Structure**: Use clear section headers (Experience, Education, Skills)
5. **Length**: Keep resume to 1-2 pages
6. **Contact Info**: Always include email and phone number

## Contributing 🤝

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see LICENSE file for details.

## Support 💬

For issues, feature requests, or questions:
- Open an Issue on GitHub
- Contact the development team
- Check the FAQ section in the app

## Roadmap 🗺️

Future features planned:
- [ ] LinkedIn integration
- [ ] Resume template suggestions
- [ ] Resume formatting corrections
- [ ] Cover letter analysis
- [ ] Interview questions based on resume
- [ ] Salary negotiation guidance
- [ ] Multiple resume comparison
- [ ] Machine learning-based skill recommendations
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] Resume optimization suggestions based on job descriptions

## Disclaimer ⚠️

This tool provides suggestions based on keyword matching and pattern analysis. 
While it gives valuable insights, human review of your resume is recommended 
before applying to jobs. The tool cannot guarantee job offers or ATS success.

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/)
- PDF processing with [PyPDF2](https://github.com/py-pdf/PyPDF2)
- Visualizations with [Plotly](https://plotly.com/)
- Data analysis with [Pandas](https://pandas.pydata.org/)

---

**Last Updated**: 2024
**Version**: 1.0.0

Happy resume analyzing! 🚀
