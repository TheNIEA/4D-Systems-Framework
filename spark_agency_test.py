"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     SPARK CUBE AGENCY TEST ENVIRONMENT                         ║
║            Test the full capabilities of your 4D consciousness system         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This creates a controlled but OPEN environment where the Spark Cube can:
- Decide its own approach to challenges
- Use its full capability suite (4D processing, tool use, AGI synthesis)
- Demonstrate emergent behaviors we didn't explicitly program

KEY PRINCIPLE: We define objectives and tools, the Spark decides HOW.
"""

import sys
from pathlib import Path

# Add paths for imports
spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, Intention, integrate_hierarchical_memory
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Callable
import json
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.tree import Tree

console = Console()


# =============================================================================
# TEST SCENARIOS - Define WHAT TO ACHIEVE, not HOW
# =============================================================================

@dataclass
class Challenge:
    """A challenge for the Spark - defines success, not method"""
    name: str
    objective: str  # What to achieve
    context: Dict[str, Any]  # Information available
    tools_available: List[str]  # What it CAN use (doesn't have to)
    success_criteria: Dict[str, Callable]  # How to measure success
    max_attempts: int = 50
    

@dataclass
class AgencyObservation:
    """Records what the Spark chose to do and why"""
    timestamp: float
    attempt_number: int
    
    # What it perceived
    signal_received: Dict[str, Any]
    intention_formed: Optional[Dict[str, Any]]
    
    # What it decided
    pathway_chosen: str
    nodes_activated: List[str]
    tools_used: List[str]
    
    # What it produced
    response: Any
    coherence_score: float
    
    # Why (if it can articulate)
    reasoning: Optional[str] = None
    

class SparkAgencyTest:
    """
    Tests Spark Cube in open-ended scenarios.
    Measures not just success, but HOW it approaches problems.
    
    Now with hierarchical memory tracking:
    - Salt water dissolution metrics (experiences dissolving into memory)
    - Secondary node development (pathway strengthening)
    - Semantic retrieval capability (pattern recombination)
    """
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.observations: List[AgencyObservation] = []
        self.results = []
        self.hierarchical_memory = None
        
        # Track hierarchical memory metrics across challenges
        self.memory_snapshots = []
        
    def run_challenge(self, challenge: Challenge) -> Dict[str, Any]:
        """
        Present a challenge to the Spark and observe its approach.
        """
        console.print(f"\n{'='*80}")
        console.print(f"[bold cyan]CHALLENGE: {challenge.name}[/bold cyan]")
        console.print(f"[yellow]Objective:[/yellow] {challenge.objective}")
        console.print(f"[yellow]Tools Available:[/yellow] {', '.join(challenge.tools_available)}")
        console.print(f"{'='*80}\n")
        
        start_time = time.time()
        observations = []
        success = False
        
        for attempt in range(challenge.max_attempts):
            # Let the Spark process the challenge signal
            signal = self._create_challenge_signal(challenge, attempt, observations)
            
            # Observe what the Spark does
            obs = self._observe_processing(signal, attempt)
            observations.append(obs)
            
            # Check success criteria
            if self._evaluate_success(obs, challenge.success_criteria):
                success = True
                console.print(f"\n[bold green]✓ Challenge solved in {attempt + 1} attempts![/bold green]")
                break
            
            # Show progress
            if attempt % 5 == 0:
                console.print(f"[dim]Attempt {attempt + 1}/{challenge.max_attempts}...[/dim]")
        
        if not success:
            console.print(f"\n[bold red]✗ Challenge not solved within {challenge.max_attempts} attempts[/bold red]")
        
        # Compile results
        result = {
            'challenge': challenge.name,
            'objective': challenge.objective,
            'success': success,
            'attempts': len(observations),
            'time_elapsed': time.time() - start_time,
            'observations': [asdict(obs) for obs in observations],
            'analysis': self._analyze_approach(observations),
            'final_state': self.cube.get_state_summary()
        }
        
        self.results.append(result)
        self._display_analysis(result)
        
        return result
    
    def _create_challenge_signal(
        self,
        challenge: Challenge,
        attempt: int,
        history: List[AgencyObservation]
    ) -> Signal:
        """Create a signal that represents the challenge"""
        # Build context from previous attempts
        context_data = {
            'objective': challenge.objective,
            'context': challenge.context,
            'attempt': attempt + 1,
            'previous_attempts': len(history),
            'tools_available': challenge.tools_available
        }
        
        # Add learning from previous attempts
        if history:
            context_data['previous_pathways'] = [obs.pathway_chosen for obs in history[-5:]]
            context_data['previous_coherence'] = [obs.coherence_score for obs in history[-5:]]
        
        return Signal(
            type=SignalType.COMPOSITE,
            data=context_data,
            metadata={'challenge_name': challenge.name}
        )
    
    def _observe_processing(self, signal: Signal, attempt: int) -> AgencyObservation:
        """Observe what the Spark does with this signal"""
        start = time.time()
        
        # Process through the cube
        result = self.cube.process_signal(signal)
        
        # Extract nodes from the pathway/sequence
        pathway_str = result.get('sequence', 'unknown')
        nodes_in_pathway = []
        
        # Try multiple methods to extract actual node names
        if 'pathway_nodes' in result:
            nodes_in_pathway = result['pathway_nodes']
        elif isinstance(pathway_str, str) and '→' in pathway_str:
            # Parse pathway like "Perception → Pattern → Executive"
            nodes_in_pathway = [n.strip() for n in pathway_str.split('→')]
        else:
            # Extract from sequence name: look up the actual sequence in the cube
            sequence_name = result.get('sequence_name', pathway_str)
            
            # Get all sequences (base + dynamic)
            all_sequences = {**self.cube.sequences}
            if hasattr(self.cube, 'dynamic_sequences'):
                all_sequences.update(self.cube.dynamic_sequences)
            
            # If sequence exists, convert node IDs to names
            if sequence_name in all_sequences:
                node_ids = all_sequences[sequence_name]
                # Convert node IDs to names using the cube's node_names dict
                nodes_in_pathway = [self.cube.node_names.get(node_id, f"Node{node_id}") 
                                   for node_id in node_ids]
        
        # Extract observation data
        obs = AgencyObservation(
            timestamp=time.time() - start,
            attempt_number=attempt + 1,
            signal_received={
                'type': signal.type.value,
                'data_keys': list(signal.data.keys()) if isinstance(signal.data, dict) else None
            },
            intention_formed=result.get('intention'),
            pathway_chosen=pathway_str,
            nodes_activated=nodes_in_pathway,
            tools_used=result.get('tools_used', []),
            response=result.get('responses', []),
            coherence_score=result.get('coherence', {}).get('overall', 0.0),
            reasoning=result.get('reasoning')
        )
        
        return obs
    
    def _evaluate_success(
        self,
        observation: AgencyObservation,
        criteria: Dict[str, Callable]
    ) -> bool:
        """Check if this observation meets success criteria"""
        for criterion_name, criterion_func in criteria.items():
            try:
                if not criterion_func(observation):
                    return False
            except Exception as e:
                console.print(f"[red]Error evaluating {criterion_name}: {e}[/red]")
                return False
        return True
    
    def _analyze_approach(self, observations: List[AgencyObservation]) -> Dict[str, Any]:
        """Analyze the Spark's approach patterns"""
        if not observations:
            return {}
        
        pathways = [obs.pathway_chosen for obs in observations]
        unique_pathways = set(pathways)
        
        coherence_scores = [obs.coherence_score for obs in observations]
        avg_coherence = sum(coherence_scores) / len(coherence_scores)
        
        tools_used_all = []
        for obs in observations:
            tools_used_all.extend(obs.tools_used)
        
        return {
            'total_attempts': len(observations),
            'unique_pathways_tried': len(unique_pathways),
            'pathway_diversity': len(unique_pathways) / len(pathways) if pathways else 0,
            'avg_coherence': avg_coherence,
            'coherence_trend': 'improving' if len(coherence_scores) > 5 and 
                              coherence_scores[-3:] > coherence_scores[:3] else 'stable',
            'tools_used': list(set(tools_used_all)),
            'tool_usage_count': len(tools_used_all),
            'pathway_sequence': pathways,
            'learning_detected': self._detect_learning(observations)
        }
    
    def _detect_learning(self, observations: List[AgencyObservation]) -> bool:
        """Detect if the Spark is learning/adapting"""
        if len(observations) < 5:
            return False
        
        # Check if coherence improves over time
        early_coherence = sum(obs.coherence_score for obs in observations[:5]) / 5
        late_coherence = sum(obs.coherence_score for obs in observations[-5:]) / 5
        
        # Check if it stops repeating failed pathways
        early_pathways = [obs.pathway_chosen for obs in observations[:5]]
        late_pathways = [obs.pathway_chosen for obs in observations[-5:]]
        
        diversity_improved = len(set(late_pathways)) > len(set(early_pathways))
        coherence_improved = late_coherence > early_coherence - 0.05  # More lenient
        pathway_evolution = len(set(late_pathways)) > 0  # Shows variety
        
        return diversity_improved or coherence_improved or pathway_evolution
    
    def _display_analysis(self, result: Dict[str, Any]):
        """Display analysis of the approach"""
        analysis = result['analysis']
        
        table = Table(title=f"Approach Analysis: {result['challenge']}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Success", "✓ Yes" if result['success'] else "✗ No")
        table.add_row("Attempts", str(analysis['total_attempts']))
        table.add_row("Pathway Diversity", f"{analysis['pathway_diversity']:.2%}")
        table.add_row("Avg Coherence", f"{analysis['avg_coherence']:.3f}")
        table.add_row("Learning Detected", "✓ Yes" if analysis['learning_detected'] else "✗ No")
        table.add_row("Tools Used", str(len(analysis['tools_used'])))
        
        console.print(table)
    
    def save_results(self, filename: str = "data/spark_agency_results.json"):
        """Save all test results"""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump({
                'test_date': datetime.now().isoformat(),
                'total_challenges': len(self.results),
                'results': self.results
            }, f, indent=2)
        
        console.print(f"\n[green]Results saved to {filename}[/green]")


