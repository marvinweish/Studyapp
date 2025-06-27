# Configuration for AWS deployment
import os
from typing import Optional

class AWSConfig:
    """Configuration settings for AWS deployment"""
    
    # Port configuration
    PORT = int(os.environ.get("PORT", 8080))
    
    # API Keys
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    
    # File storage (use /tmp for temporary files in AWS Lambda/App Runner)
    TEMP_DIR = os.environ.get("TEMP_DIR", "/tmp")
    
    # Database configuration (for future use)
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    
    # AWS specific settings
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    
    # Application settings
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    @classmethod
    def get_config(cls) -> dict:
        """Get all configuration as a dictionary"""
        return {
            "port": cls.PORT,
            "gemini_api_key": cls.GEMINI_API_KEY,
            "temp_dir": cls.TEMP_DIR,
            "database_url": cls.DATABASE_URL,
            "aws_region": cls.AWS_REGION,
            "debug": cls.DEBUG
        }
    
    @classmethod
    def validate_config(cls) -> tuple[bool, list[str]]:
        """Validate configuration and return errors if any"""
        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY environment variable is required")
        
        if not os.path.exists(cls.TEMP_DIR):
            try:
                os.makedirs(cls.TEMP_DIR, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create temp directory {cls.TEMP_DIR}: {e}")
        
        return len(errors) == 0, errors
