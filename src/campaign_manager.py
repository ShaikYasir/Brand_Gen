"""
Campaign management module for BrandGen
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import logging

from .data_processor import DataProcessor
from .image_generator import ImageGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignManager:
    """Manages marketing campaigns from creation to analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CampaignManager
        
        Args:
            api_key: OpenAI API key for image generation
        """
        self.data_processor = DataProcessor()
        self.image_generator = ImageGenerator(api_key)
        self.campaigns: Dict[str, Dict[str, Any]] = {}
        
    def create_campaign(self, 
                       campaign_config: Dict[str, Any],
                       customer_data: Optional[pd.DataFrame] = None) -> str:
        """
        Create a new marketing campaign
        
        Args:
            campaign_config: Campaign configuration dictionary
            customer_data: Customer data for personalization
            
        Returns:
            Campaign ID
        """
        # Generate unique campaign ID
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Validate required fields
        required_fields = ['name', 'product', 'target_audience', 'style', 'mood']
        for field in required_fields:
            if field not in campaign_config:
                raise ValueError(f"Missing required field: {field}")
        
        # Create campaign structure
        campaign = {
            'id': campaign_id,
            'config': campaign_config,
            'created_at': datetime.now().isoformat(),
            'status': 'created',
            'customer_data': customer_data.to_dict() if customer_data is not None else None,
            'segments': None,
            'generated_images': [],
            'performance_metrics': {},
            'history': [f"Campaign created at {datetime.now().isoformat()}"]
        }
        
        self.campaigns[campaign_id] = campaign
        logger.info(f"Created campaign: {campaign_id}")
        
        return campaign_id
    
    def analyze_target_audience(self, 
                               campaign_id: str,
                               segmentation_features: List[str] = None,
                               n_segments: int = 4) -> Dict[str, Any]:
        """
        Analyze target audience and create customer segments
        
        Args:
            campaign_id: Campaign identifier
            segmentation_features: Features to use for segmentation
            n_segments: Number of customer segments to create
            
        Returns:
            Segmentation analysis results
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        if campaign['customer_data'] is None:
            raise ValueError("No customer data available for analysis")
        
        # Load customer data
        customer_df = pd.DataFrame(campaign['customer_data'])
        self.data_processor.data = customer_df
        
        # Clean data
        self.data_processor.clean_data()
        
        # Default segmentation features
        if segmentation_features is None:
            available_features = customer_df.columns.tolist()
            segmentation_features = [col for col in ['age', 'gender', 'location', 'interests', 'purchase_history'] 
                                   if col in available_features]
        
        # Perform segmentation
        segmentation_results = self.data_processor.perform_customer_segmentation(
            features=segmentation_features,
            n_clusters=n_segments
        )
        
        # Generate insights
        insights = self.data_processor.generate_insights()
        
        # Update campaign
        campaign['segments'] = segmentation_results
        campaign['insights'] = insights
        campaign['status'] = 'analyzed'
        campaign['history'].append(f"Audience analysis completed at {datetime.now().isoformat()}")
        
        logger.info(f"Completed audience analysis for campaign {campaign_id}")
        
        return {
            'segmentation': segmentation_results,
            'insights': insights
        }
    
    def generate_campaign_images(self, 
                                campaign_id: str,
                                images_per_segment: int = 2,
                                image_size: str = "1024x1024",
                                quality: str = "standard") -> Dict[str, Any]:
        """
        Generate personalized images for campaign segments
        
        Args:
            campaign_id: Campaign identifier
            images_per_segment: Number of images to generate per segment
            image_size: Size of generated images
            quality: Image quality setting
            
        Returns:
            Generation results
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        if campaign['segments'] is None:
            raise ValueError("No segments available. Please run audience analysis first.")
        
        # Generate personalized prompts
        prompts = self.image_generator.generate_personalized_prompts(
            campaign_data=campaign['config'],
            segment_data=campaign['segments']['segments']
        )
        
        # Generate multiple images per segment if requested
        all_prompts = []
        for prompt in prompts:
            for i in range(images_per_segment):
                variant_prompt = prompt + f" (Variation {i+1})"
                all_prompts.append(variant_prompt)
        
        # Generate images
        generation_results = self.image_generator.generate_batch(
            prompts=all_prompts,
            size=image_size,
            quality=quality,
            style=campaign['config'].get('style', 'vivid')
        )
        
        # Save images
        output_dir = f"generated_images/{campaign_id}"
        saved_files = self.image_generator.save_batch_results(
            results=generation_results,
            output_dir=output_dir,
            prefix=f"{campaign['config']['name']}_segment"
        )
        
        # Update campaign
        campaign['generated_images'] = generation_results
        campaign['saved_files'] = saved_files
        campaign['status'] = 'generated'
        campaign['history'].append(f"Images generated at {datetime.now().isoformat()}")
        
        logger.info(f"Generated {len(saved_files)} images for campaign {campaign_id}")
        
        return {
            'total_generated': len(generation_results),
            'successful_generations': sum(1 for r in generation_results if r['success']),
            'saved_files': saved_files,
            'generation_results': generation_results
        }
    
    def analyze_campaign_performance(self, 
                                   campaign_id: str,
                                   performance_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze campaign performance metrics
        
        Args:
            campaign_id: Campaign identifier
            performance_data: Optional performance data to analyze
            
        Returns:
            Performance analysis results
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        # Mock performance metrics if no real data provided
        if performance_data is None:
            performance_data = self._generate_mock_performance_data(campaign)
        
        # Calculate key metrics
        metrics = {
            'engagement_rate': performance_data.get('total_engagements', 0) / max(performance_data.get('total_impressions', 1), 1) * 100,
            'click_through_rate': performance_data.get('total_clicks', 0) / max(performance_data.get('total_impressions', 1), 1) * 100,
            'conversion_rate': performance_data.get('total_conversions', 0) / max(performance_data.get('total_clicks', 1), 1) * 100,
            'cost_per_acquisition': performance_data.get('total_spend', 0) / max(performance_data.get('total_conversions', 1), 1),
            'return_on_ad_spend': performance_data.get('total_revenue', 0) / max(performance_data.get('total_spend', 1), 1) * 100
        }
        
        # Segment performance analysis
        segment_performance = {}
        if 'segment_data' in performance_data:
            for segment_id, segment_perf in performance_data['segment_data'].items():
                segment_performance[segment_id] = {
                    'engagement_rate': segment_perf.get('engagements', 0) / max(segment_perf.get('impressions', 1), 1) * 100,
                    'conversion_rate': segment_perf.get('conversions', 0) / max(segment_perf.get('clicks', 1), 1) * 100,
                    'roi': segment_perf.get('revenue', 0) / max(segment_perf.get('spend', 1), 1) * 100
                }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, segment_performance)
        
        # Update campaign
        campaign['performance_metrics'] = {
            'overall_metrics': metrics,
            'segment_performance': segment_performance,
            'recommendations': recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
        campaign['status'] = 'analyzed'
        campaign['history'].append(f"Performance analysis completed at {datetime.now().isoformat()}")
        
        return campaign['performance_metrics']
    
    def _generate_mock_performance_data(self, campaign: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock performance data for demonstration"""
        import random
        
        total_impressions = random.randint(10000, 100000)
        total_clicks = random.randint(int(total_impressions * 0.01), int(total_impressions * 0.05))
        total_conversions = random.randint(int(total_clicks * 0.02), int(total_clicks * 0.08))
        total_spend = random.randint(500, 5000)
        total_revenue = random.randint(int(total_spend * 1.2), int(total_spend * 3.5))
        
        return {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_engagements': random.randint(total_clicks, int(total_clicks * 1.5)),
            'total_conversions': total_conversions,
            'total_spend': total_spend,
            'total_revenue': total_revenue
        }
    
    def _generate_recommendations(self, 
                                metrics: Dict[str, float],
                                segment_performance: Dict[str, Dict[str, float]]) -> List[str]:
        """Generate actionable recommendations based on performance metrics"""
        recommendations = []
        
        # Overall performance recommendations
        if metrics['engagement_rate'] < 2.0:
            recommendations.append("Low engagement rate detected. Consider refreshing creative content or adjusting targeting.")
        
        if metrics['click_through_rate'] < 1.0:
            recommendations.append("CTR is below industry average. Review ad copy and visual elements.")
        
        if metrics['conversion_rate'] < 2.0:
            recommendations.append("Low conversion rate. Optimize landing pages and review user journey.")
        
        if metrics['return_on_ad_spend'] < 300:
            recommendations.append("ROAS is below target. Consider budget reallocation or campaign optimization.")
        
        # Segment-specific recommendations
        if segment_performance:
            best_segment = max(segment_performance.keys(), 
                             key=lambda x: segment_performance[x]['roi'])
            worst_segment = min(segment_performance.keys(), 
                              key=lambda x: segment_performance[x]['roi'])
            
            recommendations.append(f"Segment {best_segment} shows highest ROI. Consider increasing budget allocation.")
            recommendations.append(f"Segment {worst_segment} underperforming. Review targeting and creative for this segment.")
        
        return recommendations
    
    def get_campaign_summary(self, campaign_id: str) -> Dict[str, Any]:
        """Get comprehensive campaign summary"""
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        summary = {
            'campaign_info': {
                'id': campaign['id'],
                'name': campaign['config']['name'],
                'status': campaign['status'],
                'created_at': campaign['created_at'],
                'product': campaign['config']['product']
            },
            'audience_analysis': campaign.get('insights', {}),
            'image_generation': {
                'total_images': len(campaign.get('generated_images', [])),
                'successful_generations': sum(1 for img in campaign.get('generated_images', []) if img.get('success', False))
            },
            'performance': campaign.get('performance_metrics', {}),
            'history': campaign['history']
        }
        
        return summary
    
    def export_campaign_data(self, 
                           campaign_id: str,
                           output_dir: str = "exports") -> Dict[str, str]:
        """
        Export campaign data to files
        
        Args:
            campaign_id: Campaign identifier
            output_dir: Output directory for exports
            
        Returns:
            Dictionary of exported file paths
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        os.makedirs(output_dir, exist_ok=True)
        
        campaign = self.campaigns[campaign_id]
        exported_files = {}
        
        # Export campaign summary
        summary_path = os.path.join(output_dir, f"{campaign_id}_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(self.get_campaign_summary(campaign_id), f, indent=2, default=str)
        exported_files['summary'] = summary_path
        
        # Export customer segments if available
        if campaign.get('segments'):
            segments_path = os.path.join(output_dir, f"{campaign_id}_segments.json")
            with open(segments_path, 'w') as f:
                json.dump(campaign['segments'], f, indent=2, default=str)
            exported_files['segments'] = segments_path
        
        # Export performance metrics if available
        if campaign.get('performance_metrics'):
            performance_path = os.path.join(output_dir, f"{campaign_id}_performance.json")
            with open(performance_path, 'w') as f:
                json.dump(campaign['performance_metrics'], f, indent=2, default=str)
            exported_files['performance'] = performance_path
        
        logger.info(f"Exported campaign data to {len(exported_files)} files")
        return exported_files
    
    def list_campaigns(self) -> List[Dict[str, Any]]:
        """List all campaigns with basic information"""
        campaign_list = []
        
        for campaign_id, campaign in self.campaigns.items():
            campaign_list.append({
                'id': campaign_id,
                'name': campaign['config']['name'],
                'status': campaign['status'],
                'created_at': campaign['created_at'],
                'product': campaign['config']['product'],
                'images_generated': len(campaign.get('generated_images', []))
            })
        
        return campaign_list
