"""
BrandGen API Usage Examples
This file demonstrates how to use BrandGen programmatically
"""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import BrandGen modules
from src.data_analysis import DataAnalyzer
from src.config import Config

def example_customer_analysis():
    """Example: Analyze customer data and create segments."""
    print("🔍 Customer Analysis Example")
    print("-" * 40)
    
    # Initialize analyzer
    analyzer = DataAnalyzer()
    
    # Generate sample data
    print("📊 Generating sample customer data...")
    customer_data = analyzer.generate_sample_customer_data(500)
    print(f"✅ Generated data for {len(customer_data)} customers")
    
    # Perform segmentation
    print("🎯 Performing customer segmentation...")
    segments = analyzer.perform_customer_segmentation(n_clusters=4)
    print(f"✅ Created {len(segments['profiles'])} customer segments")
    
    # Display segment insights
    print("\n📈 Segment Insights:")
    for segment_id, profile in segments['profiles'].items():
        print(f"  Segment {segment_id}: {profile['name']}")
        print(f"    Size: {profile['size']} customers")
        print(f"    Avg Age: {profile['avg_age']:.1f}")
        print(f"    Avg Income: ${profile['avg_income']:,.0f}")
        print(f"    Digital Savvy: {profile['digital_savvy_score']:.1f}/10")
        
        # Get recommendations
        recommendations = analyzer.get_segment_recommendations(segment_id)
        print(f"    Recommended Channels: {', '.join(recommendations['preferred_channels'][:3])}")
        print(f"    Messaging Tone: {recommendations['messaging_tone']}")
        print()
    
    return segments

def example_campaign_template():
    """Example: Work with campaign templates."""
    print("🎨 Campaign Template Example")
    print("-" * 40)
    
    # Load campaign templates
    config = Config()
    
    # Example campaign data
    campaign_data = {
        "name": "Summer Fashion Collection",
        "description": "Bright and vibrant summer fashion campaign",
        "product": "Summer fashion collection",
        "style": "bright and airy",
        "mood": "energetic and fun",
        "target_audience": "young fashion enthusiasts aged 18-35",
        "additional_elements": ["beach setting", "natural lighting", "vibrant colors"],
        "industry": "Fashion",
        "budget_range": "medium"
    }
    
    print("📋 Campaign Configuration:")
    for key, value in campaign_data.items():
        print(f"  {key.title()}: {value}")
    
    return campaign_data

def example_prompt_engineering():
    """Example: Generate optimized prompts for image generation."""
    print("✍️ Prompt Engineering Example")
    print("-" * 40)
    
    # Campaign data
    campaign = {
        "product": "Premium skincare line",
        "target_audience": "health-conscious women aged 25-45",
        "style": "clean and minimalist",
        "mood": "serene and confident",
        "additional_elements": ["natural ingredients", "soft lighting", "spa-like atmosphere"]
    }
    
    # Generate prompt
    base_prompt = f"""
    Create a high-quality, professional marketing image for {campaign['product']} 
    targeting {campaign['target_audience']}.
    
    Style: {campaign['style']}
    Mood: {campaign['mood']}
    Include: {', '.join(campaign['additional_elements'])}
    
    The image should be visually striking, suitable for digital marketing,
    and convey premium quality and trustworthiness.
    """
    
    print("🎯 Generated Marketing Prompt:")
    print(base_prompt.strip())
    
    # Prompt variations for A/B testing
    variations = [
        f"{base_prompt} - Focus on product packaging and premium materials",
        f"{base_prompt} - Emphasize natural ingredients and organic feel", 
        f"{base_prompt} - Show lifestyle application with elegant model"
    ]
    
    print("\n🔄 A/B Testing Variations:")
    for i, variation in enumerate(variations, 1):
        print(f"  Variation {i}: {variation.split(' - ')[1]}")
    
    return base_prompt, variations

