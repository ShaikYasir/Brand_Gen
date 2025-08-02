"""
AI Image Generation module using OpenAI DALL-E API
"""

import openai
import requests
from PIL import Image
import io
import os
import json
from typing import List, Dict, Any, Optional, Tuple
import time
import logging
from datetime import datetime

from src.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerator:
    """Handles AI image generation using OpenAI DALL-E API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ImageGenerator
        
        Args:
            api_key: OpenAI API key (optional, will use config if not provided)
        """
        self.config = Config()
        self.api_key = api_key or self.config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Please set OPENAI_API_KEY in your environment.")
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai
        
        # Image generation history
        self.generation_history: List[Dict[str, Any]] = []
        
    def create_marketing_prompt(self, 
                              product: str,
                              target_audience: str,
                              style: str = "modern",
                              mood: str = "professional",
                              additional_elements: List[str] = None) -> str:
        """
        Create a detailed prompt for marketing image generation
        
        Args:
            product: Product or service to promote
            target_audience: Description of target audience
            style: Visual style (modern, vintage, minimalist, etc.)
            mood: Mood/tone (professional, friendly, energetic, etc.)
            additional_elements: Additional elements to include
            
        Returns:
            Formatted prompt string
        """
        base_prompt = f"Create a {style} marketing image for {product} targeting {target_audience}. "
        base_prompt += f"The mood should be {mood}. "
        
        if additional_elements:
            base_prompt += f"Include these elements: {', '.join(additional_elements)}. "
        
        base_prompt += "High quality, professional photography style, clean composition, "
        base_prompt += "suitable for digital marketing campaigns."
        
        return base_prompt
    
    def generate_personalized_prompts(self, 
                                    campaign_data: Dict[str, Any],
                                    segment_data: Dict[str, Any]) -> List[str]:
        """
        Generate personalized prompts based on customer segments
        
        Args:
            campaign_data: Campaign configuration
            segment_data: Customer segment characteristics
            
        Returns:
            List of personalized prompts
        """
        prompts = []
        
        for segment_name, segment_info in segment_data.items():
            # Extract segment characteristics
            characteristics = segment_info.get('characteristics', {})
            
            # Build personalized prompt
            prompt = f"Create a {campaign_data.get('style', 'modern')} marketing image for "
            prompt += f"{campaign_data.get('product', 'product')} targeting "
            
            # Add demographic information
            if 'age' in characteristics:
                age_mean = characteristics['age'].get('mean', 30)
                if age_mean < 25:
                    prompt += "young adults (18-25) "
                elif age_mean < 35:
                    prompt += "millennials (25-35) "
                elif age_mean < 50:
                    prompt += "middle-aged professionals (35-50) "
                else:
                    prompt += "mature adults (50+) "
            
            if 'gender' in characteristics:
                gender_mode = characteristics['gender'].get('mode', 'diverse')
                if gender_mode.lower() in ['male', 'female']:
                    prompt += f"primarily {gender_mode.lower()} audience "
                else:
                    prompt += "diverse audience "
            
            # Add interest-based elements
            if 'interests' in characteristics:
                interest_mode = characteristics['interests'].get('mode', '')
                if interest_mode:
                    prompt += f"with interests in {interest_mode} "
            
            # Add style and mood
            prompt += f". Style: {campaign_data.get('style', 'modern')}, "
            prompt += f"Mood: {campaign_data.get('mood', 'professional')}. "
            prompt += "High quality, professional, suitable for digital marketing."
            
            prompts.append(prompt)
        
        return prompts
    
    def generate_image(self, 
                      prompt: str,
                      size: str = "1024x1024",
                      quality: str = "standard",
                      style: str = "vivid",
                      model: str = "dall-e-3") -> Dict[str, Any]:
        """
        Generate a single image using DALL-E
        
        Args:
            prompt: Text prompt for image generation
            size: Image size (1024x1024, 1792x1024, 1024x1792)
            quality: Image quality (standard, hd)
            style: Image style (vivid, natural)
            model: DALL-E model to use
            
        Returns:
            Dictionary containing image data and metadata
        """
        try:
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            # Generate image using OpenAI API
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1
            )
            
            # Extract image URL
            image_url = response.data[0].url
            
            # Download image
            image_data = self._download_image(image_url)
            
            # Create result dictionary
            result = {
                'success': True,
                'image_data': image_data,
                'image_url': image_url,
                'prompt': prompt,
                'size': size,
                'quality': quality,
                'style': style,
                'model': model,
                'timestamp': datetime.now().isoformat(),
                'revised_prompt': getattr(response.data[0], 'revised_prompt', prompt)
            }
            
            # Add to history
            self.generation_history.append(result)
            
            logger.info("Image generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'prompt': prompt,
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_batch(self, 
                      prompts: List[str],
                      size: str = "1024x1024",
                      quality: str = "standard",
                      style: str = "vivid",
                      delay: float = 1.0) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch with rate limiting
        
        Args:
            prompts: List of prompts for image generation
            size: Image size
            quality: Image quality
            style: Image style
            delay: Delay between requests (seconds)
            
        Returns:
            List of generation results
        """
        results = []
        
        logger.info(f"Starting batch generation of {len(prompts)} images")
        
        for i, prompt in enumerate(prompts):
            logger.info(f"Generating image {i+1}/{len(prompts)}")
            
            result = self.generate_image(
                prompt=prompt,
                size=size,
                quality=quality,
                style=style
            )
            
            results.append(result)
            
            # Rate limiting
            if i < len(prompts) - 1:
                time.sleep(delay)
        
        logger.info(f"Batch generation completed. {sum(1 for r in results if r['success'])} successful generations")
        return results
    
    def _download_image(self, url: str) -> bytes:
        """
        Download image from URL
        
        Args:
            url: Image URL
            
        Returns:
            Image data as bytes
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            raise
    
    def save_image(self, 
                   image_data: bytes,
                   filename: str,
                   output_dir: str = "generated_images") -> str:
        """
        Save image data to file
        
        Args:
            image_data: Image data as bytes
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            Full path to saved file
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Ensure filename has extension
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename += '.png'
            
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            image = Image.open(io.BytesIO(image_data))
            image.save(filepath)
            
            logger.info(f"Image saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise
    
    def save_batch_results(self, 
                          results: List[Dict[str, Any]],
                          output_dir: str = "generated_images",
                          prefix: str = "campaign") -> List[str]:
        """
        Save batch generation results to files
        
        Args:
            results: List of generation results
            output_dir: Output directory
            prefix: Filename prefix
            
        Returns:
            List of saved file paths
        """
        saved_files = []
        
        for i, result in enumerate(results):
            if result['success']:
                filename = f"{prefix}_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                try:
                    filepath = self.save_image(
                        image_data=result['image_data'],
                        filename=filename,
                        output_dir=output_dir
                    )
                    saved_files.append(filepath)
                except Exception as e:
                    logger.error(f"Failed to save image {i+1}: {str(e)}")
        
        return saved_files
    
    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Get the history of image generations"""
        return self.generation_history
    
    def export_history(self, filepath: str = "generation_history.json") -> str:
        """
        Export generation history to JSON file
        
        Args:
            filepath: Output file path
            
        Returns:
            Path to exported file
        """
        try:
            # Remove binary data for JSON serialization
            export_data = []
            for item in self.generation_history:
                export_item = item.copy()
                if 'image_data' in export_item:
                    del export_item['image_data']  # Remove binary data
                export_data.append(export_item)
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Generation history exported to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting history: {str(e)}")
            raise
