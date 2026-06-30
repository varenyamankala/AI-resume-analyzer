"""
Skill Analyzer Module

This module analyzes and extracts skills from resume text and compares them 
with required skills for different job roles.
"""

import re
import json
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillAnalyzer:
    """Analyzes skills in resume text and matches them with job requirements."""
    
    def __init__(self, job_roles_data: Dict):
        """
        Initialize the SkillAnalyzer with job roles data.
        
        Args:
            job_roles_data: Dictionary containing job roles and their required skills
        """
        self.job_roles_data = job_roles_data
        self.all_skills = self._extract_all_skills()
    
    def _extract_all_skills(self) -> List[str]:
        """
        Extract all unique skills from all job roles.
        
        Returns:
            List of all skills across all job roles
        """
        all_skills = set()
        for role_data in self.job_roles_data.values():
            all_skills.update(role_data.get("required_skills", []))
            all_skills.update(role_data.get("preferred_skills", []))
        return list(all_skills)
    
    def extract_skills_from_resume(self, resume_text: str) -> Dict[str, int]:
        """
        Extract skills from resume text using keyword matching.
        
        Args:
            resume_text: Extracted text from resume PDF
            
        Returns:
            Dictionary with skills as keys and frequency as values
        """
        # Convert resume text to lowercase for matching
        resume_lower = resume_text.lower()
        
        # Dictionary to store found skills and their frequencies
        found_skills = {}
        
        for skill in self.all_skills:
            # Use word boundary regex for more accurate matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            matches = len(re.findall(pattern, resume_lower))
            
            if matches > 0:
                found_skills[skill] = matches
        
        logger.info(f"Found {len(found_skills)} skills in resume")
        return found_skills
    
    def compare_with_job_role(self, found_skills: Dict[str, int], 
                             job_role: str) -> Dict:
        """
        Compare found skills with requirements for a specific job role.
        
        Args:
            found_skills: Dictionary of skills found in resume
            job_role: Name of the job role to compare with
            
        Returns:
            Dictionary containing skill comparison details
        """
        if job_role not in self.job_roles_data:
            raise ValueError(f"Job role '{job_role}' not found in database")
        
        role_data = self.job_roles_data[job_role]
        required_skills = set(role_data.get("required_skills", []))
        preferred_skills = set(role_data.get("preferred_skills", []))
        
        # Find matched and missing skills
        found_skills_set = set(found_skills.keys())
        
        matched_required = required_skills & found_skills_set
        missing_required = required_skills - found_skills_set
        matched_preferred = preferred_skills & found_skills_set
        missing_preferred = preferred_skills - found_skills_set
        
        # Calculate match percentage
        total_required = len(required_skills)
        matched_required_count = len(matched_required)
        required_match_percentage = (matched_required_count / total_required * 100) if total_required > 0 else 0
        
        total_preferred = len(preferred_skills)
        matched_preferred_count = len(matched_preferred)
        preferred_match_percentage = (matched_preferred_count / total_preferred * 100) if total_preferred > 0 else 0
        
        return {
            "job_role": job_role,
            "matched_required_skills": list(matched_required),
            "missing_required_skills": list(missing_required),
            "matched_required_count": matched_required_count,
            "total_required_skills": total_required,
            "required_match_percentage": round(required_match_percentage, 2),
            "matched_preferred_skills": list(matched_preferred),
            "missing_preferred_skills": list(missing_preferred),
            "matched_preferred_count": matched_preferred_count,
            "total_preferred_skills": total_preferred,
            "preferred_match_percentage": round(preferred_match_percentage, 2),
            "job_description": role_data.get("description", ""),
            "salary_range": role_data.get("salary_range", ""),
        }
    
    def get_improvement_suggestions(self, comparison_data: Dict) -> List[str]:
        """
        Generate suggestions to improve resume based on skill comparison.
        
        Args:
            comparison_data: Result from compare_with_job_role method
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        # Suggest adding missing required skills
        if comparison_data["missing_required_skills"]:
            missing = ", ".join(comparison_data["missing_required_skills"][:5])  # Top 5
            suggestions.append(f"Add experience with: {missing}")
        
        # Suggest adding missing preferred skills
        if comparison_data["missing_preferred_skills"]:
            missing = ", ".join(comparison_data["missing_preferred_skills"][:3])  # Top 3
            suggestions.append(f"Consider adding: {missing}")
        
        # Add general suggestions based on match percentage
        required_match = comparison_data["required_match_percentage"]
        if required_match < 50:
            suggestions.append("Your current skills don't strongly match this role. Consider pivoting or gaining more relevant experience.")
        elif required_match < 75:
            suggestions.append("You have a moderate match. Focus on acquiring the missing required skills.")
        elif required_match < 90:
            suggestions.append("You're a good fit! Polish your resume and highlight your matching skills.")
        else:
            suggestions.append("Excellent match! You have most of the required skills. Consider highlighting achievements.")
        
        return suggestions
    
    def get_all_job_roles(self) -> List[str]:
        """
        Get list of all available job roles.
        
        Returns:
            List of job role names
        """
        return list(self.job_roles_data.keys())