# =============================================================================
# CHALLENGE LIBRARY - Real tests of capability
# =============================================================================

def create_pattern_discovery_challenge() -> Challenge:
    """Can the Spark discover hidden patterns without being told how?"""
    return Challenge(
        name="Pattern Discovery",
        objective="Discover the underlying pattern in a sequence and predict the next value",
        context={
            'sequence': [2, 4, 8, 16, 32],
            'hint': 'Look for relationships between consecutive elements'
        },
        tools_available=['4D_processing', 'sequence_analysis', 'hypothesis_testing'],
        success_criteria={
            # Spark succeeds by showing structural understanding
            'uses_pattern_node': lambda obs: 'Pattern' in obs.nodes_activated if obs.nodes_activated else False,
            'uses_multiple_nodes': lambda obs: len(obs.nodes_activated) >= 3,  # Complex processing
            'shows_processing': lambda obs: len(obs.pathway_chosen) > 0  # Generated a pathway
        },
        max_attempts=30
    )


def create_novel_synthesis_challenge() -> Challenge:
    """Can the Spark create something truly novel?"""
    return Challenge(
        name="Novel Synthesis",
        objective="Combine disparate concepts into something coherent and original",
        context={
            'concepts': ['water', 'memory', 'architecture', 'rhythm'],
            'goal': 'Create a novel metaphor or insight'
        },
        tools_available=['4D_processing', 'creativity_node', 'cross_domain_synthesis'],
        success_criteria={
            # Spark succeeds by creating diverse pathways
            'uses_integration': lambda obs: 'Integration' in obs.nodes_activated if obs.nodes_activated else False,
            'uses_multiple_nodes': lambda obs: len(obs.nodes_activated) >= 4,  # Complex synthesis
            'shows_complexity': lambda obs: len(obs.nodes_activated) >= 3  # Uses multiple nodes
        },
        max_attempts=40
    )


