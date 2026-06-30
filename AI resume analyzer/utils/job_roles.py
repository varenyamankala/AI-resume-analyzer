"""
Job Roles Module

This module loads and manages job role data including required skills, 
preferred skills, and job descriptions.
"""

import json
import logging
from pathlib import Path
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_job_roles_data() -> Dict:
    """
    Load job roles and skills data from JSON file.
    
    Returns:
        Dictionary containing job roles data
    """
    try:
        # Get the path to the job_skills.json file
        current_dir = Path(__file__).parent.parent
        data_path = current_dir / "data" / "job_skills.json"
        
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        logger.info(f"Successfully loaded job roles data from {data_path}")
        return data
    
    except FileNotFoundError:
        logger.error(f"Job skills data file not found at {data_path}")
        # Return default data if file not found
        return get_default_job_roles()
    
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from job skills file")
        return get_default_job_roles()


def get_default_job_roles() -> Dict:
    """
    Get default job roles data in case file loading fails.
    
    Returns:
        Dictionary with default job roles
    """
    return {
        "Software Engineer": {
            "description": "Develop and maintain software applications",
            "salary_range": "$100,000 - $180,000",
            "required_skills": [
                "Python", "Java", "JavaScript", "Git", "SQL", "REST API",
                "Object-Oriented Programming", "Data Structures", "Algorithms"
            ],
            "preferred_skills": [
                "Docker", "Kubernetes", "AWS", "CI/CD", "Microservices",
                "React", "Node.js", "MongoDB"
            ]
        },
        "Data Scientist": {
            "description": "Analyze data and build predictive models",
            "salary_range": "$110,000 - $190,000",
            "required_skills": [
                "Python", "SQL", "Statistics", "Machine Learning", "Data Analysis",
                "Pandas", "NumPy", "Scikit-learn", "R", "Excel"
            ],
            "preferred_skills": [
                "TensorFlow", "Deep Learning", "PyTorch", "Tableau", "Power BI",
                "Hadoop", "Spark", "Big Data"
            ]
        },
        "Full Stack Developer": {
            "description": "Develop front-end and back-end web applications",
            "salary_range": "$95,000 - $160,000",
            "required_skills": [
                "JavaScript", "HTML", "CSS", "React", "Node.js", "SQL",
                "REST API", "Git", "MongoDB", "Express"
            ],
            "preferred_skills": [
                "TypeScript", "Docker", "AWS", "CI/CD", "GraphQL",
                "Vue.js", "Angular", "PostgreSQL"
            ]
        },
        "DevOps Engineer": {
            "description": "Manage infrastructure and deployment pipelines",
            "salary_range": "$105,000 - $175,000",
            "required_skills": [
                "Linux", "Docker", "Kubernetes", "CI/CD", "Git", "AWS",
                "Terraform", "Jenkins", "Python", "Bash"
            ],
            "preferred_skills": [
                "Ansible", "Prometheus", "ELK Stack", "Azure", "GCP",
                "Scripting", "Networking", "Security"
            ]
        },
        "Cloud Architect": {
            "description": "Design and implement cloud-based solutions",
            "salary_range": "$120,000 - $200,000",
            "required_skills": [
                "AWS", "Azure", "Cloud Architecture", "Docker", "Kubernetes",
                "Networking", "Security", "SQL", "Python", "Infrastructure as Code"
            ],
            "preferred_skills": [
                "GCP", "Terraform", "Cost Optimization", "Microservices",
                "Machine Learning", "Big Data"
            ]
        },
        "Mobile Developer": {
            "description": "Develop mobile applications for iOS and Android",
            "salary_range": "$95,000 - $170,000",
            "required_skills": [
                "Swift", "Kotlin", "Java", "React Native", "Mobile UI",
                "REST API", "Git", "Firebase", "SQLite"
            ],
            "preferred_skills": [
                "Flutter", "Objective-C", "Xamarin", "MVVM", "Unit Testing",
                "App Store Deployment"
            ]
        },
        "Frontend Developer": {
            "description": "Build user interfaces and web applications",
            "salary_range": "$90,000 - $155,000",
            "required_skills": [
                "JavaScript", "React", "HTML", "CSS", "Git", "REST API",
                "Responsive Design", "CSS Frameworks", "Redux", "npm"
            ],
            "preferred_skills": [
                "TypeScript", "Vue.js", "Angular", "Next.js", "Tailwind CSS",
                "WebPack", "Testing Libraries"
            ]
        },
        "Backend Developer": {
            "description": "Build server-side applications and APIs",
            "salary_range": "$95,000 - $170,000",
            "required_skills": [
                "Python", "Java", "Node.js", "SQL", "REST API", "Databases",
                "Git", "Server Management", "Linux"
            ],
            "preferred_skills": [
                "GraphQL", "Docker", "Microservices", "Message Queues",
                "Caching", "PostgreSQL", "MongoDB"
            ]
        }
    }
