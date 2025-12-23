#!/bin/bash

# CryptoTracker Quick Start Script
# This script sets up and runs CryptoTracker

echo "🛡️  CryptoTracker - Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys before running the application"
    echo "   You can get a free Etherscan API key at: https://etherscan.io/apis"
    echo ""
    read -p "Press Enter to continue after editing .env, or Ctrl+C to exit..."
fi

# Create necessary directories
mkdir -p data static templates

echo ""
echo "🚀 Starting CryptoTracker..."
echo "================================"
echo ""
echo "📍 Application will be available at: http://localhost:5000"
echo "📖 Documentation: README.md"
echo "🛑 Press Ctrl+C to stop the application"
echo ""

# Run the application
python app.py