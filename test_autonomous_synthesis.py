#!/usr/bin/env python3
"""
Test autonomous capability synthesis in sequence.
Should synthesize: text_processing → semantic_response
"""
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType

print("="*70)
print("AUTONOMOUS CAPABILITY SYNTHESIS TEST")
print("="*70)

cube = MinimalSparkCube()

print("\n📝 Question 1: What is 2 + 2?")
print("Expected: Synthesize text_processing")
signal1 = Signal(type=SignalType.TEXT, data={'question': 'What is 2 + 2?'})
result1 = cube.process_with_synthesis(signal1)
print(f"\n✓ Synthesized: {result1.get('synthesis', {}).get('capability_type', 'None')}")
print(f"   Capabilities now: {list(cube.nodes[12].capability_registry.keys())}")

print("\n" + "="*70)
print("\n📝 Question 2: What is 5 + 3?")
print("Expected: Synthesize semantic_response (text_processing already exists)")
signal2 = Signal(type=SignalType.TEXT, data={'question': 'What is 5 + 3?'})
result2 = cube.process_with_synthesis(signal2)
print(f"\n✓ Synthesized: {result2.get('synthesis', {}).get('capability_type', 'None')}")
print(f"   Capabilities now: {list(cube.nodes[12].capability_registry.keys())}")
print(f"\n💬 Response: {result2.get('semantic_response', 'NONE')}")
print(f"\nFull result keys: {list(result2.keys())}")
print(f"Responses in result: {result2.get('responses', [])}")

print("\n" + "="*70)
print("\n📊 FINAL STATUS:")
print(f"   text_processing: {'✓' if 'text_processing' in cube.nodes[12].capability_registry else '✗'}")
print(f"   semantic_response: {'✓' if 'semantic_response' in cube.nodes[12].capability_registry else '✗'}")
print(f"   Total capabilities: {len(cube.nodes[12].capability_registry)}")
print("="*70)
