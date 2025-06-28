#!/usr/bin/env python3
"""
App Runner compatibility test
Tests Python 3.8 compatibility and required dependencies
"""

import sys
import subprocess

def test_python_version():
    """Test if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible with App Runner")
        return True
    else:
        print("❌ Python version not compatible")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    packages_to_test = [
        'flet',
        'google.generativeai',
        'dotenv',
        'PyPDF2',
        'docx',
        'pptx',
        'ebooklib',
        'bs4',
        'requests'
    ]
    
    failed_imports = []
    for package in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_flet_web():
    """Test if Flet can run in web mode"""
    try:
        import flet as ft
        print("✅ Flet imported successfully")
        
        # Test web renderer
        if hasattr(ft, 'WebRenderer'):
            print("✅ Web renderer available")
        else:
            print("⚠️ Web renderer not available in this version")
        
        return True
    except Exception as e:
        print(f"❌ Flet test failed: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("🧪 App Runner Compatibility Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_imports),
        ("Flet Web Mode", test_flet_web)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! App Runner deployment should work.")
        return True
    else:
        print("⚠️ Some tests failed. Fix issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
