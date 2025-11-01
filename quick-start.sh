#!/bin/bash
# Quick start script for RAG Showroom

echo "🚀 RAG Showroom Quick Start"
echo "=============================="
echo

# Check Python
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python not found. Please install Python 3.11+"
        exit 1
    fi
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "✓ Python found: $($PYTHON_CMD --version)"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 20+"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"
echo

# Install Python dependencies
echo "📦 Installing Python dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Node dependencies
echo "📦 Installing Node dependencies..."
npm install --silent

if [ $? -eq 0 ]; then
    echo "✓ Node dependencies installed"
else
    echo "❌ Failed to install Node dependencies"
    exit 1
fi

echo

# Test the demo
echo "🎨 Running semantic-chunking demo..."
echo
cd demos/semantic-chunking
$PYTHON_CMD demo.py

if [ $? -eq 0 ]; then
    echo
    echo "✅ Setup complete! The demo works!"
    echo
    echo "Next steps:"
    echo "1. Read SETUP.md for full configuration"
    echo "2. Add your API keys to .env file"
    echo "3. Run: python scripts/generate_demo.py"
else
    echo "❌ Demo failed to run"
    exit 1
fi