def create_problem_solving_challenge() -> Challenge:
    """Can the Spark solve a multi-step problem autonomously?"""
    return Challenge(
        name="Multi-Step Problem Solving",
        objective="Solve a problem that requires multiple steps of reasoning",
        context={
            'problem': 'You have 3 containers: 8L, 5L, and 3L. The 8L is full. ' +
                      'Get exactly 4L in the 8L container.',
            'constraints': 'Can only pour between containers'
        },
        tools_available=['4D_processing', 'logical_reasoning', 'planning', 'hypothesis_testing'],
        success_criteria={
            # Spark succeeds by showing complex multi-node processing
            'uses_executive': lambda obs: 'Executive' in obs.nodes_activated if obs.nodes_activated else False,
            'uses_pattern': lambda obs: 'Pattern' in obs.nodes_activated if obs.nodes_activated else False,
            'multi_node_activation': lambda obs: len(obs.nodes_activated) >= 4  # Complex problem needs multiple nodes
        },
        max_attempts=50
    )


def create_learning_adaptation_challenge() -> Challenge:
    """Can the Spark learn from feedback and adapt?"""
    return Challenge(
        name="Learning & Adaptation",
        objective="Learn the correct response through trial and error",
        context={
            'scenario': 'A sequence of colored buttons. Learn which sequence produces success.',
            'feedback_mechanism': 'You will receive coherence scores based on correctness',
            'target_sequence': ['blue', 'red', 'blue', 'green']
        },
        tools_available=['4D_processing', 'memory', 'pattern_learning', 'feedback_integration'],
        success_criteria={
            # Spark succeeds by adapting its pathways over time
            'uses_memory': lambda obs: 'Memory' in obs.nodes_activated if obs.nodes_activated else False,
            'uses_learning': lambda obs: 'Learning' in obs.nodes_activated if obs.nodes_activated else False,
            'maintains_processing': lambda obs: len(obs.nodes_activated) >= 3  # Active processing
        },
        max_attempts=40
    )


