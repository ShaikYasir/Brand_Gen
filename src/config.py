"""
BrandGen Configuration Module
Handles all configuration settings, API keys, and environment variables.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for BrandGen application."""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Image Generation Settings
    DEFAULT_IMAGE_SIZE = "1024x1024"
    DEFAULT_IMAGE_QUALITY = "standard"
    DEFAULT_IMAGE_STYLE = "vivid"
    MAX_IMAGES_PER_BATCH = 4
    
    # File Paths
    DATA_DIR = "data"
    GENERATED_IMAGES_DIR = "generated_images"
    TEMPLATES_FILE = os.path.join(DATA_DIR, "campaign_templates.json")
    CUSTOMER_DATA_FILE = os.path.join(DATA_DIR, "customer_segments.csv")
    
    # Streamlit Configuration
    PAGE_TITLE = "BrandGen - AI Marketing Image Generator"
    PAGE_ICON = "🎨"
    LAYOUT = "wide"
    
    # DALL-E Prompt Settings
    BASE_PROMPT_TEMPLATE = """
    Create a high-quality marketing image for {product} targeting {target_audience}.
    Style: {style}, Mood: {mood}
    Include: {additional_elements}
    The image should be professional, engaging, and suitable for {industry} marketing campaigns.
    """
    
    # Marketing Campaign Settings
    CAMPAIGN_TYPES = [
        "Product Launch",
        "Brand Awareness", 
        "Seasonal Promotion",
        "Social Media Campaign",
        "Email Marketing",
        "Website Banner"
    ]
    
    IMAGE_STYLES = [
        "Photorealistic",
        "Artistic/Stylized", 
        "Minimalist",
        "Vintage/Retro",
        "Modern/Contemporary",
        "Luxury/Premium"
    ]
    
    TARGET_AUDIENCES = [
        "Young Adults (18-30)",
        "Professionals (25-45)", 
        "Families (30-50)",
        "Seniors (50+)",
        "Tech Enthusiasts",
        "Luxury Buyers",
        "Budget Conscious"
    ]

def get_config() -> Dict[str, Any]:
    """Return configuration as dictionary."""
    return {
        'openai_api_key': Config.OPENAI_API_KEY,
        'image_size': Config.DEFAULT_IMAGE_SIZE,
        'data_dir': Config.DATA_DIR,
        'generated_images_dir': Config.GENERATED_IMAGES_DIR,
        'templates_file': Config.TEMPLATES_FILE
    }

def validate_config() -> bool:
    """Validate that all required configuration is present."""
    if not Config.OPENAI_API_KEY:
        return False
    return True
