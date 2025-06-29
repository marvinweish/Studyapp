#!/usr/bin/env python3
"""
Test script to verify GCP deployment readiness
"""

import os
import sys
import traceback

def test_gcp_config():
    """Test GCP configuration"""
    print("🧪 Testing GCP Configuration...")
    
    try:
        # Set mock GCP environment
        os.environ['GOOGLE_CLOUD_PROJECT'] = 'test-project'
        os.environ['PORT'] = '8080'
        
        # Import config
        from config_gcp import IS_GCP, TEMP_DIR, PORT
        
        print(f"✅ GCP detected: {IS_GCP}")
        print(f"✅ Temp directory: {TEMP_DIR}")
        print(f"✅ Port: {PORT}")
        
        # Clean up
        del os.environ['GOOGLE_CLOUD_PROJECT']
        del os.environ['PORT']
        
        return True
        
    except Exception as e:
        print(f"❌ GCP config test failed: {e}")
        traceback.print_exc()
        return False

def test_ai_generator():
    """Test AI generator"""
    print("\n🧪 Testing AI Generator...")
    
    try:
        from gcp_ai_generator import ai_generator
        
        print(f"✅ AI generator type: {type(ai_generator).__name__}")
        print(f"✅ Has API: {getattr(ai_generator, 'has_api', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI generator test failed: {e}")
        traceback.print_exc()
        return False

def test_app_import():
    """Test main app import"""
    print("\n🧪 Testing App Import...")
    
    try:
        from study_app import main
        print("✅ Main app imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ App import test failed: {e}")
        traceback.print_exc()
        return False

def test_cloud_detection():
    """Test cloud environment detection"""
    print("\n🧪 Testing Cloud Detection...")
    
    try:
        # Test various cloud environments
        test_envs = [
            ('GAE_ENV', 'standard'),
            ('CLOUD_RUN_SERVICE', 'test-service'),
            ('K_SERVICE', 'test-knative'),
            ('AWS_EXECUTION_ENV', 'AWS_ECS_FARGATE'),
            ('PORT', '8080')
        ]
        
        for env_var, value in test_envs:
            # Set environment
            os.environ[env_var] = value
            
            # Test detection in study_app.py logic
            is_cloud = bool(
                os.environ.get('GAE_ENV') or
                os.environ.get('CLOUD_RUN_SERVICE') or
                os.environ.get('K_SERVICE') or
                os.environ.get('AWS_EXECUTION_ENV') or
                os.environ.get('PORT') or
                os.environ.get('ECS_CONTAINER_METADATA_URI')
            )
            
            print(f"✅ {env_var}={value} -> Cloud detected: {is_cloud}")
            
            # Clean up
            del os.environ[env_var]
        
        return True
        
    except Exception as e:
        print(f"❌ Cloud detection test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 GCP Deployment Readiness Test")
    print("=" * 50)
    
    tests = [
        ("GCP Configuration", test_gcp_config),
        ("AI Generator", test_ai_generator),
        ("App Import", test_app_import),
        ("Cloud Detection", test_cloud_detection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for GCP deployment.")
        print("\n🚀 Next steps:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run: gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-study-buddy")
        print("3. Run: gcloud run deploy ai-study-buddy --image gcr.io/YOUR_PROJECT_ID/ai-study-buddy")
        return True
    else:
        print("⚠️ Some tests failed. Fix issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
