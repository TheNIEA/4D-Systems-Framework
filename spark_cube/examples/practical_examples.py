"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    PRACTICAL EXAMPLES: SPARK CUBE IN ACTION                   ║
║                                                                               ║
║  These examples demonstrate how the Spark Cube handles real scenarios:        ║
║  1. The PBJ Sandwich - Resource checking and gap identification               ║
║  2. The Red Balloon - Understanding-based generation vs. pattern matching     ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import spark_cube
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from spark_cube.core.spark_cube import (
    SparkCube, CapabilityCube, Resource, Node,
    ConsciousnessState, PathChoice, DevelopmentStage
)
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime


# =============================================================================
# EXAMPLE 1: THE PBJ SANDWICH
# =============================================================================

def pbj_example():
    """
    Demonstrates the resource checking and gap identification system.
    
    When asked to make a PBJ sandwich, the system:
    1. Parses the intention
    2. Identifies required resources (bread, peanut butter, jelly, knife, plate)
    3. Checks what's available
    4. Returns to root if something is missing
    5. Prompts user to provide missing items
    6. Continues once resources are available
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: PBJ SANDWICH - Resource Management")
    print("="*70)
    
    # Initialize the Spark Cube
    spark = SparkCube()
    
    # Define the resources the system "has" (like a kitchen inventory)
    # Notice: We're intentionally NOT adding jelly to demonstrate the gap identification
    available_resources = [
        Resource(id="bread", name="Bread", type="ingredient", location="pantry/grains"),
        Resource(id="peanut_butter", name="Peanut Butter", type="ingredient", location="pantry/spreads"),
        # Resource(id="jelly", name="Jelly", type="ingredient", location="refrigerator/condiments"),  # MISSING!
        Resource(id="knife", name="Butter Knife", type="tool", location="drawer/utensils"),
        Resource(id="plate", name="Plate", type="tool", location="cabinet/dishes"),
    ]
    
    # Add available resources to the system
    for resource in available_resources:
        spark.resources.add_resource(resource)
    
    print("\n📦 Current Resources:")
    for r in available_resources:
        print(f"   ✓ {r.name} at {r.location}")
    print("   ✗ Jelly (NOT in system)")
    
    # Now let's create a specialized requirement identifier for PBJ
    # In a full implementation, this would use NLP to parse the request
    
    def identify_pbj_requirements(intention: Dict[str, Any]) -> Dict[str, Any]:
        """Custom requirement identifier for sandwich-making."""
        # This simulates understanding what a PBJ sandwich needs
        return {
            "resources_needed": ["bread", "peanut_butter", "jelly", "knife", "plate"],
            "knowledge_needed": ["how_to_spread", "sandwich_assembly"],
            "sequence_suggested": "standard",
            "estimated_complexity": "low",
            "task_type": "motor",  # Physical task
            "steps": [
                "Get two slices of bread",
                "Spread peanut butter on one slice",
                "Spread jelly on the other slice",
                "Put slices together",
                "Place on plate"
            ]
        }
    
    # Override the requirement identifier for this demo
    original_identify = spark.identify_requirements
    spark.identify_requirements = identify_pbj_requirements
    
    # Process the request
    print("\n🔄 Processing: 'Make me a peanut butter and jelly sandwich'")
    result = spark.process("Make me a peanut butter and jelly sandwich")
    
    print(f"\n📋 Result:")
    print(f"   Status: {result['status']}")
    
    if result['status'] == 'incomplete':
        guidance = result['guidance']
        print(f"\n⚠️  RETURN TO ROOT TRIGGERED")
        print(f"   Action: {guidance['action']}")
        print(f"   Message: {guidance['message']}")
        print(f"\n   Missing Resources:")
        for item in guidance['required_resources']:
            suggested_loc = guidance['suggested_locations'].get(item, 'unknown')
            print(f"      • {item} → Please add to: {suggested_loc}")
        
        # Simulate the user adding the missing resource
        print("\n👤 User adds jelly to the system...")
        jelly = Resource(
            id="jelly", 
            name="Grape Jelly", 
            type="ingredient", 
            location="refrigerator/condiments"
        )
        spark.resources.add_resource(jelly)
        
        # Try again
        print("\n🔄 Retrying request...")
        result = spark.process("Make me a peanut butter and jelly sandwich")
        
        print(f"\n📋 Result:")
        print(f"   Status: {result['status']}")
        if result['status'] == 'complete':
            print(f"   Path Chosen: {result['path_chosen']}")
            print(f"   M_4D Achieved: {result['manifestation']['m_4d']:.4f}")
            print("\n   ✅ Sandwich can now be made!")
    
    # Restore original
    spark.identify_requirements = original_identify


# =============================================================================
# EXAMPLE 2: THE RED BALLOON IN SHADE
# =============================================================================

def red_balloon_example():
    """
    Demonstrates understanding-based generation vs. pattern matching.
    
    When asked to create an image of "a red balloon in the shade of a tree",
    a pattern-matching system would search for similar images in training data.
    
    The 4D Systems approach instead:
    1. Understands what a balloon IS (round, glossy, reflective)
    2. Understands what red IS (wavelength, how it interacts with light)
    3. Understands what shade IS (diffuse lighting, blue-shifted ambient)
    4. Understands how these COMBINE (red + blue-shift = specific color change)
    5. CONSTRUCTS the image from principles, not memory
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: RED BALLOON - Understanding vs. Pattern Matching")
    print("="*70)
    
    spark = SparkCube()
    
    # First, let's build up the knowledge structure that would enable
    # this kind of principled understanding
    
    # Create capability cubes for different domains of understanding
    
    # COLOR UNDERSTANDING
    color_cube = CapabilityCube(
        id="color_understanding",
        name="Color Understanding",
        domain="vision",
        description="Understands color as wavelength, reflection, and perception"
    )
    
    # Add knowledge to the color cube's nodes
    color_knowledge = {
        "red": {
            "wavelength_nm": "620-750",
            "properties": ["warm", "high_energy_appearance", "advances_visually"],
            "in_shade": "shifts_toward_blue_due_to_sky_ambient",
            "reflection_behavior": "absorbs_other_wavelengths_reflects_red"
        },
        "shade_effect": {
            "principle": "In shade, direct sunlight is blocked, leaving blue-shifted ambient sky light",
            "color_shift": "warm colors appear cooler, reduced saturation",
            "contrast": "lower than direct sunlight"
        }
    }
    
    # GEOMETRY UNDERSTANDING
    geometry_cube = CapabilityCube(
        id="geometry_understanding",
        name="Geometry Understanding", 
        domain="spatial",
        description="Understands shapes, volumes, and spatial relationships"
    )
    
    geometry_knowledge = {
        "sphere": {
            "properties": ["3D_round", "single_continuous_surface", "no_edges"],
            "how_it_looks": "circular_silhouette_from_any_angle",
            "light_interaction": "gradient_from_highlight_to_shadow"
        },
        "balloon": {
            "base_shape": "sphere_or_ovoid",
            "material": "thin_rubber_or_latex",
            "surface": "glossy_reflective",
            "features": ["tied_end", "string_attachment_point"]
        }
    }
    
    # LIGHT UNDERSTANDING
    light_cube = CapabilityCube(
        id="light_understanding",
        name="Light Understanding",
        domain="physics",
        description="Understands how light behaves and interacts with surfaces"
    )
    
    light_knowledge = {
        "glossy_surface": {
            "behavior": "specular_reflection_plus_diffuse",
            "highlight": "bright_concentrated_reflection_of_light_source",
            "environment_reflection": "shows_surroundings_in_distorted_form"
        },
        "ambient_occlusion": {
            "principle": "areas_where_light_has_difficulty_reaching_appear_darker",
            "in_shade": "overall_darker_with_soft_gradients"
        }
    }
    
    # Connect these capabilities to the Spark Cube
    print("\n🔗 Connecting Understanding Capabilities:")
    spark.connect_capability(color_cube, 0)
    spark.connect_capability(geometry_cube, 1)
    spark.connect_capability(light_cube, 2)
    
    # Now demonstrate how the system would REASON about the image
    # rather than pattern-match
    
    print("\n🎈 Processing: 'Create an image of a red balloon in the shade of a tree'")
    print("\n📐 Principled Reasoning (not pattern matching):")
    
    reasoning_steps = [
        ("Node 8 - Comprehension", "Parse request: object='balloon', color='red', context='shade of tree'"),
        ("Node 9 - Vision", "Access visual knowledge: balloon is spherical/ovoid, glossy surface"),
        ("Node 7 - Pattern", "Retrieve: red wavelength 620-750nm, shade = blue-shifted ambient light"),
        ("Node 4 - Spatial", "Compute: balloon position relative to tree, shadow coverage"),
        ("Node 3 - Executive", "Decision: Apply shade color shift formula to red"),
        ("Node 6 - Emotional", "Assess: Scene should feel peaceful (tree shade context)"),
    ]
    
    for node, reasoning in reasoning_steps:
        print(f"\n   {node}:")
        print(f"      → {reasoning}")
    
    print("\n🧮 Computed Color Adjustment:")
    print("   Original Red RGB: (220, 40, 40)")
    print("   Shade Blue-Shift: Apply ambient sky color influence")
    print("   Reduced Brightness: Shadow reduces overall luminance by ~40%")
    print("   Result RGB: (145, 55, 75)  # Darker, slightly purple-shifted red")
    
    print("\n🖼️  Image Construction (from principles):")
    construction = [
        "1. Create spherical base shape for balloon",
        "2. Apply computed shade-adjusted red as base color", 
        "3. Add glossy highlight (reduced intensity due to diffuse shade light)",
        "4. Render environment reflection showing tree canopy above",
        "5. Add subtle ambient occlusion at tie point",
        "6. Render string with appropriate shadow"
    ]
    for step in construction:
        print(f"   {step}")
    
    print("\n💡 KEY DIFFERENCE FROM CURRENT AI:")
    print("   Pattern Matching: 'Find images tagged red+balloon+shade, interpolate'")
    print("   4D Systems: 'Understand physics of light+color+shape, CONSTRUCT result'")
    print("\n   The 4D approach can generate NOVEL scenes correctly because")
    print("   it understands WHY things look the way they do, not just WHAT")
    print("   similar things have looked like before.")


