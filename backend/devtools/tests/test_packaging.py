"""
Test script to verify the packaging system works correctly
"""

import os
import sys
from pathlib import Path

def main():
    print("🧪 AI Study Buddy - Packaging Test")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("study_app.py").exists():
        print("❌ Error: study_app.py not found!")
        print("Please run this script from the AI Study Buddy directory.")
        return
    
    print("✅ Found study_app.py")
    
    # Check dist directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        print(f"📁 Found dist directory")
        
        # List contents
        contents = list(dist_dir.iterdir())
        if contents:
            print(f"📋 Contents in dist directory:")
            for item in contents:
                if item.is_file():
                    size = item.stat().st_size
                    size_mb = size / (1024 * 1024)
                    print(f"  📄 {item.name} ({size_mb:.1f} MB)")
                else:
                    print(f"  📁 {item.name}/")
        else:
            print("📋 Dist directory is empty")
    else:
        print("📁 No dist directory found")
    
    # Check build directory
    build_dir = Path("build")
    if build_dir.exists():
        print(f"🔧 Found build directory (build artifacts)")
    
    print("\n🎯 Available build commands:")
    print("Desktop (Windows): .\\build_desktop.bat")
    print("Android (APK):     .\\build_android.bat")
    print("Cross-platform:    python build_app.py")
    
    print("\n📝 Manual commands:")
    print("Desktop: flet pack study_app.py --name 'AI Study Buddy' -y")
    print("Android: flet build apk --project 'AI Study Buddy' --org 'com.studybuddy'")
    print("Web:     flet build web --project 'AI Study Buddy' --org 'com.studybuddy'")
    
    print("\n💡 Tips:")
    print("- Use -y flag to skip confirmation prompts")
    print("- Clear dist directory before building: Remove-Item -Recurse -Force dist")
    print("- Android builds require internet connection")
    print("- Desktop builds create standalone executables")

if __name__ == "__main__":
    main()
