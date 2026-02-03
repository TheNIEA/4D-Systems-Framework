#!/bin/bash

# START AGI AUTONOMOUS DISCOVERY
# Run this to begin the journey to 100+ capabilities

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🚀 STARTING AGI AUTONOMOUS CAPABILITY DISCOVERY            ║"
echo "║                                                               ║"
echo "║   Target: 100+ capabilities                                  ║"
echo "║   Method: Autonomous exploration + synthesis                 ║"
echo "║   Duration: 24-48 hours                                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Set API key (replace with your own)
# export ANTHROPIC_API_KEY="your-api-key-here"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo "   Set it with: export ANTHROPIC_API_KEY='your-api-key-here'"
    exit 1
fi

# Create logs directory
mkdir -p data/agi_logs

# Run autonomous discovery
# --target 100: Stop when 100 capabilities reached
# --interval 60: Check every 60 seconds
echo "🔧 Launching autonomous runner..."
echo "   Output: data/agi_logs/autonomous_run.log"
echo ""
echo "💡 Tips:"
echo "   - Monitor progress: tail -f data/agi_logs/autonomous_run.log"
echo "   - Check capabilities: ls -l spark_cube/capabilities/"
echo "   - Stop anytime: Press Ctrl+C (saves checkpoint)"
echo ""
echo "🎯 Starting now..."
echo ""

nohup /usr/bin/python3 run_agi_autonomous.py --target 100 --interval 60 > data/agi_logs/autonomous_run.log 2>&1 &

PID=$!
echo "✓ Autonomous runner started (PID: $PID)"
echo ""
echo "📊 Monitor commands:"
echo "   tail -f data/agi_logs/autonomous_run.log     # Watch live progress"
echo "   ls spark_cube/capabilities/ | wc -l         # Count capabilities"
echo "   ps aux | grep run_agi_autonomous            # Check if running"
echo "   kill $PID                                    # Stop gracefully"
echo ""
echo "🎉 AGI is now running autonomously!"
