#!/usr/bin/env python3
"""
Test script for the unified D&D Character Art Generator
Validates all components and functionality
"""

import os
import sys
import json
import time
from typing import Dict, Any

# Add the apps directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from apps.unified_app import UnifiedArtGenerator, create_unified_app
        print("✅ Unified app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import unified app: {e}")
        return False
    
    try:
        from apps.openai_integration import PromptEnhancer, CharacterAnalyzer
        print("✅ OpenAI integration imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import OpenAI integration: {e}")
        return False
    
    try:
        from apps.system_diagnostics import SystemDiagnostics
        print("✅ System diagnostics imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import system diagnostics: {e}")
        return False
    
    try:
        from apps.comfyui_export import ComfyUIExporter
        print("✅ ComfyUI export imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ComfyUI export: {e}")
        return False
    
    return True

def test_system_diagnostics():
    """Test system diagnostics functionality"""
    print("\n🧪 Testing system diagnostics...")
    
    try:
        from apps.system_diagnostics import SystemDiagnostics
        
        diagnostics = SystemDiagnostics()
        analysis = diagnostics.analyze_system()
        
        print(f"✅ System analysis completed")
        print(f"   - GPU available: {analysis['system_info']['gpu']['available']}")
        print(f"   - Performance score: {analysis['performance_score']}")
        print(f"   - Health status: {analysis['health_status']['overall']}")
        
        return True
    except Exception as e:
        print(f"❌ System diagnostics test failed: {e}")
        return False

def test_openai_integration():
    """Test OpenAI integration functionality"""
    print("\n🧪 Testing OpenAI integration...")
    
    try:
        from apps.openai_integration import PromptEnhancer, CharacterAnalyzer
        
        # Test without API key
        enhancer = PromptEnhancer()
        print(f"✅ PromptEnhancer created (available: {enhancer.available})")
        
        # Test character analyzer
        analyzer = CharacterAnalyzer(enhancer)
        print("✅ CharacterAnalyzer created")
        
        # Test with sample data
        test_character = {
            "name": "Test Character",
            "race": "Human",
            "class_name": "Fighter",
            "appearance": "Tall and muscular",
            "equipment": ["Sword", "Shield"]
        }
        
        if enhancer.available:
            enhanced = enhancer.enhance_character_prompt(test_character, "fantasy_realistic", "A warrior")
            print(f"✅ Prompt enhancement: {len(enhanced)} characters")
        else:
            print("ℹ️  OpenAI not available (expected without API key)")
        
        return True
    except Exception as e:
        print(f"❌ OpenAI integration test failed: {e}")
        return False

def test_comfyui_export():
    """Test ComfyUI export functionality"""
    print("\n🧪 Testing ComfyUI export...")
    
    try:
        from apps.comfyui_export import ComfyUIExporter
        
        exporter = ComfyUIExporter()
        print("✅ ComfyUIExporter created")
        
        # Test workflow creation
        test_settings = {
            "positive": "Fantasy warrior, detailed armor",
            "negative": "blurry, low quality",
            "width": 896,
            "height": 1120,
            "steps": 30,
            "cfg": 6.5,
            "use_lineart": True,
            "use_refiner": True
        }
        
        workflow_path = exporter.export_from_gradio_settings(test_settings, "test_workflow")
        print(f"✅ Workflow exported to: {workflow_path}")
        
        # Test workflow validation
        validation = exporter.validate_workflow(workflow_path)
        print(f"✅ Workflow validation: {validation['valid']}")
        
        return True
    except Exception as e:
        print(f"❌ ComfyUI export test failed: {e}")
        return False

def test_unified_generator():
    """Test the unified art generator"""
    print("\n🧪 Testing unified art generator...")
    
    try:
        from apps.unified_app import UnifiedArtGenerator
        
        # Create generator without API keys
        generator = UnifiedArtGenerator(auto_optimize=False)
        print("✅ UnifiedArtGenerator created")
        
        # Test system diagnostics
        diagnostics = generator.get_system_diagnostics()
        print(f"✅ System diagnostics: {diagnostics['performance_score']} score")
        
        # Test ComfyUI export
        export_result = generator.export_to_comfyui("test_workflow")
        print(f"✅ ComfyUI export: {export_result}")
        
        return True
    except Exception as e:
        print(f"❌ Unified generator test failed: {e}")
        return False

def test_gradio_app():
    """Test Gradio app creation"""
    print("\n🧪 Testing Gradio app creation...")
    
    try:
        from apps.unified_app import create_unified_app
        
        # Create app without API keys
        app = create_unified_app(auto_optimize=False)
        print("✅ Gradio app created successfully")
        
        # Test app structure
        if hasattr(app, 'blocks'):
            print("✅ App has blocks structure")
        else:
            print("⚠️  App structure may be incomplete")
        
        return True
    except Exception as e:
        print(f"❌ Gradio app test failed: {e}")
        return False

def test_configuration_files():
    """Test configuration files"""
    print("\n🧪 Testing configuration files...")
    
    config_files = [
        "config/default_settings.json",
        "requirements.txt",
        "assets/workflows/comfy_sdxl_character_art.json"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} exists")
            
            # Test JSON files
            if config_file.endswith('.json'):
                try:
                    with open(config_file, 'r') as f:
                        json.load(f)
                    print(f"✅ {config_file} is valid JSON")
                except json.JSONDecodeError as e:
                    print(f"❌ {config_file} is invalid JSON: {e}")
                    return False
        else:
            print(f"❌ {config_file} missing")
            return False
    
    return True

def test_notebook_structure():
    """Test notebook structure"""
    print("\n🧪 Testing notebook structure...")
    
    notebook_file = "main_notebook.ipynb"
    if os.path.exists(notebook_file):
        print(f"✅ {notebook_file} exists")
        
        try:
            with open(notebook_file, 'r') as f:
                notebook = json.load(f)
            
            if 'cells' in notebook:
                print(f"✅ Notebook has {len(notebook['cells'])} cells")
                
                # Check for required cells
                cell_types = [cell.get('cell_type', '') for cell in notebook['cells']]
                if 'markdown' in cell_types and 'code' in cell_types:
                    print("✅ Notebook has required cell types")
                else:
                    print("⚠️  Notebook may be missing required cell types")
            else:
                print("❌ Notebook structure invalid")
                return False
        except json.JSONDecodeError as e:
            print(f"❌ Notebook is invalid JSON: {e}")
            return False
    else:
        print(f"❌ {notebook_file} missing")
        return False
    
    return True

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("🚀 Starting comprehensive test suite...")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("System Diagnostics", test_system_diagnostics),
        ("OpenAI Integration", test_openai_integration),
        ("ComfyUI Export", test_comfyui_export),
        ("Unified Generator", test_unified_generator),
        ("Gradio App", test_gradio_app),
        ("Configuration Files", test_configuration_files),
        ("Notebook Structure", test_notebook_structure)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
