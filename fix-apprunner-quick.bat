@echo off
echo 🔧 App Runner Service Fix - Quick Start
echo =====================================
echo.

echo Checking AWS CLI...
aws --version >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS CLI not found. Please install AWS CLI first.
    pause
    exit /b 1
)
echo ✅ AWS CLI found

echo.
echo Checking AWS credentials...
aws sts get-caller-identity >nul 2>&1
if errorlevel 1 (
    echo ❌ AWS credentials not configured. Please run 'aws configure'
    pause
    exit /b 1
)
echo ✅ AWS credentials configured

echo.
echo 📋 Steps to fix your App Runner service:
echo.
echo 1. Go to AWS App Runner Console:
echo    https://us-east-1.console.aws.amazon.com/apprunner/home?region=us-east-1#/services
echo.
echo 2. Find your service 'myAi' and delete it if it exists and is in failed state
echo.
echo 3. Create a new service with these settings:
echo    - Source: GitHub repository
echo    - Repository: marvinweish/Studyapp
echo    - Branch: master
echo    - Configuration: Use configuration file (apprunner.yaml)
echo    - Service name: myAi-fixed
echo.
echo 4. Add environment variable:
echo    GEMINI_API_KEY = your_api_key_here
echo.
echo 5. Wait for deployment to complete
echo.
echo Alternative: Run the PowerShell script for automation:
echo    PowerShell -ExecutionPolicy Bypass -File fix-apprunner-service.ps1
echo.
echo Or use ECS Fargate for more reliability:
echo    python ecs_deploy_optimized.py
echo.
pause
