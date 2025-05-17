#!/bin/bash

echo "❤️ Starting your GF Telegram Bot..."
echo "Creating virtual environment..."

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "🚀 Running the bot..."
python3 bot.py
