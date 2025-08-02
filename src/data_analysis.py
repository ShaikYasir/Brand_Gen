"""
Data Analysis Module for BrandGen
Handles customer segmentation, campaign analysis, and data processing.
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Any, Tuple
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from src.config import Config

class DataAnalyzer:
    """Handles all data analysis and customer segmentation tasks."""
    
    def __init__(self):
        self.config = Config()
        self.customer_data = None
        self.segments = None
        
    def load_customer_data(self, file_path: str = None) -> pd.DataFrame:
        """Load customer data from CSV file."""
        if file_path is None:
            file_path = self.config.CUSTOMER_DATA_FILE
            
        try:
            if os.path.exists(file_path):
                self.customer_data = pd.read_csv(file_path)
                return self.customer_data
            else:
                # Create sample data if file doesn't exist
                return self.generate_sample_customer_data()
        except Exception as e:
            print(f"Error loading customer data: {e}")
            return self.generate_sample_customer_data()
    
    def generate_sample_customer_data(self, n_customers: int = 1000) -> pd.DataFrame:
        """Generate sample customer data for demonstration."""
        np.random.seed(42)
        
        data = {
            'customer_id': range(1, n_customers + 1),
            'age': np.random.normal(35, 12, n_customers).astype(int),
            'income': np.random.lognormal(10.5, 0.5, n_customers).astype(int),
            'spending_score': np.random.randint(1, 101, n_customers),
            'purchase_frequency': np.random.poisson(3, n_customers),
            'preferred_category': np.random.choice(['Fashion', 'Technology', 'Food', 'Beauty', 'Automotive'], n_customers),
            'engagement_rate': np.random.beta(2, 5, n_customers),
            'digital_savvy': np.random.randint(1, 11, n_customers),
            'brand_loyalty': np.random.beta(3, 2, n_customers)
        }
        
        self.customer_data = pd.DataFrame(data)
        
        # Ensure age is reasonable
        self.customer_data['age'] = self.customer_data['age'].clip(18, 80)
        
        # Save sample data
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        self.customer_data.to_csv(self.config.CUSTOMER_DATA_FILE, index=False)
        
        return self.customer_data
    
    def perform_customer_segmentation(self, n_clusters: int = 5) -> Dict[str, Any]:
        """Perform customer segmentation using K-means clustering."""
        if self.customer_data is None:
            self.load_customer_data()
        
        # Select features for clustering
        features = ['age', 'income', 'spending_score', 'purchase_frequency', 
                   'engagement_rate', 'digital_savvy', 'brand_loyalty']
        
        X = self.customer_data[features].copy()
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Add cluster labels to data
        self.customer_data['segment'] = clusters
        
        # Generate segment profiles
        segment_profiles = self._generate_segment_profiles()
        
        self.segments = {
            'data': self.customer_data,
            'profiles': segment_profiles,
            'n_clusters': n_clusters
        }
        
        return self.segments
    
    def _generate_segment_profiles(self) -> Dict[int, Dict[str, Any]]:
        """Generate descriptive profiles for each customer segment."""
        profiles = {}
        
        for segment in self.customer_data['segment'].unique():
            segment_data = self.customer_data[self.customer_data['segment'] == segment]
            
            profile = {
                'size': len(segment_data),
                'avg_age': segment_data['age'].mean(),
                'avg_income': segment_data['income'].mean(),
                'avg_spending_score': segment_data['spending_score'].mean(),
                'preferred_categories': segment_data['preferred_category'].value_counts().to_dict(),
                'avg_engagement': segment_data['engagement_rate'].mean(),
                'digital_savvy_score': segment_data['digital_savvy'].mean(),
                'brand_loyalty_score': segment_data['brand_loyalty'].mean()
            }
            
            # Generate segment name based on characteristics
            profile['name'] = self._generate_segment_name(profile)
            profiles[segment] = profile
            
        return profiles
    
    def _generate_segment_name(self, profile: Dict[str, Any]) -> str:
        """Generate descriptive name for customer segment."""
        age = profile['avg_age']
        income = profile['avg_income']
        spending = profile['avg_spending_score']
        digital = profile['digital_savvy_score']
        
        if age < 30:
            age_group = "Young"
        elif age < 50:
            age_group = "Middle-aged"
        else:
            age_group = "Mature"
            
        if income > 75000:
            income_level = "High-income"
        elif income > 45000:
            income_level = "Mid-income"
        else:
            income_level = "Budget-conscious"
            
        if digital > 7:
            tech_level = "Tech-savvy"
        elif digital > 4:
            tech_level = "Moderate-tech"
        else:
            tech_level = "Traditional"
            
        return f"{age_group} {income_level} {tech_level}"
    
    def get_segment_recommendations(self, segment_id: int) -> Dict[str, Any]:
        """Get marketing recommendations for a specific segment."""
        if self.segments is None:
            self.perform_customer_segmentation()
            
        profile = self.segments['profiles'][segment_id]
        
        recommendations = {
            'preferred_channels': self._recommend_channels(profile),
            'campaign_types': self._recommend_campaign_types(profile),
            'messaging_tone': self._recommend_messaging_tone(profile),
            'budget_allocation': self._recommend_budget_allocation(profile)
        }
        
        return recommendations
    
    def _recommend_channels(self, profile: Dict[str, Any]) -> List[str]:
        """Recommend marketing channels based on segment profile."""
        channels = []
        
        if profile['digital_savvy_score'] > 6:
            channels.extend(['Social Media', 'Email Marketing', 'Online Ads'])
        if profile['avg_age'] < 35:
            channels.extend(['Instagram', 'TikTok', 'YouTube'])
        if profile['avg_income'] > 60000:
            channels.extend(['Premium Publications', 'LinkedIn'])
        if profile['digital_savvy_score'] < 5:
            channels.extend(['Traditional Media', 'Print Ads', 'Radio'])
            
        return list(set(channels))
    
    def _recommend_campaign_types(self, profile: Dict[str, Any]) -> List[str]:
        """Recommend campaign types based on segment profile."""
        campaigns = []
        
        if profile['brand_loyalty_score'] > 0.7:
            campaigns.append('Loyalty Program')
        if profile['avg_spending_score'] > 70:
            campaigns.append('Premium Product Launch')
        if profile['avg_age'] < 30:
            campaigns.append('Trend-focused Campaign')
        if profile['digital_savvy_score'] > 7:
            campaigns.append('Interactive Digital Campaign')
            
        return campaigns
    
    def _recommend_messaging_tone(self, profile: Dict[str, Any]) -> str:
        """Recommend messaging tone based on segment profile."""
        if profile['avg_age'] < 30:
            return "Casual and trendy"
        elif profile['avg_income'] > 75000:
            return "Professional and sophisticated"
        elif profile['digital_savvy_score'] > 7:
            return "Tech-forward and innovative"
        else:
            return "Friendly and trustworthy"
    
    def _recommend_budget_allocation(self, profile: Dict[str, Any]) -> Dict[str, float]:
        """Recommend budget allocation based on segment profile."""
        base_allocation = {
            'Digital': 0.4,
            'Traditional': 0.3,
            'Content Creation': 0.2,
            'Analytics': 0.1
        }
        
        if profile['digital_savvy_score'] > 7:
            base_allocation['Digital'] += 0.2
            base_allocation['Traditional'] -= 0.2
        
        if profile['avg_age'] < 30:
            base_allocation['Content Creation'] += 0.1
            base_allocation['Analytics'] += 0.1
            base_allocation['Traditional'] -= 0.2
            
        return base_allocation
    
    def create_segment_visualization(self) -> Dict[str, Any]:
        """Create visualizations for customer segments."""
        if self.segments is None:
            self.perform_customer_segmentation()
            
        data = self.segments['data']
        
        # Scatter plot of segments
        fig_scatter = px.scatter(
            data, 
            x='income', 
            y='spending_score',
            color='segment',
            size='age',
            title='Customer Segments by Income and Spending Score',
            hover_data=['age', 'purchase_frequency']
        )
        
        # Segment size pie chart
        segment_sizes = data['segment'].value_counts()
        fig_pie = px.pie(
            values=segment_sizes.values,
            names=[f"Segment {i}" for i in segment_sizes.index],
            title='Customer Segment Distribution'
        )
        
        return {
            'scatter_plot': fig_scatter,
            'pie_chart': fig_pie,
            'segment_profiles': self.segments['profiles']
        }
