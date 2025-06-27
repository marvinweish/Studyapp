# 🚀 AI Study Buddy - AWS App Runner Deployment

A Flet-based web application for AI-powered study materials generation, optimized for AWS App Runner deployment.

## ✨ Features

- 📚 Upload documents (PDF, DOCX, PPTX, EPUB, TXT)
- 🤖 AI-powered flashcard generation using Google Gemini
- ❓ Interactive quizzes and tests
- 💾 Save and manage study topics
- 📱 Mobile and web responsive design
- 🔍 OCR support for image-based PDFs

## 🚀 Quick Deploy to AWS App Runner

### Prerequisites
1. AWS account with App Runner access
2. GitHub repository with your code
3. Google Gemini API key

### Step-by-Step Deployment

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for AWS App Runner deployment"
   git push origin main
   ```

2. **Deploy to AWS App Runner:**
   - Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
   - Click "Create service"
   - Choose "Source code repository"
   - Connect to GitHub and select your repository
   - Branch: `main`
   - Configuration: "Use configuration file" (apprunner.yaml)
   - Add environment variable:
     - Name: `GEMINI_API_KEY`
     - Value: `your_actual_api_key_here`
   - Click "Create & Deploy"

3. **Access your app:**
   - App Runner will provide a URL (e.g., `https://xxxxx.us-east-1.awsapprunner.com`)
   - Your Study Buddy app will be live in ~5 minutes!

## 📝 Environment Variables

Required environment variables for production:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8080  # (automatically set by App Runner)
```

## 🔄 Updating Your App

Simply push changes to your GitHub repository:

```bash
git add .
git commit -m "Updated study features"
git push origin main
```

App Runner will automatically rebuild and deploy your changes.

## 🏃‍♂️ Local Development

Run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY=your_api_key_here

# Run the app
python study_app.py
```

## 📊 AWS App Runner Benefits

- ✅ **Auto-scaling**: Handles traffic spikes automatically
- ✅ **Fully managed**: No server maintenance required
- ✅ **CI/CD built-in**: Deploys on Git push
- ✅ **Free tier**: 25 hours/month free
- ✅ **Custom domains**: Easy to add your own domain
- ✅ **SSL included**: HTTPS by default

## 🛠️ Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App won't start**: Verify `GEMINI_API_KEY` environment variable is set
3. **File upload issues**: App Runner has ephemeral storage (files don't persist)

### Useful AWS CLI Commands:

```bash
# List App Runner services
aws apprunner list-services

# Describe service status
aws apprunner describe-service --service-arn YOUR_SERVICE_ARN

# View logs
aws logs describe-log-groups --log-group-name-prefix "/aws/apprunner"
```

## 💰 Cost Estimation

**Free Tier (First 12 months):**
- 25 hours of App Runner compute time per month
- Typical small app usage: ~$0-5/month

**After Free Tier:**
- ~$0.064/hour for compute time
- Estimated cost for light usage: $10-30/month

## 🔒 Security Features

- Environment variables for sensitive data
- HTTPS enabled by default
- VPC connectivity available
- AWS IAM integration
- Non-root container user

## 📈 Monitoring

App Runner provides built-in monitoring:
- Application logs
- Metrics (CPU, memory, requests)
- Health checks
- CloudWatch integration

## 🆘 Support

- **AWS App Runner**: [Documentation](https://docs.aws.amazon.com/apprunner/)
- **Flet Framework**: [Documentation](https://flet.dev/)
- **Issues**: Open an issue in this repository

---

**Ready to deploy?** Just push to GitHub and create your App Runner service! 🚀
