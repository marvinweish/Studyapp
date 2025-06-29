@echo off
REM Check status of AI Study Buddy deployment

set PROJECT_ID=gen-lang-client-0207268394
set SERVICE_NAME=ai-study-buddy
set REGION=us-central1

echo 🔍 Checking AI Study Buddy deployment status
echo Project: %PROJECT_ID%
echo Service: %SERVICE_NAME%
echo Region: %REGION%
echo.

echo 📊 Build Status:
gcloud builds list --limit=3 --format="table(id,status,createTime,duration)"

echo.
echo 🚀 Cloud Run Services:
gcloud run services list --region=%REGION%

echo.
echo 🌐 Service Details (if deployed):
gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="table(metadata.name,status.url,status.conditions[0].type,status.conditions[0].status)" 2>nul

echo.
echo 📝 Recent Logs (if service exists):
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=%SERVICE_NAME%" --limit=10 --format="table(timestamp,severity,textPayload)" 2>nul

echo.
echo 💡 Direct Console Links:
echo Build History: https://console.cloud.google.com/cloud-build/builds?project=%PROJECT_ID%
echo Cloud Run: https://console.cloud.google.com/run?project=%PROJECT_ID%

pause
