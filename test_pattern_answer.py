#!/usr/bin/env python3
"""
Test if the synthesized semantic response capability can answer pattern questions.
"""
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType

def test_pattern_question():
    """Test with a clearer pattern question."""
    cube = MinimalSparkCube()
    
    # Test 1: Simple doubling sequence with explicit "next"
    print("Test 1: What comes after 2, 4, 8, 16 in the sequence?")
    signal = Signal(type=SignalType.TEXT, data={'question': 'What comes after 2, 4, 8, 16 in the sequence?'})
    result = cube.process_with_synthesis(signal)
    
    print(f"\nResponse: {result.get('semantic_response', 'No response')}")
    print(f"Synthesis info: {result.get('synthesis_info', {})}")
    
    # Test 2: Simpler question
    print("\n" + "="*60)
    print("\nTest 2: What is 2 + 2?")
    signal2 = Signal(type=SignalType.TEXT, data={'question': 'What is 2 + 2?'})
    result2 = cube.process_with_synthesis(signal2)
    
    print(f"\nResponse: {result2.get('semantic_response', 'No response')}")
    
    # Test 3: Definition question
    print("\n" + "="*60)
    print("\nTest 3: What is a pattern?")
    signal3 = Signal(type=SignalType.TEXT, data={'question': 'What is a pattern?'})
    result3 = cube.process_with_synthesis(signal3)
    
    print(f"\nResponse: {result3.get('semantic_response', 'No response')}")
    
    print("\n" + "="*60)
    print("✓ Capability synthesis test complete")
    print(f"  - Capability exists: {hasattr(cube.nodes[10], 'semantic_response')}")
    print(f"  - Registered: {'semantic_response' in cube.nodes[12].capability_registry}")

if __name__ == '__main__':
    test_pattern_question()
