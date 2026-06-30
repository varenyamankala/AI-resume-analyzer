/**
 * AI Resume Analyzer - Frontend JavaScript
 * Handles API communication, UI updates, and analytics
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000/api';
let selectedFile = null;
let currentAnalysisResult = null;
let skillsChart = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Resume Analyzer Frontend Initialized');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load job roles
    loadJobRoles();
    
    // Setup drag and drop
    setupDragAndDrop();
});

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            navigateTo(section);
        });
    });

    // File input
    document.getElementById('fileInput').addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0]);
    });
}

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Click to upload
    uploadArea.addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
}

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    if (file.type !== 'application/pdf') {
        Swal.fire({
            icon: 'error',
            title: 'Invalid File',
            text: 'Please upload a PDF file'
        });
        return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        Swal.fire({
            icon: 'error',
            title: 'File Too Large',
            text: 'Please upload a file smaller than 10MB'
        });
        return;
    }

    selectedFile = file;
    
    // Show file info
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.innerHTML = `
        <div class="upload-content">
            <div style="font-size: 2rem; margin-bottom: 1rem;">✓</div>
            <h3>${file.name}</h3>
            <p>${(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <button class="btn btn-secondary" onclick="document.getElementById('fileInput').click()" style="margin-top: 1rem;">
                Change File
            </button>
        </div>
    `;

    // Show job role selection
    document.getElementById('jobRoleSection').style.display = 'block';
    document.getElementById('analyzeButtonSection').style.display = 'block';
}

/**
 * Load available job roles
 */
async function loadJobRoles() {
    try {
        const response = await fetch(`${API_BASE_URL}/job-roles`);
        const data = await response.json();

        if (data.success) {
            const jobRoleSelect = document.getElementById('jobRole');
            
            // Clear existing options (keep the first empty one)
            jobRoleSelect.innerHTML = '<option value="">-- Select a job role --</option>';
            
            // Add role options
            data.roles.forEach(role => {
                const option = document.createElement('option');
                option.value = role.name;
                option.textContent = role.name;
                jobRoleSelect.appendChild(option);
            });

            // Display roles in about section
            displayJobRolesInAbout(data.roles);
        }
    } catch (error) {
        console.error('Error loading job roles:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to load job roles. Make sure the backend is running.'
        });
    }
}

/**
 * Display job roles in about section
 */
function displayJobRolesInAbout(roles) {
    const rolesGrid = document.getElementById('rolesGrid');
    rolesGrid.innerHTML = '';

    roles.forEach(role => {
        const card = document.createElement('div');
        card.className = 'role-card';
        card.innerHTML = `
            <strong>${role.name}</strong><br>
            ${role.salary_range}<br>
            <small>${role.required_skills_count} required skills</small>
        `;
        rolesGrid.appendChild(card);
    });
}

/**
 * Analyze resume
 */
async function analyzeResume() {
    if (!selectedFile) {
        Swal.fire({
            icon: 'error',
            title: 'No File Selected',
            text: 'Please select a resume file first'
        });
        return;
    }

    const jobRole = document.getElementById('jobRole').value;
    if (!jobRole) {
        Swal.fire({
            icon: 'error',
            title: 'No Job Role Selected',
            text: 'Please select a target job role'
        });
        return;
    }

    // Show loading indicator
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('job_role', jobRole);

        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const result = await response.json();
        currentAnalysisResult = result;

        // Display results
        displayResults(result);

        // Hide loading, show results
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';

    } catch (error) {
        console.error('Error analyzing resume:', error);
        document.getElementById('loadingIndicator').style.display = 'none';
        
        Swal.fire({
            icon: 'error',
            title: 'Analysis Failed',
            text: error.message || 'An error occurred during analysis'
        });
    }
}

/**
 * Display analysis results
 */
