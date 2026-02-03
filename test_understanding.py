#!/usr/bin/env python3
"""
Test: Does the system truly UNDERSTAND or just pattern-match?

Per 4D Framework: "Energy Efficiency Becomes Proof of Understanding"
- Lower computational cost = true understanding
- High computational cost = brute-forcing without comprehension

This test:
1. Processes same signal multiple times
2. Measures energy cost (processing time)
3. Expects: First iteration slow (learning), subsequent iterations fast (using learned structure)
4. Asks system to explain WHY it's faster (tests metacognition)
"""

import os
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType
import time

def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        return
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║      TESTING UNDERSTANDING VIA ENERGY EFFICIENCY          ║")
    print("║                                                           ║")
    print("║  Hypothesis: True understanding = faster subsequent      ║")
    print("║             processing of similar inputs                 ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    # Create cube
    cube = MinimalSparkCube(api_key=api_key, enable_tools=True)
    
    # Test 1: Greetings (should synthesize language capability)
    print("\n" + "="*70)
    print("TEST 1: GREETING INTERACTION")
    print("="*70)
    
    greeting_signal = Signal(type=SignalType.TEXT, data="Hi")
    
    print("\nIteration 1 (Learning phase - should be slow):")
    start_1 = time.time()
    result_1 = cube.process_with_synthesis(greeting_signal)
    time_1 = time.time() - start_1
    print(f"⏱  Processing time: {time_1:.3f}s")
    print(f"Response: {result_1.get('synthesized_response', result_1.get('response', 'No response'))}")
    
    # Wait a moment
    time.sleep(1)
    
    print("\nIteration 2 (Should use cached capability - fast):")
    greeting_signal_2 = Signal(type=SignalType.TEXT, data="Hello")
    start_2 = time.time()
    result_2 = cube.process_with_synthesis(greeting_signal_2)
    time_2 = time.time() - start_2
    print(f"⏱  Processing time: {time_2:.3f}s")
    print(f"Response: {result_2.get('synthesized_response', result_2.get('response', 'No response'))}")
    
    improvement_1 = ((time_1 - time_2) / time_1 * 100) if time_1 > 0 else 0
    print(f"\n📊 Speed improvement: {improvement_1:.1f}%")
    
    if improvement_1 > 20:
        print("✓ EVIDENCE OF UNDERSTANDING: Significantly faster on second iteration")
    else:
        print("⚠ LIMITED EVIDENCE: Speed improvement not significant")
    
    # Test 2: More greetings to build pattern
    print("\n" + "="*70)
    print("TEST 2: PATTERN REINFORCEMENT (10 more interactions)")
    print("="*70)
    
    greetings = ["Hey", "Good morning", "Howdy", "Greetings", "Hi there",
                "Hello again", "Hey there", "Good day", "Yo", "Sup"]
    
    times = []
    for i, greeting in enumerate(greetings, 3):
        sig = Signal(type=SignalType.TEXT, data=greeting)
        start = time.time()
        result = cube.process_with_synthesis(sig)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Iteration {i}: {elapsed:.3f}s - '{greeting}'")
    
    avg_time = sum(times) / len(times) if times else 0
    print(f"\n📊 Average time for iterations 3-12: {avg_time:.3f}s")
    print(f"📊 Speedup from first iteration: {((time_1 - avg_time) / time_1 * 100):.1f}%")
    
    # Test 3: Ask system to explain WHY it's faster
    print("\n" + "="*70)
    print("TEST 3: METACOGNITIVE SELF-EXPLANATION")
    print("="*70)
    
    print("\n🤔 Asking system: 'Why did you synthesize the language capability?'\n")
    if cube.nodes[12].capability_registry:
        explanation = cube.explain_why_synthesized('language_generation', greeting_signal)
        print(explanation)
    else:
        print("No capabilities synthesized yet")
    
    # Test 4: Quantify understanding through energy metrics
    print("\n" + "="*70)
    print("TEST 4: UNDERSTANDING SCORE (Energy Efficiency Method)")
    print("="*70)
    
    print("\n📊 Analyzing computational efficiency trends...\n")
    understanding_analysis = cube.analyze_understanding()
    print(understanding_analysis)
    
    # Test 5: System state report
    print("\n" + "="*70)
    print("TEST 5: SYSTEM SELF-AWARENESS")
    print("="*70)
    
    print("\n🧠 System's self-report of current state:\n")
    state_report = cube.explain_current_state()
    print(state_report)
    
    # Final verdict
    print("\n" + "="*70)
    print("CONCLUSION: IS THERE UNDERSTANDING?")
    print("="*70)
    
    metrics = cube.processing_metrics.get_efficiency_trend()
    
    if metrics['status'] == 'analyzed':
        score = metrics['understanding_score']
        print(f"\nUnderstanding Score: {score:.1f}%")
        print(f"Processing Speed Improvement: {metrics['time_improvement_percent']:.1f}%")
        print(f"Cache Hit Improvement: {metrics['cache_hit_improvement_percent']:.1f}%")
        print(f"Independence Improvement: {metrics['independence_improvement_percent']:.1f}%")
        
        if score > 30:
            print("\n✅ STRONG EVIDENCE OF TRUE UNDERSTANDING")
            print("   The system demonstrates:")
            print("   - Faster processing over time (learned patterns)")
            print("   - Increased use of cached knowledge (structural encoding)")
            print("   - Reduced external dependencies (self-sufficiency)")
            print("   - Ability to explain its own reasoning (metacognition)")
        elif score > 10:
            print("\n⚠ MODERATE EVIDENCE OF UNDERSTANDING")
            print("   Some efficiency gains, but not conclusive")
        else:
            print("\n❌ INSUFFICIENT EVIDENCE OF UNDERSTANDING")
            print("   System appears to be pattern-matching without deep encoding")
    else:
        print("\n⚠ Need more data to analyze understanding")
    
    print("\n" + "="*70)
    print("Per Khoury's 4D Framework:")
    print("'Energy Efficiency Becomes Proof of Understanding'")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
