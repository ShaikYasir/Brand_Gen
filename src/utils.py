"""
Utility functions for BrandGen application
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
import base64
from PIL import Image
import io
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_file_upload(file_path: str, max_size_mb: int = 100) -> Dict[str, Any]:
    """
    Validate uploaded file
    
    Args:
        file_path: Path to the file to validate
        max_size_mb: Maximum file size in MB
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': False,
        'errors': [],
        'warnings': [],
        'file_info': {}
    }
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            result['errors'].append("File does not exist")
            return result
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        
        result['file_info'] = {
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'extension': file_extension,
            'name': os.path.basename(file_path)
        }
        
        # Check file size
        if file_size > max_size_mb * 1024 * 1024:
            result['errors'].append(f"File size ({result['file_info']['size_mb']} MB) exceeds maximum allowed size ({max_size_mb} MB)")
        
        # Check file extension
        supported_extensions = ['.csv', '.xlsx', '.xls', '.json']
        if file_extension not in supported_extensions:
            result['errors'].append(f"Unsupported file type. Supported types: {', '.join(supported_extensions)}")
        
        # Try to read file content for validation
        if file_extension == '.csv':
            try:
                df = pd.read_csv(file_path, nrows=5)  # Read first 5 rows for validation
                if len(df.columns) == 0:
                    result['errors'].append("CSV file appears to be empty or invalid")
                else:
                    result['file_info']['columns'] = df.columns.tolist()
                    result['file_info']['sample_rows'] = len(df)
            except Exception as e:
                result['errors'].append(f"Unable to read CSV file: {str(e)}")
        
        elif file_extension in ['.xlsx', '.xls']:
            try:
                df = pd.read_excel(file_path, nrows=5)
                if len(df.columns) == 0:
                    result['errors'].append("Excel file appears to be empty or invalid")
                else:
                    result['file_info']['columns'] = df.columns.tolist()
                    result['file_info']['sample_rows'] = len(df)
            except Exception as e:
                result['errors'].append(f"Unable to read Excel file: {str(e)}")
        
        elif file_extension == '.json':
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                result['file_info']['json_type'] = type(data).__name__
            except Exception as e:
                result['errors'].append(f"Unable to read JSON file: {str(e)}")
        
        # Set validation result
        result['valid'] = len(result['errors']) == 0
        
        if result['valid']:
            logger.info(f"File validation successful: {file_path}")
        else:
            logger.warning(f"File validation failed: {file_path}, Errors: {result['errors']}")
        
        return result
        
    except Exception as e:
        result['errors'].append(f"Unexpected error during validation: {str(e)}")
        logger.error(f"Error validating file {file_path}: {str(e)}")
        return result

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format currency amount for display
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format percentage for display
    
    Args:
        value: Percentage value
        decimal_places: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimal_places}f}%"

def format_number(value: Union[int, float], abbreviate: bool = True) -> str:
    """
    Format large numbers with abbreviations
    
    Args:
        value: Number to format
        abbreviate: Whether to use abbreviations (K, M, B)
        
    Returns:
        Formatted number string
    """
    if not abbreviate:
        return f"{value:,}"
    
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return str(value)