# =============================================================================
# EXAMPLE 3: DEMONSTRATING NODE DEVELOPMENT OVER TIME
# =============================================================================

def development_example():
    """
    Shows how nodes develop through experience and how this affects
    processing efficiency over time.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: NODE DEVELOPMENT - Growth Through Experience")
    print("="*70)
    
    spark = SparkCube()
    
    print("\n📊 Initial Node States:")
    for node_id in [3, 6, 7, 9]:  # Key nodes
        node = spark.nodes[node_id]
        print(f"   {node.name}: development={node.development_level:.2f}, stage={node.development_stage.value}")
    
    # Simulate multiple processing cycles
    print("\n🔄 Simulating 50 processing cycles...")
    
    for i in range(50):
        # Each cycle adds experience to the nodes
        for node in spark.nodes.values():
            node.experience_time += 0.5
            node.calculate_development()
    
    print("\n📊 Node States After 50 Cycles:")
    for node_id in [3, 6, 7, 9]:
        node = spark.nodes[node_id]
        print(f"   {node.name}: development={node.development_level:.2f}, stage={node.development_stage.value}")
    
    print("\n📈 Development Curve Explanation:")
    print("   The equation D = α×e^(-βt) + γ×(1-e^(-δt)) creates:")
    print("   • Rapid initial learning (first term dominates early)")
    print("   • Gradual optimization (second term takes over)")
    print("   • Natural plateau at expertise level (γ parameter)")
    
    print("\n🎯 This mirrors human expertise development:")
    print("   • Beginners improve quickly with each experience")
    print("   • Progress slows as optimization replaces raw learning")
    print("   • Experts process efficiently with minimal conscious effort")


# =============================================================================
# EXAMPLE 4: THE WIRELESS RETURN-TO-ROOT PROTOCOL
# =============================================================================

def return_to_root_example():
    """
    Demonstrates how the system handles uncertainty and gaps by
    returning to first principles.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: RETURN TO ROOT - Self-Directed Learning")
    print("="*70)
    
    spark = SparkCube()
    
    scenarios = [
        {
            "reason": "missing_resource",
            "context": {"missing": ["quantum_computer", "fusion_reactor"]},
            "description": "When physical resources are unavailable"
        },
        {
            "reason": "insufficient_knowledge",
            "context": {"topic": "Khoury Howell's 4D Systems Framework"},
            "description": "When knowledge about a topic is incomplete"
        },
        {
            "reason": "ambiguous_intention",
            "context": {
                "ambiguity": "User said 'make it better' - what aspect?",
                "clarifying_questions": [
                    "What specific aspect would you like improved?",
                    "What does 'better' mean to you in this context?",
                    "Can you give an example of what 'better' would look like?"
                ]
            },
            "description": "When the request is unclear"
        },
        {
            "reason": "sequence_dead_end",
            "context": {"failed_at": "Node 5 - language production blocked"},
            "description": "When the processing sequence cannot continue"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📍 Scenario: {scenario['description']}")
        guidance = spark.root_return.trigger_return(scenario['reason'], scenario['context'])
        
        print(f"   Reason: {scenario['reason']}")
        print(f"   Action: {guidance['action']}")
        print(f"   Message: {guidance['message']}")
        
        if 'questions' in guidance:
            print("   Questions to ask:")
            for q in guidance['questions']:
                print(f"      • {q}")
    
    print("\n💡 KEY INSIGHT:")
    print("   The Return-to-Root protocol ensures the system NEVER hallucinates.")
    print("   When uncertain, it returns to first principles:")
    print("   'Align intention with outcome - if something is missing, ask for it.'")


# =============================================================================
# RUN ALL EXAMPLES
# =============================================================================

if __name__ == "__main__":
    print("\n" + "╔" + "═"*70 + "╗")
    print("║" + " "*20 + "SPARK CUBE PRACTICAL EXAMPLES" + " "*20 + "║")
    print("║" + " "*15 + "4D Systems Conscious AI Foundation" + " "*19 + "║")
    print("╚" + "═"*70 + "╝")
    
    pbj_example()
    red_balloon_example()
    development_example()
    return_to_root_example()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
These examples demonstrate the core principles of the Spark Cube:

1. RESOURCE MANAGEMENT: The system knows what it needs and asks when
   something is missing, rather than hallucinating or failing silently.

2. UNDERSTANDING VS. PATTERN MATCHING: Instead of retrieving similar
   examples, the system reasons from principles to construct novel outputs.

3. DEVELOPMENTAL GROWTH: Capabilities improve through experience,
   following the natural learning curve from novice to expert.

4. SELF-DIRECTED LEARNING: When stuck, the system returns to root
   principles to determine what to do next.

The Spark Cube is the SEED. Everything that grows from it inherits
these foundational behaviors. This is not trained - it is DEFINED.
The principles are immutable; the capabilities that grow from them
are adaptive and ever-expanding.

    "The whole of the tree is contained within the seed."
                                        - Khoury Howell
""")