function displayResults(result) {
    // File Information
    document.getElementById('fileName').textContent = result.file_info.filename;
    document.getElementById('filePages').textContent = result.file_info.pages;
    document.getElementById('fileSize').textContent = result.file_info.size_mb + ' MB';
    document.getElementById('skillsFound').textContent = result.skills_found.total;

    // ATS Score
    const atsScore = result.ats_score;
    const atsScoreDisplay = document.getElementById('atsScoreDisplay');
    atsScoreDisplay.innerHTML = `${Math.round(atsScore)}<span style="font-size: 1rem; color: #999;">/100</span>`;

    // Set color based on score
    let scoreColor = '#e74c3c';
    if (atsScore >= 80) scoreColor = '#2ecc71';
    else if (atsScore >= 60) scoreColor = '#f39c12';
    else if (atsScore >= 40) scoreColor = '#e67e22';
    
    atsScoreDisplay.style.color = scoreColor;

    document.getElementById('atsStatus').innerHTML = `
        <strong>Status:</strong> ${result.ats_status}
    `;

    // ATS Breakdown
    const atsBreakdown = document.getElementById('atsBreakdown');
    atsBreakdown.innerHTML = '';
    Object.entries(result.ats_breakdown).forEach(([key, value]) => {
        const item = document.createElement('div');
        item.className = 'ats-item';
        item.innerHTML = `
            <div class="ats-item-label">${formatLabel(key)}</div>
            <div class="ats-item-score">${Math.round(value)}</div>
        `;
        atsBreakdown.appendChild(item);
    });

    // ATS Feedback
    const atsFeedback = document.getElementById('atsFeedback');
    atsFeedback.innerHTML = '<ul>';
    result.ats_feedback.forEach(feedback => {
        atsFeedback.innerHTML += `<li>${feedback}</li>`;
    });
    atsFeedback.innerHTML += '</ul>';

    // Job Role Analysis (if available)
    if (result.job_role_analysis) {
        displayJobRoleAnalysis(result.job_role_analysis, result.skills_found.top_skills);
    }
}

/**
 * Display job role analysis
 */
function displayJobRoleAnalysis(analysis, topSkills) {
    // Show analysis card
    document.getElementById('skillsAnalysisCard').style.display = 'block';
    document.getElementById('recommendationsCard').style.display = 'block';

    // Update metrics
    document.getElementById('requiredMatch').textContent = 
        `${analysis.matched_required_count}/${analysis.total_required_skills}`;
    document.getElementById('requiredPercent').textContent = 
        `${analysis.required_match_percentage}%`;

    document.getElementById('preferredMatch').textContent = 
        `${analysis.matched_preferred_count}/${analysis.total_preferred_skills}`;
    document.getElementById('preferredPercent').textContent = 
        `${analysis.preferred_match_percentage}%`;

    // Display matched skills
    displaySkillsList('matchedRequired', analysis.matched_required_skills, true);
    displaySkillsList('missingRequired', analysis.missing_required_skills, false);

    // Display skills chart
    displaySkillsChart(topSkills);

    // Display suggestions
    displaySuggestions(analysis.suggestions);
}

/**
 * Display skills list
 */
function displaySkillsList(elementId, skills, isMatched) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    if (skills.length === 0) {
        container.innerHTML = '<p style="color: #999; font-size: 0.9rem;">None</p>';
        return;
    }

    skills.forEach(skill => {
        const tag = document.createElement('span');
        tag.className = isMatched ? 'skill-tag matched' : 'skill-tag missing';
        tag.textContent = skill;
        container.appendChild(tag);
    });
}

/**
 * Display skills chart
 */
