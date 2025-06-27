# AI Study Buddy - Mobile & Desktop Packaging Guide

## 📱 Android APK Build

### Prerequisites
- Python 3.8+ with Flet installed
- Android SDK (optional, Flet can use online build service)
- Java JDK 8+ (for local builds)

### Method 1: Online Build Service (Recommended)
```bash
# Build APK using Flet's build system
flet build apk --project "AI Study Buddy" --description "Intelligent study companion with OCR support" --org "com.studybuddy"

# This will:
# 1. Package your app
# 2. Build using Flet's cloud build service
# 3. Download the compiled APK
```

### Method 2: Local Build (Advanced)
```bash
# Build locally (requires Flutter SDK setup)
flet build apk --project "AI Study Buddy" --description "Intelligent study companion" --org "com.studybuddy" --local
```

## 🖥️ Windows Desktop App

### Standard Desktop Build
```bash
# Build Windows executable
flet pack study_app.py --name "AI Study Buddy" --product-name "AI Study Buddy" --file-description "AI-powered study companion"

# This creates:
# - Standalone .exe file
# - All dependencies bundled
# - No Python installation required on target machine
```

### Advanced Desktop Build with Custom Settings
```bash
# Build with custom options
flet pack study_app.py \
  --name "AI Study Buddy" \
  --product-name "AI Study Buddy" \
  --file-description "Intelligent study companion with OCR and AI features" \
  --product-version "1.0.0" \
  --icon app_icon.ico \
  --add-data "poppler-21.11.0;poppler-21.11.0" \
  --add-data "test_files;test_files" \
  --hidden-import pytesseract \
  --hidden-import pdf2image \
  --distpath dist
```

## 📁 File Structure for Packaging
```
studyapp/
├── study_app.py           # Main app file
├── ai_generator.py        # AI module
├── file_processor.py      # File processing
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── app_icon.ico          # App icon (optional)
├── poppler-21.11.0/      # OCR dependencies
├── test_files/           # Sample files (optional)
└── key.env              # API keys
```

## ⚙️ Build Configuration Options

### Common Flet Pack Options
- `--name`: App display name
- `--description`: App description
- `--author`: Developer name
- `--version`: App version
- `--icon`: Path to app icon (.ico for Windows, .png for Android)
- `--android`: Build for Android
- `--web`: Build for web deployment
- `--distpath`: Output directory

### Android-Specific Options
- `--android-adaptive-icon-background`: Background color for adaptive icon
- `--android-adaptive-icon-foreground`: Foreground image for adaptive icon
- `--template`: Use custom template

## 🔧 Dependencies Management

The build process should automatically include most dependencies, but some OCR components may need special handling:

### For Windows Desktop:
- Tesseract: Will be bundled if installed
- Poppler: Include the poppler-21.11.0 folder

### For Android:
- OCR functionality may be limited
- Consider cloud-based OCR alternatives for mobile

## 📋 Build Script Templates
