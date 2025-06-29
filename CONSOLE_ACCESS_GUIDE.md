# Google Cloud Console - Viewing Your Deployment

## Quick Access Links for Your Project

### 🏠 Project Dashboard
**Main project overview with all services**
https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0207268394

### 🚀 Cloud Run Service
**Your deployed AI Study Buddy service**
https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy?project=gen-lang-client-0207268394

### 📝 Service Logs
**Real-time logs for debugging**
https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy/logs?project=gen-lang-client-0207268394

### 🔨 Cloud Build History
**Build logs and status**
https://console.cloud.google.com/cloud-build/builds?project=gen-lang-client-0207268394

### 📊 Logging Dashboard
**All project logs**
https://console.cloud.google.com/logs/query?project=gen-lang-client-0207268394

## How to Navigate the Console

### 1. Cloud Run Service Page
- **Overview Tab**: Service status, URL, resource usage
- **Logs Tab**: Real-time application logs
- **Metrics Tab**: Performance metrics (CPU, memory, requests)
- **Security Tab**: IAM and security settings
- **Networking Tab**: Custom domains and traffic allocation

### 2. What to Look For When Debugging

#### ✅ Service Status Indicators:
- **Green checkmark**: Service is healthy
- **Yellow warning**: Service has issues
- **Red X**: Service is down

#### 📊 Key Metrics to Monitor:
- **Request Count**: How many requests your app is handling
- **Response Time**: How fast your app responds
- **Error Rate**: Percentage of failed requests
- **Memory Usage**: RAM consumption
- **CPU Usage**: Processing power usage

#### 🔍 Log Types to Watch:
- **INFO**: General application information
- **ERROR**: Application errors
- **WARNING**: Potential issues
- **DEBUG**: Detailed debugging information

### 3. Common Debugging Steps

1. **Check Service Health**
   - Go to Cloud Run service page
   - Look for green status indicator
   - Check if URL is accessible

2. **Review Recent Logs**
   - Click on "Logs" tab
   - Look for recent ERROR or WARNING messages
   - Check startup logs for initialization issues

3. **Monitor Resource Usage**
   - Click on "Metrics" tab
   - Check if memory/CPU limits are exceeded
   - Look for request patterns

4. **Test the Application**
   - Click on the service URL
   - Verify the Flet web interface loads
   - Try uploading a file and generating study materials

## Browser Bookmarks
Save these links as bookmarks for quick access:

1. **AI Study Buddy Service**: https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy?project=gen-lang-client-0207268394
2. **Service Logs**: https://console.cloud.google.com/run/detail/us-central1/ai-study-buddy/logs?project=gen-lang-client-0207268394
3. **Project Dashboard**: https://console.cloud.google.com/home/dashboard?project=gen-lang-client-0207268394

## Mobile Access
You can also access these links on your mobile device using the Google Cloud Console mobile app or mobile browser.
