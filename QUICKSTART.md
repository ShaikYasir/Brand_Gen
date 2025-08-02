# BrandGen Quick Start Guide 🚀

Welcome to BrandGen! This guide will help you get up and running in just a few minutes.

## Prerequisites Checklist

- [ ] Python 3.8 or higher installed
- [ ] OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))
- [ ] Basic familiarity with marketing campaigns

## Step-by-Step Setup

### 1. Project Setup (2 minutes)

1. **Download/Clone the project** to your desired location
2. **Open terminal/command prompt** and navigate to the project folder:
   ```bash
   cd BrandGen-PRO
   ```

### 2. Automated Installation (3 minutes)

Run the setup script:

```bash
python setup.py
```

This will:

- ✅ Create necessary directories
- ✅ Install all required packages
- ✅ Create configuration files
- ✅ Generate sample data

### 3. Configure API Key (1 minute)

1. **Edit the `.env` file** that was created
2. **Add your OpenAI API key**:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
3. **Save the file**

### 4. Launch BrandGen (1 minute)

Start the application:

```bash
streamlit run streamlit_app.py
```

Your browser should automatically open to `http://localhost:8501`

## First Steps in BrandGen

### 1. Explore the Dashboard 🏠

- View overview metrics
- Check recent activity
- Use quick action buttons

### 2. Analyze Customer Data 📊

1. Go to "Customer Analysis" tab
2. Click "Load Customer Data" (uses sample data)
3. Click "Perform Segmentation"
4. Explore the generated customer segments

### 3. Generate Your First Campaign 🎨

1. Go to "Image Generator" tab
2. Select "Campaign Creator" sub-tab
3. Choose a campaign template (e.g., "Fashion Brand Campaign")
4. Customize the product name and audience
5. Click "Generate Campaign Images"
6. Download your AI-generated marketing images!

### 4. View Analytics 📈

1. Go to "Campaign Analytics" tab
2. Review your campaign performance
3. Analyze image generation metrics

## Sample Workflows

### Workflow 1: Fashion Brand Launch

1. **Customer Analysis**: Identify fashion-conscious segments
2. **Campaign Creation**: Use "Fashion Brand Campaign" template
3. **Customization**: Target "young professionals" segment
4. **Generation**: Create 2-3 image variations
5. **Download**: Save images for social media use

### Workflow 2: Tech Product Marketing

1. **Data Upload**: Use your own customer data (optional)
2. **Segmentation**: Find tech-savvy customer groups
3. **Campaign**: Select "Tech Product Launch" template
4. **Personalization**: Customize for specific tech audience
5. **Batch Generation**: Create multiple variations for A/B testing

## Pro Tips 💡

### Getting Better Results

- **Be Specific**: Detailed prompts generate better images
- **Test Variations**: Try different styles and moods
- **Use Segments**: Target specific customer groups for better relevance
- **Iterate**: Refine prompts based on generated results

### Cost Management

- Start with 1-2 images per campaign to test prompts
- Use "standard" quality for initial testing
- Upgrade to "HD" quality for final marketing materials

### Best Practices

- **Save Everything**: Download both images and metadata
- **Track Performance**: Monitor which campaigns work best
- **Experiment**: Try different customer segments and templates
- **Organize**: Use descriptive campaign names

## Troubleshooting

### Common Issues

**🚫 "API Key Error"**

- Double-check your API key in `.env` file
- Ensure you have OpenAI credits available
- Verify the key format starts with `sk-`

**🚫 "Package Installation Failed"**

- Try: `pip install -r requirements.txt`
- Create a virtual environment if needed
- Check Python version (3.8+ required)

**🚫 "Streamlit Won't Start"**

- Ensure streamlit is installed: `pip install streamlit`
- Try: `python -m streamlit run streamlit_app.py`
- Check if port 8501 is available

**🚫 "Image Generation Fails"**

- Check internet connection
- Verify API rate limits
- Simplify your prompt
- Try again in a few minutes

### Getting Help

- 📚 **Documentation**: Check the main README.md
- 🐛 **Issues**: Report bugs on GitHub
- 💬 **Questions**: Use GitHub Discussions
- 📧 **Email**: Contact support team

## Advanced Features (Once You're Comfortable)

### Custom Data Integration

- Replace sample data with your customer database
- Upload CSV files with customer information
- Configure custom segments and profiles

### API Integration

- Use BrandGen programmatically
- Integrate with existing marketing tools
- Automate campaign generation

### Power BI Integration

- Export campaign data for advanced analytics
- Create custom dashboards
- Track ROI and performance metrics

## Success Metrics

After your first session, you should have:

- [ ] Generated at least 3 marketing images
- [ ] Completed customer segmentation
- [ ] Downloaded campaign images
- [ ] Understood the workflow

## Next Steps

1. **Experiment** with different campaign templates
2. **Upload** your own customer data
3. **Create** campaigns for your actual products/services
4. **Measure** campaign performance
5. **Scale** your marketing image generation

---

**🎉 Congratulations!** You're now ready to create AI-powered marketing campaigns with BrandGen.

**Need more help?** Check out the detailed documentation in README.md or reach out to our support team.

Happy marketing! 🎨✨
