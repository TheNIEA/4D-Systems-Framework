#!/bin/bash

echo "🚀 Starting Phase 4 AGI - True Autonomous Intelligence"
echo ""
echo "Built on 4D Systems Framework Principles:"
echo "  ✓ Sequence Determines Outcome"
echo "  ✓ Energy Efficiency = Understanding"
echo "  ✓ Goal-Directed Exploration"
echo "  ✓ Self-Correction Loops"
echo ""

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo ""
    echo "Get your API key from: https://console.anthropic.com/"
    echo "Then run:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo "  ./start_phase4_agi.sh"
    exit 1
fi

echo "✓ API key found"
echo ""

# Run with custom goal if provided
if [ -n "$1" ]; then
    echo "🎯 Custom Goal: $1"
    /usr/bin/python3 run_phase4_agi.py --goal "$1"
else
    echo "🎯 Running default goal sequence"
    /usr/bin/python3 run_phase4_agi.py
fi