def example_roi_calculation():
    """Example: Calculate campaign ROI metrics."""
    print("💰 ROI Calculation Example")
    print("-" * 40)
    
    # Sample campaign results
    campaign_results = {
        "images_generated": 4,
        "cost_per_image": 0.02,  # DALL-E pricing
        "estimated_impressions": 50000,
        "click_through_rate": 0.025,  # 2.5%
        "conversion_rate": 0.05,      # 5%
        "revenue_per_conversion": 75   # $75 AOV
    }
    
    # Calculate metrics
    total_cost = campaign_results["images_generated"] * campaign_results["cost_per_image"]
    total_clicks = campaign_results["estimated_impressions"] * campaign_results["click_through_rate"]
    total_conversions = total_clicks * campaign_results["conversion_rate"]
    total_revenue = total_conversions * campaign_results["revenue_per_conversion"]
    roi_percentage = ((total_revenue - total_cost) / total_cost) * 100
    
    print("📊 Campaign Performance:")
    print(f"  Images Generated: {campaign_results['images_generated']}")
    print(f"  Total Cost: ${total_cost:.2f}")
    print(f"  Estimated Impressions: {campaign_results['estimated_impressions']:,}")
    print(f"  Estimated Clicks: {total_clicks:,.0f}")
    print(f"  Estimated Conversions: {total_conversions:.0f}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  ROI: {roi_percentage:.0f}%")
    print(f"  Cost per Conversion: ${total_cost/max(total_conversions, 1):.2f}")
    
    return {
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "roi_percentage": roi_percentage,
        "conversions": total_conversions
    }

def example_batch_workflow():
    """Example: Complete workflow for batch campaign generation."""
    print("🔄 Batch Workflow Example")
    print("-" * 40)
    
    # Step 1: Analyze customers
    print("Step 1: Customer Analysis")
    analyzer = DataAnalyzer()
    segments = analyzer.perform_customer_segmentation(n_clusters=3)
    print(f"✅ Created {len(segments['profiles'])} segments")
    
    # Step 2: Create targeted campaigns for each segment
    print("\nStep 2: Segment-Specific Campaigns")
    campaigns = []
    
    for segment_id, profile in segments['profiles'].items():
        # Customize campaign based on segment
        campaign = {
            "name": f"Campaign for {profile['name']}",
            "target_segment": segment_id,
            "product": "Premium lifestyle product",
            "target_audience": profile['name'].lower(),
            "estimated_audience_size": profile['size']
        }
        
        # Adjust style based on segment characteristics
        if profile['digital_savvy_score'] > 7:
            campaign["style"] = "modern and tech-forward"
            campaign["channels"] = ["Social Media", "Digital Ads"]
        elif profile['avg_income'] > 60000:
            campaign["style"] = "luxury and sophisticated"
            campaign["channels"] = ["Premium Publications", "Email"]
        else:
            campaign["style"] = "friendly and approachable"
            campaign["channels"] = ["Traditional Media", "Local Ads"]
        
        campaigns.append(campaign)
        print(f"  📋 {campaign['name']}")
        print(f"     Style: {campaign['style']}")
        print(f"     Channels: {', '.join(campaign['channels'])}")
        print(f"     Audience Size: {campaign['estimated_audience_size']}")
    
    # Step 3: Estimate batch generation costs
    print("\nStep 3: Cost Estimation")
    images_per_campaign = 3
    total_images = len(campaigns) * images_per_campaign
    total_cost = total_images * 0.02  # DALL-E pricing
    
    print(f"  Campaigns: {len(campaigns)}")
    print(f"  Images per Campaign: {images_per_campaign}")
    print(f"  Total Images: {total_images}")
    print(f"  Estimated Cost: ${total_cost:.2f}")
    
    return campaigns

def main():
    """Run all examples."""
    print("🎨 BrandGen API Examples")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Customer Analysis
        segments = example_customer_analysis()
        print()
        
        # Campaign Templates
        campaign = example_campaign_template()
        print()
        
        # Prompt Engineering
        prompt, variations = example_prompt_engineering()
        print()
        
        # ROI Calculation
        roi_data = example_roi_calculation()
        print()
        
        # Batch Workflow
        batch_campaigns = example_batch_workflow()
        print()
        
        print("✅ All examples completed successfully!")
        print("\n💡 Next Steps:")
        print("  1. Configure your OpenAI API key in .env")
        print("  2. Run: streamlit run streamlit_app.py")
        print("  3. Generate actual images using the web interface")
        print("  4. Integrate these examples into your own workflow")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Ensure all dependencies are installed")
        print("  2. Check that src modules are accessible")
        print("  3. Verify Python path configuration")

if __name__ == "__main__":
    main()