def image_to_base64(image_path: str) -> str:
    """
    Convert image to base64 string for display in Streamlit
    
    Args:
        image_path: Path to image file
        
    Returns:
        Base64 encoded image string
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return ""

def resize_image(image_path: str, max_width: int = 800, max_height: int = 600) -> str:
    """
    Resize image and save to temporary file
    
    Args:
        image_path: Path to original image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Path to resized image
    """
    try:
        with Image.open(image_path) as img:
            # Calculate new dimensions
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save resized image
            output_path = f"{os.path.splitext(image_path)[0]}_resized.png"
            img.save(output_path, "PNG")
            
            return output_path
            
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return image_path  # Return original path if resize fails

def create_sample_data() -> pd.DataFrame:
    """
    Create sample customer data for demonstration
    
    Returns:
        Sample customer DataFrame
    """
    np.random.seed(42)
    
    sample_data = {
        'customer_id': range(1, 501),
        'name': [f"Customer_{i}" for i in range(1, 501)],
        'age': np.random.randint(18, 70, 500),
        'gender': np.random.choice(['Male', 'Female', 'Other'], 500, p=[0.45, 0.45, 0.1]),
        'location': np.random.choice(['New York', 'California', 'Texas', 'Florida', 'Illinois', 'Pennsylvania', 'Ohio'], 500),
        'interests': np.random.choice(['Technology', 'Fashion', 'Sports', 'Travel', 'Food', 'Art', 'Music'], 500),
        'annual_income': np.random.randint(25000, 150000, 500),
        'purchase_history': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Beauty', 'Sports'], 500),
        'customer_since': pd.date_range('2020-01-01', '2023-12-31', periods=500),
        'total_spent': np.random.randint(100, 5000, 500)
    }
    
    return pd.DataFrame(sample_data)

def generate_campaign_templates() -> Dict[str, Any]:
    """
    Generate pre-defined campaign templates
    
    Returns:
        Dictionary of campaign templates
    """
    templates = {
        "fashion_brand": {
            "name": "Fashion Brand Campaign",
            "product": "Fashion collection",
            "style": "modern",
            "mood": "stylish",
            "target_audience": "fashion-conscious consumers",
            "additional_elements": ["trendy models", "urban background", "vibrant colors"],
            "industry": "Fashion",
            "budget_range": "medium"
        },
        "tech_product": {
            "name": "Tech Product Launch",
            "product": "Tech gadget",
            "style": "futuristic",
            "mood": "innovative",
            "target_audience": "tech enthusiasts",
            "additional_elements": ["sleek design", "minimalist", "high-tech environment"],
            "industry": "Technology",
            "budget_range": "high"
        },
        "food_restaurant": {
            "name": "Restaurant Promotion",
            "product": "Gourmet food",
            "style": "appetizing",
            "mood": "warm and inviting",
            "target_audience": "food lovers",
            "additional_elements": ["delicious presentation", "cozy atmosphere", "natural lighting"],
            "industry": "Food & Beverage",
            "budget_range": "low"
        },
        "fitness_health": {
            "name": "Fitness Brand",
            "product": "Fitness program",
            "style": "energetic",
            "mood": "motivational",
            "target_audience": "fitness enthusiasts",
            "additional_elements": ["active people", "gym environment", "dynamic poses"],
            "industry": "Health & Fitness",
            "budget_range": "medium"
        },
        "luxury_goods": {
            "name": "Luxury Brand",
            "product": "Luxury items",
            "style": "elegant",
            "mood": "sophisticated",
            "target_audience": "affluent consumers",
            "additional_elements": ["premium materials", "elegant lighting", "refined setting"],
            "industry": "Luxury",
            "budget_range": "high"
        }
    }
    
    return templates

def calculate_campaign_roi(total_revenue: float, total_spend: float) -> Dict[str, float]:
    """
    Calculate campaign ROI metrics
    
    Args:
        total_revenue: Total revenue generated
        total_spend: Total amount spent
        
    Returns:
        Dictionary containing ROI metrics
    """
    if total_spend == 0:
        return {
            'roi_percentage': 0,
            'roas': 0,
            'profit': total_revenue,
            'profit_margin': 100 if total_revenue > 0 else 0
        }
    
    roi_percentage = ((total_revenue - total_spend) / total_spend) * 100
    roas = (total_revenue / total_spend) * 100
    profit = total_revenue - total_spend
    profit_margin = (profit / total_revenue) * 100 if total_revenue > 0 else 0
    
    return {
        'roi_percentage': round(roi_percentage, 2),
        'roas': round(roas, 2),
        'profit': round(profit, 2),
        'profit_margin': round(profit_margin, 2)
    }

def export_to_powerbi_format(data: Dict[str, Any], output_path: str) -> str:
    """
    Export data in Power BI compatible format
    
    Args:
        data: Data to export
        output_path: Output file path
        
    Returns:
        Path to exported file
    """
    try:
        # Convert nested dictionaries to flat structure for Power BI
        flattened_data = []
        
        if 'campaigns' in data:
            for campaign_id, campaign_data in data['campaigns'].items():
                row = {
                    'campaign_id': campaign_id,
                    'campaign_name': campaign_data.get('config', {}).get('name', ''),
                    'product': campaign_data.get('config', {}).get('product', ''),
                    'status': campaign_data.get('status', ''),
                    'created_at': campaign_data.get('created_at', ''),
                    'images_generated': len(campaign_data.get('generated_images', [])),
                }
                
                # Add performance metrics if available
                if 'performance_metrics' in campaign_data:
                    metrics = campaign_data['performance_metrics'].get('overall_metrics', {})
                    row.update({
                        'engagement_rate': metrics.get('engagement_rate', 0),
                        'click_through_rate': metrics.get('click_through_rate', 0),
                        'conversion_rate': metrics.get('conversion_rate', 0),
                        'cost_per_acquisition': metrics.get('cost_per_acquisition', 0),
                        'return_on_ad_spend': metrics.get('return_on_ad_spend', 0)
                    })
                
                flattened_data.append(row)
        
        # Convert to DataFrame and save as CSV for Power BI import
        df = pd.DataFrame(flattened_data)
        df.to_csv(output_path, index=False)
        
        logger.info(f"Data exported to Power BI format: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error exporting to Power BI format: {str(e)}")
        raise

def get_color_palette(theme: str = "default") -> List[str]:
    """
    Get color palette for visualizations
    
    Args:
        theme: Color theme name
        
    Returns:
        List of color codes
    """
    palettes = {
        "default": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"],
        "modern": ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe", "#00f2fe", "#43e97b", "#38f9d7"],
        "corporate": ["#2c3e50", "#3498db", "#e74c3c", "#f39c12", "#27ae60", "#9b59b6", "#1abc9c", "#34495e"],
        "vibrant": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd"]
    }
    
    return palettes.get(theme, palettes["default"])

def log_user_action(action: str, details: Dict[str, Any] = None) -> None:
    """
    Log user actions for analytics
    
    Args:
        action: Action name
        details: Additional details about the action
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details or {}
    }
    
    logger.info(f"User Action: {action} - {details}")
    
    # In a production environment, you might want to save this to a database
    # or send to an analytics service
