#!/usr/bin/env python3
"""
Quick test: Can the Spark Cube respond to questions in natural language?
"""
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType

def test_language_responses():
    """Test if semantic response capability works."""
    print("🧪 Testing Natural Language Response Capability\n")
    
    cube = MinimalSparkCube()
    
    questions = [
        "What is 2 + 2?",
        "What comes next: 2, 4, 8, 16?",
        "Explain what a pattern is",
        "Why is the sky blue?",
        "How does learning work?"
    ]
    
    print("="*70)
    for i, question in enumerate(questions, 1):
        print(f"\n🔹 Question {i}: {question}")
        
        signal = Signal(
            type=SignalType.TEXT,
            data={'question': question}
        )
        
        # Use process_with_synthesis to trigger capability creation if needed
        result = cube.process_with_synthesis(signal)
        
        # Check for semantic response
        if 'semantic_response' in result:
            print(f"✅ Response: {result['semantic_response']}")
        elif 'responses' in result and result['responses']:
            print(f"✅ Response: {result['responses'][0].get('response', 'No response')}")
        else:
            print(f"❌ No response generated")
            print(f"   Result keys: {list(result.keys())}")
        
        print("-"*70)
    
    # Check if capability is now permanent
    print(f"\n📊 Capability Status:")
    print(f"   - Semantic response capability: {hasattr(cube.nodes[10], 'semantic_response')}")
    print(f"   - Total capabilities: {len(cube.nodes[12].capability_registry)}")
    
if __name__ == '__main__':
    test_language_responses()
