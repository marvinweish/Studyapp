# 🔧 App Runner Deployment Fix Guide

## ❌ Error: "The specified runtime version is not supported"

### Root Cause
App Runner doesn't support Python 3.11 yet. The latest supported versions are:
- Python 3.8 ✅
- Python 3.9 ✅ 
- Python 3.10 ✅

### ✅ Solution Applied

**Updated `apprunner.yaml`:**
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies for Python 3.8..."
      - python --version
      - pip --version
      - pip install --upgrade pip
      - pip install -r requirements.txt
      - echo "Dependencies installed successfully"
run:
  runtime-version: 3.8  # Changed from 3.11 to 3.8
  command: python study_app.py
  network:
    port: 8080
  env:
    - name: PORT
      value: "8080"
    - name: FLET_WEB_RENDERER
      value: "html"
    - name: PYTHONUNBUFFERED
      value: "1"
```

**Updated `requirements.txt`:**
- Added version constraints for Python 3.8 compatibility
- Pinned dependency versions to avoid conflicts

### 🧪 Test Before Deploying

Run the compatibility test:
```bash
python test_apprunner_compatibility.py
```

### 🚀 Next Steps

1. **Commit the changes:**
   ```bash
   git add apprunner.yaml requirements.txt
   git commit -m "Fix App Runner Python version compatibility"
   git push origin main
   ```

2. **Redeploy in App Runner:**
   - Go to AWS App Runner console
   - Select your service
   - Click "Deploy" to trigger a new deployment
   - Or create a new service if needed

3. **Monitor deployment:**
   - Check the deployment logs
   - Look for successful build and run phases

### 🔄 Alternative Python Versions

If Python 3.8 doesn't work, try these alternatives (in order):

1. **Python 3.9** - Replace `runtime-version: 3.8` with `3.9`
2. **Python 3.10** - Replace `runtime-version: 3.8` with `3.10`

### 📋 Troubleshooting Checklist

- ✅ Python version changed to 3.8
- ✅ Requirements.txt updated with version constraints
- ✅ apprunner.yaml includes build verification
- ✅ Environment variables properly set
- ✅ Code pushed to GitHub
- ✅ App Runner service configured correctly

### 🆘 If Still Failing

1. **Check App Runner logs** for specific error messages
2. **Verify GitHub connection** and branch selection
3. **Test locally** with Python 3.8:
   ```bash
   python3.8 -m venv test_env
   source test_env/bin/activate  # or test_env\Scripts\activate on Windows
   pip install -r requirements.txt
   python study_app.py
   ```
4. **Contact AWS Support** if the issue persists

### 📞 Quick Support

- **App Runner supported runtimes**: https://docs.aws.amazon.com/apprunner/latest/dg/service-source-code.html
- **Flet deployment guide**: https://flet.dev/docs/guides/python/deploying-web-app/aws-app-runner/
- **AWS App Runner troubleshooting**: https://docs.aws.amazon.com/apprunner/latest/dg/troubleshooting.html
