#!/bin/bash

# Web Scraper Application Runner Script

set -e  # Exit on error

echo "Starting Web Scraper setup..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e .

# Install Playwright browsers
echo "Installing Playwright browsers..."
python -m playwright install chromium

# Start the application
echo "Starting server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload