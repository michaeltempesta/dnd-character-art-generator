# 🎨 D&D Character Art Generator - User Guide

## 🚀 Quick Start

### For Complete Beginners
1. **Upload the notebook to Google Colab**
2. **Click "Runtime" → "Run all"**
3. **Wait for setup (2-3 minutes)**
4. **Click the generated link**
5. **Start creating art!**

### For Advanced Users
1. **Configure API keys in Cell 3** (optional but recommended)
2. **Customize settings in the app**
3. **Use advanced tools in Cell 5**
4. **Export to ComfyUI for complex workflows**

---

## 🎭 Art Styles

### Fantasy Realistic
- **Best for**: Photorealistic character portraits
- **Style**: Professional photography quality
- **Settings**: High quality, 30 steps, CFG 6.5

### Epic Fantasy
- **Best for**: Heroic character art
- **Style**: Dramatic fantasy art
- **Settings**: High quality, 28 steps, CFG 7.0

### Dark Fantasy
- **Best for**: Gothic, mysterious characters
- **Style**: Dark, atmospheric art
- **Settings**: High quality, 32 steps, CFG 6.0

### Anime Style
- **Best for**: Manga/anime characters
- **Style**: Japanese animation style
- **Settings**: Medium quality, 25 steps, CFG 7.5

### Watercolor Fantasy
- **Best for**: Artistic, hand-painted look
- **Style**: Traditional watercolor painting
- **Settings**: High quality, 35 steps, CFG 6.0

---

## 🛠️ Features Guide

### Generate Art Tab
- **Character Data**: Optional JSON input for character information
- **Style Selection**: Choose from 5 art styles
- **Prompts**: Positive and negative prompts
- **Settings**: Resolution, steps, CFG, seed
- **ControlNet**: Line-Art and Tile ControlNet options
- **Refiner**: Optional SDXL Refiner for enhanced quality

### Inpaint & Edit Tab
- **Base Image**: Upload the image to edit
- **Mask**: Paint white areas to edit, black areas to keep
- **Settings**: Strength, steps, CFG for inpainting

### Mask Helper Tab
- **Paint Masks**: Create masks for inpainting
- **Save to Drive**: Automatically save masks to Google Drive

### AI Enhancement Tab
- **OpenAI Integration**: AI-powered prompt enhancement
- **Character Analysis**: Extract visual characteristics
- **Prompt Optimization**: Improve prompts automatically

### System Diagnostics Tab
- **Performance Monitor**: Real-time system analysis
- **Optimization Suggestions**: AI-powered recommendations
- **Health Check**: System status and performance

### Advanced Tools Tab
- **ComfyUI Export**: Export workflows to ComfyUI
- **Batch Processing**: Process multiple characters
- **Settings Management**: Advanced configuration

---

## 🔧 Advanced Usage

### OpenAI Integration
1. **Get API Key**: Sign up at openai.com
2. **Add to Cell 3**: Paste your API key
3. **Enable Features**: AI prompt enhancement and character analysis

### ComfyUI Export
1. **Configure Settings**: Set up your preferred workflow
2. **Click Export**: Generate ComfyUI workflow JSON
3. **Import to ComfyUI**: Use the generated workflow

### Batch Processing
1. **Prepare Characters**: Organize character data files
2. **Run Batch**: Process multiple characters at once
3. **Monitor Progress**: Track batch processing status

---

## 🎯 Tips for Best Results

### Prompt Writing
- **Be Specific**: Include details about appearance, clothing, equipment
- **Use Style Keywords**: Add style-specific terms
- **Negative Prompts**: Exclude unwanted elements
- **AI Enhancement**: Use OpenAI integration for better prompts

### Settings Optimization
- **Resolution**: Higher resolution = better quality, slower generation
- **Steps**: More steps = better quality, slower generation
- **CFG**: Higher CFG = more adherence to prompt, may be over-saturated
- **Seed**: Use same seed for consistent results

### ControlNet Usage
- **Line-Art**: Use for precise pose control
- **Tile**: Use for detail refinement
- **Weights**: Adjust weights for control strength

### Refiner Usage
- **Strength**: 0.2-0.3 for subtle enhancement
- **Steps**: 20-30 steps for refiner
- **CFG**: Slightly lower than base generation

---

## 🚨 Troubleshooting

### Common Issues

#### "Out of Memory" Error
- **Solution**: Reduce resolution or batch size
- **Check**: GPU memory usage in diagnostics
- **Optimize**: Use system diagnostics for recommendations

#### Slow Generation
- **Check**: GPU availability in diagnostics
- **Optimize**: Reduce steps or resolution
- **Upgrade**: Consider Colab Pro for better GPU

#### Poor Quality Results
- **Prompts**: Improve prompt specificity
- **Settings**: Increase steps and CFG
- **Style**: Try different art styles
- **AI Enhancement**: Use OpenAI integration

#### App Won't Launch
- **Check**: All cells ran successfully
- **Restart**: Restart runtime and try again
- **Dependencies**: Ensure all packages installed

### Getting Help

#### System Diagnostics
1. **Run Diagnostics**: Use the System Diagnostics tab
2. **Check Performance**: Monitor GPU and memory usage
3. **Optimize Settings**: Follow AI recommendations

#### Support Resources
- **GitHub Issues**: Report bugs and request features
- **Community**: Join Discord/Slack for help
- **Documentation**: Check this guide and API reference

---

## 🔒 Security & Privacy

### Data Protection
- **No Logging**: Prompts and images are not logged
- **Local Processing**: All generation happens locally
- **Secure Auth**: Password-protected access

### Content Filtering
- **Denylist**: Automatic filtering of inappropriate content
- **Input Validation**: Resolution and parameter limits
- **Quality Control**: Built-in safety measures

### API Keys
- **Secure Storage**: Keys stored in environment variables
- **No Hardcoding**: Keys never stored in code
- **Optional**: App works without API keys

---

## 📊 Performance Optimization

### System Requirements
- **GPU**: Recommended for best performance
- **RAM**: 8GB+ recommended
- **Storage**: 10GB+ for models

### Optimization Tips
- **Use GPU**: Enable GPU runtime in Colab
- **Monitor Memory**: Check VRAM usage
- **Batch Size**: Adjust based on available memory
- **Quality Settings**: Balance quality vs speed

### Performance Monitoring
- **Real-time Metrics**: Monitor during generation
- **System Analysis**: Regular diagnostics
- **Optimization Suggestions**: AI-powered recommendations

---

## 🎯 Best Practices

### Workflow
1. **Start Simple**: Begin with basic generation
2. **Iterate**: Refine prompts and settings
3. **Use AI**: Leverage OpenAI integration
4. **Export**: Save good workflows to ComfyUI

### Quality Control
- **Test Settings**: Try different configurations
- **Compare Results**: A/B test different approaches
- **Document**: Keep track of successful settings
- **Share**: Contribute to community knowledge

### Advanced Techniques
- **ControlNet**: Use for precise control
- **Inpainting**: Edit specific areas
- **Batch Processing**: Process multiple characters
- **ComfyUI**: Use for complex workflows

---

*This guide is regularly updated. Check the repository for the latest version.*
