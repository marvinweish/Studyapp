#!/usr/bin/env python3
"""
AWS ECS Fargate deployment script for Study Buddy application
"""

import boto3
import json
import sys
import time
from typing import Optional

class ECSDeployer:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.ecr = boto3.client('ecr', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        
    def create_ecr_repository(self, repository_name: str) -> str:
        """Create ECR repository and return the URI"""
        try:
            response = self.ecr.create_repository(repositoryName=repository_name)
            repo_uri = response['repository']['repositoryUri']
            print(f"✅ Created ECR repository: {repo_uri}")
            return repo_uri
        except self.ecr.exceptions.RepositoryAlreadyExistsException:
            response = self.ecr.describe_repositories(repositoryNames=[repository_name])
            repo_uri = response['repositories'][0]['repositoryUri']
            print(f"ℹ️ ECR repository already exists: {repo_uri}")
            return repo_uri
        except Exception as e:
            print(f"❌ Error creating ECR repository: {e}")
            return None
    
    def get_ecr_login_token(self) -> str:
        """Get ECR login token for Docker"""
        try:
            response = self.ecr.get_authorization_token()
            token = response['authorizationData'][0]['authorizationToken']
            return token
        except Exception as e:
            print(f"❌ Error getting ECR login token: {e}")
            return None
    
    def deploy_with_cloudformation(self, stack_name: str, image_uri: str, 
                                 vpc_id: str, subnet_ids: list, gemini_api_key: str) -> bool:
        """Deploy using CloudFormation"""
        try:
            with open('ecs-cloudformation.json', 'r') as f:
                template_body = f.read()
            
            parameters = [
                {'ParameterKey': 'GeminiApiKey', 'ParameterValue': gemini_api_key},
                {'ParameterKey': 'VpcId', 'ParameterValue': vpc_id},
                {'ParameterKey': 'SubnetIds', 'ParameterValue': ','.join(subnet_ids)},
                {'ParameterKey': 'ImageUri', 'ParameterValue': image_uri}
            ]
            
            try:
                response = self.cloudformation.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=['CAPABILITY_IAM']
                )
                print(f"✅ CloudFormation stack creation initiated: {response['StackId']}")
            except self.cloudformation.exceptions.AlreadyExistsException:
                print("ℹ️ Stack already exists, updating...")
                response = self.cloudformation.update_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=['CAPABILITY_IAM']
                )
                print(f"✅ CloudFormation stack update initiated")
            
            # Wait for completion
            print("⏳ Waiting for CloudFormation deployment to complete...")
            waiter = self.cloudformation.get_waiter('stack_create_complete')
            try:
                waiter.wait(StackName=stack_name, WaiterConfig={'MaxAttempts': 30})
            except:
                waiter = self.cloudformation.get_waiter('stack_update_complete')
                waiter.wait(StackName=stack_name, WaiterConfig={'MaxAttempts': 30})
            
            # Get outputs
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            outputs = response['Stacks'][0].get('Outputs', [])
            
            print("\n🎉 Deployment completed successfully!")
            for output in outputs:
                print(f"🔗 {output['Description']}: {output['OutputValue']}")
            
            return True
            
        except Exception as e:
            print(f"❌ CloudFormation deployment failed: {e}")
            return False
    
    def get_default_vpc_info(self):
        """Get default VPC and subnet information"""
        try:
            ec2 = boto3.client('ec2', region_name=self.region)
            
            # Get default VPC
            vpcs = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
            if not vpcs['Vpcs']:
                print("❌ No default VPC found")
                return None, None
            
            vpc_id = vpcs['Vpcs'][0]['VpcId']
            
            # Get public subnets
            subnets = ec2.describe_subnets(
                Filters=[
                    {'Name': 'vpc-id', 'Values': [vpc_id]},
                    {'Name': 'default-for-az', 'Values': ['true']}
                ]
            )
            
            subnet_ids = [subnet['SubnetId'] for subnet in subnets['Subnets']]
            
            print(f"✅ Found default VPC: {vpc_id}")
            print(f"✅ Found subnets: {', '.join(subnet_ids)}")
            
            return vpc_id, subnet_ids
            
        except Exception as e:
            print(f"❌ Error getting VPC info: {e}")
            return None, None

def main():
    """Main deployment function"""
    print("🚀 AWS ECS Fargate Deployment for Study Buddy")
    print("=" * 60)
    
    # Check AWS credentials
    try:
        boto3.Session().get_credentials()
    except Exception as e:
        print("❌ AWS credentials not configured. Please run 'aws configure'")
        sys.exit(1)
    
    # Get user inputs
    region = input("Enter AWS region (default: us-east-1): ").strip() or "us-east-1"
    stack_name = input("Enter CloudFormation stack name (default: studyapp-ecs): ").strip() or "studyapp-ecs"
    repository_name = input("Enter ECR repository name (default: studyapp): ").strip() or "studyapp"
    
    gemini_api_key = input("Enter your Gemini API key: ").strip()
    if not gemini_api_key:
        print("❌ Gemini API key is required")
        sys.exit(1)
    
    deployer = ECSDeployer(region)
    
    # Step 1: Create ECR repository
    print("\n📋 Step 1: Creating ECR repository...")
    repo_uri = deployer.create_ecr_repository(repository_name)
    if not repo_uri:
        sys.exit(1)
    
    # Step 2: Get VPC information
    print("\n📋 Step 2: Getting VPC information...")
    vpc_id, subnet_ids = deployer.get_default_vpc_info()
    if not vpc_id or not subnet_ids:
        print("Please manually provide VPC ID and subnet IDs")
        vpc_id = input("Enter VPC ID: ").strip()
        subnet_input = input("Enter subnet IDs (comma-separated): ").strip()
        subnet_ids = [s.strip() for s in subnet_input.split(',')]
    
    # Step 3: Build and push Docker image
    print("\n📋 Step 3: Build and push Docker image...")
    print("Please run the following commands to build and push your Docker image:")
    print(f"""
    # Get ECR login token
    aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {repo_uri.split('/')[0]}
    
    # Build the image
    docker build -t {repository_name} .
    
    # Tag the image
    docker tag {repository_name}:latest {repo_uri}:latest
    
    # Push the image
    docker push {repo_uri}:latest
    """)
    
    proceed = input("Have you completed the Docker build and push? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Please complete the Docker build and push, then run this script again.")
        sys.exit(0)
    
    # Step 4: Deploy with CloudFormation
    print("\n📋 Step 4: Deploying with CloudFormation...")
    image_uri = f"{repo_uri}:latest"
    
    success = deployer.deploy_with_cloudformation(
        stack_name, image_uri, vpc_id, subnet_ids, gemini_api_key
    )
    
    if success:
        print("\n🎉 ECS Fargate deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. Access your app via the Load Balancer URL provided above")
        print("2. Monitor your service in the ECS console")
        print("3. Check CloudWatch logs for any issues")
        print("4. Update your app by pushing a new image and updating the service")
    else:
        print("❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
