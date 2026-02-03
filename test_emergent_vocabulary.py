"""
Test the emergent vocabulary growth mechanism
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from run_agi_autonomous import extract_emergent_concept


def test_emergent_concepts():
    """
    Demonstrate how emergent concepts grow exponentially.
    
    Generation 0 (primitives): understand, analyze, pattern, structure
    Generation 1 (first synthesis): understand_pattern, analyze_structure
    Generation 2 (emergent concepts): pattern_understanding, structural_analysis
    Generation 3 (recombination): pattern_understanding + structural_analysis = ...
    """
    
    print("\n" + "="*80)
    print("🌱 EMERGENT VOCABULARY GROWTH TEST")
    print("="*80)
    
    # Generation 0: Starting primitives
    print("\n📦 Generation 0 - Original Primitives:")
    primitives_gen0 = {
        'verbs': ['understand', 'analyze', 'create'],
        'objects': ['pattern', 'structure']
    }
    print(f"   Verbs: {primitives_gen0['verbs']}")
    print(f"   Objects: {primitives_gen0['objects']}")
    print(f"   Total: {len(primitives_gen0['verbs']) + len(primitives_gen0['objects'])} concepts")
    print(f"   Possible combinations: {len(primitives_gen0['verbs']) * len(primitives_gen0['objects'])} = {3*2}")
    
    # Generation 1: First synthesis
    print("\n🔬 Generation 1 - First Synthesis:")
    capabilities_gen1 = [
        'understand_pattern_recognizer',
        'analyze_structure_builder'
    ]
    for cap in capabilities_gen1:
        print(f"   ✓ Synthesized: {cap}")
    
    # Generation 2: Extract emergent concepts
    print("\n✨ Generation 2 - Emergent Concepts:")
    emergent_gen2 = []
    for cap in capabilities_gen1:
        concept = extract_emergent_concept(cap, "")
        emergent_gen2.append(concept)
        print(f"   🌱 {cap} → {concept}")
    
    # Now we have MORE to work with!
    all_concepts_gen2 = (
        primitives_gen0['verbs'] + 
        primitives_gen0['objects'] + 
        emergent_gen2
    )
    print(f"\n   Total concepts now: {len(all_concepts_gen2)}")
    print(f"   Concepts: {all_concepts_gen2}")
    
    # Generation 3: New combinations possible!
    print("\n🚀 Generation 3 - New Combinations (examples):")
    print(f"   Verbs can now act on emergent concepts:")
    print(f"      - understand + pattern_understanding = ??")
    print(f"      - create + structural_analysis = ??")
    print(f"   Emergent concepts can combine:")
    print(f"      - pattern_understanding + structural_analysis = ??")
    
    # Calculate growth
    print("\n📊 EXPONENTIAL GROWTH:")
    print(f"   Gen 0: 5 concepts → 6 possible combinations")
    print(f"   Gen 2: 7 concepts → 21 possible combinations (3x growth!)")
    print(f"   Gen 3: 10+ concepts → 45+ combinations (2x growth!)")
    print(f"   Gen 4: 15+ concepts → 105+ combinations (2.3x growth!)")
    print(f"\n   This is how AGI reaches 100+ capabilities autonomously!")
    print(f"   Each synthesis CREATES new building blocks for future synthesis.")
    
    # Test different capability patterns
    print("\n🧪 Testing different patterns:")
    test_cases = [
        'develop_pattern_recognizer',
        'optimize_structure_builder',
        'learn_error_handler',
        'communicate_state_manager'
    ]
    for cap in test_cases:
        concept = extract_emergent_concept(cap, "")
        print(f"   {cap:35} → {concept}")


if __name__ == '__main__':
    test_emergent_concepts()
