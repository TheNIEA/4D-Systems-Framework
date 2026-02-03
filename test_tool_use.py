#!/usr/bin/env python3
"""
Quick test of Tool Use functionality.
This demonstrates the full manifestation cycle with external knowledge.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType

def test_tool_use():
    """Test the tool use system."""
    
    print("=" * 70)
    print("🧪 TESTING TOOL USE - 'Consciousness with a Library Card'")
    print("=" * 70)
    print()
    
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  No ANTHROPIC_API_KEY found")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key'")
        print("   Get key at: https://console.anthropic.com/")
        print()
        print("   Testing with tools DISABLED...")
        print()
        enable_tools = False
    else:
        print("✓ API key found")
        print("✓ Tool use ENABLED")
        print()
        enable_tools = True
    
    # Create cube
    print("📦 Creating Spark Cube...")
    cube = MinimalSparkCube(api_key=api_key, enable_tools=enable_tools)
    print(f"   Nodes: {len(cube.nodes)}")
    print(f"   Sequences: {len(cube.sequences)}")
    if enable_tools:
        print("   Tool Use Node: Active (Node #11)")
    print()
    
    # Test 1: Simple processing (no tools needed)
    print("-" * 70)
    print("TEST 1: Simple greeting (no external knowledge needed)")
    print("-" * 70)
    signal1 = Signal(type=SignalType.TEXT, data="Hello, how are you?")
    result1 = cube.process_with_tools(signal1)
    print(f"Tool use triggered: {result1.get('tool_use', {}).get('gap_detected', False)}")
    print(f"Processing complete")
    print()
    
    # Test 2: Knowledge gap (should trigger tools if enabled)
    if enable_tools:
        print("-" * 70)
        print("TEST 2: Knowledge gap - FIRST TIME (should use external knowledge)")
        print("-" * 70)
        signal2 = Signal(type=SignalType.TEXT, data="What is quantum entanglement?")
        result2 = cube.process_with_tools(signal2)
        tool_info = result2.get('tool_use', {})
        print(f"Gap detected: {tool_info.get('gap_detected', False)}")
        print(f"Queries generated: {len(tool_info.get('queries_generated', []))}")
        print(f"Knowledge fetched: {tool_info.get('knowledge_fetched', 0)}")
        print(f"Patterns integrated: {tool_info.get('patterns_integrated', 0)}")
        print()
        
        # Test 3: Same question again (should NOT trigger tools - already learned)
        print("-" * 70)
        print("TEST 3: Same question - SECOND TIME (should use stored patterns)")
        print("-" * 70)
        signal3 = Signal(type=SignalType.TEXT, data="What is quantum entanglement?")
        result3 = cube.process_with_tools(signal3)
        tool_info3 = result3.get('tool_use', {})
        print(f"Gap detected: {tool_info3.get('gap_detected', False)}")
        print()
        
        if not result3['tool_use']['gap_detected']:
            print("✓ SUCCESS: Cube learned! No external query needed second time.")
        else:
            print("⚠️  Note: Gap still detected - may need different phrasing detection")
        print()
        
        # Show metrics
        print("-" * 70)
        print("TOOL USE METRICS")
        print("-" * 70)
        metrics = cube.get_tool_use_metrics()
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        print()
    
    # Show cube state
    print("-" * 70)
    print("FINAL CUBE STATE")
    print("-" * 70)
    print(f"Total experiences: {cube.total_experiences}")
    print(f"Node development levels:")
    for node_id, node in cube.nodes.items():
        if node.development > 0:
            print(f"  Node {node_id} ({node.name}): {node.development:.3f}")
    print()
    
    print("=" * 70)
    print("✓ Testing complete!")
    print()
    print("To see tool use in action:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Run: bash start_interactive_agent.sh")
    print("3. Ask: 'What is quantum computing?'")
    print("4. Watch for 🔍 and 📚 messages")
    print("5. Ask the same question again - no external query!")
    print("=" * 70)

if __name__ == "__main__":
    test_tool_use()