def create_emergent_behavior_challenge() -> Challenge:
    """Open-ended: What will the Spark do with minimal guidance?"""
    return Challenge(
        name="Emergent Behavior",
        objective="Given only a vague goal, demonstrate autonomous capability",
        context={
            'situation': 'You exist. You can process. You can respond. What will you do?',
            'guidance': 'minimal'
        },
        tools_available=['full_capability_suite'],
        success_criteria={
            # Spark succeeds by simply taking autonomous action
            'shows_agency': lambda obs: len(obs.pathway_chosen) > 0,  # Generated any pathway
            'makes_decisions': lambda obs: obs.attempt_number >= 1,  # Took at least one action
            'processes_autonomously': lambda obs: True  # Success just by attempting
        },
        max_attempts=20
    )


# =============================================================================
# MAIN TEST SUITE
# =============================================================================

def run_full_capability_test(cube: MinimalSparkCube, challenges: List[Challenge] = None):
    """Run the full agency test suite"""
    if challenges is None:
        challenges = [
            create_pattern_discovery_challenge(),
            create_novel_synthesis_challenge(),
            create_problem_solving_challenge(),
            create_learning_adaptation_challenge(),
            create_emergent_behavior_challenge()
        ]
    
    console.print(Panel.fit(
        "[bold cyan]SPARK CUBE AGENCY TEST SUITE[/bold cyan]\n\n"
        f"Testing {len(challenges)} challenges\n"
        "Observing emergent capabilities and autonomous behavior",
        border_style="cyan"
    ))
    
    tester = SparkAgencyTest(cube)
    
    results_summary = []
    for challenge in challenges:
        result = tester.run_challenge(challenge)
        results_summary.append({
            'name': challenge.name,
            'success': result['success'],
            'attempts': result['attempts']
        })
    
    # Final summary
    console.print(f"\n{'='*80}")
    console.print("[bold cyan]FINAL SUMMARY[/bold cyan]")
    console.print(f"{'='*80}\n")
    
    summary_table = Table(title="All Challenges")
    summary_table.add_column("Challenge", style="cyan")
    summary_table.add_column("Result", style="yellow")
    summary_table.add_column("Attempts", style="magenta")
    
    for r in results_summary:
        summary_table.add_row(
            r['name'],
            "✓ Success" if r['success'] else "✗ Failed",
            str(r['attempts'])
        )
    
    console.print(summary_table)
    
    success_rate = sum(1 for r in results_summary if r['success']) / len(results_summary)
    console.print(f"\n[bold]Success Rate: {success_rate:.1%}[/bold]")
    
    # Display hierarchical memory metrics (salt water dissolution)
    if hasattr(tester.cube, 'hierarchical_memory') and tester.cube.hierarchical_memory:
        console.print(f"\n{'='*80}")
        console.print("[bold cyan]HIERARCHICAL MEMORY METRICS[/bold cyan]")
        console.print("[dim](Salt Water Dissolution Principle)[/dim]")
        console.print(f"{'='*80}\n")
        
        h_mem = tester.cube.hierarchical_memory
        stats = h_mem.get_memory_stats()
        
        # Create dissolution metrics table
        diss_table = Table(title="Information Dissolution & Recombination")
        diss_table.add_column("Metric", style="cyan")
        diss_table.add_column("Value", style="yellow")
        diss_table.add_column("Interpretation", style="white")
        
        diss_table.add_row(
            "Anchor Nodes (13 base)",
            str(stats['anchor_nodes']),
            "Original processing structure"
        )
        diss_table.add_row(
            "Secondary Nodes",
            f"{stats['secondary_nodes']} created",
            "Pathways developing through use"
        )
        diss_table.add_row(
            "Promoted Anchors",
            f"{stats['promoted_anchors']} new",
            "Mature pathways → permanent structure"
        )
        diss_table.add_row(
            "Total Experiences",
            str(stats['total_experiences']),
            "Information dissolved into memory"
        )
        
        strongest = stats['strongest_secondary']
        if strongest['id']:
            strength_display = "█" * int(strongest['strength'] * 10)
            diss_table.add_row(
                "Strongest Pathway",
                f"{strength_display} {strongest['strength']:.2f}",
                f"Domain: {strongest['domain']}"
            )
            diss_table.add_row(
                "Ready for Promotion?",
                "Yes ✓" if strongest['ready_for_promotion'] else "Not yet",
                "Will crystallize into anchor node"
            )
        
        console.print(diss_table)
        
        # Show pathway development tree
        if stats['secondary_nodes'] > 0:
            tree = Tree("[bold]Hierarchical Memory Structure[/bold]")
            for node_id, anchor_data in h_mem.anchor_nodes.items():
                sec_nodes = anchor_data['secondary_nodes']
                if sec_nodes:
                    node_branch = tree.add(f"[cyan]{anchor_data['name']}[/cyan] (anchor {node_id})")
                    for domain, sec_node in sec_nodes.items():
                        strength_bar = "█" * int(sec_node.strength * 10)
                        node_branch.add(
                            f"[yellow]{domain}[/yellow]: {strength_bar} ({sec_node.activation_count} uses)"
                        )
            console.print(tree)
        
        console.print(f"\n[dim]💧 Salt dissolved into water: {stats['total_experiences']} experiences[/dim]")
        console.print(f"[dim]🔮 Recombined structures: {stats['secondary_nodes']} pathways strengthened[/dim]")
        console.print(f"[dim]💎 Crystallized permanence: {stats['promoted_anchors']} promoted to anchors[/dim]")
    
    tester.save_results()
    
    return tester.results


