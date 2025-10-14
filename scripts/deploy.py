#!/usr/bin/env python3
"""
Deployment script for D&D Character Art Generator
Automates the deployment process and validates the system
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    print("🔍 Checking requirements...")
    
    required_files = [
        "main_notebook.ipynb",
        "apps/unified_app.py",
        "apps/openai_integration.py",
        "apps/system_diagnostics.py",
        "apps/comfyui_export.py",
        "config/default_settings.json",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def validate_notebook():
    """Validate the main notebook structure"""
    print("🔍 Validating notebook structure...")
    
    try:
        with open("main_notebook.ipynb", 'r') as f:
            notebook = json.load(f)
        
        if 'cells' not in notebook:
            print("❌ Notebook missing cells")
            return False
        
        cell_count = len(notebook['cells'])
        if cell_count < 4:
            print(f"❌ Notebook has only {cell_count} cells, expected at least 4")
            return False
        
        # Check for required cell types
        cell_types = [cell.get('cell_type', '') for cell in notebook['cells']]
        if 'markdown' not in cell_types:
            print("❌ Notebook missing markdown cells")
            return False
        
        if 'code' not in cell_types:
            print("❌ Notebook missing code cells")
            return False
        
        print(f"✅ Notebook validated: {cell_count} cells")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Notebook JSON invalid: {e}")
        return False
    except Exception as e:
        print(f"❌ Notebook validation failed: {e}")
        return False

def validate_config():
    """Validate configuration files"""
    print("🔍 Validating configuration...")
    
    config_files = [
        "config/default_settings.json",
        "assets/workflows/comfy_sdxl_character_art.json"
    ]
    
    for config_file in config_files:
        if not os.path.exists(config_file):
            print(f"❌ Missing config file: {config_file}")
            return False
        
        try:
            with open(config_file, 'r') as f:
                json.load(f)
            print(f"✅ {config_file} is valid JSON")
        except json.JSONDecodeError as e:
            print(f"❌ {config_file} is invalid JSON: {e}")
            return False
    
    return True

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    
    # Add apps directory to path
    apps_path = os.path.join(os.getcwd(), 'apps')
    if apps_path not in sys.path:
        sys.path.insert(0, apps_path)
    
    # Test file existence first
    required_modules = [
        "openai_integration.py",
        "system_diagnostics.py", 
        "comfyui_export.py",
        "unified_app.py"
    ]
    
    for module in required_modules:
        module_path = os.path.join(apps_path, module)
        if not os.path.exists(module_path):
            print(f"❌ Missing module: {module}")
            return False
        print(f"✅ {module} exists")
    
    # Test basic import (may fail due to missing dependencies, but that's OK)
    try:
        import openai_integration
        print("✅ OpenAI integration module structure valid")
    except ImportError as e:
        if "No module named" in str(e) and "psutil" in str(e):
            print("ℹ️  System diagnostics requires psutil (expected without dependencies)")
        else:
            print(f"❌ OpenAI integration import failed: {e}")
            return False
    
    try:
        import system_diagnostics
        print("✅ System diagnostics module structure valid")
    except ImportError as e:
        if "No module named" in str(e) and "psutil" in str(e):
            print("ℹ️  System diagnostics requires psutil (expected without dependencies)")
        else:
            print(f"❌ System diagnostics import failed: {e}")
            return False
    
    try:
        import comfyui_export
        print("✅ ComfyUI export module structure valid")
    except ImportError as e:
        print(f"❌ ComfyUI export import failed: {e}")
        return False
    
    return True

def create_deployment_package():
    """Create deployment package"""
    print("📦 Creating deployment package...")
    
    # Create deployment directory
    deploy_dir = "deployment"
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Copy essential files
    essential_files = [
        "main_notebook.ipynb",
        "apps/",
        "config/",
        "assets/",
        "docs/",
        "requirements.txt",
        "README.md",
        "DEPLOYMENT_GUIDE.md"
    ]
    
    for item in essential_files:
        if os.path.isdir(item):
            subprocess.run(["cp", "-r", item, deploy_dir], check=True)
        else:
            subprocess.run(["cp", item, deploy_dir], check=True)
    
    print(f"✅ Deployment package created in {deploy_dir}/")
    return True

def generate_deployment_summary():
    """Generate deployment summary"""
    print("📊 Generating deployment summary...")
    
    # Count files
    total_files = 0
    total_lines = 0
    
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and git
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'deployment']
        
        for file in files:
            if file.endswith(('.py', '.ipynb', '.json', '.md', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_files += 1
                        total_lines += len(lines)
                except:
                    pass
    
    summary = {
        "total_files": total_files,
        "total_lines": total_lines,
        "components": {
            "notebook": "main_notebook.ipynb",
            "unified_app": "apps/unified_app.py",
            "openai_integration": "apps/openai_integration.py",
            "system_diagnostics": "apps/system_diagnostics.py",
            "comfyui_export": "apps/comfyui_export.py"
        },
        "features": [
            "5 Art Styles",
            "AI Prompt Enhancement",
            "System Diagnostics",
            "ComfyUI Export",
            "Security Hardening",
            "Auto-Optimization"
        ]
    }
    
    with open("deployment_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Deployment summary: {total_files} files, {total_lines} lines")
    return True

def main():
    """Main deployment process"""
    print("🚀 D&D Character Art Generator - Deployment Script")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    # Validate notebook
    if not validate_notebook():
        print("❌ Notebook validation failed")
        return False
    
    # Validate config
    if not validate_config():
        print("❌ Configuration validation failed")
        return False
    
    # Test imports (without dependencies)
    if not test_imports():
        print("❌ Import test failed")
        return False
    
    # Create deployment package
    if not create_deployment_package():
        print("❌ Deployment package creation failed")
        return False
    
    # Generate summary
    if not generate_deployment_summary():
        print("❌ Summary generation failed")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 DEPLOYMENT READY!")
    print("=" * 60)
    print("✅ All validations passed")
    print("✅ Deployment package created")
    print("✅ System ready for deployment")
    print("\n📋 Next Steps:")
    print("1. Upload main_notebook.ipynb to Google Colab")
    print("2. Click 'Runtime' → 'Run all'")
    print("3. Wait for setup (2-3 minutes)")
    print("4. Click the generated link")
    print("5. Start creating art!")
    print("\n🎯 Ready to deploy! 🚀")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
