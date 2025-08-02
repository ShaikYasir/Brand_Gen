# BrandGen - Automated Image Generator for Personalized Marketing Campaigns

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-DALL--E-green)](https://openai.com/dall-e-2/)
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/651fb79c-cd0d-4b55-a989-cc313ab51ba7" />

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

\
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🚀 Future Enhancements

- [ ] Integration with social media platforms
- [ ] Advanced A/B testing capabilities
- [ ] Machine learning-based optimization
- [ ] Multi-language support
- [ ] Power BI integration for advanced analytics
- [ ] Real-time campaign monitoring

-

