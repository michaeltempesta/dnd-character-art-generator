#!/usr/bin/env python3
"""
OpenAI Integration for D&D Character Art Generator
Provides AI-powered prompt enhancement and character analysis
"""

import json
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not installed. Install with: pip install openai")

@dataclass
class CharacterData:
    """Structured character data for analysis"""
    name: str
    race: str
    class_name: str
    level: int
    background: str
    appearance: str
    equipment: List[str]
    personality: str
    backstory: str

class PromptEnhancer:
    """AI-powered prompt enhancement using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = None
        self.available = False
        
        if api_key and OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=api_key)
                self.available = True
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")
        elif not OPENAI_AVAILABLE:
            print("OpenAI package not available")
    
    def enhance_character_prompt(self, 
                                character_data: Dict[str, Any], 
                                style: str, 
                                base_prompt: str) -> str:
        """Enhance prompt using OpenAI with character context"""
        if not self.available:
            return base_prompt
        
        try:
            system_prompt = f"""
            You are an expert D&D character art prompt engineer specializing in {style} art style.
            Your task is to enhance prompts for AI art generation based on character data.
            
            Focus on:
            - Visual characteristics (appearance, clothing, equipment)
            - Style-specific elements for {style}
            - Artistic quality and composition
            - D&D fantasy elements
            - Professional art terminology
            
            Return only the enhanced prompt, no explanations.
            """
            
            character_context = self._format_character_data(character_data)
            
            user_prompt = f"""
            Character Data:
            {character_context}
            
            Art Style: {style}
            Base Prompt: {base_prompt}
            
            Enhance this prompt for optimal {style} character art generation.
            Focus on visual details, artistic quality, and style consistency.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content.strip()
            return self._clean_prompt(enhanced_prompt)
            
        except Exception as e:
            print(f"OpenAI enhancement failed: {e}")
            return base_prompt
    
    def analyze_character(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze character data and extract visual characteristics"""
        if not self.available:
            return {
                "analysis": "OpenAI not available",
                "suggestions": [],
                "visual_traits": [],
                "equipment_details": []
            }
        
        try:
            system_prompt = """
            You are an expert D&D character analyst specializing in visual art generation.
            Analyze character data and extract key visual characteristics for art generation.
            
            Focus on:
            - Physical appearance and features
            - Clothing and armor details
            - Equipment and weapons
            - Personality traits that affect appearance
            - Artistic style suggestions
            - Prompt enhancement recommendations
            """
            
            character_context = self._format_character_data(character_data)
            
            user_prompt = f"""
            Character Data:
            {character_context}
            
            Analyze this character and provide:
            1. Key visual characteristics
            2. Equipment and clothing details
            3. Personality traits that affect appearance
            4. Suggested art styles
            5. Prompt enhancement suggestions
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "analysis": analysis,
                "suggestions": self._extract_suggestions(analysis),
                "visual_traits": self._extract_visual_traits(analysis),
                "equipment_details": self._extract_equipment(analysis)
            }
            
        except Exception as e:
            return {
                "analysis": f"Analysis failed: {e}",
                "suggestions": [],
                "visual_traits": [],
                "equipment_details": []
            }
    
    def generate_style_variations(self, base_prompt: str, style: str) -> List[str]:
        """Generate multiple style variations of a prompt"""
        if not self.available:
            return [base_prompt]
        
        try:
            system_prompt = f"""
            You are an expert art prompt engineer.
            Generate 3 different variations of the given prompt optimized for {style} art style.
            Each variation should have a different artistic approach while maintaining the core character.
            """
            
            user_prompt = f"""
            Base Prompt: {base_prompt}
            Style: {style}
            
            Generate 3 variations:
            1. Focus on dramatic lighting and composition
            2. Focus on detailed character features and equipment
            3. Focus on atmospheric and environmental elements
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            variations_text = response.choices[0].message.content
            variations = self._parse_variations(variations_text)
            return [self._clean_prompt(v) for v in variations]
            
        except Exception as e:
            print(f"Style variation generation failed: {e}")
            return [base_prompt]
    
    def suggest_improvements(self, current_prompt: str, style: str) -> List[str]:
        """Provide actionable prompt improvement suggestions"""
        if not self.available:
            return ["OpenAI not available for suggestions"]
        
        try:
            system_prompt = f"""
            You are an expert art prompt engineer.
            Analyze the given prompt and provide specific improvement suggestions for {style} art style.
            Focus on actionable, specific recommendations.
            """
            
            user_prompt = f"""
            Current Prompt: {current_prompt}
            Target Style: {style}
            
            Provide 3-5 specific improvement suggestions.
            Be actionable and specific.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            suggestions_text = response.choices[0].message.content
            return self._parse_suggestions(suggestions_text)
            
        except Exception as e:
            print(f"Improvement suggestions failed: {e}")
            return ["Unable to generate suggestions"]
    
    def _format_character_data(self, character_data: Dict[str, Any]) -> str:
        """Format character data for AI analysis"""
        if not character_data:
            return "No character data provided"
        
        formatted = []
        for key, value in character_data.items():
            if value:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No character data provided"
    
    def _clean_prompt(self, prompt: str) -> str:
        """Clean and validate prompt"""
        if not prompt:
            return ""
        
        # Remove common AI response artifacts
        prompt = re.sub(r'^(Enhanced prompt:|Prompt:|Here\'s the enhanced prompt:)\s*', '', prompt, flags=re.IGNORECASE)
        prompt = re.sub(r'^\d+\.\s*', '', prompt)  # Remove numbered lists
        prompt = prompt.strip()
        
        return prompt
    
    def _extract_suggestions(self, analysis: str) -> List[str]:
        """Extract improvement suggestions from analysis"""
        suggestions = []
        lines = analysis.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['suggest', 'recommend', 'improve', 'enhance']):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _extract_visual_traits(self, analysis: str) -> List[str]:
        """Extract visual traits from analysis"""
        traits = []
        lines = analysis.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['appearance', 'feature', 'physical', 'visual']):
                traits.append(line.strip())
        
        return traits[:5]  # Limit to 5 traits
    
    def _extract_equipment(self, analysis: str) -> List[str]:
        """Extract equipment details from analysis"""
        equipment = []
        lines = analysis.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['equipment', 'weapon', 'armor', 'gear', 'item']):
                equipment.append(line.strip())
        
        return equipment[:5]  # Limit to 5 equipment items
    
    def _parse_variations(self, variations_text: str) -> List[str]:
        """Parse style variations from AI response"""
        variations = []
        lines = variations_text.split('\n')
        
        current_variation = ""
        for line in lines:
            if re.match(r'^\d+\.', line.strip()):
                if current_variation:
                    variations.append(current_variation.strip())
                current_variation = line.strip()
            else:
                current_variation += " " + line.strip()
        
        if current_variation:
            variations.append(current_variation.strip())
        
        return variations[:3]  # Limit to 3 variations
    
    def _parse_suggestions(self, suggestions_text: str) -> List[str]:
        """Parse improvement suggestions from AI response"""
        suggestions = []
        lines = suggestions_text.split('\n')
        
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # Limit to 5 suggestions

