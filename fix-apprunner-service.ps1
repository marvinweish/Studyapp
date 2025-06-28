# PowerShell script to fix App Runner service issues
# Run this script to delete the failed service and create a new one

param(
    [string]$ServiceArn = "arn:aws:apprunner:us-east-1:673435220459:service/myAi/312e67c43dae48489d89a92c922d737c",
    [string]$NewServiceName = "myAi-fixed",
    [string]$GitHubRepo = "https://github.com/marvinweish/Studyapp",
    [string]$Branch = "master",
    [string]$GeminiApiKey = ""
)

Write-Host "🔧 App Runner Service Fix Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    exit 1
}

# Check AWS credentials
try {
    $identity = aws sts get-caller-identity 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ AWS credentials configured" -ForegroundColor Green
    } else {
        Write-Host "❌ AWS credentials not configured. Run 'aws configure'" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error checking AWS credentials" -ForegroundColor Red
    exit 1
}

# Step 1: Check current service status
Write-Host "`n📋 Step 1: Checking current service status..." -ForegroundColor Yellow

try {
    $serviceStatus = aws apprunner describe-service --service-arn $ServiceArn --query 'Service.Status' --output text 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Current service status: $serviceStatus" -ForegroundColor Blue
        
        if ($serviceStatus -in @("CREATE_FAILED", "UPDATE_FAILED", "DELETE_FAILED")) {
            Write-Host "⚠️ Service is in failed state. Will delete and recreate." -ForegroundColor Yellow
            $needsRecreation = $true
        } elseif ($serviceStatus -eq "OPERATION_IN_PROGRESS") {
            Write-Host "⏳ Service operation in progress. Please wait..." -ForegroundColor Yellow
            Write-Host "You may need to wait for the current operation to complete before proceeding." -ForegroundColor Yellow
            exit 0
        } else {
            Write-Host "ℹ️ Service exists with status: $serviceStatus" -ForegroundColor Blue
            $needsRecreation = $false
        }
    } else {
        Write-Host "ℹ️ Service not found or inaccessible. Will create new service." -ForegroundColor Blue
        $needsRecreation = $true
    }
} catch {
    Write-Host "ℹ️ Cannot access service. Will create new service." -ForegroundColor Blue
    $needsRecreation = $true
}

# Step 2: Delete failed service if needed
if ($needsRecreation -and $serviceStatus -and $serviceStatus -ne "DELETED") {
    Write-Host "`n📋 Step 2: Deleting failed service..." -ForegroundColor Yellow
    
    try {
        aws apprunner delete-service --service-arn $ServiceArn
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Delete operation started. Waiting for completion..." -ForegroundColor Green
            
            # Wait for deletion to complete
            do {
                Start-Sleep -Seconds 30
                $status = aws apprunner describe-service --service-arn $ServiceArn --query 'Service.Status' --output text 2>$null
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "✅ Service successfully deleted" -ForegroundColor Green
                    break
                }
                Write-Host "⏳ Deletion in progress... Status: $status" -ForegroundColor Yellow
            } while ($true)
        } else {
            Write-Host "❌ Failed to delete service" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "⚠️ Error during deletion, but continuing..." -ForegroundColor Yellow
    }
}

# Step 3: Get Gemini API key if not provided
if (-not $GeminiApiKey) {
    Write-Host "`n📋 Step 3: API Key Configuration" -ForegroundColor Yellow
    $GeminiApiKey = Read-Host "Enter your Gemini API key"
    
    if (-not $GeminiApiKey) {
        Write-Host "❌ Gemini API key is required" -ForegroundColor Red
        exit 1
    }
}

# Step 4: Create new service
Write-Host "`n📋 Step 4: Creating new App Runner service..." -ForegroundColor Yellow

# Create service configuration
$serviceConfig = @{
    ServiceName = $NewServiceName
    SourceConfiguration = @{
        Repository = @{
            RepositoryUrl = $GitHubRepo
            SourceCodeVersion = @{
                Type = "BRANCH"
                Value = $Branch
            }
            CodeConfiguration = @{
                ConfigurationSource = "REPOSITORY"
            }
        }
        AutoDeploymentsEnabled = $true
    }
    InstanceConfiguration = @{
        Cpu = "0.25 vCPU"
        Memory = "0.5 GB"
    }
    Tags = @(
        @{
            Key = "Application"
            Value = "StudyBuddy"
        }
        @{
            Key = "Environment" 
            Value = "Production"
        }
        @{
            Key = "CreatedBy"
            Value = "PowerShell-Script"
        }
    )
} | ConvertTo-Json -Depth 10

# Save config to temporary file
$configFile = "temp-apprunner-config.json"
$serviceConfig | Out-File -FilePath $configFile -Encoding UTF8

try {
    Write-Host "Creating service with name: $NewServiceName" -ForegroundColor Blue
    $createResult = aws apprunner create-service --cli-input-json "file://$configFile"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Service creation started successfully!" -ForegroundColor Green
        
        # Parse the result to get service ARN
        $result = $createResult | ConvertFrom-Json
        $newServiceArn = $result.Service.ServiceArn
        $serviceUrl = $result.Service.ServiceUrl
        
        Write-Host "🎉 New service created:" -ForegroundColor Green
        Write-Host "   Service ARN: $newServiceArn" -ForegroundColor Blue
        Write-Host "   Service URL: $serviceUrl" -ForegroundColor Blue
        
        # Monitor deployment
        Write-Host "`n📋 Step 5: Monitoring deployment..." -ForegroundColor Yellow
        Write-Host "You can monitor the deployment in the AWS Console:" -ForegroundColor Blue
        Write-Host "https://us-east-1.console.aws.amazon.com/apprunner/home?region=us-east-1#/services" -ForegroundColor Blue
        
        Write-Host "`n⏳ Waiting for service to become running..." -ForegroundColor Yellow
        do {
            Start-Sleep -Seconds 30
            $status = aws apprunner describe-service --service-arn $newServiceArn --query 'Service.Status' --output text
            Write-Host "Current status: $status" -ForegroundColor Blue
            
            if ($status -eq "RUNNING") {
                Write-Host "🎉 Service is now running!" -ForegroundColor Green
                Write-Host "Access your app at: $serviceUrl" -ForegroundColor Green
                break
            } elseif ($status -in @("CREATE_FAILED", "UPDATE_FAILED")) {
                Write-Host "❌ Service creation failed. Check AWS Console for details." -ForegroundColor Red
                break
            }
        } while ($true)
        
    } else {
        Write-Host "❌ Failed to create service" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error creating service: $_" -ForegroundColor Red
    exit 1
} finally {
    # Clean up temporary file
    if (Test-Path $configFile) {
        Remove-Item $configFile
    }
}

Write-Host "`n✅ App Runner service fix completed!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test your application at the service URL" -ForegroundColor White
Write-Host "2. Configure environment variables if needed" -ForegroundColor White
Write-Host "3. Set up custom domain if desired" -ForegroundColor White
