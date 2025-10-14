# 📁 Project Structure

## 🎯 Clean, Organized Repository

```
dnd-character-art-generator/
├── 📱 main_notebook.ipynb              # Single unified Colab notebook
├── 🏗️ apps/                           # Core application modules
│   ├── unified_app.py                 # Main Gradio application
│   ├── openai_integration.py          # AI prompt enhancement
│   ├── system_diagnostics.py          # Performance monitoring
│   └── comfyui_export.py              # ComfyUI workflow export
├── 🔧 config/                          # Configuration files
│   └── default_settings.json          # Optimized defaults
├── 🎨 assets/                          # Templates and workflows
│   └── workflows/
│       └── comfy_sdxl_character_art.json
├── 📚 docs/                           # Documentation
│   └── user_guide.md                  # User guide
├── 🧪 scripts/                        # Utility scripts
│   └── deploy.py                      # Deployment validation
├── 📄 README.md                       # Main documentation
├── 📋 requirements.txt                # Dependencies
└── 🔧 Configuration files
    ├── .gitignore                     # Git ignore rules
    ├── .env.example                   # Environment template
    ├── pyproject.toml                 # Project configuration
    └── LICENSE                        # MIT License
```

## 🎯 Core Components

### **Main Entry Point**
- **`main_notebook.ipynb`** - Single unified Colab notebook for one-click deployment

### **Application Modules**
- **`apps/unified_app.py`** - Complete Gradio application with 6 tabs
- **`apps/openai_integration.py`** - AI-powered prompt enhancement
- **`apps/system_diagnostics.py`** - Performance monitoring and optimization
- **`apps/comfyui_export.py`** - ComfyUI workflow export functionality

### **Configuration**
- **`config/default_settings.json`** - Optimized defaults for all art styles
- **`requirements.txt`** - Complete dependency list
- **`.env.example`** - Environment variable template

### **Documentation**
- **`README.md`** - Main project documentation
- **`docs/user_guide.md`** - Detailed usage instructions
- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide
- **`FINAL_SUMMARY.md`** - Implementation summary

### **Assets**
- **`assets/workflows/`** - ComfyUI workflow templates
- **`scripts/deploy.py`** - Deployment validation script

## 🚀 Usage

### **For Users (Google Colab)**
1. Upload `main_notebook.ipynb` to Google Colab
2. Click "Runtime" → "Run all"
3. Wait for setup (2-3 minutes)
4. Click the generated link
5. Start creating art!

### **For Developers (Local)**
```bash
git clone <repository-url>
cd dnd-character-art-generator
pip install -r requirements.txt
python -m apps.unified_app
```

## 📊 File Count
- **Total Files**: 25 files
- **Core Modules**: 4 Python modules
- **Documentation**: 5 markdown files
- **Configuration**: 3 config files
- **Assets**: 1 ComfyUI workflow

## 🎯 Clean Structure Benefits
- ✅ **Focused**: Only essential files included
- ✅ **Organized**: Clear directory structure
- ✅ **Maintainable**: Easy to navigate and modify
- ✅ **Deployable**: Ready for production use
- ✅ **Documented**: Comprehensive guides included
