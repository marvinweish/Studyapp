#!/bin/bash

# AWS EC2 User Data Script for Study Buddy App
# This script runs when the EC2 instance starts

# Update system
sudo yum update -y

# Install Python 3.11 and pip
sudo yum install -y python3.11 python3.11-pip git

# Install development tools
sudo yum groupinstall -y "Development Tools"

# Create application directory
sudo mkdir -p /opt/studyapp
cd /opt/studyapp

# Clone your repository (replace with your actual repository URL)
# sudo git clone https://github.com/yourusername/studyapp.git .

# For now, we'll create the app files manually
# In production, you would push your code to a Git repository and clone it

# Create a virtual environment
sudo python3.11 -m venv venv
sudo chown -R ec2-user:ec2-user /opt/studyapp

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip

# Install application dependencies
pip install flet>=0.24.0
pip install google-generativeai>=0.3.0
pip install python-dotenv>=1.0.0
pip install PyPDF2>=3.0.0
pip install python-docx>=0.8.11
pip install python-pptx>=0.6.21
pip install ebooklib>=0.18
pip install beautifulsoup4>=4.9.3
pip install gunicorn>=21.2.0
pip install uvicorn>=0.24.0

# Create systemd service file
sudo tee /etc/systemd/system/studyapp.service > /dev/null <<EOF
[Unit]
Description=AI Study Buddy Application
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/studyapp
Environment=PATH=/opt/studyapp/venv/bin
Environment=PORT=8080
ExecStart=/opt/studyapp/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable studyapp
# sudo systemctl start studyapp

# Configure firewall (if needed)
# sudo firewall-cmd --permanent --add-port=8080/tcp
# sudo firewall-cmd --reload

# Create a simple nginx configuration for reverse proxy (optional)
sudo yum install -y nginx

sudo tee /etc/nginx/conf.d/studyapp.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Start nginx
sudo systemctl enable nginx
sudo systemctl start nginx

echo "Setup completed. Upload your application files to /opt/studyapp and run 'sudo systemctl start studyapp'"
