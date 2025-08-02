"""
BrandGen - Automated Image Generator for Personalized Marketing Campaigns
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
from datetime import datetime
from PIL import Image
import io
import base64

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules
from src.data_processor import DataProcessor
from src.image_generator import ImageGenerator
from src.campaign_manager import CampaignManager
from src.utils import (
    validate_file_upload, format_currency, format_percentage, format_number,
    create_sample_data, generate_campaign_templates, calculate_campaign_roi,
    get_color_palette, log_user_action
)
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="BrandGen - AI Marketing Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.375rem;
        color: #155724;
    }
    .warning-message {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.375rem;
        color: #856404;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.375rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'campaign_manager' not in st.session_state:
    st.session_state.campaign_manager = None
if 'current_campaign_id' not in st.session_state:
    st.session_state.current_campaign_id = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []

def initialize_campaign_manager():
    """Initialize campaign manager with API key validation"""
    try:
        config = Config()
        if not config.OPENAI_API_KEY:
            st.error("⚠️ OpenAI API key not found. Please set your API key in the .env file.")
            st.info("Create a .env file in the project root and add: OPENAI_API_KEY=your_api_key_here")
            return False
        
        st.session_state.campaign_manager = CampaignManager()
        return True
    except Exception as e:
        st.error(f"Error initializing campaign manager: {str(e)}")
        return False

def main_dashboard():
    """Main dashboard page"""
    st.markdown("""
    <div class="main-header">
        <h1>🎨 BrandGen</h1>
        <h3>Automated Image Generator for Personalized Marketing Campaigns</h3>
        <p>Harness the power of AI to create stunning, personalized marketing visuals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats if campaigns exist
    if st.session_state.campaign_manager:
        campaigns = st.session_state.campaign_manager.list_campaigns()
        if campaigns:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Campaigns", len(campaigns))
            
            with col2:
                total_images = sum(c['images_generated'] for c in campaigns)
                st.metric("Images Generated", total_images)
            
            with col3:
                active_campaigns = sum(1 for c in campaigns if c['status'] in ['created', 'analyzed', 'generated'])
                st.metric("Active Campaigns", active_campaigns)
            
            with col4:
                completed_campaigns = sum(1 for c in campaigns if c['status'] == 'analyzed')
                st.metric("Completed", completed_campaigns)
    
    # Feature highlights
    st.markdown("---")
    st.header("🚀 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Data Analysis
        - Customer segmentation
        - Demographic insights
        - Behavioral analysis
        - Performance tracking
        """)
    
    with col2:
        st.markdown("""
        ### 🎨 AI Image Generation
        - OpenAI DALL-E integration
        - Personalized prompts
        - Multiple styles & moods
        - Batch processing
        """)
    
    with col3:
        st.markdown("""
        ### 📈 Campaign Management
        - End-to-end workflows
        - Performance analytics
        - ROI calculation
        - Export capabilities
        """)
    
    # Quick start guide
    st.markdown("---")
    st.header("🎯 Quick Start Guide")
    
    with st.expander("How to create your first campaign", expanded=True):
        st.markdown("""
        1. **📁 Upload Data**: Go to 'Data Upload' and upload your customer data (CSV/Excel)
        2. **🎯 Create Campaign**: Navigate to 'Campaign Creation' and set up your campaign
        3. **🔍 Analyze Audience**: Let AI segment your customers and generate insights
        4. **🎨 Generate Images**: Create personalized marketing visuals for each segment
        5. **📊 Track Performance**: Monitor campaign performance and optimize
        """)

def data_upload_page():
    """Data upload and validation page"""
    st.header("📁 Data Upload & Management")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Customer Data",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a CSV or Excel file containing customer data"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Validate file
            validation_result = validate_file_upload(temp_path)
            
            if validation_result['valid']:
                st.success("✅ File uploaded and validated successfully!")
                
                # Load and display data
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(temp_path)
                else:
                    df = pd.read_excel(temp_path)
                
                st.subheader("📋 Data Preview")
                st.dataframe(df.head(10))
                
                # Data summary
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Data Summary")
                    st.metric("Total Rows", len(df))
                    st.metric("Total Columns", len(df.columns))
                    st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                
                with col2:
                    st.subheader("🔍 Column Information")
                    column_info = pd.DataFrame({
                        'Column': df.columns,
                        'Type': df.dtypes,
                        'Non-Null': df.count(),
                        'Null %': ((len(df) - df.count()) / len(df) * 100).round(1)
                    })
                    st.dataframe(column_info)
                
                # Store data in session state
                st.session_state.customer_data = df
                st.session_state.data_file_path = temp_path
                
            else:
                st.error("❌ File validation failed:")
                for error in validation_result['errors']:
                    st.error(f"• {error}")
            
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Sample data option
    st.markdown("---")
    st.subheader("📝 Use Sample Data")
    st.info("Don't have customer data? Use our sample dataset to explore BrandGen features.")
    
    if st.button("Load Sample Data"):
        sample_df = create_sample_data()
        st.session_state.customer_data = sample_df
        st.success("✅ Sample data loaded successfully!")
        st.dataframe(sample_df.head(10))
    
    # Data insights
    if 'customer_data' in st.session_state:
        st.markdown("---")
        st.subheader("🔍 Data Insights")
        
        df = st.session_state.customer_data
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'age' in df.columns:
                fig_age = px.histogram(df, x='age', title='Age Distribution', 
                                     color_discrete_sequence=get_color_palette('modern'))
                st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            if 'gender' in df.columns:
                gender_counts = df['gender'].value_counts()
                fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                                  title='Gender Distribution', 
                                  color_discrete_sequence=get_color_palette('vibrant'))
                st.plotly_chart(fig_gender, use_container_width=True)

def campaign_creation_page():
    """Campaign creation and configuration page"""
    st.header("🎯 Campaign Creation")
    
    # Check if data is loaded
    if 'customer_data' not in st.session_state:
        st.warning("⚠️ Please upload customer data first before creating a campaign.")
        st.info("Go to 'Data Upload' page to upload your customer data or use sample data.")
        return
    
    # Initialize campaign manager
    if not st.session_state.campaign_manager:
        if not initialize_campaign_manager():
            return
    
    # Campaign templates
    st.subheader("📋 Campaign Templates")
    templates = generate_campaign_templates()
    
    template_names = ["Custom Campaign"] + list(templates.keys())
    selected_template = st.selectbox("Choose a template", template_names)
    
    # Campaign configuration
    st.subheader("⚙️ Campaign Configuration")
    
    with st.form("campaign_config"):
        col1, col2 = st.columns(2)
        
        with col1:
            if selected_template == "Custom Campaign":
                campaign_name = st.text_input("Campaign Name", "My Marketing Campaign")
                product = st.text_input("Product/Service", "Your product")
                target_audience = st.text_input("Target Audience", "Your target customers")
            else:
                template_data = templates[selected_template]
                campaign_name = st.text_input("Campaign Name", template_data['name'])
                product = st.text_input("Product/Service", template_data['product'])
                target_audience = st.text_input("Target Audience", template_data['target_audience'])
        
        with col2:
            style_options = ["modern", "vintage", "minimalist", "elegant", "dynamic", "futuristic", "artistic"]
            if selected_template != "Custom Campaign":
                default_style = templates[selected_template]['style']
                style = st.selectbox("Visual Style", style_options, 
                                   index=style_options.index(default_style) if default_style in style_options else 0)
            else:
                style = st.selectbox("Visual Style", style_options)
            
            mood_options = ["professional", "friendly", "energetic", "sophisticated", "playful", "inspiring", "confident"]
            if selected_template != "Custom Campaign":
                default_mood = templates[selected_template]['mood']
                mood = st.selectbox("Mood/Tone", mood_options,
                                  index=mood_options.index(default_mood) if default_mood in mood_options else 0)
            else:
                mood = st.selectbox("Mood/Tone", mood_options)
        
        # Additional elements
        st.subheader("🎨 Additional Elements")
        additional_elements = st.text_area(
            "Additional Elements (one per line)",
            "vibrant colors\nurban background\nmodern design" if selected_template == "Custom Campaign" 
            else "\n".join(templates.get(selected_template, {}).get('additional_elements', []))
        )
        
        # Campaign settings
        st.subheader("⚙️ Generation Settings")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            n_segments = st.slider("Number of Customer Segments", 2, 8, 4)
        
        with col2:
            images_per_segment = st.slider("Images per Segment", 1, 5, 2)
        
        with col3:
            image_size = st.selectbox("Image Size", ["1024x1024", "1792x1024", "1024x1792"])
        
        # Submit button
        submitted = st.form_submit_button("🚀 Create Campaign", type="primary")
        
        if submitted:
            # Prepare campaign configuration
            campaign_config = {
                'name': campaign_name,
                'product': product,
                'target_audience': target_audience,
                'style': style,
                'mood': mood,
                'additional_elements': [elem.strip() for elem in additional_elements.split('\n') if elem.strip()],
                'template': selected_template,
                'settings': {
                    'n_segments': n_segments,
                    'images_per_segment': images_per_segment,
                    'image_size': image_size
                }
            }
            
            try:
                # Create campaign
                campaign_id = st.session_state.campaign_manager.create_campaign(
                    campaign_config=campaign_config,
                    customer_data=st.session_state.customer_data
                )
                
                st.session_state.current_campaign_id = campaign_id
                st.success(f"✅ Campaign '{campaign_name}' created successfully!")
                st.info(f"Campaign ID: {campaign_id}")
                
                # Log user action
                log_user_action("campaign_created", {
                    'campaign_id': campaign_id,
                    'template': selected_template,
                    'segments': n_segments
                })
                
                # Auto-redirect to next step
                st.info("🔄 Proceeding to audience analysis...")
                
            except Exception as e:
                st.error(f"Error creating campaign: {str(e)}")

def audience_analysis_page():
    """Audience analysis and segmentation page"""
    st.header("🔍 Audience Analysis & Segmentation")
    
    if not st.session_state.campaign_manager:
        if not initialize_campaign_manager():
            return
    
    # Campaign selection
    campaigns = st.session_state.campaign_manager.list_campaigns()
    if not campaigns:
        st.warning("⚠️ No campaigns found. Please create a campaign first.")
        return
    
    # Select campaign
    campaign_options = {f"{c['name']} ({c['id']})": c['id'] for c in campaigns}
    selected_campaign = st.selectbox("Select Campaign", list(campaign_options.keys()))
    campaign_id = campaign_options[selected_campaign]
    
    # Get campaign details
    campaign_summary = st.session_state.campaign_manager.get_campaign_summary(campaign_id)
    
    # Display campaign info
    st.subheader("📋 Campaign Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Campaign Name", campaign_summary['campaign_info']['name'])
    with col2:
        st.metric("Product", campaign_summary['campaign_info']['product'])
    with col3:
        st.metric("Status", campaign_summary['campaign_info']['status'])
    
    # Segmentation controls
    st.subheader("🎯 Customer Segmentation")
    
    if 'customer_data' in st.session_state:
        df = st.session_state.customer_data
        available_features = df.columns.tolist()
        
        # Feature selection for segmentation
        default_features = [col for col in ['age', 'gender', 'location', 'interests', 'annual_income'] 
                          if col in available_features]
        
        selected_features = st.multiselect(
            "Select features for segmentation",
            available_features,
            default=default_features
        )
        
        n_segments = st.slider("Number of segments", 2, 8, 4)
        
        if st.button("🔍 Analyze Audience", type="primary"):
            if not selected_features:
                st.error("Please select at least one feature for segmentation.")
                return
            
            try:
                with st.spinner("Analyzing customer data and creating segments..."):
                    analysis_result = st.session_state.campaign_manager.analyze_target_audience(
                        campaign_id=campaign_id,
                        segmentation_features=selected_features,
                        n_segments=n_segments
                    )
                
                st.success("✅ Audience analysis completed!")
                
                # Display segmentation results
                st.subheader("📊 Segmentation Results")
                
                segments = analysis_result['segmentation']['segments']
                
                # Segment overview
                segment_data = []
                for segment_name, segment_info in segments.items():
                    segment_data.append({
                        'Segment': segment_name,
                        'Size': segment_info['size'],
                        'Percentage': f"{segment_info['percentage']:.1f}%"
                    })
                
                df_segments = pd.DataFrame(segment_data)
                st.dataframe(df_segments)
                
                # Segment visualization
                fig_segments = px.pie(
                    df_segments, 
                    values='Size', 
                    names='Segment',
                    title='Customer Segment Distribution',
                    color_discrete_sequence=get_color_palette('modern')
                )
                st.plotly_chart(fig_segments, use_container_width=True)
                
                # Detailed segment characteristics
                st.subheader("🔍 Segment Characteristics")
                
                for segment_name, segment_info in segments.items():
                    with st.expander(f"📈 {segment_name} Details"):
                        st.write(f"**Size:** {segment_info['size']} customers ({segment_info['percentage']:.1f}%)")
                        
                        characteristics = segment_info['characteristics']
                        for feature, stats in characteristics.items():
                            if isinstance(stats, dict):
                                if 'mean' in stats:
                                    st.write(f"**{feature}:** Average {stats['mean']:.1f}")
                                elif 'mode' in stats:
                                    st.write(f"**{feature}:** Most common '{stats['mode']}'")
                
                # Data insights
                if 'insights' in analysis_result:
                    st.subheader("💡 Key Insights")
                    insights = analysis_result['insights']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Total Customers", insights['total_customers'])
                        if 'age_distribution' in insights:
                            st.metric("Average Age", f"{insights['age_distribution']['mean_age']:.1f} years")
                    
                    with col2:
                        if 'gender_distribution' in insights:
                            gender_dist = insights['gender_distribution']
                            most_common_gender = max(gender_dist.keys(), key=lambda x: gender_dist[x])
                            st.metric("Primary Gender", most_common_gender)
                
                log_user_action("audience_analyzed", {
                    'campaign_id': campaign_id,
                    'features': selected_features,
                    'segments': n_segments
                })
                
            except Exception as e:
                st.error(f"Error during audience analysis: {str(e)}")

def image_generation_page():
    """AI image generation page"""
    st.header("🎨 AI Image Generation")
    
    if not st.session_state.campaign_manager:
        if not initialize_campaign_manager():
            return
    
    # Campaign selection
    campaigns = st.session_state.campaign_manager.list_campaigns()
    analyzed_campaigns = [c for c in campaigns if c['status'] in ['analyzed', 'generated']]
    
    if not analyzed_campaigns:
        st.warning("⚠️ No analyzed campaigns found. Please complete audience analysis first.")
        return
    
    # Select campaign
    campaign_options = {f"{c['name']} ({c['id']})": c['id'] for c in analyzed_campaigns}
    selected_campaign = st.selectbox("Select Campaign", list(campaign_options.keys()))
    campaign_id = campaign_options[selected_campaign]
    
    # Get campaign details
    campaign_summary = st.session_state.campaign_manager.get_campaign_summary(campaign_id)
    
    # Display campaign info
    st.subheader("📋 Campaign Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Campaign", campaign_summary['campaign_info']['name'])
    with col2:
        st.metric("Product", campaign_summary['campaign_info']['product'])
    with col3:
        segments_count = len(campaign_summary.get('audience_analysis', {}).get('segments', {}))
        st.metric("Segments", segments_count)
    
    # Generation settings
    st.subheader("⚙️ Generation Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        images_per_segment = st.slider("Images per Segment", 1, 5, 2)
    
    with col2:
        image_size = st.selectbox("Image Size", ["1024x1024", "1792x1024", "1024x1792"])
    
    with col3:
        quality = st.selectbox("Quality", ["standard", "hd"])
    
    # Generate images
    if st.button("🎨 Generate Images", type="primary"):
        try:
            with st.spinner("Generating personalized marketing images..."):
                generation_result = st.session_state.campaign_manager.generate_campaign_images(
                    campaign_id=campaign_id,
                    images_per_segment=images_per_segment,
                    image_size=image_size,
                    quality=quality
                )
            
            st.success(f"✅ Generated {generation_result['successful_generations']} images successfully!")
            
            # Display generation summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Generated", generation_result['total_generated'])
            with col2:
                st.metric("Successful", generation_result['successful_generations'])
            with col3:
                st.metric("Files Saved", len(generation_result['saved_files']))
            
            # Store results in session state
            st.session_state.generated_images = generation_result['generation_results']
            
            log_user_action("images_generated", {
                'campaign_id': campaign_id,
                'images_count': generation_result['successful_generations']
            })
            
        except Exception as e:
            st.error(f"Error generating images: {str(e)}")
    
    # Display generated images
    if st.session_state.generated_images:
        st.subheader("🖼️ Generated Images")
        
        # Image gallery
        cols = st.columns(3)
        for i, result in enumerate(st.session_state.generated_images):
            if result['success'] and 'image_data' in result:
                with cols[i % 3]:
                    try:
                        # Display image
                        image = Image.open(io.BytesIO(result['image_data']))
                        st.image(image, caption=f"Image {i+1}", use_column_width=True)
                        
                        # Show prompt
                        with st.expander(f"Prompt for Image {i+1}"):
                            st.text(result['prompt'])
                        
                        # Download button
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=result['image_data'],
                            file_name=f"generated_image_{i+1}.png",
                            mime="image/png"
                        )
                        
                    except Exception as e:
                        st.error(f"Error displaying image {i+1}: {str(e)}")

def performance_analytics_page():
    """Performance analytics and reporting page"""
    st.header("📊 Performance Analytics")
    
    if not st.session_state.campaign_manager:
        if not initialize_campaign_manager():
            return
    
    # Campaign selection
    campaigns = st.session_state.campaign_manager.list_campaigns()
    if not campaigns:
        st.warning("⚠️ No campaigns found.")
        return
    
    campaign_options = {f"{c['name']} ({c['id']})": c['id'] for c in campaigns}
    selected_campaign = st.selectbox("Select Campaign", list(campaign_options.keys()))
    campaign_id = campaign_options[selected_campaign]
    
    # Get campaign summary
    campaign_summary = st.session_state.campaign_manager.get_campaign_summary(campaign_id)
    
    # Performance analysis
    st.subheader("📈 Performance Analysis")
    
    if st.button("📊 Analyze Performance", type="primary"):
        try:
            with st.spinner("Analyzing campaign performance..."):
                performance_result = st.session_state.campaign_manager.analyze_campaign_performance(campaign_id)
            
            st.success("✅ Performance analysis completed!")
            
            # Overall metrics
            st.subheader("🎯 Overall Performance")
            
            metrics = performance_result['overall_metrics']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Engagement Rate",
                    format_percentage(metrics['engagement_rate']),
                    delta=f"{metrics['engagement_rate'] - 2.5:.1f}%" if metrics['engagement_rate'] > 2.5 else None
                )
            
            with col2:
                st.metric(
                    "Click-Through Rate",
                    format_percentage(metrics['click_through_rate']),
                    delta=f"{metrics['click_through_rate'] - 1.0:.1f}%" if metrics['click_through_rate'] > 1.0 else None
                )
            
            with col3:
                st.metric(
                    "Conversion Rate",
                    format_percentage(metrics['conversion_rate']),
                    delta=f"{metrics['conversion_rate'] - 2.0:.1f}%" if metrics['conversion_rate'] > 2.0 else None
                )
            
            with col4:
                st.metric(
                    "ROAS",
                    format_percentage(metrics['return_on_ad_spend'], 0),
                    delta=f"{metrics['return_on_ad_spend'] - 300:.0f}%" if metrics['return_on_ad_spend'] > 300 else None
                )
            
            # Performance visualization
            st.subheader("📊 Performance Visualization")
            
            # Create performance chart
            metric_names = ['Engagement Rate', 'CTR', 'Conversion Rate', 'ROAS (%)']
            metric_values = [
                metrics['engagement_rate'],
                metrics['click_through_rate'],
                metrics['conversion_rate'],
                metrics['return_on_ad_spend'] / 100  # Scale ROAS for better visualization
            ]
            
            fig_performance = go.Figure(data=[
                go.Bar(x=metric_names, y=metric_values, 
                      marker_color=get_color_palette('modern'))
            ])
            fig_performance.update_layout(
                title="Campaign Performance Metrics",
                xaxis_title="Metrics",
                yaxis_title="Values (%)"
            )
            st.plotly_chart(fig_performance, use_container_width=True)
            
            # Segment performance
            if 'segment_performance' in performance_result:
                st.subheader("🎯 Segment Performance")
                
                segment_perf = performance_result['segment_performance']
                if segment_perf:
                    segment_df = pd.DataFrame.from_dict(segment_perf, orient='index')
                    
                    # Segment performance chart
                    fig_segments = px.bar(
                        segment_df.reset_index(),
                        x='index',
                        y=['engagement_rate', 'conversion_rate'],
                        title='Performance by Segment',
                        barmode='group',
                        color_discrete_sequence=get_color_palette('vibrant')
                    )
                    fig_segments.update_xaxis_title("Segments")
                    fig_segments.update_yaxis_title("Rate (%)")
                    st.plotly_chart(fig_segments, use_container_width=True)
            
            # Recommendations
            if 'recommendations' in performance_result:
                st.subheader("💡 Recommendations")
                
                for i, recommendation in enumerate(performance_result['recommendations'], 1):
                    st.info(f"**{i}.** {recommendation}")
            
            log_user_action("performance_analyzed", {'campaign_id': campaign_id})
            
        except Exception as e:
            st.error(f"Error analyzing performance: {str(e)}")
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 Export Campaign Summary"):
            try:
                exported_files = st.session_state.campaign_manager.export_campaign_data(campaign_id)
                st.success(f"✅ Exported {len(exported_files)} files successfully!")
                for file_type, file_path in exported_files.items():
                    st.info(f"**{file_type.title()}**: {file_path}")
            except Exception as e:
                st.error(f"Error exporting data: {str(e)}")
    
    with col2:
        if st.button("📊 Export for Power BI"):
            st.info("🔄 Power BI export functionality coming soon!")
            # TODO: Implement Power BI export functionality

def main():
    """Main application function"""
    # Sidebar navigation
    st.sidebar.title("🎨 BrandGen Navigation")
    
    pages = {
        "🏠 Dashboard": main_dashboard,
        "📁 Data Upload": data_upload_page,
        "🎯 Campaign Creation": campaign_creation_page,
        "🔍 Audience Analysis": audience_analysis_page,
        "🎨 Image Generation": image_generation_page,
        "📊 Performance Analytics": performance_analytics_page
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    
    # API key status
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Configuration")
    
    config = Config()
    if config.OPENAI_API_KEY:
        st.sidebar.success("✅ OpenAI API Key Configured")
    else:
        st.sidebar.error("❌ OpenAI API Key Missing")
        st.sidebar.info("Add your API key to .env file")
    
    # Campaign status
    if st.session_state.campaign_manager:
        campaigns = st.session_state.campaign_manager.list_campaigns()
        st.sidebar.metric("Active Campaigns", len(campaigns))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**BrandGen v1.0.0**")
    st.sidebar.markdown("Powered by OpenAI DALL-E")
    
    # Run selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()
