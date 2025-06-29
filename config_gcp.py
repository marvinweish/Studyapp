# Configuration file for AI Study Buddy - GCP Compatible

import os

# Detect GCP environment
IS_GCP = bool(
    os.environ.get('GAE_ENV') or  # App Engine
    os.environ.get('CLOUD_RUN_SERVICE') or  # Cloud Run
    os.environ.get('K_SERVICE') or  # Cloud Run (Knative)
    os.environ.get('GOOGLE_CLOUD_PROJECT')  # General GCP
)

# Gemini API Configuration
# Priority: Environment variable > config value
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Study Settings
DEFAULT_FLASHCARD_COUNT = 10
DEFAULT_QUIZ_QUESTIONS = 5
DEFAULT_TEST_QUESTIONS = 10

# GCP optimizations
if IS_GCP:
    USE_MOCK_DATA_IF_NO_API = False  # Don't use mock data in production
    # File storage for temporary files (GCP has ephemeral storage)
    TEMP_DIR = "/tmp"
    # Ensure temp directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)
else:
    USE_MOCK_DATA_IF_NO_API = True  # Use mock data for local development
    TEMP_DIR = "temp"
    os.makedirs(TEMP_DIR, exist_ok=True)

# Port configuration for web deployment
PORT = int(os.environ.get('PORT', 8080))

# GCP specific settings
WEB_RENDERER = os.environ.get('FLET_WEB_RENDERER', 'html')

# Logging configuration for GCP
ENABLE_STRUCTURED_LOGGING = IS_GCP

print(f"🌐 Running in {'GCP' if IS_GCP else 'Local'} mode")
if GEMINI_API_KEY:
    print("✅ Gemini API key configured")
else:
    print("⚠️ Gemini API key not found - using mock data" if USE_MOCK_DATA_IF_NO_API else "❌ Gemini API key required for production")
