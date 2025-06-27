# Deploy to AWS EC2 Free Tier
# This script helps deploy the Study Buddy app to AWS EC2

import boto3
import json
import os
import sys
from typing import Optional

class AWSDeployer:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
    
    def create_key_pair(self, key_name: str) -> bool:
        """Create a new EC2 key pair"""
        try:
            response = self.ec2.create_key_pair(KeyName=key_name)
            
            # Save the private key to a file
            with open(f"{key_name}.pem", 'w') as f:
                f.write(response['KeyMaterial'])
            
            # Set correct permissions
            os.chmod(f"{key_name}.pem", 0o400)
            
            print(f"✅ Key pair '{key_name}' created successfully")
            print(f"🔐 Private key saved as '{key_name}.pem'")
            return True
            
        except Exception as e:
            if "already exists" in str(e):
                print(f"ℹ️ Key pair '{key_name}' already exists")
                return True
            else:
                print(f"❌ Error creating key pair: {e}")
                return False
    
    def deploy_with_cloudformation(self, stack_name: str, key_name: str, gemini_api_key: str) -> bool:
        """Deploy the application using CloudFormation"""
        try:
            # Read the CloudFormation template
            with open('cloudformation-template.json', 'r') as f:
                template_body = f.read()
            
            # Create the stack
            response = self.cloudformation.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=[
                    {
                        'ParameterKey': 'KeyName',
                        'ParameterValue': key_name
                    },
                    {
                        'ParameterKey': 'GeminiApiKey',
                        'ParameterValue': gemini_api_key
                    }
                ],
                Capabilities=['CAPABILITY_IAM']
            )
            
            print(f"✅ CloudFormation stack '{stack_name}' creation initiated")
            print(f"📊 Stack ID: {response['StackId']}")
            
            # Wait for stack creation to complete
            print("⏳ Waiting for stack creation to complete...")
            waiter = self.cloudformation.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
            
            # Get stack outputs
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            outputs = response['Stacks'][0].get('Outputs', [])
            
            for output in outputs:
                print(f"🔗 {output['Description']}: {output['OutputValue']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error deploying with CloudFormation: {e}")
            return False
    
    def get_latest_amazon_linux_ami(self) -> Optional[str]:
        """Get the latest Amazon Linux 2 AMI ID"""
        try:
            response = self.ec2.describe_images(
                Owners=['amazon'],
                Filters=[
                    {
                        'Name': 'name',
                        'Values': ['amzn2-ami-hvm-*-x86_64-gp2']
                    },
                    {
                        'Name': 'state',
                        'Values': ['available']
                    }
                ]
            )
            
            # Sort by creation date and get the latest
            images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
            
            if images:
                return images[0]['ImageId']
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error getting AMI: {e}")
            return None

def main():
    """Main deployment function"""
    print("🚀 AWS Study Buddy Deployment Script")
    print("=" * 50)
    
    # Check if AWS credentials are configured
    try:
        boto3.Session().get_credentials()
    except Exception as e:
        print("❌ AWS credentials not configured. Please run 'aws configure'")
        sys.exit(1)
    
    # Get deployment parameters
    region = input("Enter AWS region (default: us-east-1): ").strip() or "us-east-1"
    stack_name = input("Enter CloudFormation stack name (default: studyapp-stack): ").strip() or "studyapp-stack"
    key_name = input("Enter EC2 key pair name (default: studyapp-key): ").strip() or "studyapp-key"
    
    # Get Gemini API key
    gemini_api_key = input("Enter your Gemini API key: ").strip()
    if not gemini_api_key:
        print("❌ Gemini API key is required")
        sys.exit(1)
    
    # Initialize deployer
    deployer = AWSDeployer(region)
    
    # Create key pair
    print("\n📋 Step 1: Creating EC2 Key Pair...")
    if not deployer.create_key_pair(key_name):
        print("❌ Failed to create key pair")
        sys.exit(1)
    
    # Update CloudFormation template with correct AMI
    print("\n📋 Step 2: Getting latest Amazon Linux AMI...")
    ami_id = deployer.get_latest_amazon_linux_ami()
    if ami_id:
        print(f"✅ Latest AMI: {ami_id}")
        
        # Update the CloudFormation template
        with open('cloudformation-template.json', 'r') as f:
            template = json.load(f)
        
        # Update AMI ID in template
        template['Resources']['StudyAppInstance']['Properties']['ImageId'] = ami_id
        
        with open('cloudformation-template.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print("✅ CloudFormation template updated with latest AMI")
    else:
        print("❌ Could not get latest AMI ID")
        sys.exit(1)
    
    # Deploy with CloudFormation
    print("\n📋 Step 3: Deploying with CloudFormation...")
    if deployer.deploy_with_cloudformation(stack_name, key_name, gemini_api_key):
        print("\n🎉 Deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. SSH into your EC2 instance using the generated key pair")
        print("2. Upload your application files to /opt/studyapp")
        print("3. Start the application service: sudo systemctl start studyapp")
        print("4. Access your app through the provided URL")
    else:
        print("❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
