"""
Configuration loading utilities
File: src/config_loader.py
"""

import os
import yaml
from dotenv import load_dotenv

def load_env():
    """Load environment variables from .env file"""
    load_dotenv()
    return {
        "email": os.getenv("NAUKRI_EMAIL"),
        "password": os.getenv("NAUKRI_PASSWORD"),
        "headless": os.getenv("HEADLESS", "true").lower() == "true"
    }

def load_config():
    """Load configuration from config/config.yaml"""
    config_path = "config/config.yaml"
    
    if not os.path.exists(config_path):
        # Return default config if file doesn't exist
        return {
            "site": {
                "name": "naukri",
                "url": "https://www.naukri.com/mnjuser/profile"
            },
            "schedule": {
                "enabled": True,
                "mode": "daily",
                "time_ist": "09:32",
                "cron": "32 9 * * *"
            },
            "resume": {
                "path": "resumes/latest_resume.pdf"
            },
            "behavior": {
                "retry_on_fail": True,
                "max_retries": 2,
                "wait_after_login_sec": 4,
                "wait_after_upload_sec": 5
            },
            "observability": {
                "screenshots_on_error": True,
                "trace_on_error": False
            },
            "timezone": "Asia/Kolkata",
            "user_agent": "auto"
        }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return load_config()  # Return default config on error