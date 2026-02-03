#!/bin/bash
# Run the Interactive Spark Cube with API key

# Set your Anthropic API key
# export ANTHROPIC_API_KEY="your-api-key-here"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo "   Set it with: export ANTHROPIC_API_KEY='your-api-key-here'"
    exit 1
fi

# Run the interactive agent
cd "/Users/khouryhowell/4D Systems"
/usr/bin/python3 interactive_agent.py
