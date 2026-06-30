"""
ATS Calculator Module

This module calculates the ATS (Applicant Tracking System) score for a resume.
ATS score is based on various factors like formatting, keyword matching, and structure.
"""

import re
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ATSCalculator:
    """Calculates ATS compatibility score for a resume."""
    
    # ATS-friendly keywords and patterns
    COMMON_SECTIONS = [
        "experience", "skills", "education", "summary", "professional",
        "certifications", "projects", "achievements", "contact", "objective"
    ]
    
    EDUCATION_KEYWORDS = ["bachelor", "master", "diploma", "phd", "b.s.", "m.s.", "university", "college"]
    EXPERIENCE_KEYWORDS = ["experience", "work", "employment", "job", "position", "role"]
    
    def __init__(self):
        """Initialize the ATS Calculator."""
        self.score = 0
        self.feedback = []
        self.breakdown = {}
    
    def calculate_ats_score(self, resume_text: str, found_skills: Dict[str, int]) -> Dict:
        """
        Calculate comprehensive ATS score for a resume.
        
        Args:
            resume_text: Extracted resume text
            found_skills: Skills found in the resume
            
        Returns:
            Dictionary containing ATS score and detailed breakdown
        """
        self.score = 0
        self.feedback = []
        self.breakdown = {}
        
        # Calculate individual scoring components
        formatting_score = self._check_formatting(resume_text)
        structure_score = self._check_structure(resume_text)
        keyword_score = self._check_keywords(found_skills, resume_text)
        contact_score = self._check_contact_info(resume_text)
        content_score = self._check_content_quality(resume_text)
        
        # Weighted average (adjust weights as needed)
        weights = {
            "formatting": 0.15,
            "structure": 0.20,
            "keywords": 0.35,
            "contact": 0.15,
            "content": 0.15
        }
        
        self.breakdown = {
            "formatting": {"score": formatting_score, "weight": weights["formatting"]},
            "structure": {"score": structure_score, "weight": weights["structure"]},
            "keywords": {"score": keyword_score, "weight": weights["keywords"]},
            "contact": {"score": contact_score, "weight": weights["contact"]},
            "content": {"score": content_score, "weight": weights["content"]},
        }
        
        # Calculate weighted score
        self.score = (
            formatting_score * weights["formatting"] +
            structure_score * weights["structure"] +
            keyword_score * weights["keywords"] +
            contact_score * weights["contact"] +
            content_score * weights["content"]
        )
        
        self.score = round(min(100, self.score), 2)  # Cap at 100
        
        logger.info(f"ATS Score calculated: {self.score}")
        
        return {
            "ats_score": self.score,
            "breakdown": self.breakdown,
            "feedback": self.feedback,
            "status": self._get_score_status(self.score)
        }
    
    def _check_formatting(self, resume_text: str) -> float:
        """Check formatting quality of resume."""
        score = 50  # Base score
        
        # Check for clean formatting (no excessive special characters)
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s\n.,;:\-]', resume_text)) / len(resume_text)
        if special_char_ratio < 0.05:
            score += 25
            self.feedback.append("✓ Good formatting - minimal special characters")
        else:
            score -= 10
            self.feedback.append("⚠ Consider reducing special characters for better ATS compatibility")
        
        # Check for proper line breaks
        lines = resume_text.split('\n')
        if 10 < len(lines) < 200:  # Reasonable number of lines
            score += 15
            self.feedback.append("✓ Good text structure with proper line breaks")
        else:
            score -= 5
            self.feedback.append("⚠ Check resume formatting for proper line breaks")
        
        # Check for tables or complex formatting (reduce score if present)
        if "|" in resume_text or "┌" in resume_text:
            score -= 20
            self.feedback.append("⚠ Avoid using tables or complex formatting - ATS may not parse them correctly")
        
        return min(100, score)
    
    def _check_structure(self, resume_text: str) -> float:
        """Check for standard resume sections."""
        score = 40  # Base score
        
        resume_lower = resume_text.lower()
        sections_found = 0
        
        # Check for standard sections
        for section in self.COMMON_SECTIONS:
            if section in resume_lower:
                sections_found += 1
        
        # Award points based on sections found
        section_score = (sections_found / len(self.COMMON_SECTIONS)) * 50
        score += section_score
        
        # Specific section checks
        if any(edu_kw in resume_lower for edu_kw in self.EDUCATION_KEYWORDS):
            score += 5
            self.feedback.append("✓ Education section detected")
        
        if any(exp_kw in resume_lower for exp_kw in self.EXPERIENCE_KEYWORDS):
            score += 5
            self.feedback.append("✓ Experience section detected")
        
        return min(100, score)
    
    def _check_keywords(self, found_skills: Dict[str, int], resume_text: str) -> float:
        """Check for relevant keywords and skills."""
        score = 30  # Base score
        
        num_skills = len(found_skills)
        
        # Award points based on number of skills
        if num_skills < 5:
            score += 10
        elif num_skills < 15:
            score += 30
        elif num_skills < 30:
            score += 50
        else:
            score += 60
        
        if num_skills > 0:
            self.feedback.append(f"✓ Found {num_skills} relevant skills in resume")
        else:
            self.feedback.append("⚠ Consider adding more relevant skills to your resume")
        
        # Check for action verbs (common in ATS-friendly resumes)
        action_verbs = [
            "managed", "developed", "led", "created", "designed", "implemented",
            "improved", "increased", "reduced", "solved", "achieved", "delivered"
        ]
        
        action_verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
        if action_verb_count > 5:
            score += 10
            self.feedback.append("✓ Good use of action verbs throughout resume")
        
        return min(100, score)
    
    def _check_contact_info(self, resume_text: str) -> float:
        """Check for proper contact information."""
        score = 50  # Base score
        
        # Check for email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if re.search(email_pattern, resume_text):
            score += 20
            self.feedback.append("✓ Email address found")
        else:
            score -= 10
            self.feedback.append("⚠ Consider adding your email address")
        
        # Check for phone number
        phone_pattern = r'(\+?1?\s?)?\(?[\d]{3}\)?[\s.-]?[\d]{3}[\s.-]?[\d]{4}'
        if re.search(phone_pattern, resume_text):
            score += 20
            self.feedback.append("✓ Phone number found")
        else:
            self.feedback.append("⚠ Consider adding your phone number")
        
        # Check for location
        location_keywords = ["location", "based", "city", "state"]
        if any(kw in resume_text.lower() for kw in location_keywords):
            score += 10
            self.feedback.append("✓ Location information found")
        
        return min(100, score)
    
    def _check_content_quality(self, resume_text: str) -> float:
        """Check content quality and completeness."""
        score = 50  # Base score
        
        # Check for minimum content length
        words = resume_text.split()
        if 200 < len(words) < 1000:
            score += 30
            self.feedback.append(f"✓ Appropriate resume length ({len(words)} words)")
        elif len(words) >= 1000:
            score -= 10
            self.feedback.append("⚠ Resume seems too long. Consider trimming to 1 page")
        elif len(words) < 50:
            score -= 30
            self.feedback.append("⚠ Resume is too short. Add more content")
        
        # Check for numbers and metrics (quantifiable achievements)
        number_pattern = r'\d+'
        numbers_found = len(re.findall(number_pattern, resume_text))
        if numbers_found > 10:
            score += 15
            self.feedback.append("✓ Good use of metrics and quantifiable achievements")
        else:
            score -= 5
            self.feedback.append("⚠ Add more quantifiable metrics to your achievements")
        
        return min(100, score)
    
    def _get_score_status(self, score: float) -> str:
        """
        Get status based on ATS score.
        
        Args:
            score: ATS score (0-100)
            
        Returns:
            Status string
        """
        if score >= 80:
            return "Excellent - Your resume is well-optimized for ATS"
        elif score >= 60:
            return "Good - Your resume has decent ATS compatibility"
        elif score >= 40:
            return "Fair - Consider making improvements to ATS compatibility"
        else:
            return "Poor - Significant improvements needed for better ATS compatibility"
