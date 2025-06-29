@echo off
REM Log monitoring script for debugging Cloud Run deployment

echo 📊 Monitoring AI Study Buddy logs on Cloud Run
echo Project: gen-lang-client-0207268394
echo Service: ai-study-buddy
echo.

echo Choose monitoring option:
echo 1. View recent logs
echo 2. Follow live logs
echo 3. View error logs only
echo 4. View build logs
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo 📄 Showing recent logs...
    gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy" --limit=50 --format="table(timestamp,severity,textPayload)"
) else if "%choice%"=="2" (
    echo 🔄 Following live logs... (Press Ctrl+C to stop)
    gcloud logs tail "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy" --follow
) else if "%choice%"=="3" (
    echo ❌ Showing error logs...
    gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy AND severity>=ERROR" --limit=20 --format="table(timestamp,severity,textPayload)"
) else if "%choice%"=="4" (
    echo 🔨 Showing build logs...
    gcloud logs read "resource.type=build" --limit=20 --format="table(timestamp,severity,textPayload)"
) else (
    echo Invalid choice. Please run the script again.
)

pause
