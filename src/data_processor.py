"""
Data processing and customer segmentation module for BrandGen
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import json
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles data processing, analysis, and customer segmentation"""
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.segments: Optional[Dict[str, pd.DataFrame]] = None
        self.scaler = StandardScaler()
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load customer data from various file formats
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Loaded DataFrame
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.csv':
                self.data = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            elif file_extension == '.json':
                self.data = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
            logger.info(f"Successfully loaded data with {len(self.data)} rows and {len(self.data.columns)} columns")
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data
        
        Returns:
            Cleaned DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        # Remove duplicates
        initial_rows = len(self.data)
        self.data = self.data.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(self.data)} duplicate rows")
        
        # Handle missing values
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        
        # Fill numeric missing values with median
        for col in numeric_columns:
            if self.data[col].isnull().any():
                self.data[col].fillna(self.data[col].median(), inplace=True)
        
        # Fill categorical missing values with mode
        for col in categorical_columns:
            if self.data[col].isnull().any():
                self.data[col].fillna(self.data[col].mode()[0] if len(self.data[col].mode()) > 0 else 'Unknown', inplace=True)
        
        logger.info("Data cleaning completed")
        return self.data
    
    def perform_customer_segmentation(self, features: List[str], n_clusters: int = 4) -> Dict[str, Any]:
        """
        Perform customer segmentation using K-means clustering
        
        Args:
            features: List of feature columns to use for clustering
            n_clusters: Number of clusters to create
            
        Returns:
            Dictionary containing segmentation results
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        try:
            # Prepare features for clustering
            feature_data = self.data[features].copy()
            
            # Handle categorical variables
            categorical_features = feature_data.select_dtypes(include=['object']).columns
            for col in categorical_features:
                feature_data = pd.get_dummies(feature_data, columns=[col], prefix=col)
            
            # Scale features
            scaled_features = self.scaler.fit_transform(feature_data)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(scaled_features)
            
            # Add cluster labels to original data
            self.data['segment'] = clusters
            
            # Create segment analysis
            segment_analysis = {}
            for i in range(n_clusters):
                segment_data = self.data[self.data['segment'] == i]
                segment_analysis[f'Segment_{i}'] = {
                    'size': len(segment_data),
                    'percentage': round(len(segment_data) / len(self.data) * 100, 2),
                    'characteristics': self._analyze_segment(segment_data, features)
                }
            
            logger.info(f"Customer segmentation completed with {n_clusters} segments")
            return {
                'segments': segment_analysis,
                'cluster_centers': kmeans.cluster_centers_,
                'inertia': kmeans.inertia_
            }
            
        except Exception as e:
            logger.error(f"Error in customer segmentation: {str(e)}")
            raise
    
    def _analyze_segment(self, segment_data: pd.DataFrame, features: List[str]) -> Dict[str, Any]:
        """
        Analyze characteristics of a customer segment
        
        Args:
            segment_data: DataFrame containing segment data
            features: List of features used for segmentation
            
        Returns:
            Dictionary containing segment characteristics
        """
        characteristics = {}
        
        for feature in features:
            if feature in segment_data.columns:
                if segment_data[feature].dtype in ['int64', 'float64']:
                    characteristics[feature] = {
                        'mean': round(segment_data[feature].mean(), 2),
                        'median': round(segment_data[feature].median(), 2),
                        'std': round(segment_data[feature].std(), 2)
                    }
                else:
                    characteristics[feature] = {
                        'mode': segment_data[feature].mode().iloc[0] if len(segment_data[feature].mode()) > 0 else 'N/A',
                        'unique_values': segment_data[feature].nunique()
                    }
        
        return characteristics
    
    def generate_insights(self) -> Dict[str, Any]:
        """
        Generate insights from the data
        
        Returns:
            Dictionary containing data insights
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        insights = {
            'total_customers': len(self.data),
            'data_quality': {
                'missing_values': self.data.isnull().sum().sum(),
                'duplicate_rows': self.data.duplicated().sum()
            },
            'summary_stats': self.data.describe(include='all').to_dict()
        }
        
        # Age distribution if age column exists
        if 'age' in self.data.columns:
            insights['age_distribution'] = {
                'mean_age': round(self.data['age'].mean(), 1),
                'age_ranges': {
                    '18-25': len(self.data[(self.data['age'] >= 18) & (self.data['age'] <= 25)]),
                    '26-35': len(self.data[(self.data['age'] >= 26) & (self.data['age'] <= 35)]),
                    '36-45': len(self.data[(self.data['age'] >= 36) & (self.data['age'] <= 45)]),
                    '46+': len(self.data[self.data['age'] >= 46])
                }
            }
        
        # Gender distribution if gender column exists
        if 'gender' in self.data.columns:
            insights['gender_distribution'] = self.data['gender'].value_counts().to_dict()
        
        # Location distribution if location column exists
        if 'location' in self.data.columns:
            insights['location_distribution'] = self.data['location'].value_counts().head(10).to_dict()
        
        return insights
    
    def export_segments(self, output_dir: str = "data/segments") -> List[str]:
        """
        Export customer segments to separate CSV files
        
        Args:
            output_dir: Directory to save segment files
            
        Returns:
            List of exported file paths
        """
        if self.data is None or 'segment' not in self.data.columns:
            raise ValueError("No segmented data available. Please perform segmentation first.")
        
        os.makedirs(output_dir, exist_ok=True)
        exported_files = []
        
        for segment_id in self.data['segment'].unique():
            segment_data = self.data[self.data['segment'] == segment_id]
            filename = f"segment_{segment_id}.csv"
            filepath = os.path.join(output_dir, filename)
            segment_data.to_csv(filepath, index=False)
            exported_files.append(filepath)
            logger.info(f"Exported segment {segment_id} to {filepath}")
        
        return exported_files
