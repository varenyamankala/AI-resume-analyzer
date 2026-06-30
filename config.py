"""
Configuration file for AI Resume Analyzer deployment
Contains settings for different deployment platforms
"""

# ============================================
# DEPLOYMENT CONFIGURATION
# ============================================

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "server": {
        "port": 8501,
        "headless": True,
        "enableCORS": False,
        "enableXsrfProtection": True,
    },
    "theme": {
        "primaryColor": "#2ECC71",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    }
}

# AWS EC2 Configuration
AWS_EC2_CONFIG = {
    "instance_type": "t2.micro",  # Free tier eligible
    "ami": "ami-0c55b159cbfafe1f0",  # Amazon Linux 2
    "security_group_rules": [
        {
            "protocol": "tcp",
            "port": 8501,
            "cidr_ip": "0.0.0.0/0"
        },
        {
            "protocol": "tcp",
            "port": 22,
            "cidr_ip": "0.0.0.0/0"
        }
    ]
}

# Heroku Configuration
HEROKU_CONFIG = {
    "buildpacks": [
        "heroku/python"
    ],
    "env": {
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_SERVER_PORT": "8501"
    }
}

# Docker Configuration
DOCKER_CONFIG = {
    "image_name": "ai-resume-analyzer",
    "tag": "latest",
    "ports": {
        "8501": "8501"
    },
    "environment": {
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_SERVER_ADDRESS": "0.0.0.0"
    }
}

# Application Settings
APP_CONFIG = {
    "max_upload_size": 10 * 1024 * 1024,  # 10 MB
    "supported_formats": ["pdf"],
    "min_resume_length": 50,  # characters
    "max_resume_length": 100000,  # characters
}

# ATS Score Weights
ATS_WEIGHTS = {
    "formatting": 0.15,
    "structure": 0.20,
    "keywords": 0.35,
    "contact": 0.15,
    "content": 0.15
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Feature Flags
FEATURES = {
    "enable_skill_suggestions": True,
    "enable_ats_score": True,
    "enable_report_download": True,
    "enable_analytics": False,
    "enable_user_authentication": False,
}

print("Configuration loaded successfully!")
