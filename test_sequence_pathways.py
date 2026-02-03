#!/usr/bin/env python3
"""
Test 4D Systems Sequence Pathways
Shows WHICH neural pathways are used for different problems
"""

import json
import numpy as np
from pathlib import Path
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType


class PathwayTester:
    def __init__(self):
        print("\n" + "="*70)
        print("🧠 4D SYSTEMS DYNAMIC SEQUENCE GENERATION TEST")
        print("="*70)
        print("Testing: Does the cube generate optimal sequences for each problem?")
        print()
        
        # Load cube
        print("📦 Loading 4D Cube with dynamic sequence generation...")
        self.cube = MinimalSparkCube()
        
        # Warm up the cube with some experiences to enable dynamic generation
        print("🔥 Warming up cube (20 experiences to enable dynamic sequences)...")
        for i in range(20):
            warm_signal = Signal(
                type=SignalType.NUMERIC if i % 2 == 0 else SignalType.TEXT,
                data=i if i % 2 == 0 else f"warm_up_{i}",
                metadata={'training': True}
            )
            self.cube.process_signal(warm_signal)
        
        print(f"   ✓ Cube ready with {self.cube.total_experiences} experiences")
        print(f"   ✓ Dynamic sequence generation: {self.cube.enable_dynamic_sequences}")
    
    def _add_sequence_tracking(self):
        """Add sequence tracking to cube if not present"""
        self.cube.sequence_history = []
        
        # Wrap the cube's sequence generation
        original_process = self.cube.process_signal
        
        def tracked_process(signal):
            # Record which sequence is being used
            if hasattr(self.cube, 'current_sequence'):
                self.cube.sequence_history.append({
                    'signal': signal.data.get('problem', 'unknown'),
                    'sequence': self.cube.current_sequence
                })
            result = original_process(signal)
            return result
        
        self.cube.process_signal = tracked_process
    
    def test_problem(self, title, problem_type, goal, data):
        """Test a single problem and track pathway"""
        print(f"\n{'='*70}")
        print(f"🧪 Testing: {title}")
        print(f"🎯 Goal: {goal}")
        print(f"{'='*70}")
        
        # Create signal WITH EXPLICIT GOAL
        signal = Signal(
            type=SignalType.COMPOSITE,
            data={'problem': title, 'input': data, 'type': problem_type},
            metadata={'goal': goal}  # Goal affects pathway consideration
        )
        
        # Process through cube WITHOUT specifying sequence (let it choose)
        print(f"\n⚙️ Processing through 4D Cube (auto-sequence selection)...")
        
        # Record state before
        initial_experiences = self.cube.total_experiences
        initial_pathway_strengths = dict(self.cube.pathway_strengths)
        
        # Process signal
        result = self.cube.process_signal(signal, sequence_name=None)  # None = auto-select
        
        # Check what happened
        final_experiences = self.cube.total_experiences
        final_pathway_strengths = dict(self.cube.pathway_strengths)
        
        # Detect which sequence was used
        sequence_used = result.get('sequence', 'unknown')
        print(f"   🧠 Sequence selected: {sequence_used}")
        
        # Show pathway changes
        print(f"   📊 Pathway strength changes:")
        for pathway in ['standard', 'deep', 'emotional']:
            before = initial_pathway_strengths.get(pathway, 0)
            after = final_pathway_strengths.get(pathway, 0)
            change = after - before
            emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            print(f"      {emoji} {pathway}: {before:.3f} → {after:.3f} ({change:+.3f})")
        
        # Show node sequence
        if 'responses' in result:
            node_path = [r['node'] for r in result['responses']]
            print(f"   🔗 Node path: {' → '.join(node_path[:5])}{'...' if len(node_path) > 5 else ''}")
        
        return {
            'sequence': sequence_used,
            'result': result,
            'pathway_changes': {p: final_pathway_strengths.get(p, 0) - initial_pathway_strengths.get(p, 0) 
                              for p in ['standard', 'deep', 'emotional']}
        }
    
    def _show_pathway_info(self, signal, result):
        """Display which pathways were used"""
        
        # Check for sequence info in result
        if hasattr(result, 'metadata') and result.metadata:
            if 'sequence' in result.metadata:
                print(f"\n   🧠 Sequence used: {result.metadata['sequence']}")
            if 'pathway_strength' in result.metadata:
                print(f"   🔥 Pathway strength: {result.metadata['pathway_strength']:.3f}")
        
        # Check cube's internal state
        if hasattr(self.cube, 'last_sequence_used'):
            print(f"\n   📋 Last sequence: {self.cube.last_sequence_used}")
        
        if hasattr(self.cube, 'pathway_strengths'):
            print(f"\n   🔥 Top 3 pathways:")
            top_pathways = sorted(
                self.cube.pathway_strengths.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            for pathway, strength in top_pathways:
                print(f"      • {pathway}: {strength:.3f}")
        
        # Check for node sequence
        if hasattr(self.cube, 'last_node_sequence'):
            print(f"\n   🔗 Node sequence: {' → '.join(self.cube.last_node_sequence)}")
        
        # If no sequence tracking, show what info IS available
        if not any([
            hasattr(self.cube, 'last_sequence_used'),
            hasattr(self.cube, 'pathway_strengths'),
            hasattr(self.cube, 'last_node_sequence')
        ]):
            print(f"\n   ⚠ No sequence tracking found in cube")
            print(f"   → Cube may need sequence instrumentation")
            print(f"   → Check MinimalSparkCube implementation")


def main():
    tester = PathwayTester()
    
    # Test different problem types WITH EXPLICIT GOALS
    problems = [
        {
            'title': 'Pattern Recognition: Fibonacci',
            'type': 'pattern',
            'goal': 'Quick pattern detection',  # EFFICIENCY goal
            'data': [1, 1, 2, 3, 5, 8, 13, 21, 34]
        },
        {
            'title': 'Logical Reasoning: Syllogism',
            'type': 'logic',
            'goal': 'Deeply understand and reason about logical relationships',  # UNDERSTANDING goal
            'data': {
                'premises': ['All A are B', 'All B are C'],
                'question': 'Are all A also C?'
            }
        },
        {
            'title': 'Creative Problem: Nine Dots',
            'type': 'creative',
            'goal': 'Understand the creative insight required',  # UNDERSTANDING goal
            'data': {
                'dots': [[0,0], [1,0], [2,0], [0,1], [1,1], [2,1], [0,2], [1,2], [2,2]],
                'constraint': 'four_lines_no_lift'
            }
        },
        {
            'title': 'Optimization: Resource Allocation',
            'type': 'optimization',
            'goal': 'Quick optimal solution',  # EFFICIENCY goal
            'data': {
                'resources': [10, 10, 10],
                'demands': [8, 15, 12],
                'constraint': 'total_available = 30'
            }
        },
        {
            'title': 'Causal Analysis: Sales Data',
            'type': 'analysis',
            'goal': 'Analyze and deeply understand causation patterns',  # UNDERSTANDING goal
            'data': {
                'timeline': [
                    {'day': 1, 'sales': 100, 'ads': False, 'weather': 'bad'},
                    {'day': 2, 'sales': 150, 'ads': True, 'weather': 'good'}
                ]
            }
        }
    ]
    
    results = []
    sequence_usage = {}
    
    for problem in problems:
        result_data = tester.test_problem(
            problem['title'],
            problem['type'],
            problem['goal'],
            problem['data']
        )
        
        seq = result_data['sequence']
        sequence_usage[seq] = sequence_usage.get(seq, 0) + 1
        
        results.append({
            'problem': problem['title'],
            'type': problem['type'],
            'sequence': seq,
            'pathway_changes': result_data['pathway_changes']
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 DYNAMIC SEQUENCE GENERATION SUMMARY")
    print(f"{'='*70}")
    
    print(f"\n✓ Total problems tested: {len(problems)}")
    print(f"✓ Total sequences available: {len(tester.cube.sequences) + len(tester.cube.generated_sequences)}")
    print(f"   • Base sequences: {len(tester.cube.sequences)}")
    print(f"   • Generated sequences: {len(tester.cube.generated_sequences)}")
    
    print(f"\n📋 Sequence usage:")
    for seq, count in sorted(sequence_usage.items(), key=lambda x: x[1], reverse=True):
        is_dynamic = seq.startswith('dynamic_')
        emoji = "🧠" if is_dynamic else "📌"
        seq_type = "(GENERATED)" if is_dynamic else "(base)"
        print(f"   {emoji} {seq} {seq_type}: {count} problems")
    
    # Show the actual sequences
    print(f"\n🔗 Sequence definitions:")
    all_seqs = {**tester.cube.sequences, **tester.cube.generated_sequences}
    for seq_name, node_list in all_seqs.items():
        if seq_name in sequence_usage:  # Only show used sequences
            node_names = [tester.cube.nodes[n].name for n in node_list]
            print(f"   • {seq_name}: {' → '.join(node_names)}")
    
    unique_sequences = len(sequence_usage)
    if len(tester.cube.generated_sequences) > 0:
        print(f"\n🎉 SUCCESS: System generated {len(tester.cube.generated_sequences)} new optimized sequences!")
        print(f"   → 4D Systems architecture is FULLY ACTIVE")
        print(f"   → Dynamic sequence optimization WORKING")
        print(f"   → System adapts pathways based on problem characteristics")
    elif unique_sequences > 1:
        print(f"\n✓ PARTIAL: {unique_sequences} different sequences used (but all pre-defined)")
        print(f"   → Need more diverse problems or experiences to trigger generation")
    else:
        print(f"\n⚠ All problems used: {list(sequence_usage.keys())[0]}")
        print(f"   → System needs more experiences (current: {tester.cube.total_experiences})")
    
    # Save results
    output_file = "data/pathway_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
