#!/usr/bin/env python3
"""
Demo script for AI Study Buddy
Run this to start the application with sample data
"""

import flet as ft
from study_app import main

if __name__ == "__main__":
    print("🚀 Starting AI Study Buddy...")
    print("📚 Upload a document (TXT, PDF, DOCX, PPTX, EPUB) to get started!")
    print("🤖 AI features available with Gemini API key")
    print("💡 Demo mode uses mock data if no API key is configured")
    print("-" * 50)
    
    # Run the Flet app
    ft.app(target=main, view=ft.AppView.FLET_APP)
