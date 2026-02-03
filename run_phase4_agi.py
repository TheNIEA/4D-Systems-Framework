#!/usr/bin/env python3
"""
Phase 4 AGI Runner
Autonomous goal pursuit system based on 4D Framework principles
"""

import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube
from spark_cube.core.phase4_agi import Phase4AGIEngine


def main():
    parser = argparse.ArgumentParser(description='Run Phase 4 AGI with goal pursuit')
    parser.add_argument('--goal', type=str, 
                       help='Specific goal to pursue (optional, will use default goals if not provided)')
    parser.add_argument('--max-iterations', type=int, default=10,
                       help='Maximum iterations per goal (default: 10)')
    parser.add_argument('--checkpoint', type=str, default='phase4_checkpoint.json',
                       help='Checkpoint file path')
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("\n" + "="*80)
    print("🚀 PHASE 4 AGI - TRUE AUTONOMOUS INTELLIGENCE")
    print("Built on 4D Systems Framework Principles")
    print("="*80)
    
    # Initialize system
    print("\n📦 Initializing system...")
    cube = MinimalSparkCube()
    engine = Phase4AGIEngine(
        cube=cube,
        api_key=api_key,
        capabilities_dir="spark_cube/capabilities"
    )
    
    print("✓ Spark Cube initialized")
    print("✓ Phase 4 AGI Engine initialized")
    
    # Define goals to pursue
    if args.goal:
        goals = [args.goal]
    else:
        # Default goal sequence - progressively complex
        goals = [
            "Perform basic arithmetic operations",
            "Parse and validate JSON data",
            "Analyze text patterns",
            "Optimize data structures",
            "Generate creative content",
        ]
    
    print(f"\n🎯 Goal Queue: {len(goals)} goals")
    for i, goal in enumerate(goals, 1):
        print(f"   {i}. {goal}")
    
    # Pursue each goal
    start_time = datetime.now()
    
    for i, goal in enumerate(goals, 1):
        print(f"\n{'='*80}")
        print(f"GOAL {i}/{len(goals)}")
        print(f"{'='*80}")
        
        success = engine.pursue_goal(goal, max_iterations=args.max_iterations)
        
        # Show statistics after each goal
        stats = engine.get_statistics()
        print(f"\n📊 Current Statistics:")
        print(f"   Total capabilities: {stats['total_capabilities_synthesized']}")
        print(f"   Goals achieved: {stats['goals_achieved']}")
        print(f"   Goals blocked: {stats['goals_blocked']}")
        print(f"   Requirements discovered: {stats['discovered_requirements']}")
        print(f"   Code patterns learned: {stats['code_learning']['total_patterns_learned']}")
        print(f"   Sequence optimizations: {stats['sequence_optimizations']}")
        
        # Save checkpoint
        engine.save_state(args.checkpoint)
        
        # Brief pause between goals
        if i < len(goals):
            print("\n⏸️  Pausing 2 seconds before next goal...")
            time.sleep(2)
    
    # Final summary
    duration = (datetime.now() - start_time).total_seconds()
    stats = engine.get_statistics()
    
    print("\n" + "="*80)
    print("🏁 SESSION COMPLETE")
    print("="*80)
    
    print(f"\n⏱️  Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total capabilities synthesized: {stats['total_capabilities_synthesized']}")
    print(f"   Goals achieved: {stats['goals_achieved']}/{len(goals)}")
    print(f"   Goals blocked: {stats['goals_blocked']}")
    print(f"   Requirements discovered: {stats['discovered_requirements']}")
    
    print(f"\n🧠 Learning Progress:")
    print(f"   Code patterns learned: {stats['code_learning']['total_patterns_learned']}")
    print(f"   Successful patterns: {stats['code_learning']['successful_patterns']}")
    print(f"   Domains covered: {stats['code_learning']['domains_covered']}")
    
    print(f"\n🔬 4D Framework Optimization:")
    print(f"   Sequence optimizations performed: {stats['sequence_optimizations']}")
    
    # Show achieved goals
    if engine.goals_achieved:
        print(f"\n✅ Goals Achieved:")
        for goal in engine.goals_achieved:
            print(f"   - {goal['goal']} (in {goal['iterations']} iterations)")
    
    # Show blocked goals
    if engine.goals_blocked:
        print(f"\n⚠️  Goals Blocked:")
        for goal in engine.goals_blocked:
            print(f"   - {goal['goal']} (reason: {goal['reason']})")
    
    print("\n" + "="*80)
    
    if stats['goals_achieved'] == len(goals):
        print("🎉 SUCCESS: All goals achieved!")
        return 0
    elif stats['goals_achieved'] > 0:
        print(f"⚡ PARTIAL SUCCESS: {stats['goals_achieved']}/{len(goals)} goals achieved")
        return 0
    else:
        print("⚠️  No goals achieved - may need debugging")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
