# 🚀 AWS ECS Fargate Deployment Guide

Complete guide for deploying Study Buddy app on AWS ECS with Fargate.

## 🏗️ **ECS with Fargate vs App Runner**

| Feature | **ECS Fargate** | **App Runner** |
|---------|----------------|----------------|
| **Control** | 🟢 Full control over infrastructure | 🟡 Limited customization |
| **Scaling** | 🟢 Fine-grained auto-scaling rules | 🟢 Automatic scaling |
| **Networking** | 🟢 VPC, security groups, load balancer | 🟡 Managed networking |
| **Cost** | 🟡 Pay for compute + load balancer | 🟢 Pay only for compute time |
| **Complexity** | 🔴 More complex setup | 🟢 Simple push-to-deploy |
| **Monitoring** | 🟢 Full CloudWatch integration | 🟡 Basic monitoring |
| **Load Balancing** | 🟢 Application Load Balancer included | 🟡 Built-in, limited config |

## 📋 **Prerequisites**

1. **AWS Account** with ECS and ECR permissions
2. **Docker** installed locally
3. **AWS CLI** configured
4. **Gemini API Key** from Google AI Studio

## 🚀 **Deployment Methods**

### Option 1: Automated Script (Recommended)

```bash
# Run the automated deployment script
python ecs_deploy.py
```

### Option 2: Manual Step-by-Step

#### Step 1: Create ECR Repository
```bash
# Create repository
aws ecr create-repository --repository-name studyapp --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### Step 2: Build and Push Docker Image
```bash
# Build the image
docker build -t studyapp .

# Tag for ECR
docker tag studyapp:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/studyapp:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/studyapp:latest
```

#### Step 3: Deploy Infrastructure
```bash
# Deploy using CloudFormation
aws cloudformation create-stack \
  --stack-name studyapp-ecs \
  --template-body file://ecs-cloudformation.json \
  --parameters ParameterKey=GeminiApiKey,ParameterValue=YOUR_API_KEY \
               ParameterKey=VpcId,ParameterValue=vpc-xxxxxxxx \
               ParameterKey=SubnetIds,ParameterValue="subnet-xxxxxxxx,subnet-yyyyyyyy" \
               ParameterKey=ImageUri,ParameterValue=YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/studyapp:latest \
  --capabilities CAPABILITY_IAM
```

## 🔧 **Configuration Files**

### Files Optimized for ECS:

1. **`ecs-task-definition.json`** - ECS task configuration
2. **`ecs-cloudformation.json`** - Complete infrastructure as code
3. **`Dockerfile`** - Container configuration with health checks
4. **`ecs_deploy.py`** - Automated deployment script

### Key ECS Optimizations:

✅ **Fargate Launch Type** - Serverless containers
✅ **Application Load Balancer** - Public web access with health checks
✅ **Auto Scaling** - Scale based on CPU/memory usage
✅ **Security Groups** - Proper network isolation
✅ **CloudWatch Logs** - Centralized logging
✅ **Secrets Manager** - Secure API key storage
✅ **Health Checks** - Application and container level

## 📊 **Resource Configuration**

```json
{
  "CPU": "256",           // 0.25 vCPU
  "Memory": "512",        // 512 MB RAM
  "DesiredCount": 1,      // Number of running tasks
  "MaxCapacity": 10,      // Auto-scaling limit
  "TargetCPU": 70        // Scale at 70% CPU
}
```

## 🔒 **Security Features**

- **VPC Isolation** - Run in private subnets
- **Security Groups** - Fine-grained network access
- **IAM Roles** - Least privilege access
- **Secrets Manager** - Encrypted API key storage
- **Non-root Container** - Security best practices
- **HTTPS Ready** - Easy SSL certificate integration

## 📈 **Monitoring & Logging**

### CloudWatch Integration:
- **Container Logs** - `/ecs/studyapp` log group
- **Metrics** - CPU, memory, network usage
- **Health Checks** - Application availability
- **Alarms** - Auto-scaling triggers

### Useful CloudWatch Queries:
```bash
# View recent logs
aws logs tail /ecs/studyapp --follow

# Get service status
aws ecs describe-services --cluster studyapp-cluster --services studyapp-service
```

## 💰 **Cost Breakdown**

### Monthly Costs (us-east-1):
- **Fargate (0.25 vCPU, 512MB)**: ~$10-15/month
- **Application Load Balancer**: ~$18/month
- **CloudWatch Logs**: ~$1-3/month
- **Data Transfer**: ~$1-5/month
- **Total**: ~$30-41/month

### Cost Optimization:
- Use **Spot Fargate** for development (50% savings)
- **Schedule scaling** to zero during off-hours
- **Optimize container size** for your workload

## 🔄 **Updates & Maintenance**

### Update Application:
```bash
# Build new image
docker build -t studyapp .
docker tag studyapp:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/studyapp:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/studyapp:latest

# Force new deployment
aws ecs update-service --cluster studyapp-cluster --service studyapp-service --force-new-deployment
```

### Scale Service:
```bash
# Scale to 3 instances
aws ecs update-service --cluster studyapp-cluster --service studyapp-service --desired-count 3
```

## 🆘 **Troubleshooting**

### Common Issues:

1. **Service won't start**
   ```bash
   # Check service events
   aws ecs describe-services --cluster studyapp-cluster --services studyapp-service
   
   # Check task status
   aws ecs list-tasks --cluster studyapp-cluster --service-name studyapp-service
   ```

2. **Health check failures**
   ```bash
   # Check container logs
   aws logs tail /ecs/studyapp --follow
   
   # Verify health endpoint
   curl http://LOAD_BALANCER_URL/
   ```

3. **Cannot pull image**
   ```bash
   # Verify ECR permissions
   aws ecr describe-repositories --repository-names studyapp
   
   # Check task execution role
   aws iam get-role --role-name ecsTaskExecutionRole
   ```

### Useful Commands:
```bash
# Check cluster status
aws ecs describe-clusters --clusters studyapp-cluster

# View running tasks
aws ecs list-tasks --cluster studyapp-cluster

# Stop a task (forces restart)
aws ecs stop-task --cluster studyapp-cluster --task TASK_ARN

# Update service configuration
aws ecs update-service --cluster studyapp-cluster --service studyapp-service --task-definition studyapp-task:2
```

## 🎯 **When to Choose ECS Fargate**

**Choose ECS Fargate when you need:**
- Full control over networking and security
- Integration with existing AWS infrastructure
- Custom auto-scaling rules
- Multiple environments (dev/staging/prod)
- Advanced monitoring and alerting
- Load balancer with custom rules

**Choose App Runner when you want:**
- Simple push-to-deploy workflow
- Minimal infrastructure management
- Quick prototyping and development
- Lower operational overhead

## 📚 **Additional Resources**

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [CloudFormation ECS Examples](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-ecs.html)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)

---

**Ready to deploy?** Run `python ecs_deploy.py` to get started! 🚀
