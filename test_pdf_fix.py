"""Test script to verify PDF extraction fix"""

import requests
import json
from pathlib import Path

# Create a simple test PDF using reportlab
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO
except ImportError:
    print("Installing reportlab...")
    import subprocess
    subprocess.run(['pip', 'install', 'reportlab', '-q'], check=True)
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from io import BytesIO

def create_test_pdf():
    """Create a sample resume PDF for testing"""
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Write sample resume content
    y = 750
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "John Smith - Senior Software Engineer")
    
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Email: john@example.com | Phone: 555-0123")
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROFESSIONAL SUMMARY")
    
    y -= 15
    c.setFont("Helvetica", 10)
    summary = """Experienced Software Engineer with 7 years in full-stack development. 
Expert in Python, JavaScript, React, and SQL. Strong background in REST APIs, 
microservices, and cloud deployment on AWS."""
    
    for line in summary.split('\n'):
        c.drawString(50, y, line)
        y -= 12
    
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TECHNICAL SKILLS")
    
    y -= 15
    c.setFont("Helvetica", 10)
    skills = "Python, JavaScript, React, Node.js, SQL, PostgreSQL, Docker, AWS, Git, REST API, FastAPI, Vue.js"
    c.drawString(50, y, skills)
    
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "WORK EXPERIENCE")
    
    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Senior Developer | Tech Corp | 2020 - Present")
    
    y -= 12
    c.setFont("Helvetica", 10)
    duties = "• Led development of microservices architecture using Python and FastAPI\n• Built React frontends serving 1M+ users\n• Managed AWS infrastructure and deployment pipelines"
    for line in duties.split('\n'):
        c.drawString(50, y, line)
        y -= 12
    
    y -= 12
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Full Stack Developer | StartUp Inc | 2018 - 2020")
    
    y -= 12
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "• Developed full-stack web applications using JavaScript and Python")
    
    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EDUCATION")
    
    y -= 12
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Bachelor of Science in Computer Science | State University | 2018")
    
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

print("=" * 60)
print("Testing AI Resume Analyzer - PDF Extraction Fix")
print("=" * 60)

# Test 1: Health check
print("\n[1/3] Testing health check endpoint...")
try:
    response = requests.get("http://localhost:8000/api/health")
    if response.status_code == 200:
        print("[PASS] Health check passed")
        print(f"  Response: {response.json()}")
    else:
        print(f"[FAIL] Health check failed: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Error: {e}")

# Test 2: Get job roles
print("\n[2/3] Testing job roles endpoint...")
try:
    response = requests.get("http://localhost:8000/api/job-roles")
    if response.status_code == 200:
        data = response.json()
        print(f"[PASS] Retrieved {data['total_roles']} job roles")
        for role in data['roles'][:3]:
            print(f"  - {role['name']}")
    else:
        print(f"[FAIL] Failed to get job roles: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Error: {e}")

# Test 3: Test PDF upload and analysis
print("\n[3/3] Testing PDF upload and analysis...")
try:
    pdf_bytes = create_test_pdf()
    print("[PASS] Generated test PDF (sample resume)")
    
    files = {'file': ('test_resume.pdf', pdf_bytes, 'application/pdf')}
    data = {'job_role': 'Software Engineer'}
    
    response = requests.post("http://localhost:8000/api/analyze", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("[PASS] PDF upload and analysis successful!")
        print(f"\n  File: {result['file_info']['filename']}")
        print(f"  Pages: {result['file_info']['pages']}")
        print(f"  Size: {result['file_info']['size_mb']} MB")
        print(f"  ATS Score: {result['ats_score']}/100")
        print(f"  Skills Found: {result['skills_found']['total']}")
        print(f"  Top Skills: {list(result['skills_found']['top_skills'].keys())[:5]}")
        
        if 'job_role_analysis' in result:
            jra = result['job_role_analysis']
            print(f"\n  Job Role Analysis (Software Engineer):")
            print(f"    Required Skills Match: {jra['required_match_percentage']:.1f}%")
            print(f"    Preferred Skills Match: {jra['preferred_match_percentage']:.1f}%")
            print(f"    Suggestions: {len(jra['suggestions'])} recommendations")
        
        print("\n[SUCCESS] PDF EXTRACTION FIX SUCCESSFUL!")
    else:
        print(f"[FAIL] Analysis failed: {response.status_code}")
        print(f"  Error: {response.json()}")
except Exception as e:
    print(f"[FAIL] Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
