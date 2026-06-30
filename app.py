"""
AI Resume Analyzer - Main Application

This is a Streamlit web application for analyzing resumes against job requirements.
It provides insights on skill matching, ATS score calculation, and recommendations
for resume improvement.

Author: AI Resume Analyzer
Date: 2024
"""

import streamlit as st
import logging
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import custom modules
from utils.pdf_extractor import extract_text_from_pdf, get_pdf_info
from utils.skill_analyzer import SkillAnalyzer
from utils.ats_calculator import ATSCalculator
from utils.job_roles import load_job_roles_data
from components.ui import (
    render_header, render_sidebar, render_skill_comparison,
    render_suggestions, render_ats_details, render_resume_info,
    render_download_report
)
from components.charts import (
    create_skill_match_chart, create_skill_match_gauge,
    create_ats_score_gauge, create_skills_list_chart,
    create_ats_breakdown_chart
)


def initialize_session_state():
    """Initialize session state variables."""
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'resume_info' not in st.session_state:
        st.session_state.resume_info = None
    if 'comparison_data' not in st.session_state:
        st.session_state.comparison_data = None
    if 'ats_result' not in st.session_state:
        st.session_state.ats_result = None
    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = []
    if 'found_skills' not in st.session_state:
        st.session_state.found_skills = {}


def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Load job roles data
    try:
        job_roles_data = load_job_roles_data()
    except Exception as e:
        st.error(f"Error loading job roles data: {str(e)}")
        logger.error(f"Failed to load job roles: {e}")
        return
    
    # Render header and sidebar
    render_header()
    render_sidebar()
    
    # Main content area
    st.markdown("## 📤 Step 1: Upload Your Resume")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF format)",
        type=["pdf"],
        help="Please upload a PDF file of your resume"
    )
    
    if uploaded_file is not None:
        try:
            # Extract text from PDF
            with st.spinner("Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                resume_info = get_pdf_info(uploaded_file)
                
                # Store in session state
                st.session_state.resume_text = resume_text
                st.session_state.resume_info = resume_info
            
            # Display resume information
            st.success("✅ Resume uploaded successfully!")
            render_resume_info(resume_info)
            
            # Job role selection
            st.markdown("## 🎯 Step 2: Select Job Role")
            
            job_roles = sorted(list(job_roles_data.keys()))
            selected_job_role = st.selectbox(
                "Choose a job role to compare with your resume:",
                job_roles,
                index=0
            )
            
            if st.button("🔍 Analyze Resume", use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    try:
                        # Initialize analyzers
                        skill_analyzer = SkillAnalyzer(job_roles_data)
                        ats_calculator = ATSCalculator()
                        
                        # Extract skills from resume
                        found_skills = skill_analyzer.extract_skills_from_resume(resume_text)
                        st.session_state.found_skills = found_skills
                        
                        # Compare with job role
                        comparison_data = skill_analyzer.compare_with_job_role(
                            found_skills, selected_job_role
                        )
                        st.session_state.comparison_data = comparison_data
                        
                        # Calculate ATS score
                        ats_result = ats_calculator.calculate_ats_score(
                            resume_text, found_skills
                        )
                        st.session_state.ats_result = ats_result
                        
                        # Generate suggestions
                        suggestions = skill_analyzer.get_improvement_suggestions(comparison_data)
                        st.session_state.suggestions = suggestions
                        
                        logger.info(f"Analysis completed for {selected_job_role}")
                    
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        logger.error(f"Analysis error: {e}")
                        return
            
            # Display results if analysis has been performed
            if st.session_state.comparison_data is not None:
                st.markdown("---")
                st.markdown("## 📊 Step 3: View Analysis Results")
                
                # Tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📈 Skill Analysis",
                    "📋 ATS Score",
                    "💡 Recommendations",
                    "📄 Report"
                ])
                
                with tab1:
                    st.subheader("Skill Matching Analysis")
                    
                    # Display skill comparison metrics
                    render_skill_comparison(st.session_state.comparison_data)
                    
                    st.markdown("---")
                    
                    # Display charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            create_skill_match_chart(st.session_state.comparison_data),
                            use_container_width=True
                        )
                    with col2:
                        st.plotly_chart(
                            create_skill_match_gauge(
                                st.session_state.comparison_data['required_match_percentage'],
                                st.session_state.comparison_data['preferred_match_percentage']
                            ),
                            use_container_width=True
                        )
                    
                    # Display skills found in resume
                    st.plotly_chart(
                        create_skills_list_chart(st.session_state.found_skills),
                        use_container_width=True
                    )
                
                with tab2:
                    st.subheader("ATS Compatibility Analysis")
                    
                    # Display ATS gauge
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.plotly_chart(
                            create_ats_score_gauge(st.session_state.ats_result['ats_score']),
                            use_container_width=True
                        )
                    with col2:
                        st.plotly_chart(
                            create_ats_breakdown_chart(st.session_state.ats_result['breakdown']),
                            use_container_width=True
                        )
                    
                    st.markdown("---")
                    
                    # Display ATS details
                    render_ats_details(st.session_state.ats_result)
                
                with tab3:
                    st.subheader("Improvement Suggestions")
                    render_suggestions(st.session_state.suggestions)
                
                with tab4:
                    st.subheader("Generate Report")
                    st.write("Download a comprehensive analysis report of your resume.")
                    render_download_report(
                        st.session_state.comparison_data,
                        st.session_state.ats_result
                    )
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logger.error(f"Application error: {e}")
    
    else:
        # Display information when no file is uploaded
        st.info("👆 Please upload a PDF resume to get started with the analysis!")
        
        with st.expander("📖 How it works"):
            st.markdown("""
            1. **Upload**: Start by uploading your resume in PDF format
            2. **Select**: Choose a target job role you're interested in
            3. **Analyze**: Click the analyze button to get insights
            4. **Review**: View detailed skill matching and ATS analysis
            5. **Improve**: Follow the recommendations to enhance your resume
            
            ### Features:
            - 📊 **Skill Matching**: See which skills match the job requirements
            - 📋 **ATS Score**: Get an ATS compatibility rating for your resume
            - 💡 **Smart Recommendations**: Receive actionable advice to improve
            - 📈 **Visual Analytics**: Easy-to-understand charts and metrics
            - 📄 **Downloadable Reports**: Export your analysis results
            """)
        
        with st.expander("❓ FAQ"):
            st.markdown("""
            **Q: What is ATS?**
            A: ATS (Applicant Tracking System) is software used by companies to filter resumes. 
            Our score indicates how well your resume is optimized for automated systems.
            
            **Q: Why is my ATS score low?**
            A: Common reasons include complex formatting, lack of keywords, or poor structure. 
            Check the feedback for specific improvements.
            
            **Q: Can I use any PDF format?**
            A: Most PDF formats work, but text-based PDFs (not scanned images) work best.
            
            **Q: How accurate is the skill matching?**
            A: Our analysis uses keyword matching. Explicitly mention your skills for best results.
            """)


if __name__ == "__main__":
    main()
