# AWS Study Buddy Deployment Guide

This guide will help you deploy your AI Study Buddy application to AWS using the free tier.

## Prerequisites

1. **AWS Account**: Create a free AWS account at https://aws.amazon.com/
2. **AWS CLI**: Install and configure AWS CLI
3. **Python Dependencies**: Install boto3 for the deployment script
4. **Gemini API Key**: Have your Google Gemini API key ready

## Setup AWS CLI

```bash
# Install AWS CLI
pip install awscli boto3

# Configure AWS credentials
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., us-east-1)
- Default output format (json)

## Deployment Options

### Option 1: AWS EC2 Free Tier (Recommended)

1. **Run the deployment script**:
   ```bash
   python aws_deploy.py
   ```

2. **Follow the prompts**:
   - Choose AWS region (us-east-1 recommended for free tier)
   - Enter stack name (e.g., studyapp-stack)
   - Enter key pair name (e.g., studyapp-key)
   - Enter your Gemini API key

3. **Upload your application**:
   ```bash
   # Connect to your EC2 instance
   ssh -i studyapp-key.pem ec2-user@YOUR_INSTANCE_IP
   
   # Upload application files
   scp -i studyapp-key.pem -r * ec2-user@YOUR_INSTANCE_IP:/opt/studyapp/
   
   # Start the application
   sudo systemctl start studyapp
   ```

### Option 2: AWS App Runner

1. **Create a GitHub repository** with your code
2. **Use the App Runner console** to deploy directly from GitHub
3. **Set environment variables**:
   - `GEMINI_API_KEY`: Your API key
   - `PORT`: 8080

### Option 3: Manual EC2 Setup

1. **Launch EC2 instance**:
   - AMI: Amazon Linux 2
   - Instance Type: t2.micro (free tier)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22), and port 8080

2. **Run setup script**:
   ```bash
   chmod +x ec2-setup.sh
   sudo ./ec2-setup.sh
   ```

3. **Upload your application files**

4. **Start the service**:
   ```bash
   sudo systemctl start studyapp
   ```

## Environment Variables

Create a `.env` file or set environment variables:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8080
DEBUG=false
```

## Free Tier Limitations

- **EC2**: 750 hours per month of t2.micro instance
- **Data Transfer**: 15 GB outbound per month
- **Storage**: 30 GB of EBS storage

## Monitoring and Maintenance

1. **Check application logs**:
   ```bash
   sudo journalctl -u studyapp -f
   ```

2. **Monitor resource usage**:
   ```bash
   htop
   df -h
   ```

3. **Update application**:
   ```bash
   sudo systemctl stop studyapp
   # Upload new files
   sudo systemctl start studyapp
   ```

## Security Considerations

1. **API Keys**: Store in environment variables, not in code
2. **SSH Keys**: Keep your .pem files secure
3. **Security Groups**: Restrict access to necessary ports only
4. **Updates**: Keep your system and dependencies updated

## Troubleshooting

### Common Issues:

1. **Port 8080 not accessible**: Check security group settings
2. **Application won't start**: Check logs with `journalctl -u studyapp`
3. **File upload issues**: Ensure proper permissions on /opt/studyapp
4. **API key errors**: Verify GEMINI_API_KEY environment variable

### Useful Commands:

```bash
# Check service status
sudo systemctl status studyapp

# Restart service
sudo systemctl restart studyapp

# View logs
sudo journalctl -u studyapp -n 50

# Check if port is listening
sudo netstat -tlnp | grep 8080
```

## Cost Optimization

1. **Stop instance when not in use**: Free tier hours are cumulative
2. **Monitor usage**: Use AWS Cost Explorer
3. **Set up billing alerts**: Get notified before charges
4. **Use CloudWatch**: Monitor application performance

## Scaling Beyond Free Tier

When you're ready to scale:

1. **Upgrade instance type**: t3.small or larger
2. **Add load balancer**: Application Load Balancer
3. **Use RDS**: For database storage
4. **Add CloudFront**: For CDN
5. **Implement Auto Scaling**: For high availability

## Support

If you encounter issues:
1. Check AWS documentation
2. Review application logs
3. Monitor CloudWatch metrics
4. Consider AWS Support plans for production use

---

**Note**: This deployment is suitable for development and testing. For production use, consider additional security measures, monitoring, and backup strategies.
