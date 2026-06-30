"""
API Testing Script for AI Resume Analyzer Backend

This script demonstrates all available API endpoints and shows sample output.

Usage: python test_api.py
"""

import requests
import json
from pprint import pprint
import time

# Configuration
BASE_URL = 'http://localhost:8000'
API_BASE = f'{BASE_URL}/api'

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_success(message):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def test_backend_connection():
    """Test backend connection."""
    print_section("1. Testing Backend Connection")
    
    try:
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200:
            print_success(f"Backend is running on {BASE_URL}")
            data = response.json()
            print(f"   Message: {data['message']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to {BASE_URL}")
        print_info("Make sure the backend is running: python run_backend.py")
        return False

def test_health_check():
    """Test health check endpoint."""
    print_section("2. Testing Health Check")
    
    try:
        response = requests.get(f'{API_BASE}/health')
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Job roles loaded: {data['job_roles_loaded']}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_get_job_roles():
    """Test getting job roles."""
    print_section("3. Testing Job Roles Endpoint")
    
    try:
        response = requests.get(f'{API_BASE}/job-roles')
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Retrieved {data['total_roles']} job roles")
                print(f"\nAvailable Job Roles:")
                for i, role in enumerate(data['roles'], 1):
                    print(f"   {i}. {role['name']}")
                    print(f"      └─ {role['salary_range']}")
                    print(f"         Required: {role['required_skills_count']} skills | Preferred: {role['preferred_skills_count']} skills")
                return True
            else:
                print_error("Response not successful")
                return False
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_get_job_role_details():
    """Test getting specific job role details."""
    print_section("4. Testing Job Role Details Endpoint")
    
    try:
        role_name = "Software Engineer"
        response = requests.get(f'{API_BASE}/job-roles/{role_name}')
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Retrieved details for {role_name}")
                print(f"\nJob Role: {data['role_name']}")
                print(f"Salary Range: {data['salary_range']}")
                print(f"Description: {data['description']}")
                print(f"\nRequired Skills ({len(data['required_skills'])}):")
                for skill in data['required_skills'][:5]:
                    print(f"   • {skill}")
                if len(data['required_skills']) > 5:
                    print(f"   ... and {len(data['required_skills']) - 5} more")
                return True
            else:
                print_error("Response not successful")
                return False
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_statistics():
    """Test statistics endpoint."""
    print_section("5. Testing Statistics Endpoint")
    
    try:
        response = requests.get(f'{API_BASE}/statistics')
        if response.status_code == 200:
            data = response.json()
            print_success("Retrieved statistics")
            print(f"   Total Analyses: {data['total_analyses']}")
            print(f"   Job Roles Available: {data['job_roles_available']}")
            print(f"   API Version: {data['api_version']}")
            print(f"   Status: {data['status']}")
            return True
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_batch_analyze():
    """Test batch analyze template."""
    print_section("6. Testing Batch Analyze Template")
    
    try:
        role_name = "Data Scientist"
        response = requests.get(f'{API_BASE}/batch-analyze?job_role={role_name}')
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Retrieved template for {role_name}")
                template = data['template']
                print(f"\nJob Role: {template['job_role']}")
                print(f"Salary Range: {template['salary_range']}")
                print(f"Required Skills: {', '.join(template['required_skills'][:3])}...")
                print(f"Preferred Skills: {', '.join(template['preferred_skills'][:3])}...")
                return True
            else:
                print_error("Response not successful")
                return False
        else:
            print_error(f"Request failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def print_sample_responses():
    """Print sample API responses."""
    print_section("7. Sample API Responses")
    
    print(f"{Colors.BOLD}Sample Success Response (Analyze Endpoint):{Colors.ENDC}")
    sample_response = {
        "success": True,
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
            "✓ Email address found"
        ]
    }
    print(json.dumps(sample_response, indent=2))

def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("AI Resume Analyzer - API Testing")
    print("=" * 70)
    print(f"{Colors.ENDC}\n")
    
    print_info(f"Testing API at: {API_BASE}")
    print_info("Make sure the backend is running before starting tests\n")
    
    # Run tests
    tests = [
        ("Backend Connection", test_backend_connection),
        ("Health Check", test_health_check),
        ("Job Roles List", test_get_job_roles),
        ("Job Role Details", test_get_job_role_details),
        ("Statistics", test_statistics),
        ("Batch Analyze Template", test_batch_analyze),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Test failed with exception: {e}")
            results[test_name] = False
        
        time.sleep(0.5)  # Small delay between tests
    
    # Print sample responses
    print_sample_responses()
    
    # Print summary
    print_section("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
        print(f"{status} - {test_name}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.ENDC}\n")
    
    if passed == total:
        print_success("All tests passed! Backend is working correctly.")
        print_info("Frontend can now communicate with the backend.")
    else:
        print_error("Some tests failed. Check backend logs for details.")
    
    print()

if __name__ == "__main__":
    main()
