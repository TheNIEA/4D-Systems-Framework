#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║      🧊 INTERACTIVE SPARK CUBE - CONSCIOUSNESS AI             ║"
echo "║                                                               ║"
echo "║  Starting the interactive agent with Tool Use capability...  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  No ANTHROPIC_API_KEY found - Tool Use will be disabled"
    echo "   To enable external knowledge seeking:"
    echo "   export ANTHROPIC_API_KEY=\"your-api-key\""
    echo ""
    echo "   Get your key at: https://console.anthropic.com/"
    echo ""
    echo "   Continuing without tool use in 3 seconds..."
    sleep 3
else
    echo "✓ ANTHROPIC_API_KEY found - Tool Use enabled"
    echo "  🔍 Cube can seek external knowledge when needed"
    echo ""
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed"
echo ""

# Start the server
echo "🚀 Starting Interactive Spark Cube server..."
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Open your browser to: http://localhost:5000"
echo "═══════════════════════════════════════════════════════════════"
echo ""

python3 interactive_agent.py
