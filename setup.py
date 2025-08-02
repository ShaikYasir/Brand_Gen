"""
BrandGen Setup Script
Run this script to set up your BrandGen environment
"""

import os
import shutil
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories for BrandGen."""
    directories = [
        'data',
        'generated_images',
        'src',
        'config',
        'docs',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file from template."""
    template_path = '.env.template'
    env_path = '.env'
    
    if os.path.exists(template_path) and not os.path.exists(env_path):
        shutil.copy(template_path, env_path)
        print(f"✅ Created {env_path} from template")
        print("📝 Please edit .env file and add your OpenAI API key")
    elif os.path.exists(env_path):
        print(f"ℹ️  {env_path} already exists")
    else:
        print(f"⚠️  Template file {template_path} not found")

def install_requirements():
    """Install required packages."""
    requirements_file = 'requirements.txt'
    
    if os.path.exists(requirements_file):
        print("📦 Installing required packages...")
        os.system(f"{sys.executable} -m pip install -r {requirements_file}")
        print("✅ Requirements installed")
    else:
        print("⚠️  requirements.txt not found")

def create_sample_data():
    """Create sample data files."""
    # Sample customer data
    sample_csv_content = """customer_id,age,income,spending_score,purchase_frequency,preferred_category,engagement_rate,digital_savvy,brand_loyalty
1,25,45000,67,3,Fashion,0.75,8,0.6
2,34,67000,82,5,Technology,0.85,9,0.8
3,45,89000,45,2,Automotive,0.45,5,0.7
4,28,52000,73,4,Beauty,0.82,7,0.65
5,52,95000,38,1,Luxury,0.35,4,0.9
"""
    
    data_dir = Path('data')
    customer_file = data_dir / 'customer_segments.csv'
    
    if not customer_file.exists():
        with open(customer_file, 'w') as f:
            f.write(sample_csv_content)
        print("✅ Created sample customer data")

def main():
    """Main setup function."""
    print("🎨 BrandGen Setup")
    print("=" * 50)
    
    try:
        create_directories()
        create_env_file()
        create_sample_data()
        install_requirements()
        
        print("\n" + "=" * 50)
        print("✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file and add your OpenAI API key")
        print("2. Run: streamlit run streamlit_app.py")
        print("3. Open your browser to the provided URL")
        print("\n💡 Need help? Check the README.md file")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
