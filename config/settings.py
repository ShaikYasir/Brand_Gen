"""
Configuration settings for BrandGen application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "dall-e-3")
    DEFAULT_IMAGE_SIZE = os.getenv("DEFAULT_IMAGE_SIZE", "1024x1024")
    MAX_IMAGES_PER_BATCH = int(os.getenv("MAX_IMAGES_PER_BATCH", "10"))
    
    # Application Settings
    APP_TITLE = "BrandGen - AI Marketing Image Generator"
    APP_ICON = "🎨"
    
    # File Paths
    DATA_DIR = "data"
    OUTPUT_DIR = "generated_images"
    CONFIG_DIR = "config"
    
    # Streamlit Configuration
    STREAMLIT_THEME = os.getenv("STREAMLIT_THEME", "light")
    
    # Image Generation Settings
    IMAGE_QUALITY = "standard"  # standard or hd
    IMAGE_STYLE = "vivid"       # vivid or natural
    
    # Data Processing Settings
    MAX_UPLOAD_SIZE_MB = 100
    SUPPORTED_FILE_TYPES = ["csv", "xlsx", "json"]
    
    # Campaign Settings
    DEFAULT_CAMPAIGN_DURATION = 30  # days
    MIN_CAMPAIGN_BUDGET = 100      # USD
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Validate if OpenAI API key is present"""
        return cls.OPENAI_API_KEY is not None and len(cls.OPENAI_API_KEY) > 0
    
    @classmethod
    def get_image_sizes(cls) -> list:
        """Get available image sizes for DALL-E"""
        return ["1024x1024", "1792x1024", "1024x1792"]
    
    @classmethod
    def get_supported_models(cls) -> list:
        """Get supported DALL-E models"""
        return ["dall-e-3", "dall-e-2"]

# Create global settings instance
settings = Settings()
