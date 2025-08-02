# BrandGen - Automated Image Generator for Personalized Marketing Campaigns

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E-green)](https://openai.com/dall-e-2/)

## 🚀 Project Overview

BrandGen is an intelligent automated image generator designed for creating personalized marketing campaigns. It combines the power of data analysis, AI image generation, and interactive dashboards to streamline your marketing content creation process.

## ✨ Features

- **Data-Driven Insights**: Analyze customer data and campaign performance with Pandas
- **AI Image Generation**: Create stunning visuals using OpenAI's DALL-E API
- **Interactive Dashboard**: User-friendly Streamlit interface for campaign management
- **Personalization Engine**: Generate targeted content based on customer segments
- **Performance Analytics**: Track and visualize campaign effectiveness
- **Batch Processing**: Generate multiple images for different customer segments

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **AI Integration**: OpenAI DALL-E API
- **Web Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Image Processing**: Pillow (PIL)
- **Configuration**: python-dotenv

## 📁 Project Structure

```
BrandGen-PRO/
├── src/
│   ├── __init__.py
│   ├── data_processor.py      # Data analysis and customer segmentation
│   ├── image_generator.py     # DALL-E API integration
│   ├── campaign_manager.py    # Campaign creation and management
│   └── utils.py              # Utility functions
├── data/
│   ├── sample_customers.csv   # Sample customer data
│   └── campaign_templates.json # Pre-defined campaign templates
├── generated_images/          # Output directory for AI-generated images
├── config/
│   └── settings.py           # Configuration settings
├── streamlit_app.py          # Main Streamlit dashboard
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd BrandGen-PRO

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application

```bash
# Start the Streamlit dashboard
streamlit run streamlit_app.py
```

## 💡 Usage

1. **Upload Customer Data**: Import your customer data (CSV format)
2. **Define Campaign Parameters**: Set campaign goals, target audience, and visual preferences
3. **Generate Images**: Use AI to create personalized marketing visuals
4. **Analyze Performance**: Track campaign metrics and optimize for better results
5. **Export Results**: Download generated images and campaign reports

## 🔧 Configuration

### API Keys

- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
- Add your API key to the `.env` file

### Custom Settings

Modify `config/settings.py` to customize:

- Image generation parameters
- Campaign templates
- Data processing options

## 📊 Data Format

### Customer Data CSV Format

```csv
customer_id,name,age,gender,location,interests,purchase_history
1,John Doe,25,Male,New York,Technology,Electronics
2,Jane Smith,34,Female,California,Fashion,Clothing
```

### Campaign Templates

Pre-defined templates in `data/campaign_templates.json` for different industries and campaign types.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the documentation
2. Open an issue on GitHub
3. Contact the development team

## 🚀 Future Enhancements

- [ ] Integration with social media platforms
- [ ] Advanced A/B testing capabilities
- [ ] Machine learning-based optimization
- [ ] Multi-language support
- [ ] Power BI integration for advanced analytics
- [ ] Real-time campaign monitoring

---

**Happy Marketing! 🎯**
