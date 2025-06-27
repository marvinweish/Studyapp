#!/bin/bash

# Simple deployment helper script for Study Buddy AWS deployment

echo "🚀 Study Buddy AWS Deployment Helper"
echo "===================================="

# Check if required files exist
required_files=("app.py" "study_app.py" "requirements-aws.txt" "Dockerfile")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ All required files present"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it:"
    echo "   pip install awscli"
    exit 1
fi

echo "✅ AWS CLI found"

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run:"
    echo "   aws configure"
    exit 1
fi

echo "✅ AWS credentials configured"

# Prompt for deployment method
echo ""
echo "Choose deployment method:"
echo "1. EC2 with CloudFormation (Recommended)"
echo "2. Docker container (for local testing)"
echo "3. Manual EC2 setup"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🔧 Starting CloudFormation deployment..."
        if [ -f "aws_deploy.py" ]; then
            python aws_deploy.py
        else
            echo "❌ aws_deploy.py not found"
            exit 1
        fi
        ;;
    2)
        echo "🐳 Building Docker container..."
        docker build -t studyapp .
        echo "🚀 Running Docker container..."
        echo "Set your GEMINI_API_KEY environment variable:"
        read -p "Enter your Gemini API key: " api_key
        docker run -p 8080:8080 -e GEMINI_API_KEY="$api_key" studyapp
        ;;
    3)
        echo "📋 Manual EC2 setup instructions:"
        echo "1. Launch an EC2 t2.micro instance with Amazon Linux 2"
        echo "2. Copy ec2-setup.sh to your instance"
        echo "3. Run: chmod +x ec2-setup.sh && sudo ./ec2-setup.sh"
        echo "4. Upload your application files to /opt/studyapp"
        echo "5. Set environment variables and start the service"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo "✅ Deployment process completed!"
