#!/usr/bin/env python3
"""
Unified D&D Character Art Generator
Consolidates all v5 features into a single, user-friendly application
"""

import os
import gc
import random
import re
import json
import time
from typing import Optional, Dict, Any, List, Tuple
import gradio as gr
import torch
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import login
from diffusers import (
    StableDiffusionXLPipeline,
    StableDiffusionXLControlNetPipeline,
    StableDiffusionXLImg2ImgPipeline,
    StableDiffusionXLInpaintPipeline,
    ControlNetModel,
)

# Import our custom modules
from .openai_integration import PromptEnhancer, CharacterAnalyzer
from .system_diagnostics import SystemDiagnostics
from .comfyui_export import ComfyUIExporter

# Load environment variables
load_dotenv()

# Remove the old SystemDiagnostics class - we'll use the imported one

# Remove the old OpenAIIntegration class - we'll use the imported one

class UnifiedArtGenerator:
    """Main unified art generation application"""
    
    def __init__(self, openai_key: Optional[str] = None, hf_token: Optional[str] = None, auto_optimize: bool = True):
        self.openai_integration = PromptEnhancer(openai_key)
        self.character_analyzer = CharacterAnalyzer(self.openai_integration)
        self.diagnostics = SystemDiagnostics()
        self.comfyui_exporter = ComfyUIExporter()
        self.auto_optimize = auto_optimize
        
        # Initialize Hugging Face
        if hf_token:
            try:
                login(token=hf_token)
            except Exception:
                pass
        
        # Model IDs
        self.BASE_ID = "stabilityai/stable-diffusion-xl-base-1.0"
        self.REFINER_ID = "stabilityai/stable-diffusion-xl-refiner-1.0"
        self.LINEART_ID = "diffusers/controlnet-lineart-sdxl-1.0"
        self.TILE_ID = "diffusers/controlnet-tile-sdxl-1.0"
        
        # Device setup
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.DTYPE = torch.float16 if self.DEVICE == "cuda" else torch.float32
        
        # Pipeline cache
        self.pipelines = {}
        
        # Default prompts and settings
        self.default_prompts = self._load_default_prompts()
        self.art_styles = self._load_art_styles()
        
        # Security settings
        self.denylist = [
            r"(?i)child|toddler|infant|kid|minor|young girl|loli|teen",
        ]
        
        # Auto-optimize if enabled
        if auto_optimize:
            self._apply_optimizations()
    
    def _load_default_prompts(self) -> Dict[str, str]:
        """Load default prompts"""
        return {
            "positive": (
                "Adult woman (late-20s/30s), Shadar-Kai ashen gray skin with subtle violet undertone, "
                "mature bone structure (defined jawline, proportional eyes), "
                "silver-white twin drills as hair-wrapped satin-keratin spiral horns (2–2.25 turns, uniform pitch); "
                "left horn near-black with gold-opal marbling halo; right horn near-black with deep oxblood marbling and a frayed crimson filament; "
                "slim gold cuffs at horn roots, soft AO at base; "
                "dark 1800s Victorian carnival couture: high collar, tight bodice, layered black satin and velvet, ornate black lace mob cap, ribbon bows, jet beadwork, cameo brooch; "
                "candlelit dim parlor, warm rim light + cool moonlight fill, dramatic chiaroscuro; "
                "painterly oil impasto; tight head-and-shoulders three-quarter; shallow DoF; "
                "do not wrap horns behind head; no hair gloss."
            ),
            "negative": (
                "child, teen, loli, babyface, chibi, youthful face, huge anime eyes, toddler nose, oversized head, "
                "school uniform, hair-only drills, hidden horns, plastic hair shine, lowres, blur, artifacts, duplicate horns"
            )
        }
    
    def _load_art_styles(self) -> Dict[str, Dict[str, Any]]:
        """Load art style configurations"""
        return {
            "fantasy_realistic": {
                "name": "Fantasy Realistic",
                "positive_suffix": "photorealistic fantasy character, detailed armor, magical weapons, dramatic lighting, high quality, professional photography",
                "negative_suffix": "blurry, low quality, distorted, deformed, ugly, cartoon, anime",
                "settings": {"steps": 30, "cfg": 6.5, "quality": "high"}
            },
            "epic_fantasy": {
                "name": "Epic Fantasy",
                "positive_suffix": "epic fantasy character, heroic pose, detailed armor, magical weapons, dramatic lighting, fantasy art style",
                "negative_suffix": "blurry, low quality, distorted, deformed, ugly, modern, realistic",
                "settings": {"steps": 28, "cfg": 7.0, "quality": "high"}
            },
            "dark_fantasy": {
                "name": "Dark Fantasy",
                "positive_suffix": "dark fantasy character, gothic armor, shadowy lighting, mysterious atmosphere, dark fantasy art",
                "negative_suffix": "blurry, low quality, distorted, deformed, ugly, bright, cheerful, colorful",
                "settings": {"steps": 32, "cfg": 6.0, "quality": "high"}
            },
            "anime_style": {
                "name": "Anime Style",
                "positive_suffix": "anime character, manga style, detailed armor, magical weapons, anime art style",
                "negative_suffix": "blurry, low quality, distorted, deformed, ugly, realistic, photorealistic",
                "settings": {"steps": 25, "cfg": 7.5, "quality": "medium"}
            },
            "watercolor_fantasy": {
                "name": "Watercolor Fantasy",
                "positive_suffix": "watercolor fantasy character, hand-painted style, artistic, detailed armor, magical weapons",
                "negative_suffix": "blurry, low quality, distorted, deformed, ugly, digital, photorealistic",
                "settings": {"steps": 35, "cfg": 6.0, "quality": "high"}
            }
        }
    
    def _apply_optimizations(self):
        """Apply system optimizations based on diagnostics"""
        optimal_settings = self.diagnostics._get_optimal_settings()
        print(f"🔧 Auto-optimization applied: {optimal_settings}")
    
    def _get_pipeline(self, pipeline_type: str):
        """Get or create pipeline with caching"""
        if pipeline_type in self.pipelines:
            return self.pipelines[pipeline_type]
        
        pipeline = None
        
        if pipeline_type == "base":
            pipeline = StableDiffusionXLPipeline.from_pretrained(
                self.BASE_ID, torch_dtype=self.DTYPE, use_safetensors=True,
                variant=("fp16" if self.DTYPE == torch.float16 else None)
            )
        elif pipeline_type == "lineart":
            cn = ControlNetModel.from_pretrained(self.LINEART_ID, torch_dtype=self.DTYPE, use_safetensors=True)
            pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
                self.BASE_ID, controlnet=cn, torch_dtype=self.DTYPE, use_safetensors=True,
                variant=("fp16" if self.DTYPE == torch.float16 else None)
            )
        elif pipeline_type == "tile":
            cn = ControlNetModel.from_pretrained(self.TILE_ID, torch_dtype=self.DTYPE, use_safetensors=True)
            pipeline = StableDiffusionXLControlNetPipeline.from_pretrained(
                self.BASE_ID, controlnet=cn, torch_dtype=self.DTYPE, use_safetensors=True,
                variant=("fp16" if self.DTYPE == torch.float16 else None)
            )
        elif pipeline_type == "refiner":
            pipeline = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                self.REFINER_ID, torch_dtype=self.DTYPE, use_safetensors=True,
                variant=("fp16" if self.DTYPE == torch.float16 else None)
            )
        elif pipeline_type == "inpaint":
            pipeline = StableDiffusionXLInpaintPipeline.from_pretrained(
                self.BASE_ID, torch_dtype=self.DTYPE, use_safetensors=True,
                variant=("fp16" if self.DTYPE == torch.float16 else None)
            )
        
        if pipeline:
            # Apply optimizations
            for fn in ("enable_vae_slicing", "enable_xformers_memory_efficient_attention", "enable_model_cpu_offload"):
                if hasattr(pipeline, fn):
                    try:
                        getattr(pipeline, fn)()
                    except Exception:
                        pass
            if hasattr(pipeline, "to"):
                pipeline.to(self.DEVICE)
            
            self.pipelines[pipeline_type] = pipeline
        
        return pipeline
    
    def validate_prompt(self, prompt: str) -> str:
        """Validate and clean prompt"""
        if not prompt or not prompt.strip():
            raise gr.Error("Prompt is empty.")
        
        for pattern in self.denylist:
            if re.search(pattern, prompt or ""):
                raise gr.Error("Prompt contains disallowed terms.")
        
        return prompt.strip()
    
    def clamp_inputs(self, width: int, height: int, steps: int, cfg: float):
        """Validate and clamp input parameters"""
        if width > 1280 or height > 1536:
            raise gr.Error("Resolution too large; keep ≤ 1280x1536.")
        if steps > 40:
            raise gr.Error("Steps too high; keep ≤ 40.")
        if not (3.0 <= cfg <= 10.0):
            raise gr.Error("CFG out of range [3,10].")
    
    def generate_art(self, 
                    character_data: Dict[str, Any],
                    style: str,
                    positive: str,
                    negative: str,
                    width: int,
                    height: int,
                    steps: int,
                    cfg: float,
                    seed: int,
                    use_lineart: bool,
                    lineart_image: Optional[Image.Image],
                    lineart_weight: float,
                    use_tile: bool,
                    tile_weight: float,
                    tile_steps: int,
                    tile_cfg: float,
                    use_refiner: bool,
                    refiner_strength: float,
                    refiner_steps: int,
                    refiner_cfg: float,
                    progress=gr.Progress(track_tqdm=True)):
        """Main art generation function"""
        
        # Validate inputs
        positive = self.validate_prompt(positive)
        self.clamp_inputs(width, height, steps, cfg)
        
        # Enhance prompt with OpenAI if available
        if self.openai_integration.available:
            positive = self.openai_integration.enhance_character_prompt(character_data, style, positive)
        
        # Set seed
        if seed < 0:
            seed = random.randint(0, 2**31-1)
        generator = torch.Generator(device=self.DEVICE).manual_seed(seed)
        
        # Base or Line-Art generation
        if use_lineart and lineart_image is not None:
            pipe = self._get_pipeline("lineart")
            image = pipe(
                prompt=positive,
                negative_prompt=negative,
                image=lineart_image.convert("RGB"),
                controlnet_conditioning_scale=lineart_weight,
                num_inference_steps=steps,
                guidance_scale=cfg,
                width=width,
                height=height,
                generator=generator
            ).images[0]
        else:
            pipe = self._get_pipeline("base")
            image = pipe(
                prompt=positive,
                negative_prompt=negative,
                num_inference_steps=steps,
                guidance_scale=cfg,
                width=width,
                height=height,
                generator=generator
            ).images[0]
        
        # Tile refinement
        if use_tile:
            pipe_tile = self._get_pipeline("tile")
            image = pipe_tile(
                prompt=positive,
                negative_prompt=negative,
                image=image,
                controlnet_conditioning_scale=tile_weight,
                num_inference_steps=tile_steps,
                guidance_scale=tile_cfg,
                generator=generator
            ).images[0]
        
        # Refiner
        if use_refiner:
            pipe_refiner = self._get_pipeline("refiner")
            image = pipe_refiner(
                prompt=positive,
                negative_prompt=negative,
                image=image,
                strength=refiner_strength,
                num_inference_steps=refiner_steps,
                guidance_scale=refiner_cfg,
                generator=generator
            ).images[0]
        
        # Cleanup
        if self.DEVICE == "cuda":
            torch.cuda.empty_cache()
        gc.collect()
        
        return image, seed
    
    def inpaint_image(self, 
                     base_img: Image.Image,
                     mask_img: Image.Image,
                     prompt: str,
                     negative: str,
                     strength: float,
                     steps: int,
                     cfg: float,
                     seed: int,
                     progress=gr.Progress(track_tqdm=True)):
        """Inpaint function"""
        
        if base_img is None or mask_img is None:
            raise gr.Error("Upload base and mask (white=edit, black=keep).")
        
        prompt = self.validate_prompt(prompt)
        self.clamp_inputs(base_img.width, base_img.height, steps, cfg if cfg else 6.0)
        
        if seed < 0:
            seed = random.randint(0, 2**31-1)
        
        pipe = self._get_pipeline("inpaint")
        generator = torch.Generator(device=self.DEVICE).manual_seed(seed)
        
        result = pipe(
            prompt=prompt,
            negative_prompt=negative,
            image=base_img.convert("RGB"),
            mask_image=mask_img.convert("L"),
            strength=strength,
            num_inference_steps=steps,
            guidance_scale=cfg,
            generator=generator
        ).images[0]
        
        if self.DEVICE == "cuda":
            torch.cuda.empty_cache()
        gc.collect()
        
        return result, seed
    
    def save_mask_pair(self, base_img: Image.Image, mask_img: Image.Image) -> str:
        """Save base and mask images to Drive"""
        if base_img is None or mask_img is None:
            return "Please upload base and draw a mask."
        
        try:
            # Create save directory
            save_dir = "/content/drive/MyDrive/colab/masks"
            os.makedirs(save_dir, exist_ok=True)
            
            # Generate filenames
            timestamp = int(time.time())
            base_path = os.path.join(save_dir, f"base_{timestamp}.png")
            mask_path = os.path.join(save_dir, f"mask_{timestamp}.png")
            
            # Save images
            base_img.save(base_path)
            mask_img.convert('L').save(mask_path)
            
            return f"Saved:\n{base_path}\n{mask_path}"
        except Exception as e:
            return f"Save failed: {str(e)}"
    
    def get_system_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive system diagnostics"""
        return self.diagnostics.analyze_system()
    
    def export_to_comfyui(self, workflow_name: str = "sdxl_character_art", settings: Optional[Dict[str, Any]] = None) -> str:
        """Export current settings to ComfyUI workflow"""
        if settings is None:
            settings = {}
        
        try:
            workflow_path = self.comfyui_exporter.export_from_gradio_settings(
                gradio_settings=settings,
                workflow_name=workflow_name
            )
            return f"ComfyUI workflow exported successfully to: {workflow_path}"
        except Exception as e:
            return f"ComfyUI export failed: {str(e)}"

def create_unified_app(openai_key: Optional[str] = None, 
                      hf_token: Optional[str] = None, 
                      auto_optimize: bool = True) -> gr.Blocks:
    """Create the unified Gradio application"""
    
    # Initialize the generator
    generator = UnifiedArtGenerator(openai_key, hf_token, auto_optimize)
    
    # Create the Gradio interface
    with gr.Blocks(css="#btn {border-radius: 14px;}") as demo:
        gr.Markdown("## 🎨 D&D Character Art Generator - Unified Studio")
        
        # Tab 1: Generate Art
        with gr.Tab("🎭 Generate Art"):
            with gr.Row():
                with gr.Column(scale=2):
                    # Character data input
                    character_data = gr.JSON(label="Character Data (Optional)", value={})
                    
                    # Style selection
                    style = gr.Dropdown(
                        choices=list(generator.art_styles.keys()),
                        value="fantasy_realistic",
                        label="Art Style"
                    )
                    
                    # Prompts
                    positive = gr.Textbox(
                        label="Positive Prompt", 
                        value=generator.default_prompts["positive"], 
                        lines=8
                    )
                    negative = gr.Textbox(
                        label="Negative Prompt", 
                        value=generator.default_prompts["negative"], 
                        lines=4
                    )
                    
                    # Basic settings
                    with gr.Row():
                        width = gr.Slider(640, 1280, value=896, step=16, label="Width")
                        height = gr.Slider(800, 1536, value=1120, step=16, label="Height")
                    with gr.Row():
                        steps = gr.Slider(15, 60, value=30, step=1, label="Steps")
                        cfg = gr.Slider(3.0, 12.0, value=6.5, step=0.1, label="Guidance (CFG)")
                    seed = gr.Number(value=321987654, precision=0, label="Seed (−1 random)")
                
                with gr.Column(scale=1):
                    # ControlNet options
                    use_lineart = gr.Checkbox(label="Use Line‑Art ControlNet", value=False)
                    lineart_image = gr.Image(label="Line‑Art Guide (PNG/JPG)", type="pil")
                    lineart_weight = gr.Slider(0.0, 1.0, value=0.45, step=0.05, label="Line‑Art Weight")
                    
                    gr.Markdown("---")
                    use_tile = gr.Checkbox(label="Use Tile ControlNet (Refine)", value=True)
                    tile_weight = gr.Slider(0.1, 1.0, value=0.7, step=0.05, label="Tile Weight")
                    tile_steps = gr.Slider(10, 60, value=24, step=1, label="Tile Steps")
                    tile_cfg = gr.Slider(0.0, 12.0, value=6.0, step=0.1, label="Tile CFG")
                    
                    gr.Markdown("---")
                    use_refiner = gr.Checkbox(label="Use SDXL Refiner (Img2Img)", value=False)
                    refiner_strength = gr.Slider(0.1, 0.5, value=0.25, step=0.01, label="Refiner Strength")
                    refiner_steps = gr.Slider(10, 50, value=20, step=1, label="Refiner Steps")
                    refiner_cfg = gr.Slider(3.0, 12.0, value=5.5, step=0.1, label="Refiner CFG")
                    
                    btn = gr.Button("🎨 Generate Art", elem_id="btn", variant="primary")
            
            # Output
            out_img = gr.Image(label="Generated Art", type="pil")
            out_seed = gr.Number(label="Used Seed", precision=0)
            
            # Generation function
            btn.click(
                fn=generator.generate_art,
                inputs=[
                    character_data, style, positive, negative, width, height, steps, cfg, seed,
                    use_lineart, lineart_image, lineart_weight, use_tile, tile_weight, tile_steps, tile_cfg,
                    use_refiner, refiner_strength, refiner_steps, refiner_cfg
                ],
                outputs=[out_img, out_seed]
            )
        
        # Tab 2: Inpaint & Edit
        with gr.Tab("🖌️ Inpaint & Edit"):
            with gr.Row():
                base_img = gr.Image(label="Base Image", type="pil")
                mask_img = gr.Image(label="Mask (white=edit, black=keep)", type="pil")
            
            with gr.Row():
                prompt_inp = gr.Textbox(
                    label="Prompt", 
                    value="thin polished gold cuffs at horn roots, subtle occlusion (AO), satin-keratin continuity; keep face and dress unchanged"
                )
                neg_inp = gr.Textbox(
                    label="Negative", 
                    value="blur, artifact, plastic, overpaint, color bleed"
                )
            
            with gr.Row():
                strength = gr.Slider(0.1, 0.8, value=0.35, step=0.01, label="Strength")
                steps_inp = gr.Slider(10, 60, value=25, step=1, label="Steps")
                cfg_inp = gr.Slider(3.0, 12.0, value=6.0, step=0.1, label="CFG")
                seed_inp = gr.Number(value=321987655, precision=0, label="Seed (−1 random)")
            
            run_inp = gr.Button("🖌️ Inpaint", variant="primary")
            out_inp = gr.Image(label="Inpainted Result", type="pil")
            out_seed_inp = gr.Number(label="Used Seed", precision=0)
            
            run_inp.click(
                fn=generator.inpaint_image,
                inputs=[base_img, mask_img, prompt_inp, neg_inp, strength, steps_inp, cfg_inp, seed_inp],
                outputs=[out_inp, out_seed_inp]
            )
        
        # Tab 3: Mask Helper
        with gr.Tab("🎭 Mask Helper"):
            gr.Markdown("**Paint white areas to edit, black areas to keep**")
            with gr.Row():
                base_for_mask = gr.Image(label="Base Image", type="pil")
                mask_painter = gr.Sketchpad(
                    label="Paint Mask (white=edit)", 
                    type="pil", 
                    image_mode='L',
                    brush=gr.Brush(default_color='white', color_mode='fixed')
                )
            save_mask_btn = gr.Button("💾 Save Mask to Drive", variant="secondary")
            mask_status = gr.Textbox(label="Status", lines=2)
            
            save_mask_btn.click(
                fn=generator.save_mask_pair,
                inputs=[base_for_mask, mask_painter],
                outputs=[mask_status]
            )
        
        # Tab 4: AI Enhancement
        with gr.Tab("🤖 AI Enhancement"):
            if generator.openai_integration.available:
                gr.Markdown("### OpenAI Integration Active")
                enhance_btn = gr.Button("🧠 Enhance Prompt with AI", variant="primary")
                enhanced_prompt = gr.Textbox(label="Enhanced Prompt", lines=6)
                character_analysis = gr.Textbox(label="Character Analysis", lines=8)
                suggestions = gr.Textbox(label="Improvement Suggestions", lines=4)
                
                def enhance_prompt_wrapper(character_data, style, base_prompt):
                    enhanced = generator.openai_integration.enhance_character_prompt(character_data, style, base_prompt)
                    analysis = generator.openai_integration.analyze_character(character_data)
                    suggestions_list = generator.openai_integration.suggest_improvements(base_prompt, style)
                    return enhanced, analysis["analysis"], "\n".join(suggestions_list)
                
                enhance_btn.click(
                    fn=enhance_prompt_wrapper,
                    inputs=[character_data, style, positive],
                    outputs=[enhanced_prompt, character_analysis, suggestions]
                )
            else:
                gr.Markdown("### OpenAI Integration Not Available")
                gr.Markdown("Add your OpenAI API key in the notebook to enable AI prompt enhancement.")
        
        # Tab 5: System Diagnostics
        with gr.Tab("📊 System Diagnostics"):
            diagnostics_btn = gr.Button("🔍 Run System Analysis", variant="primary")
            diagnostics_output = gr.JSON(label="System Analysis")
            
            diagnostics_btn.click(
                fn=generator.get_system_diagnostics,
                outputs=[diagnostics_output]
            )
        
        # Tab 6: Advanced Tools
        with gr.Tab("🔧 Advanced Tools"):
            with gr.Row():
                comfyui_btn = gr.Button("📤 Export to ComfyUI", variant="primary")
                batch_export_btn = gr.Button("🔄 Batch Export", variant="secondary")
            
            comfyui_status = gr.Textbox(label="Export Status", lines=3)
            workflow_name = gr.Textbox(label="Workflow Name", value="sdxl_character_art")
            
            def export_with_settings(workflow_name, character_data, style, positive, negative, width, height, steps, cfg, use_lineart, use_tile, use_refiner):
                settings = {
                    "positive": positive,
                    "negative": negative,
                    "width": width,
                    "height": height,
                    "steps": steps,
                    "cfg": cfg,
                    "use_lineart": use_lineart,
                    "use_tile": use_tile,
                    "use_refiner": use_refiner
                }
                return generator.export_to_comfyui(workflow_name, settings)
            
            comfyui_btn.click(
                fn=export_with_settings,
                inputs=[workflow_name, character_data, style, positive, negative, width, height, steps, cfg, use_lineart, use_tile, use_refiner],
                outputs=[comfyui_status]
            )
    
    return demo

# Health check endpoint
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "gpu": torch.cuda.is_available()}

if __name__ == "__main__":
    # Create and launch the app
    app = create_unified_app()
    app.launch(share=True, server_name="0.0.0.0")