class CharacterAnalyzer:
    """Advanced character analysis and prompt generation"""
    
    def __init__(self, openai_integration: PromptEnhancer):
        self.openai = openai_integration
    
    def create_character_prompt(self, character_data: Dict[str, Any], style: str) -> str:
        """Create a complete character prompt from character data"""
        if not self.openai.available:
            return self._create_basic_prompt(character_data, style)
        
        try:
            system_prompt = f"""
            You are an expert D&D character art prompt engineer.
            Create a comprehensive, detailed prompt for {style} character art generation.
            
            Include:
            - Physical appearance and features
            - Clothing and armor details
            - Equipment and weapons
            - Personality traits that affect appearance
            - Artistic style elements for {style}
            - Professional art terminology
            """
            
            character_context = self.openai._format_character_data(character_data)
            
            user_prompt = f"""
            Character Data:
            {character_context}
            
            Art Style: {style}
            
            Create a comprehensive prompt for {style} character art generation.
            Focus on visual details, artistic quality, and style consistency.
            """
            
            response = self.openai.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return self.openai._clean_prompt(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Character prompt creation failed: {e}")
            return self._create_basic_prompt(character_data, style)
    
    def _create_basic_prompt(self, character_data: Dict[str, Any], style: str) -> str:
        """Create basic prompt without OpenAI"""
        prompt_parts = []
        
        # Add character basics
        if character_data.get('name'):
            prompt_parts.append(f"Character: {character_data['name']}")
        
        if character_data.get('race'):
            prompt_parts.append(f"Race: {character_data['race']}")
        
        if character_data.get('class_name'):
            prompt_parts.append(f"Class: {character_data['class_name']}")
        
        if character_data.get('appearance'):
            prompt_parts.append(f"Appearance: {character_data['appearance']}")
        
        if character_data.get('equipment'):
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

# Example usage and testing
if __name__ == "__main__":
    # Test the integration
    enhancer = PromptEnhancer()
    
    # Test character data
    test_character = {
        "name": "Aria Shadowbane",
        "race": "Tiefling",
        "class_name": "Warlock",
        "level": 5,
        "background": "Noble",
        "appearance": "Dark red skin, golden eyes, small horns, elegant features",
        "equipment": ["Leather armor", "Arcane focus", "Dagger"],
        "personality": "Charismatic and mysterious",
        "backstory": "Former noble who made a pact with a fiend"
    }
    
    # Test prompt enhancement
    base_prompt = "Tiefling warlock, dark red skin, golden eyes"
    enhanced = enhancer.enhance_character_prompt(test_character, "fantasy_realistic", base_prompt)
    print(f"Enhanced prompt: {enhanced}")
    
    # Test character analysis
    analysis = enhancer.analyze_character(test_character)
    print(f"Analysis: {analysis}")
