#!/usr/bin/env python3
"""
Test script to verify AI integration is working properly
"""

import sys
import os

def test_ai_integration():
    print("🧪 Testing AI Integration...")
    print("-" * 40)
    
    try:
        # Test environment loading
        from dotenv import load_dotenv
        load_dotenv('key.env')
        print("✅ Environment file loaded")
        
        # Test API key availability
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
        else:
            print("❌ No API key found")
            return False
        
        # Test AI generator initialization
        from ai_generator import AIStudyGenerator
        ai_generator = AIStudyGenerator()
        
        if ai_generator.model:
            print("✅ Gemini model initialized successfully")
        else:
            print("❌ Failed to initialize Gemini model")
            return False
        
        print("\n🎉 All tests passed! AI integration is ready.")
        print("\n📚 You can now:")
        print("   • Upload documents")
        print("   • Generate AI-powered flashcards")
        print("   • Create quizzes and tests")
        print("   • Study with interactive content")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_integration()
    sys.exit(0 if success else 1)
