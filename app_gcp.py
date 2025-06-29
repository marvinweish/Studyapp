"""
GCP-compatible entry point for AI Study Buddy
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging for GCP
if os.environ.get('GAE_ENV') or os.environ.get('CLOUD_RUN_SERVICE'):
    # Structured logging for GCP
    try:
        import google.cloud.logging
        client = google.cloud.logging.Client()
        client.setup_logging()
    except ImportError:
        # Fallback if google-cloud-logging is not available
        logging.basicConfig(level=logging.INFO)
    
    # Set logging level
    logging.basicConfig(level=logging.INFO)
else:
    # Standard logging for local development
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def health_check():
    """Health check endpoint for GCP load balancers"""
    return {"status": "healthy", "service": "study-buddy"}

def main():
    """Main application entry point"""
    try:
        # Import and run the Flet app
        from study_app import main as app_main
        import flet as ft
        
        # Get port from environment
        port = int(os.environ.get('PORT', 8080))
        
        # Detect GCP environment
        is_gcp = bool(
            os.environ.get('GAE_ENV') or
            os.environ.get('CLOUD_RUN_SERVICE') or
            os.environ.get('K_SERVICE') or
            os.environ.get('GOOGLE_CLOUD_PROJECT')
        )
        
        if is_gcp:
            logger.info(f"🌐 Starting GCP web server on port {port}")
            ft.app(
                target=app_main,
                port=port,
                host='0.0.0.0',
                view=ft.AppView.WEB_BROWSER,
                web_renderer=ft.WebRenderer.HTML,
                route_url_strategy="hash"
            )
        else:
            logger.info("🖥️ Starting local desktop application")
            ft.app(target=app_main)
            
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()
