"""
Basic tests for BrandGen components
"""

import pytest
import os
import sys
import pandas as pd
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import Config, validate_config
from src.data_analysis import DataAnalyzer

class TestConfig:
    """Test configuration module."""
    
    def test_config_initialization(self):
        """Test Config class initialization."""
        config = Config()
        assert config.DEFAULT_IMAGE_SIZE == "1024x1024"
        assert config.DEFAULT_IMAGE_QUALITY == "standard"
        assert config.PAGE_TITLE == "BrandGen - AI Marketing Image Generator"
    
    def test_validate_config_without_api_key(self):
        """Test configuration validation without API key."""
        with patch.dict(os.environ, {}, clear=True):
            assert validate_config() == False
    
    def test_validate_config_with_api_key(self):
        """Test configuration validation with API key."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}, clear=True):
            assert validate_config() == True

class TestDataAnalyzer:
    """Test data analysis module."""
    
    def test_data_analyzer_initialization(self):
        """Test DataAnalyzer initialization."""
        analyzer = DataAnalyzer()
        assert analyzer.config is not None
        assert analyzer.customer_data is None
    
    def test_generate_sample_customer_data(self):
        """Test sample data generation."""
        analyzer = DataAnalyzer()
        data = analyzer.generate_sample_customer_data(100)
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100
        assert 'customer_id' in data.columns
        assert 'age' in data.columns
        assert 'income' in data.columns
        assert 'spending_score' in data.columns
    
    def test_customer_segmentation(self):
        """Test customer segmentation functionality."""
        analyzer = DataAnalyzer()
        data = analyzer.generate_sample_customer_data(50)
        analyzer.customer_data = data
        
        segments = analyzer.perform_customer_segmentation(3)
        
        assert 'data' in segments
        assert 'profiles' in segments
        assert 'n_clusters' in segments
        assert segments['n_clusters'] == 3
        assert len(segments['profiles']) == 3

if __name__ == "__main__":
    # Simple test runner
    print("Running BrandGen Tests...")
    
    # Test Config
    print("\n1. Testing Config...")
    try:
        config = Config()
        print("✅ Config initialization passed")
    except Exception as e:
        print(f"❌ Config test failed: {e}")
    
    # Test DataAnalyzer
    print("\n2. Testing DataAnalyzer...")
    try:
        analyzer = DataAnalyzer()
        data = analyzer.generate_sample_customer_data(10)
        print(f"✅ Sample data generation passed (generated {len(data)} records)")
    except Exception as e:
        print(f"❌ DataAnalyzer test failed: {e}")
    
    print("\n🎉 Basic tests completed!")
