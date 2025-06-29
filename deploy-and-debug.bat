@echo off
REM Deploy and debug AI Study Buddy on Google Cloud Run

set PROJECT_ID=gen-lang-client-0207268394
set SERVICE_NAME=ai-study-buddy
set REGION=us-central1
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

echo 🚀 Deploying AI Study Buddy to Google Cloud Run for debugging
echo Project ID: %PROJECT_ID%
echo Service Name: %SERVICE_NAME%
echo Region: %REGION%

REM Deploy to Cloud Run with debugging enabled
echo 🌐 Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image %IMAGE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 1 ^
  --timeout 300 ^
  --max-instances 10 ^
  --set-env-vars="FLET_WEB_RENDERER=html,GEMINI_API_KEY=AIzaSyBpW3Zh8okQV4Peu-DANqGoqeIHXw_DhEs,GAE_ENV=cloudrun" ^
  --port 8080

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Deployment failed!
    exit /b 1
)

echo ✅ Deployment complete!

REM Get the service URL
echo 🔗 Getting service URL...
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"') do set SERVICE_URL=%%i
echo Your app is available at: %SERVICE_URL%

echo.
echo 📊 Starting log monitoring (Press Ctrl+C to stop)...
echo To view logs in browser: https://console.cloud.google.com/run/detail/%REGION%/%SERVICE_NAME%/logs?project=%PROJECT_ID%
echo.

REM Stream logs for debugging
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=%SERVICE_NAME%" --format="value(timestamp,severity,textPayload)"

pause
