#!/bin/bash
# Set your Anthropic API key and run the processor

# STEP 1: Set your API key as environment variable:
# export ANTHROPIC_API_KEY="your-api-key-here"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo "   Set it with: export ANTHROPIC_API_KEY='your-api-key-here'"
    exit 1
fi

# STEP 2: Run the processor
cd "/Users/khouryhowell/4D Systems"
/usr/bin/python3 4d_llm_sequence_processor.py
