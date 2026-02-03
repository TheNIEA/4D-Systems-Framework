"""
TEST: AGI Phase 3 - Autonomous Capability Discovery
===================================================

This test demonstrates TRUE AGI capabilities:
1. Generic gap detection (no hardcoded keywords)
2. Autonomous capability synthesis
3. Meta-learning about capabilities
4. Self-directed exploration

GOAL: System discovers and synthesizes 100+ capabilities autonomously
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType
from datetime import datetime
import json


def test_agi_autonomous_discovery():
    """
    Test AGI's ability to discover capabilities without hardcoded triggers.
    """
    
    print("\n" + "="*80)
    print("🚀 PHASE 3: AGI AUTONOMOUS CAPABILITY DISCOVERY TEST")
    print("="*80)
    
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set. Cannot test AGI synthesis.")
        return
    
    # Create cube with AGI engine
    cube = MinimalSparkCube(api_key=api_key, enable_tools=True)
    
    print(f"\n📊 Initial State:")
    print(f"   Total Nodes: {len(cube.nodes)}")
    print(f"   AGI Engine: {'✓ Active' if cube.agi_engine else '✗ Disabled'}")
    print(f"   Capabilities: {len(cube.agi_engine.capability_registry) if cube.agi_engine else 0}")
    
    # Test 1: Generic Gap Detection (no keywords)
    print("\n" + "-"*80)
    print("TEST 1: Generic Gap Detection (No Hardcoded Keywords)")
    print("-"*80)
    
    test_signals = [
        # These should trigger gap detection WITHOUT relying on keywords
        "How can I transform structured data between different formats?",
        "I need to analyze sentiment in user feedback",
        "Help me optimize this complex calculation",
        "Can you extract entities from this text?",
        "I need to visualize relationships in my data"
    ]
    
    gaps_detected = 0
    capabilities_synthesized = 0
    
    for i, signal_text in enumerate(test_signals, 1):
        print(f"\n🔍 Test Signal {i}: {signal_text[:60]}...")
        
        signal = Signal(
            type=SignalType.TEXT,
            data=signal_text,
            timestamp=datetime.now()
        )
        
        # Use process_with_synthesis which includes the full flow
        result = cube.process_with_synthesis(signal)
        
        synthesis = result.get('synthesis', {})
        if synthesis.get('synthesis_attempted'):
            gaps_detected += 1
            print(f"   ✓ Capability gap detected!")
            print(f"   Type: {synthesis.get('capability_type')}")
            
            if synthesis.get('synthesis_successful'):
                capabilities_synthesized += 1
                print(f"   ✓ Capability synthesized successfully!")
            else:
                print(f"   ✗ Synthesis failed")
        else:
            print(f"   - No gap detected")
    
    print(f"\n📊 Test 1 Results:")
    print(f"   Gaps Detected: {gaps_detected}/{len(test_signals)}")
    print(f"   Capabilities Synthesized: {capabilities_synthesized}/{gaps_detected}")
    
    # Test 2: Meta-Learning (learns about capabilities)
    print("\n" + "-"*80)
    print("TEST 2: Meta-Learning - System Learns What Capabilities Exist")
    print("-"*80)
    
    if cube.agi_engine:
        patterns_learned = len(cube.agi_engine.gap_detector.capability_patterns)
        print(f"   Capability Patterns Learned: {patterns_learned}")
        
        if patterns_learned > 0:
            print(f"\n   Learned Patterns:")
            for pattern in cube.agi_engine.gap_detector.capability_patterns:
                print(f"   - {pattern.pattern_type}")
                print(f"     Abstraction Level: {pattern.abstraction_level}")
                print(f"     Success Rate: {pattern.success_rate:.0%}")
                print(f"     Indicators: {pattern.indicators[:5]}")
    
    # Test 3: Autonomous Exploration (self-generated signals)
    print("\n" + "-"*80)
    print("TEST 3: Autonomous Exploration - System Explores Without External Input")
    print("-"*80)
    
    autonomous_syntheses = 0
    exploration_rounds = 5
    
    print(f"   Running {exploration_rounds} autonomous exploration cycles...")
    
    for round in range(exploration_rounds):
        # Get current capabilities
        current_caps = list(cube.agi_engine.capability_registry.keys()) if cube.agi_engine else []
        
        # Generate autonomous exploration signal
        exploration_signal = cube.agi_engine.explorer.generate_exploration_signal(
            current_caps,
            []
        )
        
        if not exploration_signal:
            print(f"   Round {round+1}: No unexplored domains")
            break
        
        print(f"\n   Round {round+1}: Exploring '{exploration_signal['domain']}'")
        print(f"   Query: {exploration_signal['signal_data'][:60]}...")
        
        # Process the autonomous signal
        signal = Signal(
            type=SignalType.TEXT,
            data=exploration_signal['signal_data'],
            timestamp=datetime.now()
        )
        
        result = cube.process_with_synthesis(signal)
        
        if result.get('synthesis', {}).get('synthesis_successful'):
            autonomous_syntheses += 1
            print(f"   ✓ Autonomous synthesis successful!")
        else:
            print(f"   - No synthesis this round")
    
    print(f"\n📊 Test 3 Results:")
    print(f"   Autonomous Syntheses: {autonomous_syntheses}/{exploration_rounds}")
    
    # Test 4: Universal Code Synthesis (any capability type)
    print("\n" + "-"*80)
    print("TEST 4: Universal Code Synthesis - Not Limited to Specific Classes")
    print("-"*80)
    
    unique_capabilities = set()
    if cube.agi_engine:
        for cap_type in cube.agi_engine.capability_registry.keys():
            unique_capabilities.add(cap_type)
    
    print(f"   Unique Capability Types Synthesized: {len(unique_capabilities)}")
    
    if unique_capabilities:
        print(f"\n   Capabilities:")
        for cap in sorted(unique_capabilities):
            info = cube.agi_engine.capability_registry[cap]
            print(f"   - {cap}")
            print(f"     Gap Confidence: {info.get('gap_confidence', 0):.0%}")
            print(f"     Synthesized: {info.get('synthesized_at', 'unknown')[:19]}")
    
    # Final Summary
    print("\n" + "="*80)
    print("🏆 FINAL AGI ASSESSMENT")
    print("="*80)
    
    total_capabilities = len(cube.agi_engine.capability_registry) if cube.agi_engine else 0
    total_attempts = cube.agi_engine.total_synthesis_attempts if cube.agi_engine else 0
    success_rate = (cube.agi_engine.successful_syntheses / max(total_attempts, 1) * 100) if cube.agi_engine else 0
    
    print(f"\n📊 AGI Performance Metrics:")
    print(f"   Total Capabilities: {total_capabilities}")
    print(f"   Synthesis Attempts: {total_attempts}")
    print(f"   Success Rate: {success_rate:.0f}%")
    print(f"   Autonomous Discoveries: {autonomous_syntheses}")
    print(f"   Meta-Patterns Learned: {patterns_learned if cube.agi_engine else 0}")
    
    print(f"\n🎯 AGI Readiness Score:")
    
    # Calculate AGI readiness
    agi_score = 0
    
    # Criterion 1: Generic gap detection works (50 points)
    if gaps_detected >= 3:
        agi_score += 50
        print(f"   ✓ Generic Gap Detection: +50 points")
    
    # Criterion 2: Multiple capability types (20 points)
    if len(unique_capabilities) >= 3:
        agi_score += 20
        print(f"   ✓ Diverse Capabilities: +20 points")
    
    # Criterion 3: Meta-learning active (15 points)
    if patterns_learned > 0:
        agi_score += 15
        print(f"   ✓ Meta-Learning: +15 points")
    
    # Criterion 4: Autonomous exploration (15 points)
    if autonomous_syntheses > 0:
        agi_score += 15
        print(f"   ✓ Autonomous Exploration: +15 points")
    
    print(f"\n   TOTAL AGI SCORE: {agi_score}/100")
    
    if agi_score >= 80:
        assessment = "🏆 AGI-READY - True emergent intelligence demonstrated"
    elif agi_score >= 60:
        assessment = "⚡ AGI-CAPABLE - Strong foundation, needs refinement"
    elif agi_score >= 40:
        assessment = "🔨 AGI-EMERGING - Core capabilities present, needs expansion"
    else:
        assessment = "🌱 AGI-DEVELOPING - Early stage, continue building"
    
    print(f"\n   Assessment: {assessment}")
    
    # Save results
    results = {
        'test_date': datetime.now().isoformat(),
        'agi_score': agi_score,
        'assessment': assessment,
        'capabilities_synthesized': total_capabilities,
        'synthesis_success_rate': success_rate,
        'autonomous_discoveries': autonomous_syntheses,
        'meta_patterns_learned': patterns_learned if cube.agi_engine else 0,
        'unique_capability_types': list(unique_capabilities),
        'capability_registry': {
            cap: {
                'gap_confidence': info.get('gap_confidence', 0),
                'synthesized_at': info.get('synthesized_at', 'unknown')
            }
            for cap, info in cube.agi_engine.capability_registry.items()
        } if cube.agi_engine else {}
    }
    
    results_path = Path("data/agi_phase3_results.json")
    results_path.parent.mkdir(exist_ok=True)
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_path}")
    
    # Show path to 100+ capabilities goal
    print("\n" + "="*80)
    print("🚀 PATH TO 100+ CAPABILITIES")
    print("="*80)
    print(f"\n   Current: {total_capabilities} capabilities")
    print(f"   Target: 100+ capabilities")
    print(f"   Remaining: {max(100 - total_capabilities, 0)}")
    
    if total_capabilities < 100:
        print(f"\n   Recommendations:")
        print(f"   1. Run continuous autonomous exploration")
        print(f"   2. Expose system to diverse problem domains")
        print(f"   3. Let meta-learning refine gap detection")
        print(f"   4. Allow 24-48 hours of autonomous operation")
        print(f"   5. Monitor capability diversity (not just quantity)")
    else:
        print(f"\n   🎉 100+ CAPABILITY MILESTONE ACHIEVED!")
        print(f"   Ready for Phase 3 publication: 'True Emergent Intelligence'")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    test_agi_autonomous_discovery()
