@echo off
REM Setup script for Google Cloud deployment

echo 🔧 Setting up Google Cloud for AI Study Buddy deployment
echo.

echo Step 1: Authenticate with Google Cloud
echo Running: gcloud auth login
gcloud auth login

echo.
echo Step 2: List available projects
echo Running: gcloud projects list
gcloud projects list

echo.
echo Step 3: Please enter your project ID from the list above:
set /p PROJECT_ID="Project ID: "

echo.
echo Step 4: Setting active project to %PROJECT_ID%
gcloud config set project %PROJECT_ID%

echo.
echo Step 5: Enable required APIs
echo Enabling Cloud Build API...
gcloud services enable cloudbuild.googleapis.com

echo Enabling Cloud Run API...
gcloud services enable run.googleapis.com

echo Enabling Container Registry API...
gcloud services enable containerregistry.googleapis.com

echo.
echo Step 6: Verify configuration
gcloud config list

echo.
echo ✅ Setup complete! You can now deploy your app with deploy-gcp.bat
pause
