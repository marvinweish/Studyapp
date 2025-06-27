# 🚀 AWS App Runner Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] **Code is ready**: All tests pass (`python test_deployment.py`)
- [ ] **Gemini API Key**: Have your Google Gemini API key ready
- [ ] **GitHub Repository**: Code is pushed to GitHub
- [ ] **AWS Account**: Have access to AWS App Runner

## 📝 Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Deploy to AWS App Runner"
git push origin main
```

### 2. Create App Runner Service
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/home)
2. Click "Create service"
3. **Source**: Source code repository
4. **Repository**: Connect to GitHub → Select your repository
5. **Branch**: main
6. **Configuration**: Use configuration file (apprunner.yaml)
7. **Environment Variables**:
   - Name: `GEMINI_API_KEY`
   - Value: `your_actual_gemini_api_key`
8. Click "Create & Deploy"

### 3. Wait for Deployment
- Build time: ~3-5 minutes
- App will be available at provided URL
- Example: `https://xyz123.us-east-1.awsapprunner.com`

## 🔄 For Future Updates

Just push to GitHub - automatic deployment:
```bash
git add .
git commit -m "Feature update"
git push origin main
```

## 🎯 App Runner Optimizations Applied

✅ **Web-ready entry point**: Automatic host/port binding
✅ **Environment detection**: AWS vs local mode
✅ **Efficient builds**: Optimized Dockerfile and .dockerignore
✅ **Configuration file**: apprunner.yaml for service settings
✅ **Health checks**: Built-in monitoring
✅ **Security**: Non-root user, environment variables

## 💰 Expected Costs

- **Free Tier**: 25 hours/month (first 12 months)
- **After Free Tier**: ~$0.064/hour
- **Typical usage**: $0-30/month depending on traffic

## 🆘 Troubleshooting

### Build Fails
```bash
# Check logs in App Runner console
# Verify requirements.txt has all dependencies
```

### App Won't Start
```bash
# Check environment variables in App Runner
# Verify GEMINI_API_KEY is set correctly
```

### Slow Performance
```bash
# App Runner auto-scales based on traffic
# Consider upgrading instance size if needed
```

## 🔗 Useful Links

- [AWS App Runner Console](https://console.aws.amazon.com/apprunner/home)
- [Google AI Studio](https://makersuite.google.com/app/apikey) (for API keys)
- [App Runner Documentation](https://docs.aws.amazon.com/apprunner/)

---

**Ready to deploy? Follow the steps above! 🚀**
