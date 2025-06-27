# Configuration file for AI Study Buddy - AWS Compatible

import os

# Try to load from AWS config first, then fallback to original config
try:
    from aws_config import AWSConfig
    
    # Use AWS configuration if available
    GEMINI_API_KEY = AWSConfig.GEMINI_API_KEY
    USE_AWS_CONFIG = True
    
except ImportError:
    # Fallback to original configuration
    USE_AWS_CONFIG = False
    
    # Gemini API Configuration
    # The API key is automatically loaded from key.env file (recommended)
    # You can also:
    # 1. Set the GEMINI_API_KEY environment variable, or
    # 2. Replace the empty string below with your API key
    
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # Load from environment first

# Study Settings
if USE_AWS_CONFIG:
    # Use AWS configuration
    DEFAULT_FLASHCARD_COUNT = 10
    DEFAULT_QUIZ_QUESTIONS = 5
    DEFAULT_TEST_QUESTIONS = 10
    USE_MOCK_DATA_IF_NO_API = False  # Don't use mock data in production
else:
    # Use original settings
    DEFAULT_FLASHCARD_COUNT = 10
    DEFAULT_QUIZ_QUESTIONS = 5
    DEFAULT_TEST_QUESTIONS = 10
    USE_MOCK_DATA_IF_NO_API = True