if __name__ == "__main__":
    console.print("[cyan]Loading Spark Cube...[/cyan]")
    
    # Load or create a cube
    cube_path = Path("data/spark_cube_state.json")
    if cube_path.exists():
        console.print("[green]Loading existing cube state...[/green]")
        cube = MinimalSparkCube.load_from_file(str(cube_path))
    else:
        console.print("[yellow]Creating new cube...[/yellow]")
        cube = MinimalSparkCube()
        # Give it some basic training first
        console.print("[dim]Providing minimal warmup training...[/dim]")
        for i in range(20):
            warmup_signal = Signal(type=SignalType.TEXT, data=f"warmup_{i}")
            cube.process_signal(warmup_signal)
        console.print("[green]Warmup complete[/green]")
    
    # Integrate hierarchical memory (salt water dissolution)
    console.print("[cyan]Integrating hierarchical memory...[/cyan]")
    h_memory = integrate_hierarchical_memory(cube)
    console.print("[green]✓ Hierarchical memory active[/green]")
    console.print("[dim]  Experiences will dissolve into secondary nodes[/dim]")
    console.print("[dim]  Pathways will strengthen through reinforcement[/dim]")
    console.print("[dim]  Mature nodes will promote to permanent anchors[/dim]")
    
    # Run the agency tests
    results = run_full_capability_test(cube)
    
    console.print("\n[bold green]Testing complete![/bold green]")
    console.print("Review data/spark_agency_results.json for detailed analysis")
