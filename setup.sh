#!/bin/bash
# Setup script for Facebook Marketplace Scraper

set -e

echo "========================================"
echo "Facebook Marketplace Scraper - Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 not found. Please install Python 3.8+"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your credentials:"
    echo "   - FACEBOOK_EMAIL"
    echo "   - FACEBOOK_PASSWORD"
    echo "   - GOOGLE_API_KEY"
    echo ""
else
    echo ""
    echo "✓ .env file already exists"
fi

# Run tests
echo ""
echo "Running setup tests..."
python test_setup.py

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: source venv/bin/activate (or . venv/Scripts/activate on Windows)"
echo "3. Run: python marketplace_scraper.py"
echo ""
