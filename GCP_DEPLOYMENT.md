# AI Study Buddy - GCP Deployment Guide

This guide covers deploying the AI Study Buddy application to Google Cloud Platform (GCP).

## Prerequisites

1. **Google Cloud SDK**: Install and configure the gcloud CLI
   ```bash
   # Install Google Cloud SDK
   # Visit: https://cloud.google.com/sdk/docs/install
   
   # Login and set project
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable Required APIs**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Set Environment Variables**:
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   export GEMINI_API_KEY=your-gemini-api-key
   ```

## Deployment Options

### Option 1: Google Cloud Run (Recommended)

Cloud Run is perfect for containerized web applications with automatic scaling.

#### Quick Deploy
```bash
# Windows
deploy-gcp.bat

# Linux/Mac
chmod +x deploy-gcp.sh
./deploy-gcp.sh
```

#### Manual Deploy
```bash
# 1. Build and push container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-study-buddy

# 2. Deploy to Cloud Run
gcloud run deploy ai-study-buddy \
  --image gcr.io/YOUR_PROJECT_ID/ai-study-buddy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars="GEMINI_API_KEY=${GEMINI_API_KEY},FLET_WEB_RENDERER=html" \
  --port 8080
```

### Option 2: Google App Engine

App Engine provides a fully managed platform with automatic scaling.

```bash
# Deploy using app.yaml
gcloud app deploy app.yaml --project=YOUR_PROJECT_ID
```

## Configuration

### Environment Variables

Set these in your deployment:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `FLET_WEB_RENDERER`: Set to "html" for web deployment
- `PORT`: Port number (default: 8080)

### Cloud Run Environment Variables
```bash
gcloud run services update ai-study-buddy \
  --region us-central1 \
  --set-env-vars="GEMINI_API_KEY=your-key,FLET_WEB_RENDERER=html"
```

### App Engine Environment Variables
Add to `app.yaml`:
```yaml
env_variables:
  GEMINI_API_KEY: "your-api-key"
  FLET_WEB_RENDERER: "html"
```

## Storage Considerations

### Temporary Files
- GCP provides ephemeral storage in `/tmp`
- Files are automatically cleaned up between container restarts
- Saved topics are stored temporarily and will be lost on restart

### Persistent Storage (Optional)
To add persistent storage for saved topics:

1. **Cloud Storage Integration**:
   ```python
   from google.cloud import storage
   
   # Save topics to Cloud Storage bucket
   def save_to_cloud_storage(data):
       client = storage.Client()
       bucket = client.bucket('your-bucket-name')
       blob = bucket.blob('saved_topics.json')
       blob.upload_from_string(json.dumps(data))
   ```

2. **Cloud Firestore Integration**:
   ```python
   from google.cloud import firestore
   
   # Save topics to Firestore
   def save_to_firestore(data):
       db = firestore.Client()
       doc_ref = db.collection('topics').document('user_topics')
       doc_ref.set(data)
   ```

## Monitoring and Logging

### View Logs
```bash
# Cloud Run logs
gcloud run services logs read ai-study-buddy --region=us-central1

# App Engine logs
gcloud app logs tail -s default
```

### Cloud Monitoring
- Metrics are automatically collected
- Set up alerts for errors or high latency
- Monitor memory and CPU usage

## Security

### Authentication (Optional)
To require authentication:

```bash
# Remove public access
gcloud run services remove-iam-policy-binding ai-study-buddy \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# Add specific users
gcloud run services add-iam-policy-binding ai-study-buddy \
  --region=us-central1 \
  --member="user:email@example.com" \
  --role="roles/run.invoker"
```

### API Key Security
- Store API keys as environment variables
- Use Google Secret Manager for sensitive data:

```bash
# Store API key in Secret Manager
gcloud secrets create gemini-api-key --data-file=- <<< "your-api-key"

# Update Cloud Run to use secret
gcloud run services update ai-study-buddy \
  --region=us-central1 \
  --set-secrets="GEMINI_API_KEY=gemini-api-key:latest"
```

## Performance Optimization

### Memory and CPU Settings
```bash
# Optimize for your workload
gcloud run services update ai-study-buddy \
  --region=us-central1 \
  --memory=2Gi \
  --cpu=2 \
  --concurrency=80 \
  --max-instances=10
```

### Cold Start Optimization
- Keep minimum instances if needed:
```bash
gcloud run services update ai-study-buddy \
  --region=us-central1 \
  --min-instances=1
```

## Troubleshooting

### Common Issues

1. **Container Build Fails**:
   - Check Dockerfile syntax
   - Ensure all dependencies are in requirements-gcp.txt
   - Verify base image compatibility

2. **Service Won't Start**:
   - Check environment variables
   - Verify API key is valid
   - Review application logs

3. **Memory Issues**:
   - Increase memory allocation
   - Optimize file processing
   - Use streaming for large files

4. **Timeout Issues**:
   - Increase request timeout
   - Optimize AI generation calls
   - Use async processing

### Debug Commands
```bash
# Check service status
gcloud run services describe ai-study-buddy --region=us-central1

# View recent logs
gcloud run services logs read ai-study-buddy --region=us-central1 --limit=50

# Test locally with same environment
docker run -p 8080:8080 -e GEMINI_API_KEY=your-key gcr.io/YOUR_PROJECT_ID/ai-study-buddy
```

## Cost Optimization

### Cloud Run Pricing
- Pay per request and compute time
- No charges when not serving requests
- Free tier: 2 million requests/month

### Optimization Tips
- Set appropriate memory limits
- Use request-based scaling
- Implement caching where possible
- Optimize container startup time

## Updating the Application

```bash
# Build new version
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-study-buddy:v2

# Deploy update
gcloud run services update ai-study-buddy \
  --region=us-central1 \
  --image=gcr.io/YOUR_PROJECT_ID/ai-study-buddy:v2
```

## Support

For deployment issues:
1. Check the GCP documentation
2. Review application logs
3. Test locally with Docker
4. Verify all environment variables are set correctly

## Next Steps

After deployment:
1. Test all functionality
2. Set up monitoring and alerts
3. Configure custom domain (optional)
4. Set up CI/CD pipeline (optional)
5. Add persistent storage if needed
