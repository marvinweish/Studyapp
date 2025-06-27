# AWS-compatible web app entry point
import flet as ft
import os
from study_app import main

def main_web(page: ft.Page):
    """Main function adapted for web deployment"""
    # Set web-specific configurations
    page.title = "AI Study Buddy"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Call the main app function
    main(page)

if __name__ == "__main__":
    # For local development
    ft.app(target=main_web, port=int(os.environ.get("PORT", 8080)))
else:
    # For production deployment
    def create_app():
        return ft.app(target=main_web, port=int(os.environ.get("PORT", 8080)), view=ft.AppView.WEB_BROWSER)
