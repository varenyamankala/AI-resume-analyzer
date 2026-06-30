"""
UI Components Module

This module contains reusable UI components and styling functions for the Streamlit app.
"""

import streamlit as st
from typing import List, Dict


def render_header():
    """Render the application header."""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("🎯")
    with col2:
        st.title("AI Resume Analyzer")
    st.markdown("---")
    st.markdown("""
    Upload your resume and analyze it against job requirements. Get insights on skill match, 
    ATS compatibility, and actionable recommendations to improve your resume.
    """)


def render_sidebar():
    """Render the sidebar with information and instructions."""
    with st.sidebar:
        st.header("ℹ️ How to Use")
        st.markdown("""
        1. **Upload Resume**: Upload your PDF resume
        2. **Select Job Role**: Choose a target job position
        3. **View Analysis**: See your skill match and ATS score
        4. **Get Suggestions**: Follow recommendations to improve
        
        ### Supported Job Roles:
        - Software Engineer
        - Data Scientist
        - Full Stack Developer
        - DevOps Engineer
        - Cloud Architect
        - Mobile Developer
        - Frontend Developer
        - Backend Developer
        """)
        
        st.markdown("---")
        st.subheader("📊 About ATS Score")
        st.info("""
        **ATS (Applicant Tracking System) Score** evaluates how well your resume 
        is formatted for automated systems:
        - **80-100**: Excellent ✓
        - **60-79**: Good ✓
        - **40-59**: Fair ⚠
        - **Below 40**: Needs improvement ✗
        """)


def render_skill_comparison(comparison_data: Dict):
    """
    Render skill comparison results.
    
    Args:
        comparison_data: Comparison data from skill analyzer
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Required Skills Match",
            f"{comparison_data['matched_required_count']}/{comparison_data['total_required_skills']}",
            f"{comparison_data['required_match_percentage']}%"
        )
    
    with col2:
        st.metric(
            "Preferred Skills Match",
            f"{comparison_data['matched_preferred_count']}/{comparison_data['total_preferred_skills']}",
            f"{comparison_data['preferred_match_percentage']}%"
        )
    
    with col3:
        st.metric(
            "Job Role",
            comparison_data['job_role'],
            comparison_data['salary_range']
        )
    
    st.markdown("---")
    
    # Display matched skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Matched Required Skills")
        if comparison_data['matched_required_skills']:
            for skill in sorted(comparison_data['matched_required_skills']):
                st.write(f"• {skill}")
        else:
            st.warning("No required skills matched")
    
    with col2:
        st.subheader("❌ Missing Required Skills")
        if comparison_data['missing_required_skills']:
            for skill in sorted(comparison_data['missing_required_skills']):
                st.write(f"• {skill}")
        else:
            st.success("All required skills matched!")
    
    # Display preferred skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Matched Preferred Skills")
        if comparison_data['matched_preferred_skills']:
            for skill in sorted(comparison_data['matched_preferred_skills']):
                st.write(f"• {skill}")
        else:
            st.info("No preferred skills matched")
    
    with col2:
        st.subheader("🎯 Missing Preferred Skills")
        if comparison_data['missing_preferred_skills']:
            for skill in sorted(comparison_data['missing_preferred_skills'][:10]):
                st.write(f"• {skill}")
            if len(comparison_data['missing_preferred_skills']) > 10:
                st.write(f"• ... and {len(comparison_data['missing_preferred_skills']) - 10} more")
        else:
            st.success("All preferred skills matched!")


def render_suggestions(suggestions: List[str]):
    """
    Render improvement suggestions.
    
    Args:
        suggestions: List of suggestion strings
    """
    st.subheader("💡 Recommendations to Improve Your Resume")
    
    for i, suggestion in enumerate(suggestions, 1):
        st.info(f"**{i}. {suggestion}**")


def render_ats_details(ats_result: Dict):
    """
    Render ATS score details and feedback.
    
    Args:
        ats_result: ATS calculation result dictionary
    """
    st.subheader("📋 ATS Analysis Details")
    
    # Display status
    status = ats_result['status']
    score = ats_result['ats_score']
    
    if score >= 80:
        st.success(f"**{status}**")
    elif score >= 60:
        st.info(f"**{status}**")
    elif score >= 40:
        st.warning(f"**{status}**")
    else:
        st.error(f"**{status}**")
    
    # Display feedback
    st.markdown("#### Detailed Feedback:")
    for feedback in ats_result['feedback']:
        st.write(feedback)


def render_resume_info(resume_info: Dict):
    """
    Render resume file information.
    
    Args:
        resume_info: Resume metadata dictionary
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("File Name", resume_info.get('file_name', 'N/A'))
    
    with col2:
        st.metric("Pages", resume_info.get('num_pages', 'N/A'))
    
    with col3:
        file_size_mb = resume_info.get('file_size', 0) / (1024 * 1024)
        st.metric("File Size", f"{file_size_mb:.2f} MB")


def render_download_report(comparison_data: Dict, ats_result: Dict):
    """
    Render download report button.
    
    Args:
        comparison_data: Comparison data from skill analyzer
        ats_result: ATS calculation result
    """
    # Create report text
    report = f"""
=== AI RESUME ANALYZER REPORT ===

Job Role: {comparison_data['job_role']}
Salary Range: {comparison_data['salary_range']}

=== SKILL ANALYSIS ===
Required Skills Match: {comparison_data['matched_required_count']}/{comparison_data['total_required_skills']} ({comparison_data['required_match_percentage']}%)
Preferred Skills Match: {comparison_data['matched_preferred_count']}/{comparison_data['total_preferred_skills']} ({comparison_data['preferred_match_percentage']}%)

Matched Required Skills:
{chr(10).join(f"• {skill}" for skill in comparison_data['matched_required_skills'])}

Missing Required Skills:
{chr(10).join(f"• {skill}" for skill in comparison_data['missing_required_skills'])}

=== ATS SCORE ===
Overall ATS Score: {ats_result['ats_score']}/100
Status: {ats_result['status']}

Breakdown:
{chr(10).join(f"• {cat}: {data['score']:.1f}/100" for cat, data in ats_result['breakdown'].items())}

Feedback:
{chr(10).join(f"• {feedback}" for feedback in ats_result['feedback'])}

=== RECOMMENDATIONS ===
{chr(10).join(f"{i}. {suggestion}" for i, suggestion in enumerate(st.session_state.get('suggestions', []), 1))}
"""
    
    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )
