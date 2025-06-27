"""
Demo script showing how to package AI Study Buddy for different platforms
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🏗️ AI Study Buddy - Packaging Demo")
    print("=" * 50)
    print()
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if we're in the right directory
    if not (current_dir / "study_app.py").exists():
        print("❌ Error: study_app.py not found!")
        print("Please run this script from the AI Study Buddy directory.")
        return
    
    print("✅ Found study_app.py")
    
    # Check if build scripts exist
    build_scripts = [
        "build_desktop.bat",
        "build_android.bat", 
        "build_cross_platform.sh",
        "build_app.py"
    ]
    
    print("\n📋 Checking build scripts:")
    for script in build_scripts:
        if (current_dir / script).exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - Missing!")
    
    print("\n🎯 Available packaging options:")
    print("1. Windows Desktop (.exe) - Use: .\\build_desktop.bat")
    print("2. Android APK - Use: .\\build_android.bat")
    print("3. Cross-platform - Use: python build_app.py")
    print("4. Manual Flet commands")
    
    print("\n💡 Quick start commands:")
    print("For Windows Desktop:")
    print("  .\\build_desktop.bat")
    print()
    print("For Android APK:")
    print("  .\\build_android.bat")
    print()
    print("For Python build script:")
    print("  python build_app.py")
    
    print("\n🔧 Manual Flet commands:")
    print("Desktop: flet pack study_app.py --name 'AI Study Buddy'")
    print("Android: flet build apk --project 'AI Study Buddy' --org 'com.studybuddy'")
    print("Web:     flet build web --project 'AI Study Buddy' --org 'com.studybuddy'")
    
    # Check if Flet is installed
    try:
        import flet
        print(f"\n✅ Flet is installed and ready to use")
    except ImportError:
        print("\n❌ Flet is not installed!")
        print("Install with: pip install flet")
        return
    
    print("\n🚀 Ready to build! Choose a method above and run the command.")
    print("📁 Built apps will be saved in the 'dist' folder.")

if __name__ == "__main__":
    main()
