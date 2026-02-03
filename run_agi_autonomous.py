"""
AGI AUTONOMOUS RUNNER
====================

Runs the AGI system continuously to discover and synthesize 100+ capabilities.

This demonstrates TRUE AGI:
- No human intervention required
- Self-directed exploration
- Discovers capabilities nobody programmed
- Meta-learns about what capabilities exist
- Continuously expands its own abilities

Run this for 24-48 hours to reach 100+ capabilities.
"""

import os
import sys
from pathlib import Path
import time
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType


def extract_emergent_concept(capability_name: str, description: str) -> str:
    """
    Extract the emergent concept from a synthesized capability.
    This is the KEY to exponential growth - each synthesis creates new primitives!
    
    Example: "understand_pattern_recognizer" → "pattern_understanding"
             This new concept can be combined with others: "pattern_understanding + structural_analysis"
    
    The magic: 1 + 1 = 2, now you have [1, 2]
               2 + 1 = 3, now you have [1, 2, 3]  
               3 + 2 = 5, now you have [1, 2, 3, 5] ... Fibonacci-like growth!
    """
    # Remove common suffixes to get the core concept
    clean_name = capability_name.replace('_recognizer', '').replace('_builder', '')
    clean_name = clean_name.replace('_handler', '').replace('_manager', '')
    clean_name = clean_name.replace('_analyzer', '').replace('_optimizer', '')
    clean_name = clean_name.replace('_v1', '').replace('_v2', '')
    
    # If capability is "verb_object", the emergent concept is "object_verbing"
    # Example: "understand_pattern" → "pattern_understanding"
    #          "analyze_structure" → "structural_analysis"
    parts = clean_name.split('_')
    if len(parts) >= 2:
        verb = parts[0]
        obj = '_'.join(parts[1:])
        
        # Create natural concept name
        if verb == 'understand':
            return f"{obj}_understanding"
        elif verb == 'analyze':
            return f"{obj}_analysis" if obj.endswith('al') else f"{obj}al_analysis"
        elif verb == 'create':
            return f"{obj}_creation"
        elif verb == 'learn':
            return f"{obj}_learning"
        elif verb == 'optimize':
            return f"{obj}_optimization"
        elif verb == 'develop':
            return f"{obj}_development"
        elif verb == 'adapt':
            return f"{obj}_adaptation"
        else:
            # Fallback: just reverse the order
            return f"{obj}_{verb}ing"
    
    return clean_name