function displaySkillsChart(topSkills) {
    const ctx = document.getElementById('skillsChart');
    
    if (skillsChart) {
        skillsChart.destroy();
    }

    const skills = Object.keys(topSkills);
    const frequencies = Object.values(topSkills);

    skillsChart = new Chart(ctx, {
        type: 'barHorizontal',
        data: {
            labels: skills,
            datasets: [{
                label: 'Frequency',
                data: frequencies,
                backgroundColor: 'rgba(102, 126, 234, 0.7)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { beginAtZero: true }
            }
        }
    });
}

/**
 * Display suggestions
 */
function displaySuggestions(suggestions) {
    const container = document.getElementById('suggestions');
    container.innerHTML = '';

    suggestions.forEach((suggestion, index) => {
        const item = document.createElement('div');
        item.className = 'suggestion';
        item.innerHTML = `<strong>${index + 1}.</strong> ${suggestion}`;
        container.appendChild(item);
    });
}

/**
 * Download report
 */
function downloadReport() {
    if (!currentAnalysisResult) {
        Swal.fire({
            icon: 'error',
            title: 'No Results',
            text: 'No analysis results to download'
        });
        return;
    }

    const result = currentAnalysisResult;
    let report = `AI RESUME ANALYZER REPORT\n`;
    report += `Generated: ${new Date().toLocaleString()}\n`;
    report += `${'='.repeat(50)}\n\n`;

    // File Info
    report += `FILE INFORMATION\n`;
    report += `Name: ${result.file_info.filename}\n`;
    report += `Pages: ${result.file_info.pages}\n`;
    report += `Size: ${result.file_info.size_mb} MB\n\n`;

    // Skills Found
    report += `SKILLS FOUND: ${result.skills_found.total}\n`;
    report += `Top Skills:\n`;
    Object.entries(result.skills_found.top_skills).forEach(([skill, freq]) => {
        report += `  • ${skill}: ${freq}\n`;
    });
    report += `\n`;

    // ATS Score
    report += `ATS SCORE ANALYSIS\n`;
    report += `Score: ${Math.round(result.ats_score)}/100\n`;
    report += `Status: ${result.ats_status}\n`;
    report += `Breakdown:\n`;
    Object.entries(result.ats_breakdown).forEach(([category, score]) => {
        report += `  • ${formatLabel(category)}: ${Math.round(score)}\n`;
    });
    report += `Feedback:\n`;
    result.ats_feedback.forEach(feedback => {
        report += `  • ${feedback}\n`;
    });
    report += `\n`;

    // Job Role Analysis
    if (result.job_role_analysis) {
        const analysis = result.job_role_analysis;
        report += `JOB ROLE ANALYSIS: ${analysis.job_role}\n`;
        report += `Salary Range: ${analysis.salary_range}\n`;
        report += `Required Skills: ${analysis.matched_required_count}/${analysis.total_required_skills} (${analysis.required_match_percentage}%)\n`;
        report += `Preferred Skills: ${analysis.matched_preferred_count}/${analysis.total_preferred_skills} (${analysis.preferred_match_percentage}%)\n\n`;

        report += `Matched Required Skills:\n`;
        analysis.matched_required_skills.forEach(skill => {
            report += `  ✓ ${skill}\n`;
        });

        if (analysis.missing_required_skills.length > 0) {
            report += `\nMissing Required Skills:\n`;
            analysis.missing_required_skills.forEach(skill => {
                report += `  ✗ ${skill}\n`;
            });
        }

        report += `\nRecommendations:\n`;
        analysis.suggestions.forEach((suggestion, i) => {
            report += `  ${i + 1}. ${suggestion}\n`;
        });
    }

    // Download
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
    element.setAttribute('download', `resume_analysis_${new Date().getTime()}.txt`);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);

    Swal.fire({
        icon: 'success',
        title: 'Downloaded',
        text: 'Report downloaded successfully'
    });
}

/**
 * Reset analyzer
 */
function resetAnalyzer() {
    selectedFile = null;
    currentAnalysisResult = null;

    document.getElementById('uploadArea').innerHTML = `
        <div class="upload-content">
            <div class="upload-icon">📄</div>
            <h3>Drag & Drop your PDF Resume</h3>
            <p>or</p>
            <button class="btn btn-secondary" onclick="document.getElementById('fileInput').click()">
                Click to Browse
            </button>
            <input type="file" id="fileInput" accept=".pdf" style="display: none;">
        </div>
    `;

    document.getElementById('jobRoleSection').style.display = 'none';
    document.getElementById('analyzeButtonSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingIndicator').style.display = 'none';

    // Re-setup file input listener
    document.getElementById('fileInput').addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0]);
    });

    Swal.fire({
        icon: 'success',
        title: 'Ready',
        text: 'Upload another resume to analyze'
    });
}

/**
 * Navigate to section
 */
function navigateTo(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionName).classList.add('active');

    // Add active class to clicked nav link
    document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');
}

/**
 * Utility function to format label
 */
function formatLabel(label) {
    return label
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        navigateTo,
        analyzeResume,
        downloadReport,
        resetAnalyzer
    };
}
