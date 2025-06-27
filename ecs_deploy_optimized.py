#!/usr/bin/env python3
"""
Enhanced AWS ECS Fargate deployment script for Study Buddy application
Includes auto-scaling, monitoring, and optimization features
"""

import boto3
import json
import sys
import time
import subprocess
import os
from typing import Optional, Dict, List

class OptimizedECSDeployer:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.ecr = boto3.client('ecr', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
        self.cloudformation = boto3.client('cloudformation', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.application_autoscaling = boto3.client('application-autoscaling', region_name=region)
        
    def create_ecr_repository(self, repository_name: str) -> str:
        """Create ECR repository with lifecycle policy"""
        try:
            response = self.ecr.create_repository(
                repositoryName=repository_name,
                imageScanningConfiguration={'scanOnPush': True},
                encryptionConfiguration={'encryptionType': 'AES256'}
            )
            repo_uri = response['repository']['repositoryUri']
            print(f"✅ Created ECR repository: {repo_uri}")
            
            # Set lifecycle policy to manage image retention
            lifecycle_policy = {
                "rules": [
                    {
                        "rulePriority": 1,
                        "description": "Keep last 10 images",
                        "selection": {
                            "tagStatus": "any",
                            "countType": "imageCountMoreThan",
                            "countNumber": 10
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }
            
            self.ecr.put_lifecycle_policy(
                repositoryName=repository_name,
                lifecyclePolicyText=json.dumps(lifecycle_policy)
            )
            print("✅ Set ECR lifecycle policy")
            
            return repo_uri
            
        except self.ecr.exceptions.RepositoryAlreadyExistsException:
            response = self.ecr.describe_repositories(repositoryNames=[repository_name])
            repo_uri = response['repositories'][0]['repositoryUri']
            print(f"ℹ️ ECR repository already exists: {repo_uri}")
            return repo_uri
        except Exception as e:
            print(f"❌ Error creating ECR repository: {e}")
            return None
    
    def build_and_push_image(self, repository_name: str, repo_uri: str, dockerfile: str = "Dockerfile.ecs") -> bool:
        """Build and push Docker image with optimizations"""
        try:
            print("🏗️ Building optimized Docker image...")
            
            # Get ECR login token
            token_response = self.ecr.get_authorization_token()
            token = token_response['authorizationData'][0]['authorizationToken']
            endpoint = token_response['authorizationData'][0]['proxyEndpoint']
            
            # Login to ECR
            login_cmd = f"aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {endpoint}"
            result = subprocess.run(login_cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ ECR login failed: {result.stderr}")
                return False
            
            # Build image with optimizations
            build_cmd = [
                "docker", "build",
                "-f", dockerfile,
                "-t", repository_name,
                "--build-arg", "DEBIAN_FRONTEND=noninteractive",
                "--no-cache",  # Ensure fresh build
                "."
            ]
            
            print(f"Building with command: {' '.join(build_cmd)}")
            result = subprocess.run(build_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Docker build failed: {result.stderr}")
                return False
            
            print("✅ Docker image built successfully")
            
            # Tag image
            tag_cmd = ["docker", "tag", f"{repository_name}:latest", f"{repo_uri}:latest"]
            result = subprocess.run(tag_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Docker tag failed: {result.stderr}")
                return False
            
            # Push image
            print("📤 Pushing image to ECR...")
            push_cmd = ["docker", "push", f"{repo_uri}:latest"]
            result = subprocess.run(push_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Docker push failed: {result.stderr}")
                return False
            
            print("✅ Image pushed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error building/pushing image: {e}")
            return False
    
    def deploy_with_cloudformation(self, stack_name: str, image_uri: str, 
                                 vpc_id: str, subnet_ids: list, gemini_api_key: str, 
                                 environment: str = "production",
                                 min_capacity: int = 1, max_capacity: int = 10) -> bool:
        """Deploy using optimized CloudFormation template"""
        try:
            template_file = 'ecs-fargate-optimized.json'
            if not os.path.exists(template_file):
                print(f"❌ Template file not found: {template_file}")
                return False
                
            with open(template_file, 'r') as f:
                template_body = f.read()
            
            parameters = [
                {'ParameterKey': 'GeminiApiKey', 'ParameterValue': gemini_api_key},
                {'ParameterKey': 'VpcId', 'ParameterValue': vpc_id},
                {'ParameterKey': 'SubnetIds', 'ParameterValue': ','.join(subnet_ids)},
                {'ParameterKey': 'ImageUri', 'ParameterValue': image_uri},
                {'ParameterKey': 'Environment', 'ParameterValue': environment},
                {'ParameterKey': 'MinCapacity', 'ParameterValue': str(min_capacity)},
                {'ParameterKey': 'MaxCapacity', 'ParameterValue': str(max_capacity)}
            ]
            
            try:
                response = self.cloudformation.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body,
                    Parameters=parameters,
                    Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                    Tags=[
                        {'Key': 'Application', 'Value': 'StudyBuddy'},
                        {'Key': 'Environment', 'Value': environment},
                        {'Key': 'ManagedBy', 'Value': 'CloudFormation'}
                    ]
                )
                print(f"✅ CloudFormation stack creation initiated: {response['StackId']}")
                operation = 'create'
                
            except self.cloudformation.exceptions.AlreadyExistsException:
                print("ℹ️ Stack already exists, updating...")
                try:
                    response = self.cloudformation.update_stack(
                        StackName=stack_name,
                        TemplateBody=template_body,
                        Parameters=parameters,
                        Capabilities=['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
                        Tags=[
                            {'Key': 'Application', 'Value': 'StudyBuddy'},
                            {'Key': 'Environment', 'Value': environment},
                            {'Key': 'ManagedBy', 'Value': 'CloudFormation'}
                        ]
                    )
                    print(f"✅ CloudFormation stack update initiated")
                    operation = 'update'
                except self.cloudformation.exceptions.ClientError as e:
                    if 'No updates are to be performed' in str(e):
                        print("ℹ️ No changes detected, stack is up to date")
                        return True
                    else:
                        raise
            
            # Wait for completion with progress updates
            print("⏳ Waiting for CloudFormation deployment to complete...")
            self._wait_for_stack_completion(stack_name, operation)
            
            # Get and display outputs
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            outputs = response['Stacks'][0].get('Outputs', [])
            
            print("\n🎉 Deployment completed successfully!")
            print("=" * 60)
            for output in outputs:
                print(f"🔗 {output['Description']}: {output['OutputValue']}")
            
            # Show additional deployment info
            self._show_deployment_info(stack_name)
            
            return True
            
        except Exception as e:
            print(f"❌ CloudFormation deployment failed: {e}")
            return False
    
    def _wait_for_stack_completion(self, stack_name: str, operation: str):
        """Wait for stack operation to complete with progress updates"""
        waiter_name = f'stack_{operation}_complete'
        waiter = self.cloudformation.get_waiter(waiter_name)
        
        start_time = time.time()
        max_attempts = 60  # 30 minutes max
        
        try:
            waiter.wait(
                StackName=stack_name, 
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': max_attempts
                }
            )
        except Exception as e:
            print(f"⚠️ Waiter error: {e}")
            # Check stack status manually
            self._check_stack_status(stack_name)
    
    def _check_stack_status(self, stack_name: str):
        """Check and display stack status"""
        try:
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            stack = response['Stacks'][0]
            status = stack['StackStatus']
            print(f"Stack Status: {status}")
            
            if 'FAILED' in status or 'ROLLBACK' in status:
                print("❌ Stack operation failed. Checking events...")
                self._show_stack_events(stack_name)
                
        except Exception as e:
            print(f"Error checking stack status: {e}")
    
    def _show_stack_events(self, stack_name: str, max_events: int = 10):
        """Show recent stack events for debugging"""
        try:
            response = self.cloudformation.describe_stack_events(StackName=stack_name)
            events = response['StackEvents'][:max_events]
            
            print("\nRecent Stack Events:")
            print("-" * 80)
            for event in events:
                timestamp = event['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                resource = event.get('LogicalResourceId', 'N/A')
                status = event.get('ResourceStatus', 'N/A')
                reason = event.get('ResourceStatusReason', 'N/A')
                print(f"{timestamp} | {resource} | {status} | {reason}")
                
        except Exception as e:
            print(f"Error retrieving stack events: {e}")
    
    def _show_deployment_info(self, stack_name: str):
        """Show additional deployment information"""
        try:
            print("\n📊 Deployment Information:")
            print("-" * 40)
            
            # Get stack resources
            response = self.cloudformation.list_stack_resources(StackName=stack_name)
            resources = response['StackResourceSummaries']
            
            for resource in resources:
                if resource['ResourceType'] == 'AWS::ECS::Service':
                    service_name = resource['PhysicalResourceId']
                    cluster_name = None
                    
                    # Find cluster name
                    for r in resources:
                        if r['ResourceType'] == 'AWS::ECS::Cluster':
                            cluster_name = r['PhysicalResourceId']
                            break
                    
                    if cluster_name:
                        # Get service details
                        service_response = self.ecs.describe_services(
                            cluster=cluster_name,
                            services=[service_name]
                        )
                        
                        if service_response['services']:
                            service = service_response['services'][0]
                            print(f"Service: {service_name}")
                            print(f"Cluster: {cluster_name}")
                            print(f"Desired Tasks: {service['desiredCount']}")
                            print(f"Running Tasks: {service['runningCount']}")
                            print(f"Pending Tasks: {service['pendingCount']}")
            
        except Exception as e:
            print(f"Error retrieving deployment info: {e}")
    
    def get_default_vpc_info(self):
        """Get default VPC and subnet information with AZ distribution"""
        try:
            ec2 = boto3.client('ec2', region_name=self.region)
            
            # Get default VPC
            vpcs = ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
            if not vpcs['Vpcs']:
                print("❌ No default VPC found")
                return None, None
            
            vpc_id = vpcs['Vpcs'][0]['VpcId']
            
            # Get public subnets with AZ distribution
            subnets = ec2.describe_subnets(
                Filters=[
                    {'Name': 'vpc-id', 'Values': [vpc_id]},
                    {'Name': 'default-for-az', 'Values': ['true']}
                ]
            )
            
            # Ensure we have subnets in different AZs
            subnet_by_az = {}
            for subnet in subnets['Subnets']:
                az = subnet['AvailabilityZone']
                if az not in subnet_by_az:
                    subnet_by_az[az] = subnet['SubnetId']
            
            subnet_ids = list(subnet_by_az.values())
            
            if len(subnet_ids) < 2:
                print("⚠️ Warning: Less than 2 subnets found. ALB requires subnets in at least 2 AZs")
            
            print(f"✅ Found default VPC: {vpc_id}")
            print(f"✅ Found subnets in {len(subnet_ids)} AZs: {', '.join(subnet_ids)}")
            
            return vpc_id, subnet_ids
            
        except Exception as e:
            print(f"❌ Error getting VPC info: {e}")
            return None, None

def main():
    """Main enhanced deployment function"""
    print("🚀 AWS ECS Fargate Optimized Deployment for Study Buddy")
    print("=" * 70)
    
    # Check prerequisites
    try:
        boto3.Session().get_credentials()
    except Exception as e:
        print("❌ AWS credentials not configured. Please run 'aws configure'")
        sys.exit(1)
    
    # Check Docker
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not found. Please install Docker")
        sys.exit(1)
    
    # Get configuration
    print("\n📋 Configuration:")
    region = input("Enter AWS region (default: us-east-1): ").strip() or "us-east-1"
    stack_name = input("Enter CloudFormation stack name (default: studyapp-ecs): ").strip() or "studyapp-ecs"
    repository_name = input("Enter ECR repository name (default: studyapp): ").strip() or "studyapp"
    environment = input("Enter environment (development/staging/production, default: production): ").strip() or "production"
    
    if environment not in ['development', 'staging', 'production']:
        print("❌ Invalid environment. Must be development, staging, or production")
        sys.exit(1)
    
    # Auto-scaling configuration
    print(f"\n⚖️ Auto-scaling configuration for {environment}:")
    default_min = 1 if environment == 'development' else 2
    default_max = 3 if environment == 'development' else 10
    
    min_capacity = input(f"Minimum capacity (default: {default_min}): ").strip()
    min_capacity = int(min_capacity) if min_capacity else default_min
    
    max_capacity = input(f"Maximum capacity (default: {default_max}): ").strip()
    max_capacity = int(max_capacity) if max_capacity else default_max
    
    gemini_api_key = input("Enter your Gemini API key: ").strip()
    if not gemini_api_key:
        print("❌ Gemini API key is required")
        sys.exit(1)
    
    deployer = OptimizedECSDeployer(region)
    
    # Step 1: Create ECR repository
    print("\n📋 Step 1: Setting up ECR repository...")
    repo_uri = deployer.create_ecr_repository(repository_name)
    if not repo_uri:
        sys.exit(1)
    
    # Step 2: Get VPC information
    print("\n📋 Step 2: Getting VPC information...")
    vpc_id, subnet_ids = deployer.get_default_vpc_info()
    if not vpc_id or not subnet_ids:
        print("Please manually provide VPC ID and subnet IDs")
        vpc_id = input("Enter VPC ID: ").strip()
        subnet_input = input("Enter subnet IDs (comma-separated, at least 2): ").strip()
        subnet_ids = [s.strip() for s in subnet_input.split(',')]
        
        if len(subnet_ids) < 2:
            print("❌ At least 2 subnets required for ALB")
            sys.exit(1)
    
    # Step 3: Build and push Docker image
    print("\n📋 Step 3: Building and pushing Docker image...")
    if not deployer.build_and_push_image(repository_name, repo_uri):
        print("❌ Failed to build and push image")
        sys.exit(1)
    
    # Step 4: Deploy with CloudFormation
    print("\n📋 Step 4: Deploying with CloudFormation...")
    image_uri = f"{repo_uri}:latest"
    
    success = deployer.deploy_with_cloudformation(
        stack_name, image_uri, vpc_id, subnet_ids, gemini_api_key,
        environment, min_capacity, max_capacity
    )
    
    if success:
        print("\n🎉 ECS Fargate deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. Access your app via the Load Balancer URL provided above")
        print("2. Monitor your service in the ECS console")
        print("3. Check CloudWatch logs and metrics")
        print("4. Auto-scaling is configured based on CPU utilization")
        print("5. Update your app by pushing a new image and updating the service")
        print("\n💡 Monitoring URLs:")
        print(f"   - ECS Console: https://{region}.console.aws.amazon.com/ecs/home?region={region}#/clusters")
        print(f"   - CloudWatch: https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}")
    else:
        print("❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