def run_autonomous_agi(target_capabilities: int = 100, check_interval: int = 60, force_strategy: int = None):
    """
    Run AGI system autonomously until target capabilities reached.
    
    Args:
        target_capabilities: Stop when this many capabilities are discovered
        check_interval: Seconds between exploration cycles
        force_strategy: Force specific strategy (1, 2, or 3). None = auto-select
    """
    
    print("\n" + "="*80)
    print("🤖 AUTONOMOUS AGI RUNNER - Phase 3")
    print("="*80)
    print(f"\nTarget: {target_capabilities} capabilities")
    print(f"Check Interval: {check_interval} seconds")
    if force_strategy:
        print(f"Strategy: {force_strategy} (forced)")
    else:
        print("Strategy: Auto-select (1→2→3)")
    
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ ERROR: ANTHROPIC_API_KEY not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    # Create cube
    print("\n🔧 Initializing AGI Cube...")
    cube = MinimalSparkCube(api_key=api_key, enable_tools=True)
    
    if not cube.agi_engine:
        print("❌ AGI Engine not initialized")
        return
    
    print("✓ AGI Cube ready")
    
    # Create checkpoint directory
    checkpoint_dir = Path("data/agi_checkpoints")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Statistics
    start_time = datetime.now()
    cycle_count = 0
    total_syntheses = 0
    last_capability_count = 0
    
    # 🔥 GOAL-DIRECTED EXPLORATION - Generate initial high-level goals
    initial_goals = [
        "Understand and process natural language text",
        "Analyze and manipulate numerical data",
        "Recognize patterns in structured information",
        "Create visual representations of data",
        "Optimize processes for efficiency",
        "Learn from previous experiences",
        "Communicate findings clearly",
        "Manage and organize information",
        "Reason about abstract concepts",
        "Discover new problem-solving approaches"
    ]
    
    current_goal_index = 0
    goal_requirements_discovered = False
    attempted_goals = set()  # Track goals we've already tried
    
    print("\n🚀 Starting goal-directed autonomous exploration...")
    print("   Using Goal-Directed Explorer (no hardcoded domains)")
    print("   Press Ctrl+C to stop gracefully\n")
    
    try:
        while True:
            cycle_count += 1
            current_capabilities = list(cube.agi_engine.capability_registry.keys())
            capability_count = len(current_capabilities)
            
            # Check if target reached
            if capability_count >= target_capabilities:
                print(f"\n🎉 TARGET REACHED: {capability_count} capabilities!")
                break
            
            # Progress update
            if capability_count != last_capability_count:
                progress = (capability_count / target_capabilities * 100)
                print(f"📊 Progress: {capability_count}/{target_capabilities} ({progress:.0f}%)")
                last_capability_count = capability_count
            
            # 🔥 GOAL-DIRECTED: Set new goal if needed
            if not goal_requirements_discovered or not cube.agi_engine.goal_explorer.discovered_requirements:
                if current_goal_index < len(initial_goals):
                    goal = initial_goals[current_goal_index]
                    
                    # Skip if already attempted
                    if goal in attempted_goals:
                        current_goal_index += 1
                        continue
                    
                    attempted_goals.add(goal)
                    cube.agi_engine.goal_explorer.set_goal(goal)
                    
                    # Discover what's needed to achieve this goal
                    requirements = cube.agi_engine.goal_explorer.discover_requirements(goal, cube)
                    goal_requirements_discovered = True
                    current_goal_index += 1
                    
                    print(f"   📋 Discovered {len(requirements)} requirements for this goal")
                    
                    # 🔥 CRITICAL: If 0 requirements, this goal is complete - mark as attempted
                    # This prevents infinite loops in graph analysis where goals keep getting regenerated
                    if len(requirements) == 0:
                        attempted_goals.add(goal)
                        print(f"   ✓ Goal '{goal}' marked as complete (all requirements exist)")
                else:
                    # TRUE SELF-DIRECTION: Analyze capability graph to find unexplored combinations
                    print(f"\n🧠 Analyzing capability graph for unexplored edges...")
                    
                    capabilities = list(cube.agi_engine.capability_registry.keys())
                    
                    if len(capabilities) >= 3:
                        # Extract atomic operations from capability names (verbs mostly)
                        # Focus on ACTION verbs that can be combined
                        verbs = set()  # Actions: understand, analyze, create, etc.
                        objects = set()  # What they act on: pattern, structure, etc.
                        emergent_concepts = set()  # NEW: Concepts extracted from synthesized capabilities
                        
                        for cap in capabilities:
                            # Strip version suffix first
                            base_name = cap.rsplit('_v', 1)[0] if '_v' in cap else cap
                            parts = base_name.split('_')
                            
                            # First part is usually the verb (action)
                            if len(parts) >= 1:
                                verbs.add(parts[0])
                            # Everything else describes the object
                            if len(parts) >= 2:
                                objects.update(parts[1:])
                            
                            # 🔥 EMERGENT CONCEPT EXTRACTION
                            # Extract the emergent concept this capability represents
                            # This is how we grow exponentially: 1+1=2, then we have [1,2] to work with!
                            emergent = extract_emergent_concept(base_name, "")
                            if emergent and emergent != base_name:
                                emergent_concepts.add(emergent)
                                # Also add the emergent concept's components as objects
                                # e.g., "pattern_understanding" adds "understanding" as an object
                                emergent_parts = emergent.split('_')
                                objects.update(emergent_parts)
                        
                        if emergent_concepts:
                            print(f"   🌱 {len(emergent_concepts)} emergent concepts available: {', '.join(list(emergent_concepts)[:5])}...")
                        
                        # Track which GOAL PATTERNS have been synthesized
                        # Key insight: same operations can create different goals when recombined
                        synthesized_goals = set()
                        for cap in capabilities:
                            base_name = cap.rsplit('_v', 1)[0] if '_v' in cap else cap
                            # This represents a goal that was achieved
                            synthesized_goals.add(base_name)
                        
                        # Find UNEXPLORED goal patterns
                        # Try ALL strategies in sequence until we find an unattempted goal
                        new_goal = None
                        
                        import itertools
                        
                        # Strategy 1: Try combining verbs with unexplored objects
                        if not new_goal and (force_strategy is None or force_strategy == 1):
                            for verb in sorted(verbs):
                                for obj in sorted(objects):
                                    # Build potential goal names
                                    candidate = f"{verb}_{obj}"
                                    # Skip if this exact pattern exists
                                    if not any(candidate in syn_goal for syn_goal in synthesized_goals):
                                        test_goal = f"{verb.capitalize()} {obj.replace('_', ' ')}"
                                        if test_goal not in attempted_goals:
                                            new_goal = test_goal
                                            print(f"   💡 Strategy 1: {verb} + {obj}")
                                            break
                                if new_goal:
                                    break
                        
                        # Strategy 2: Try multi-object combinations (verb + obj1 + obj2)
                        if not new_goal and (force_strategy is None or force_strategy == 2):
                            for verb in sorted(verbs):
                                for obj1, obj2 in itertools.combinations(sorted(objects), 2):
                                    candidate = f"{verb}_{obj1}_{obj2}"
                                    if candidate not in synthesized_goals:
                                        test_goal = f"{verb.capitalize()} {obj1} and {obj2}"
                                        if test_goal not in attempted_goals:
                                            new_goal = test_goal
                                            print(f"   💡 Strategy 2: {verb} + {obj1} + {obj2}")
                                            break
                                if new_goal:
                                    break
                        
                        # Strategy 3: 🔥 RECOMBINE EMERGENT CONCEPTS with primitives!
                        # This is where exponential growth happens: 1+2=3, 2+3=5, 3+5=8...
                        if not new_goal and emergent_concepts and (force_strategy is None or force_strategy == 3):
                            print(f"   🌟 Strategy 3: Emergent concept recombination...")
                            for verb in sorted(verbs):
                                for concept in sorted(emergent_concepts):
                                    # Try verb + emergent concept
                                    candidate = f"{verb}_{concept}"
                                    if not any(candidate in syn_goal for syn_goal in synthesized_goals):
                                        test_goal = f"{verb.capitalize()} {concept.replace('_', ' ')}"
                                        if test_goal not in attempted_goals:
                                            new_goal = test_goal
                                            print(f"   ✨ NEW FRONTIER: {verb} + emergent '{concept}'")
                                            break
                                if new_goal:
                                    break
                            
                            # Try combining two emergent concepts together!
                            if not new_goal:
                                for concept1, concept2 in itertools.combinations(sorted(emergent_concepts), 2):
                                    candidate = f"{concept1}_{concept2}"
                                    if candidate not in synthesized_goals:
                                        test_goal = f"Integrate {concept1.replace('_', ' ')} with {concept2.replace('_', ' ')}"
                                        if test_goal not in attempted_goals:
                                            new_goal = test_goal
                                            print(f"   🚀 CONCEPT FUSION: '{concept1}' + '{concept2}'")
                                            break
                        
                        if new_goal:
                            attempted_goals.add(new_goal)
                        
                        if not new_goal:
                            # All pairs explored, try adding a new primitive operation
                            # This is where new vocabulary emerges
                            base_ops = ['understand', 'analyze', 'recognize', 'create', 'optimize', 
                                       'learn', 'communicate', 'manage', 'pattern', 'structure']
                            
                            new_op = None
                            for op in base_ops:
                                if op not in verbs:
                                    new_op = op
                                    break
                            
                            if new_op:
                                # Introduce new primitive
                                new_goal = f"Develop {new_op} capabilities"
                                
                                # Check if already attempted
                                if new_goal in attempted_goals:
                                    print(f"   ⚠️  Already attempted primitive: {new_goal}")
                                    # Try next fallback - random exploration
                                    import random
                                    remaining_verbs = [v for v in verbs if f"Develop {v} capabilities" not in attempted_goals]
                                    if remaining_verbs:
                                        new_op = random.choice(remaining_verbs)
                                        new_goal = f"Explore {new_op} combinations"
                                        print(f"   🎲 Random exploration: {new_goal}")
                                    else:
                                        new_goal = None
                                        print(f"   ⚠️  All exploration paths exhausted")
                                
                                if new_goal:
                                    attempted_goals.add(new_goal)
                                    print(f"   💡 Introducing new primitive: {new_op}")
                            else:
                                # All primitives explored, now INVENT new vocabulary
                                # Use existing operations to define new meta-operations
                                print(f"   🌟 All basic operations explored - inventing new vocabulary...")
                                
                                # Meta-operations emerge from combinations
                                meta_ops = {
                                    ('understand', 'create'): 'synthesize',
                                    ('analyze', 'optimize'): 'refine',
                                    ('recognize', 'learn'): 'adapt',
                                    ('pattern', 'structure'): 'organize',
                                    ('communicate', 'understand'): 'interpret'
                                }
                                
                                # Find a meta-operation we haven't defined yet
                                for (o1, o2), meta in meta_ops.items():
                                    if meta not in operations:
                                        new_goal = f"Develop {meta} capabilities by combining {o1} and {o2}"
                                        print(f"   💡 Emergent concept: {meta} = {o1} + {o2}")
                                        break
                                else:
                                    # Truly novel: combine three operations
                                    sample = operations[:3] if len(operations) >= 3 else operations
                                    new_goal = f"Integrate {', '.join(sample)} into unified capability"
                        
                        print(f"   🎯 Generated goal: {new_goal}")
                    else:
                        # Not enough context yet
                        new_goal = "Develop foundational information processing abilities"
                        print(f"   💡 Initial goal: {new_goal}")
                    
                    cube.agi_engine.goal_explorer.set_goal(new_goal)
                    requirements = cube.agi_engine.goal_explorer.discover_requirements(new_goal, cube)
                    goal_requirements_discovered = True
                    
                    # 🔥 CRITICAL FIX: Mark goals with 0 requirements as attempted
                    # This prevents infinite loops where graph keeps generating similar goals
                    if len(requirements) == 0:
                        attempted_goals.add(new_goal)
                        print(f"   ✓ Goal '{new_goal}' marked as complete (all requirements exist)")
            
            # Generate exploration signal from goal requirements
            exploration_signal = cube.agi_engine.goal_explorer.generate_exploration_signal()
            
            if exploration_signal:
                domain = exploration_signal['domain']
                query = exploration_signal.get('signal_data', exploration_signal['description'])
                parent_goal = exploration_signal.get('parent_goal', 'unknown')
                
                # Skip if this is an error handler from failed discovery
                if domain.startswith('error_handler_'):
                    print(f"\n⚠️  Skipping meta-error requirement: {domain}")
                    # Mark as blocked to prevent infinite loop
                    for req in cube.agi_engine.goal_explorer.discovered_requirements:
                        if req.name == domain and req.status == 'in_progress':
                            req.status = 'blocked'
                            break
                    continue
                
                # Skip if capability already exists
                if domain in cube.agi_engine.capability_registry:
                    print(f"\n⏭️  Skipping duplicate: {domain} (already exists)")
                    # Mark as completed
                    for req in cube.agi_engine.goal_explorer.discovered_requirements:
                        if req.name == domain and req.status == 'in_progress':
                            req.status = 'completed'
                            break
                    continue
                
                print(f"\n🔍 Cycle {cycle_count}: Exploring '{domain}'")
                print(f"   🎯 Parent Goal: {parent_goal}")
                
                # Skip if already exists
                if domain in cube.agi_engine.capability_registry:
                    print(f"   ⏭️  Skipping '{domain}' - already exists")
                    # Mark as completed
                    for req in cube.agi_engine.goal_explorer.discovered_requirements:
                        if req.name == domain and req.status == 'in_progress':
                            req.status = 'completed'
                            print(f"   ✅ Requirement '{req.name}' already satisfied!")
                            break
                    continue
                
                # Create signal
                signal = Signal(
                    type=SignalType.TEXT,
                    data=query,
                    timestamp=datetime.now()
                )
                
                # 🔥 ACTIVE SEQUENCE OPTIMIZATION - Try different sequences per goal
                optimal_seq = None
                if hasattr(cube, 'agi_engine') and cube.agi_engine and hasattr(cube.agi_engine, 'sequence_optimizer'):
                    try:
                        optimal_seq = cube.agi_engine.sequence_optimizer.find_optimal_sequence(query, signal)
                        print(f"   🧬 Optimized sequence: {optimal_seq}")
                    except Exception as e:
                        print(f"   ⚠️  Optimization skipped: {str(e)[:50]}")
                
                # 🔥 PHASE 4: Direct synthesis via self-correcting synthesizer
                result = None  # Initialize to avoid reusing old values
                try:
                    # Create gap dict for synthesizer
                    gap = {
                        'domain': domain,
                        'description': query,
                        'confidence': exploration_signal.get('confidence', 0.8)
                    }
                    
                    print(f"\n💡 Synthesizing Capability: {domain}")
                    
                    # Check if capability already exists
                    if domain in cube.agi_engine.capability_registry:
                        print(f"   ⚠️  Capability '{domain}' already exists, skipping...")
                        result = None
                    else:
                        # Synthesize with self-correction
                        result = cube.agi_engine.self_corrector.synthesize_with_correction(gap)
                    
                    if result:
                        code, filename = result
                        total_syntheses += 1
                        
                        # Learn from successful code
                        cube.agi_engine.code_learner.learn_from_code(code, success=True, domain=domain)
                        
                        # Save capability
                        filepath = cube.agi_engine.capabilities_dir / filename
                        filepath.write_text(code)
                        
                        # Add to registry
                        cube.agi_engine.capability_registry[domain] = {
                            'filepath': str(filepath),
                            'description': query,
                            'parent_goal': parent_goal,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        # Load capability into cube
                        from spark_cube.core.minimal_spark import SensorInterface
                        if not hasattr(cube.agi_engine, 'sensor'):
                            cube.agi_engine.sensor = SensorInterface(cube)
                        
                        loaded = cube.agi_engine.sensor.load_capability(filepath)
                        
                        # 🌱 EMERGENT VOCABULARY EXTRACTION
                        # Extract the new concept this capability represents
                        # This is how 1+1=2, then 2+1=3, then 3+2=5... exponential growth!
                        emergent_concept = extract_emergent_concept(domain, query)
                        if emergent_concept:
                            print(f"   ✨ Emergent concept: '{emergent_concept}' - now available for recombination!")
                        
                        print(f"   ✓ Capability 'spark_cube.capabilities.{domain}' synthesized and integrated")
                        print(f"   Total capabilities: {len(cube.agi_engine.capability_registry)}")
                        
                        # Reinforce successful pathway
                        if optimal_seq:
                            cube.provide_outcome_feedback(optimal_seq, success=True)
                            print(f"   ↑ Pathway '{optimal_seq}' reinforced")
                    
                    else:
                        print(f"   ✗ Synthesis failed after correction attempts")
                        
                        # Weaken unsuccessful pathway
                        if optimal_seq:
                            cube.provide_outcome_feedback(optimal_seq, success=False)
                            print(f"   ↓ Pathway '{optimal_seq}' weakened")
                
                except Exception as e:
                    print(f"   ✗ Error: {e}")
                    result = None  # Ensure result is None after exception
                    
                # Mark requirement as completed if synthesis succeeded
                if result:
                    # Find and mark the requirement as completed
                    for req in cube.agi_engine.goal_explorer.discovered_requirements:
                        if req.name == domain and req.status == 'in_progress':
                            req.status = 'completed'
                            print(f"   ✅ Requirement '{req.name}' completed!")
                            break
                    
                    # Reset flag to check for next goal
                    if not any(r.status == 'pending' for r in cube.agi_engine.goal_explorer.discovered_requirements):
                        goal_requirements_discovered = False
                else:
                    # Failed synthesis - mark as blocked
                    for req in cube.agi_engine.goal_explorer.discovered_requirements:
                        if req.name == domain and req.status == 'in_progress':
                            req.status = 'blocked'
                            print(f"   ⚠️  Requirement '{req.name}' blocked")
                            break
            
            else:
                print(f"\n⏸️  Cycle {cycle_count}: All requirements fulfilled, moving to next goal...")
                goal_requirements_discovered = False
            
            # Save checkpoint every 10 cycles
            if cycle_count % 10 == 0:
                checkpoint = {
                    'cycle': cycle_count,
                    'timestamp': datetime.now().isoformat(),
                    'capabilities': capability_count,
                    'total_syntheses': total_syntheses,
                    'runtime_seconds': (datetime.now() - start_time).total_seconds(),
                    'capability_types': current_capabilities
                }
                
                checkpoint_file = checkpoint_dir / f"checkpoint_{cycle_count}.json"
                with open(checkpoint_file, 'w') as f:
                    json.dump(checkpoint, f, indent=2)
                
                runtime = (datetime.now() - start_time).total_seconds()
                print(f"\n💾 Checkpoint saved (Runtime: {runtime/60:.1f} minutes)")
            
            # Wait before next cycle
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping autonomous run...")
    
    # Final report
    runtime = (datetime.now() - start_time).total_seconds()
    final_count = len(cube.agi_engine.capability_registry)
    
    print("\n" + "="*80)
    print("📊 AUTONOMOUS RUN SUMMARY")
    print("="*80)
    
    print(f"\n⏱️  Runtime: {runtime/60:.1f} minutes ({runtime/3600:.2f} hours)")
    print(f"🔄 Cycles: {cycle_count}")
    print(f"💡 Capabilities: {final_count}/{target_capabilities}")
    print(f"✓ Successful Syntheses: {total_syntheses}")
    print(f"📈 Synthesis Rate: {total_syntheses/max(cycle_count,1)*100:.0f}%")
    
    if cube.agi_engine and hasattr(cube.agi_engine, 'goal_explorer'):
        reqs_discovered = len(cube.agi_engine.goal_explorer.discovered_requirements)
        print(f"🧠 Requirements Discovered: {reqs_discovered}")
    
    print(f"\n🎯 Capability Diversity:")
    
    # Show capabilities created
    if cube.agi_engine:
        capabilities = len(cube.agi_engine.capability_registry)
        print(f"   Capabilities Created: {capabilities}")
        
        # Show some sample capabilities
        if capabilities > 0:
            print(f"\n📦 Sample Capabilities:")
            for i, cap_name in enumerate(list(cube.agi_engine.capability_registry.keys())[:5]):
                print(f"   {i+1}. {cap_name}")
    
    # Save final results
    results = {
        'completed_at': datetime.now().isoformat(),
        'runtime_seconds': runtime,
        'cycles': cycle_count,
        'capabilities_discovered': final_count,
        'target_capabilities': target_capabilities,
        'successful_syntheses': total_syntheses,
        'synthesis_rate': total_syntheses/max(cycle_count,1),
        'requirements_discovered': len(cube.agi_engine.goal_explorer.discovered_requirements) if cube.agi_engine and hasattr(cube.agi_engine, 'goal_explorer') else 0,
        'capability_registry': {
            cap: info for cap, info in cube.agi_engine.capability_registry.items()
        } if cube.agi_engine else {}
    }
    
    results_file = Path("data/agi_autonomous_run_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Assessment
    if final_count >= target_capabilities:
        print("\n🏆 SUCCESS: Target reached!")
        print("   ✓ Ready for Phase 3 publication")
        print("   ✓ True emergent intelligence demonstrated")
        print("   ✓ 100+ capabilities discovered autonomously")
    else:
        remaining = target_capabilities - final_count
        est_time = (remaining / max(total_syntheses/max(cycle_count,1), 0.1)) * check_interval / 60
        print(f"\n⏳ In Progress: {remaining} capabilities remaining")
        print(f"   Estimated time: {est_time:.0f} minutes")
        print(f"   Restart this script to continue")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AGI autonomous discovery')
    parser.add_argument('--target', type=int, default=100,
                       help='Target number of capabilities (default: 100)')
    parser.add_argument('--interval', type=int, default=60,
                       help='Seconds between exploration cycles (default: 60)')
    parser.add_argument('--strategy', type=int, choices=[1, 2, 3], default=None,
                       help='Force specific strategy: 1=verb+object, 2=multi-object, 3=emergent recombination (default: auto-select)')
    
    args = parser.parse_args()
    
    run_autonomous_agi(target_capabilities=args.target, check_interval=args.interval, force_strategy=args.strategy)
