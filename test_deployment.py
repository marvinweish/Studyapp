#!/usr/bin/env python3
"""
Test script to verify Study Buddy app works locally before AWS deployment
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flet',
        'google.generativeai',
        'dotenv',
        'PyPDF2',
        'docx',
        'pptx',
        'ebooklib',
        'bs4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai
            elif package == 'dotenv':
                import dotenv
            elif package == 'docx':
                import docx
            elif package == 'pptx':
                import pptx
            elif package == 'bs4':
                import bs4
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_api_key():
    """Check if Gemini API key is available"""
    # Check environment variable
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY found in environment")
        return True
    
    # Check key.env file
    if os.path.exists('key.env'):
        try:
            with open('key.env', 'r') as f:
                content = f.read()
                if 'GEMINI_API_KEY=' in content:
                    print("✅ GEMINI_API_KEY found in key.env")
                    return True
        except Exception as e:
            print(f"❌ Error reading key.env: {e}")
    
    # Check config.py
    try:
        import config
        if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
            print("✅ GEMINI_API_KEY found in config.py")
            return True
    except Exception as e:
        print(f"❌ Error importing config: {e}")
    
    print("⚠️ GEMINI_API_KEY not found. App will use mock data.")
    return True  # Not critical for testing

def check_app_files():
    """Check if required app files exist"""
    required_files = [
        'study_app.py',
        'file_processor.py',
        'ai_generator.py',
        'config.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    return True

def test_import():
    """Test if the main app can be imported"""
    try:
        import study_app
        print("✅ study_app.py imports successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing study_app: {e}")
        return False

def run_quick_test():
    """Run a quick test of the application"""
    try:
        print("🧪 Running quick functionality test...")
        
        # Test file processor
        from file_processor import FileProcessor, ContentOrganizer, get_supported_extensions
        processor = FileProcessor()
        extensions = get_supported_extensions()
        print(f"✅ File processor supports: {', '.join(extensions)}")
        
        # Test AI generator
        from ai_generator import AIStudyGenerator
        ai_gen = AIStudyGenerator()
        print("✅ AI generator initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Study Buddy Pre-Deployment Test")
    print("=" * 40)
    
    all_passed = True
    
    print("\n📋 Checking Python version...")
    if not check_python_version():
        all_passed = False
    
    print("\n📋 Checking dependencies...")
    if not check_dependencies():
        all_passed = False
    
    print("\n📋 Checking API key configuration...")
    check_api_key()  # Not critical for testing
    
    print("\n📋 Checking application files...")
    if not check_app_files():
        all_passed = False
    
    print("\n📋 Testing imports...")
    if not test_import():
        all_passed = False
    
    print("\n📋 Running functionality test...")
    if not run_quick_test():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Ready for deployment.")
        print("\n🚀 Next steps:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run deploy.py or deploy.bat to deploy to AWS")
        print("3. Or run 'python app.py' to test locally")
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
