#!/usr/bin/env python3
"""
ComfyUI Export for D&D Character Art Generator
Provides workflow export functionality for ComfyUI integration
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ComfyUIWorkflow:
    """ComfyUI workflow structure"""
    name: str
    description: str
    version: str
    nodes: Dict[str, Any]
    links: List[List[int]]
    groups: List[Dict[str, Any]]
    config: Dict[str, Any]

class ComfyUIExporter:
    """Export Gradio app settings to ComfyUI workflows"""
    
    def __init__(self):
        self.workflow_templates = self._load_workflow_templates()
        self.node_counter = 0
    
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """Load ComfyUI workflow templates"""
        return {
            "sdxl_base": {
                "name": "SDXL Base Generation",
                "description": "Basic SDXL text-to-image generation",
                "nodes": {
                    "checkpoint_loader": {
                        "type": "CheckpointLoaderSimple",
                        "inputs": {},
                        "outputs": ["MODEL", "CLIP", "VAE"],
                        "settings": {
                            "ckpt_name": "stabilityai/stable-diffusion-xl-base-1.0"
                        }
                    },
                    "positive_prompt": {
                        "type": "CLIPTextEncode",
                        "inputs": {"clip": "checkpoint_loader.CLIP"},
                        "outputs": ["CONDITIONING"],
                        "settings": {
                            "text": "{{positive_prompt}}"
                        }
                    },
                    "negative_prompt": {
                        "type": "CLIPTextEncode",
                        "inputs": {"clip": "checkpoint_loader.CLIP"},
                        "outputs": ["CONDITIONING"],
                        "settings": {
                            "text": "{{negative_prompt}}"
                        }
                    },
                    "empty_latent": {
                        "type": "EmptyLatentImage",
                        "inputs": {},
                        "outputs": ["LATENT"],
                        "settings": {
                            "width": "{{width}}",
                            "height": "{{height}}",
                            "batch_size": 1
                        }
                    },
                    "ksampler": {
                        "type": "KSampler",
                        "inputs": {
                            "model": "checkpoint_loader.MODEL",
                            "positive": "positive_prompt.CONDITIONING",
                            "negative": "negative_prompt.CONDITIONING",
                            "latent_image": "empty_latent.LATENT"
                        },
                        "outputs": ["LATENT"],
                        "settings": {
                            "seed": "{{seed}}",
                            "steps": "{{steps}}",
                            "cfg": "{{cfg}}",
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "denoise": 1.0
                        }
                    },
                    "vae_decode": {
                        "type": "VAEDecode",
                        "inputs": {
                            "samples": "ksampler.LATENT",
                            "vae": "checkpoint_loader.VAE"
                        },
                        "outputs": ["IMAGE"],
                        "settings": {}
                    },
                    "save_image": {
                        "type": "SaveImage",
                        "inputs": {
                            "filename_prefix": "character_art",
                            "images": "vae_decode.IMAGE"
                        },
                        "outputs": [],
                        "settings": {}
                    }
                }
            },
            "sdxl_with_controlnet": {
                "name": "SDXL with ControlNet",
                "description": "SDXL generation with Line-Art ControlNet",
                "nodes": {
                    "checkpoint_loader": {
                        "type": "CheckpointLoaderSimple",
                        "inputs": {},
                        "outputs": ["MODEL", "CLIP", "VAE"],
                        "settings": {
                            "ckpt_name": "stabilityai/stable-diffusion-xl-base-1.0"
                        }
                    },
                    "controlnet_loader": {
                        "type": "ControlNetLoader",
                        "inputs": {},
                        "outputs": ["CONTROL_NET"],
                        "settings": {
                            "control_net_name": "diffusers/controlnet-lineart-sdxl-1.0"
                        }
                    },
                    "controlnet_apply": {
                        "type": "ControlNetApply",
                        "inputs": {
                            "conditioning": "positive_prompt.CONDITIONING",
                            "control_net": "controlnet_loader.CONTROL_NET",
                            "image": "controlnet_image.IMAGE",
                            "strength": 0.45
                        },
                        "outputs": ["CONDITIONING"],
                        "settings": {}
                    }
                }
            },
            "sdxl_with_refiner": {
                "name": "SDXL with Refiner",
                "description": "SDXL generation with refiner enhancement",
                "nodes": {
                    "refiner_checkpoint": {
                        "type": "CheckpointLoaderSimple",
                        "inputs": {},
                        "outputs": ["MODEL", "CLIP", "VAE"],
                        "settings": {
                            "ckpt_name": "stabilityai/stable-diffusion-xl-refiner-1.0"
                        }
                    },
                    "refiner_sampler": {
                        "type": "KSampler",
                        "inputs": {
                            "model": "refiner_checkpoint.MODEL",
                            "positive": "positive_prompt.CONDITIONING",
                            "negative": "negative_prompt.CONDITIONING",
                            "latent_image": "base_sampler.LATENT"
                        },
                        "outputs": ["LATENT"],
                        "settings": {
                            "seed": "{{seed}}",
                            "steps": "{{refiner_steps}}",
                            "cfg": "{{refiner_cfg}}",
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "denoise": "{{refiner_strength}}"
                        }
                    }
                }
            }
        }
    
    def export_workflow(self, 
                       workflow_name: str,
                       settings: Dict[str, Any],
                       include_controlnet: bool = False,
                       include_refiner: bool = False) -> ComfyUIWorkflow:
        """Export current settings to ComfyUI workflow"""
        
        # Start with base workflow
        workflow = self._create_base_workflow(workflow_name, settings)
        
        # Add ControlNet if requested
        if include_controlnet:
            workflow = self._add_controlnet_nodes(workflow, settings)
        
        # Add refiner if requested
        if include_refiner:
            workflow = self._add_refiner_nodes(workflow, settings)
        
        # Generate node IDs and links
        workflow = self._generate_node_ids(workflow)
        workflow = self._generate_links(workflow)
        
        return workflow
    
    def _create_base_workflow(self, name: str, settings: Dict[str, Any]) -> ComfyUIWorkflow:
        """Create base SDXL workflow"""
        template = self.workflow_templates["sdxl_base"]
        
        nodes = {}
        for node_id, node_template in template["nodes"].items():
            nodes[node_id] = {
                "type": node_template["type"],
                "inputs": node_template["inputs"],
                "outputs": node_template["outputs"],
                "settings": self._substitute_variables(node_template["settings"], settings)
            }
        
        return ComfyUIWorkflow(
            name=name,
            description=f"Generated workflow for {name}",
            version="1.0.0",
            nodes=nodes,
            links=[],
            groups=[],
            config={}
        )
    
    def _add_controlnet_nodes(self, workflow: ComfyUIWorkflow, settings: Dict[str, Any]) -> ComfyUIWorkflow:
        """Add ControlNet nodes to workflow"""
        controlnet_template = self.workflow_templates["sdxl_with_controlnet"]
        
        for node_id, node_template in controlnet_template["nodes"].items():
            if node_id not in workflow.nodes:
                workflow.nodes[node_id] = {
                    "type": node_template["type"],
                    "inputs": node_template["inputs"],
                    "outputs": node_template["outputs"],
                    "settings": self._substitute_variables(node_template["settings"], settings)
                }
        
        return workflow
    
    def _add_refiner_nodes(self, workflow: ComfyUIWorkflow, settings: Dict[str, Any]) -> ComfyUIWorkflow:
        """Add refiner nodes to workflow"""
        refiner_template = self.workflow_templates["sdxl_with_refiner"]
        
        for node_id, node_template in refiner_template["nodes"].items():
            if node_id not in workflow.nodes:
                workflow.nodes[node_id] = {
                    "type": node_template["type"],
                    "inputs": node_template["inputs"],
                    "outputs": node_template["outputs"],
                    "settings": self._substitute_variables(node_template["settings"], settings)
                }
        
        return workflow
    
    def _substitute_variables(self, settings: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute variables in settings"""
        substituted = {}
        for key, value in settings.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                var_name = value[2:-2]
                substituted[key] = variables.get(var_name, value)
            else:
                substituted[key] = value
        return substituted
    
    def _generate_node_ids(self, workflow: ComfyUIWorkflow) -> ComfyUIWorkflow:
        """Generate sequential node IDs"""
        node_id_map = {}
        new_nodes = {}
        
        for i, (old_id, node) in enumerate(workflow.nodes.items()):
            new_id = str(i + 1)
            node_id_map[old_id] = new_id
            new_nodes[new_id] = node
        
        workflow.nodes = new_nodes
        workflow.node_id_map = node_id_map
        return workflow
    
    def _generate_links(self, workflow: ComfyUIWorkflow) -> ComfyUIWorkflow:
        """Generate links between nodes"""
        links = []
        
        # This would be more complex in a real implementation
        # For now, create basic links based on node types
        for node_id, node in workflow.nodes.items():
            if node["type"] == "KSampler":
                # Link to model, conditioning, and latent inputs
                links.append([int(node_id), 1, 0, int(node_id), 0, "MODEL"])
                links.append([int(node_id), 2, 0, int(node_id), 1, "CONDITIONING"])
                links.append([int(node_id), 3, 0, int(node_id), 2, "CONDITIONING"])
                links.append([int(node_id), 4, 0, int(node_id), 3, "LATENT"])
            elif node["type"] == "VAEDecode":
                # Link to sampler output and VAE
                links.append([int(node_id), 5, 0, int(node_id), 0, "LATENT"])
                links.append([int(node_id), 1, 2, int(node_id), 1, "VAE"])
        
        workflow.links = links
        return workflow
    
    def save_workflow(self, workflow: ComfyUIWorkflow, output_path: str) -> str:
        """Save workflow to JSON file"""
        workflow_dict = {
            "meta": {
                "title": workflow.name,
                "description": workflow.description,
                "version": workflow.version,
                "created": datetime.now().isoformat()
            },
            "nodes": workflow.nodes,
            "links": workflow.links,
            "groups": workflow.groups,
            "config": workflow.config,
            "extra": {
                "ds": {
                    "scale": 1,
                    "offset": [0, 0]
                }
            },
            "version": 0.4
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(workflow_dict, f, indent=2)
        
        return output_path
    
    def export_from_gradio_settings(self, 
                                   gradio_settings: Dict[str, Any],
                                   workflow_name: str = "sdxl_character_art") -> str:
        """Export workflow from Gradio app settings"""
        
        # Extract settings from Gradio app
        settings = {
            "positive_prompt": gradio_settings.get("positive", ""),
            "negative_prompt": gradio_settings.get("negative", ""),
            "width": gradio_settings.get("width", 896),
            "height": gradio_settings.get("height", 1120),
            "steps": gradio_settings.get("steps", 30),
            "cfg": gradio_settings.get("cfg", 6.5),
            "seed": gradio_settings.get("seed", -1),
            "use_lineart": gradio_settings.get("use_lineart", False),
            "lineart_weight": gradio_settings.get("lineart_weight", 0.45),
            "use_tile": gradio_settings.get("use_tile", False),
            "tile_weight": gradio_settings.get("tile_weight", 0.7),
            "tile_steps": gradio_settings.get("tile_steps", 24),
            "tile_cfg": gradio_settings.get("tile_cfg", 6.0),
            "use_refiner": gradio_settings.get("use_refiner", False),
            "refiner_strength": gradio_settings.get("refiner_strength", 0.25),
            "refiner_steps": gradio_settings.get("refiner_steps", 20),
            "refiner_cfg": gradio_settings.get("refiner_cfg", 5.5)
        }
        
        # Create workflow
        workflow = self.export_workflow(
            workflow_name=workflow_name,
            settings=settings,
            include_controlnet=settings.get("use_lineart", False) or settings.get("use_tile", False),
            include_refiner=settings.get("use_refiner", False)
        )
        
        # Save workflow
        output_path = f"assets/workflows/{workflow_name}.json"
        saved_path = self.save_workflow(workflow, output_path)
        
        return saved_path
    
    def create_workflow_from_character(self, 
                                      character_data: Dict[str, Any],
                                      style: str,
                                      settings: Dict[str, Any]) -> str:
        """Create workflow optimized for specific character and style"""
        
        # Generate character-specific prompt
        character_prompt = self._generate_character_prompt(character_data, style)
        
        # Update settings with character-specific values
        settings.update({
            "positive_prompt": character_prompt,
            "style": style,
            "character_name": character_data.get("name", "Character"),
            "character_race": character_data.get("race", ""),
            "character_class": character_data.get("class_name", "")
        })
        
        # Create workflow
        workflow_name = f"{character_data.get('name', 'character').lower().replace(' ', '_')}_{style}"
        workflow = self.export_workflow(
            workflow_name=workflow_name,
            settings=settings,
            include_controlnet=True,
            include_refiner=True
        )
        
        # Save workflow
        output_path = f"assets/workflows/{workflow_name}.json"
        saved_path = self.save_workflow(workflow, output_path)
        
        return saved_path
    
    def _generate_character_prompt(self, character_data: Dict[str, Any], style: str) -> str:
        """Generate character-specific prompt"""
        prompt_parts = []
        
        # Add character basics
        if character_data.get("name"):
            prompt_parts.append(f"Character: {character_data['name']}")
        
        if character_data.get("race"):
            prompt_parts.append(f"Race: {character_data['race']}")
        
        if character_data.get("class_name"):
            prompt_parts.append(f"Class: {character_data['class_name']}")
        
        if character_data.get("appearance"):
            prompt_parts.append(f"Appearance: {character_data['appearance']}")
        
        if character_data.get("equipment"):
            equipment = ', '.join(character_data['equipment']) if isinstance(character_data['equipment'], list) else character_data['equipment']
            prompt_parts.append(f"Equipment: {equipment}")
        
        # Add style-specific elements
        style_elements = {
            'fantasy_realistic': 'photorealistic fantasy character, detailed armor, magical weapons, dramatic lighting, high quality, professional photography',
            'epic_fantasy': 'epic fantasy character, heroic pose, detailed armor, magical weapons, dramatic lighting, fantasy art style',
            'dark_fantasy': 'dark fantasy character, gothic armor, shadowy lighting, mysterious atmosphere, dark fantasy art',
            'anime_style': 'anime character, manga style, detailed armor, magical weapons, anime art style',
            'watercolor_fantasy': 'watercolor fantasy character, hand-painted style, artistic, detailed armor, magical weapons'
        }
        
        if style in style_elements:
            prompt_parts.append(style_elements[style])
        
        return ', '.join(prompt_parts)
    
    def batch_export_workflows(self, 
                              characters: List[Dict[str, Any]], 
                              styles: List[str],
                              base_settings: Dict[str, Any]) -> List[str]:
        """Export workflows for multiple characters and styles"""
        exported_paths = []
        
        for character in characters:
            for style in styles:
                try:
                    workflow_path = self.create_workflow_from_character(
                        character_data=character,
                        style=style,
                        settings=base_settings
                    )
                    exported_paths.append(workflow_path)
                except Exception as e:
                    print(f"Failed to export workflow for {character.get('name', 'Unknown')} in {style} style: {e}")
        
        return exported_paths
    
    def validate_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """Validate ComfyUI workflow"""
        try:
            with open(workflow_path, 'r') as f:
                workflow = json.load(f)
            
            validation_result = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "node_count": len(workflow.get("nodes", {})),
                "link_count": len(workflow.get("links", [])),
                "has_save_node": False,
                "has_sampler_node": False
            }
            
            # Check for required nodes
            nodes = workflow.get("nodes", {})
            for node_id, node in nodes.items():
                if node.get("type") == "SaveImage":
                    validation_result["has_save_node"] = True
                elif node.get("type") == "KSampler":
                    validation_result["has_sampler_node"] = True
            
            # Check for errors
            if not validation_result["has_save_node"]:
                validation_result["warnings"].append("No SaveImage node found")
            
            if not validation_result["has_sampler_node"]:
                validation_result["errors"].append("No KSampler node found")
                validation_result["valid"] = False
            
            return validation_result
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Failed to load workflow: {e}"],
                "warnings": [],
                "node_count": 0,
                "link_count": 0,
                "has_save_node": False,
                "has_sampler_node": False
            }

# Example usage and testing
if __name__ == "__main__":
    # Test the exporter
    exporter = ComfyUIExporter()
    
    # Test settings
    test_settings = {
        "positive": "Fantasy warrior, detailed armor, magical sword",
        "negative": "blurry, low quality",
        "width": 896,
        "height": 1120,
        "steps": 30,
        "cfg": 6.5,
        "seed": 12345,
        "use_lineart": True,
        "lineart_weight": 0.45,
        "use_tile": True,
        "tile_weight": 0.7,
        "use_refiner": True,
        "refiner_strength": 0.25
    }
    
    # Export workflow
    workflow_path = exporter.export_from_gradio_settings(test_settings, "test_workflow")
    print(f"Workflow exported to: {workflow_path}")
    
    # Validate workflow
    validation = exporter.validate_workflow(workflow_path)
    print(f"Workflow validation: {validation}")
