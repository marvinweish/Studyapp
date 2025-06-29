# AI Study Buddy - Google Cloud Debugging Guide

## Current Status
Your Docker build is running on Google Cloud Build. Once it completes successfully, follow these steps:

## Step 1: Check Build Status
```bash
gcloud builds list --limit=1
```
Wait until you see STATUS: SUCCESS

## Step 2: Deploy to Cloud Run
```bash
gcloud run deploy ai-study-buddy \
  --image gcr.io/gen-lang-client-0207268394/ai-study-buddy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars="FLET_WEB_RENDERER=html,GEMINI_API_KEY=AIzaSyBpW3Zh8okQV4Peu-DANqGoqeIHXw_DhEs,GAE_ENV=cloudrun" \
  --port 8080
```

## Step 3: Get Your App URL
```bash
gcloud run services describe ai-study-buddy --region=us-central1 --format="value(status.url)"
```

## Step 4: Monitor Logs for Debugging
```bash
# View recent logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy" --limit=50

# Stream live logs (for debugging)
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=ai-study-buddy"
```

## Alternative: Use the batch scripts
- Run `deploy-and-debug.bat` - Does everything in one go
- Run `monitor-logs.bat` - Just monitors logs

## Debugging Web Console
Visit: https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy/logs?project=gen-lang-client-0207268394

## Common Issues to Watch For:
1. **Port binding** - App should bind to 0.0.0.0:8080
2. **Environment variables** - Check if GEMINI_API_KEY is accessible
3. **Flet web rendering** - Verify FLET_WEB_RENDERER=html works
4. **Memory/CPU limits** - Monitor resource usage
5. **Startup time** - Cloud Run has timeout limits

Once deployed, you'll be able to access your app via the Cloud Run URL and debug any issues through the logs!
