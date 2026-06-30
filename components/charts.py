"""
Charts Module

This module generates visualizations for skill matching and ATS score analysis.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd


def create_skill_match_chart(comparison_data: Dict) -> go.Figure:
    """
    Create a bar chart showing matched vs missing required skills.
    
    Args:
        comparison_data: Comparison data from skill analyzer
        
    Returns:
        Plotly figure object
    """
    categories = ['Matched', 'Missing']
    values = [
        comparison_data['matched_required_count'],
        len(comparison_data['missing_required_skills'])
    ]
    colors = ['#2ECC71', '#E74C3C']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(color=colors),
            text=values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f"Skill Match for {comparison_data['job_role']} Position",
        xaxis_title="Status",
        yaxis_title="Number of Skills",
        template="plotly_white",
        height=400,
        showlegend=False
    )
    
    return fig


def create_skill_match_gauge(required_match_percentage: float, 
                            preferred_match_percentage: float) -> go.Figure:
    """
    Create gauge charts showing match percentages.
    
    Args:
        required_match_percentage: Percentage of required skills matched
        preferred_match_percentage: Percentage of preferred skills matched
        
    Returns:
        Plotly figure object with subplots
    """
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=("Required Skills Match", "Preferred Skills Match")
    )
    
    # Required skills gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=required_match_percentage,
            title={'text': "Required %"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3498DB"},
                'steps': [
                    {'range': [0, 25], 'color': "#ECF0F1"},
                    {'range': [25, 50], 'color': "#F39C12"},
                    {'range': [50, 75], 'color': "#27AE60"},
                    {'range': [75, 100], 'color': "#2ECC71"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ),
        row=1, col=1
    )
    
    # Preferred skills gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=preferred_match_percentage,
            title={'text': "Preferred %"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#9B59B6"},
                'steps': [
                    {'range': [0, 25], 'color': "#ECF0F1"},
                    {'range': [25, 50], 'color': "#F39C12"},
                    {'range': [50, 75], 'color': "#27AE60"},
                    {'range': [75, 100], 'color': "#2ECC71"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 2},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig


def create_ats_score_gauge(ats_score: float) -> go.Figure:
    """
    Create a gauge chart for ATS score.
    
    Args:
        ats_score: ATS compatibility score (0-100)
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ats_score,
        title={'text': "ATS Score"},
        delta={'reference': 70},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#E74C3C"},
            'steps': [
                {'range': [0, 25], 'color': "#FADBD8"},
                {'range': [25, 50], 'color': "#F5B7B1"},
                {'range': [50, 75], 'color': "#F1948A"},
                {'range': [75, 100], 'color': "#EC7063"}
            ],
            'threshold': {
                'line': {'color': "darkred", 'width': 2},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig


def create_skills_list_chart(found_skills: Dict[str, int]) -> go.Figure:
    """
    Create a horizontal bar chart of top skills found in resume.
    
    Args:
        found_skills: Dictionary of skills and their frequencies
        
    Returns:
        Plotly figure object
    """
    # Sort and get top 15 skills
    top_skills = dict(sorted(found_skills.items(), key=lambda x: x[1], reverse=True)[:15])
    
    if not top_skills:
        # Create empty chart
        fig = go.Figure()
        fig.add_annotation(text="No skills found", showarrow=False)
        return fig
    
    fig = go.Figure(data=[
        go.Bar(
            y=list(top_skills.keys()),
            x=list(top_skills.values()),
            orientation='h',
            marker=dict(
                color=list(top_skills.values()),
                colorscale='Viridis'
            ),
            text=list(top_skills.values()),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Top Skills Found in Your Resume",
        xaxis_title="Frequency",
        yaxis_title="Skills",
        template="plotly_white",
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_ats_breakdown_chart(breakdown: Dict) -> go.Figure:
    """
    Create a radar chart showing ATS score breakdown by category.
    
    Args:
        breakdown: Dictionary with ATS breakdown data
        
    Returns:
        Plotly figure object
    """
    categories = list(breakdown.keys())
    scores = [breakdown[cat]['score'] for cat in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='ATS Score',
        line=dict(color='#3498DB'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        title="ATS Score Breakdown by Category",
        template="plotly_white",
        height=400
    )
    
    return fig
