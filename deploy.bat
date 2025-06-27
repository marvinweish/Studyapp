@echo off
REM Study Buddy AWS Deployment Helper for Windows

title Study Buddy AWS Deployment

echo.
echo 🚀 Study Buddy AWS Deployment Helper
echo ====================================

REM Check if required files exist
set missing_files=
if not exist "app.py" set missing_files=%missing_files% app.py
if not exist "study_app.py" set missing_files=%missing_files% study_app.py
if not exist "requirements-aws.txt" set missing_files=%missing_files% requirements-aws.txt
if not exist "Dockerfile" set missing_files=%missing_files% Dockerfile

if not "%missing_files%"=="" (
    echo ❌ Missing required files: %missing_files%
    pause
    exit /b 1
)

echo ✅ All required files present

REM Check if AWS CLI is installed
aws --version >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS CLI not found. Please install it:
    echo    pip install awscli
    pause
    exit /b 1
)

echo ✅ AWS CLI found

REM Check if AWS credentials are configured
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS credentials not configured. Please run:
    echo    aws configure
    pause
    exit /b 1
)

echo ✅ AWS credentials configured

echo.
echo Choose deployment method:
echo 1. EC2 with CloudFormation (Recommended)
echo 2. Docker container (for local testing)
echo 3. Manual EC2 setup instructions

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo 🔧 Starting CloudFormation deployment...
    if exist "aws_deploy.py" (
        python aws_deploy.py
    ) else (
        echo ❌ aws_deploy.py not found
        pause
        exit /b 1
    )
) else if "%choice%"=="2" (
    echo 🐳 Building Docker container...
    docker build -t studyapp .
    echo 🚀 Running Docker container...
    set /p api_key="Enter your Gemini API key: "
    docker run -p 8080:8080 -e GEMINI_API_KEY="%api_key%" studyapp
) else if "%choice%"=="3" (
    echo 📋 Manual EC2 setup instructions:
    echo 1. Launch an EC2 t2.micro instance with Amazon Linux 2
    echo 2. Copy ec2-setup.sh to your instance
    echo 3. Run: chmod +x ec2-setup.sh ^&^& sudo ./ec2-setup.sh
    echo 4. Upload your application files to /opt/studyapp
    echo 5. Set environment variables and start the service
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

echo ✅ Deployment process completed!
pause
