# Configuration file for AI Study Buddy - AWS App Runner Compatible

import os

# Detect AWS App Runner environment
IS_AWS_APP_RUNNER = bool(os.environ.get('AWS_EXECUTION_ENV') or os.environ.get('PORT'))

# Gemini API Configuration
# Priority: Environment variable > config value
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Study Settings
DEFAULT_FLASHCARD_COUNT = 10
DEFAULT_QUIZ_QUESTIONS = 5
DEFAULT_TEST_QUESTIONS = 10

# AWS App Runner optimizations
if IS_AWS_APP_RUNNER:
    USE_MOCK_DATA_IF_NO_API = False  # Don't use mock data in production
    # File storage for temporary files (App Runner has ephemeral storage)
    TEMP_DIR = "/tmp"
    # Ensure temp directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)
else:
    USE_MOCK_DATA_IF_NO_API = True  # Use mock data for local development
    TEMP_DIR = "temp"
    os.makedirs(TEMP_DIR, exist_ok=True)

# Port configuration for web deployment
PORT = int(os.environ.get('PORT', 8080))

# App Runner specific settings
WEB_RENDERER = os.environ.get('FLET_WEB_RENDERER', 'html')

print(f"🌐 Running in {'AWS App Runner' if IS_AWS_APP_RUNNER else 'Local'} mode")
if GEMINI_API_KEY:
    print("✅ Gemini API key configured")
else:
    print("⚠️ Gemini API key not found - using mock data" if USE_MOCK_DATA_IF_NO_API else "❌ Gemini API key required for production")
