@echo off
REM Quick deployment script for debugging on Cloud Run

echo 🚀 Deploying AI Study Buddy to Cloud Run for debugging
echo Project: gen-lang-client-0207268394
echo.

REM Deploy to Cloud Run with debug settings
echo 🌐 Deploying to Cloud Run...
gcloud run deploy ai-study-buddy ^
  --image gcr.io/gen-lang-client-0207268394/ai-study-buddy ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 1 ^
  --timeout 300 ^
  --max-instances 10 ^
  --set-env-vars="FLET_WEB_RENDERER=html,GEMINI_API_KEY=AIzaSyBpW3Zh8okQV4Peu-DANqGoqeIHXw_DhEs" ^
  --port 8080

echo.
echo ✅ Deployment complete!
echo 🔗 Getting service URL...
gcloud run services describe ai-study-buddy --region=us-central1 --format="value(status.url)"

echo.
echo 📊 Google Cloud Console Links:
echo.
echo 🌐 Cloud Run Service Dashboard:
echo https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy?project=gen-lang-client-0207268394
echo.
echo 📝 Service Logs:
echo https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy/logs?project=gen-lang-client-0207268394
echo.
echo 📊 Cloud Build History:
echo https://console.cloud.google.com/cloud-build/builds?project=gen-lang-client-0207268394
echo.
echo 📈 Project Overview:
echo https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0207268394
echo.
echo 💡 To view logs in terminal:
echo gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy"

pause
