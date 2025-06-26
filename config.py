# Configuration file for AI Study Buddy

# Gemini API Configuration
# The API key is automatically loaded from key.env file (recommended)
# You can also:
# 1. Set the GEMINI_API_KEY environment variable, or
# 2. Replace the empty string below with your API key

GEMINI_API_KEY = ""  # Add your Gemini API key here (optional if using key.env)

# Note: The application will use this priority order:
# 1. key.env file (GEMINI_API_KEY=your_key)
# 2. This config file
# 3. System environment variables

# Study Settings
DEFAULT_FLASHCARD_COUNT = 10
DEFAULT_QUIZ_QUESTIONS = 5
DEFAULT_TEST_QUESTIONS = 10

# If no API key is provided, the app will use mock data for demonstration
USE_MOCK_DATA_IF_NO_API = True
