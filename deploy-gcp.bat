@echo off
REM GCP Cloud Run deployment script for AI Study Buddy (Windows)

REM Configuration
set PROJECT_ID=%GOOGLE_CLOUD_PROJECT%
if "%PROJECT_ID%"=="" set PROJECT_ID=your-project-id
set SERVICE_NAME=ai-study-buddy
set REGION=us-central1
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

echo 🚀 Deploying AI Study Buddy to Google Cloud Run
echo Project ID: %PROJECT_ID%
echo Service Name: %SERVICE_NAME%
echo Region: %REGION%

REM Build and push the container image
echo 📦 Building container image...
gcloud builds submit --tag %IMAGE_NAME%

REM Deploy to Cloud Run
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
  --set-env-vars="FLET_WEB_RENDERER=html" ^
  --port 8080

echo ✅ Deployment complete!
echo 🔗 Your app will be available at:
gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"
