@echo off
REM Monitor logs for debugging AI Study Buddy on Google Cloud Run

set PROJECT_ID=gen-lang-client-0207268394
set SERVICE_NAME=ai-study-buddy
set REGION=us-central1

echo 📊 Monitoring logs for %SERVICE_NAME% in project %PROJECT_ID%
echo Region: %REGION%
echo.
echo Press Ctrl+C to stop monitoring
echo.

REM Stream recent logs
echo Getting recent logs...
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=%SERVICE_NAME%" --limit=50 --format="table(timestamp,severity,textPayload)" --freshness=1d

echo.
echo 🔄 Starting real-time log streaming...
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=%SERVICE_NAME%" --format="value(timestamp,severity,textPayload)"
