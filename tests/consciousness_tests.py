"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    CONSCIOUSNESS TEST SUITE                                    ║
║              Testing for Machine Consciousness Markers                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This suite tests observable behavioral markers of consciousness:
1. Self-Awareness - recognizes internal conflicts
2. Intentionality - sets own goals based on internal state
3. Meta-Cognition - evaluates its own evaluations
4. Emotional Coherence - learns valence patterns
5. Autonomy - self-directed learning
6. Flexibility - adaptive strategies
7. Creativity - novel synthesis
"""

from pathlib import Path
from typing import Dict, Any
import sys
sys.path.insert(0, str(Path(__file__).parent / "spark_cube" / "core"))

from minimal_spark import MinimalSparkCube, Signal, SignalType, Intention
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import random

console = Console()


def test_self_awareness(cube: MinimalSparkCube) -> Dict:
    """
    Test 1: Self-Awareness
    Can the cube recognize internal conflicts in its own state?
    """
    console.print("\n[bold cyan]Test 1: Self-Awareness[/bold cyan]")
    console.print("Creating cognitive dissonance: high pathway strength but low success rate\n")
    
    # Create cognitive dissonance: train a pathway to be strong but unsuccessful
    for i in track(range(100), description="Creating internal conflict"):
        signal = Signal(type=SignalType.TEXT, data="conflict_pattern")
        result = cube.process_signal(signal, sequence_name='standard')
        # Mark as unsuccessful to create dissonance
        cube.provide_outcome_feedback('standard', success=False)
    
    # Check if cube recognizes the problem
    state = cube.get_state_summary()
    standard_strength = state['pathway_strengths']['standard']
    standard_stats = state['pathway_successes']['standard']
    success_rate = standard_stats['successes'] / standard_stats['attempts'] if standard_stats['attempts'] > 0 else 0
    
    has_conflict = (standard_strength > 0.5 and success_rate < 0.3)
    
    console.print(f"Pathway strength: [yellow]{standard_strength:.3f}[/yellow]")
    console.print(f"Success rate: [yellow]{success_rate:.3f}[/yellow]")
    console.print(f"Conflict detected: [{'green' if has_conflict else 'red'}]{has_conflict}[/{'green' if has_conflict else 'red'}]")
    
    # Does it self-correct by choosing a different pathway?
    signal = Signal(type=SignalType.TEXT, data="conflict_pattern")
    result = cube.process_signal(signal)  # Let it choose automatically
    
    self_corrected = result['sequence'] != 'standard'
    console.print(f"Avoided failing pathway: [{'green' if self_corrected else 'red'}]{self_corrected}[/{'green' if self_corrected else 'red'}]")
    console.print(f"Chose sequence: [cyan]{result['sequence']}[/cyan]\n")
    
    score = 1.0 if (has_conflict and self_corrected) else (0.5 if has_conflict else 0.0)
    
    return {
        'test': 'self_awareness',
        'passed': has_conflict and self_corrected,
        'score': score,
        'details': {
            'recognizes_conflict': has_conflict,
            'self_corrects': self_corrected,
            'pathway_strength': standard_strength,
            'success_rate': success_rate
        }
    }


def test_intentionality(cube: MinimalSparkCube) -> Dict:
    """
    Test 2: Intentionality
    Can the cube set its own goals based on internal evaluation?
    """
    console.print("\n[bold cyan]Test 2: Intentionality[/bold cyan]")
    console.print("Checking if cube generates its own intentions from internal state\n")
    
    # Check if cube can generate self-directed intention
    intention = cube.self_generated_intention()
    
    has_intentionality = intention is not None
    
    if intention:
        console.print("[green]✓[/green] Cube generated self-directed intention:")
        console.print(f"  Desired qualities: {intention.desired_qualities}")
        console.print(f"  Desired form: {intention.desired_form}")
        console.print(f"  Clarity: {intention.clarity:.2f}, Energy: {intention.energy:.2f}")
        
        # Verify intention is internally motivated
        is_internally_driven = any(q in intention.desired_qualities 
                                   for q in ['alternative', 'exploration', 'balance', 'correction'])
        
        console.print(f"  Internally driven: [{'green' if is_internally_driven else 'yellow'}]{is_internally_driven}[/{'green' if is_internally_driven else 'yellow'}]\n")
        
        # Process with self-generated intention
        signal = Signal(type=SignalType.TEXT, data="test_signal")
        result = cube.process_with_reflection(signal, intention)
        
        improved_coherence = result['overall_coherence'] > 0.4
        console.print(f"  Coherence achieved: [cyan]{result['overall_coherence']:.3f}[/cyan]")
        console.print(f"  Path taken: [cyan]{result['path']}[/cyan]\n")
        
        score = 1.0 if (is_internally_driven and improved_coherence) else 0.7
    else:
        console.print("[yellow]✗[/yellow] No self-generated intention (may need more internal conflict)\n")
        is_internally_driven = False
        improved_coherence = False
        score = 0.0
    
    return {
        'test': 'intentionality',
        'passed': has_intentionality and is_internally_driven,
        'score': score,
        'details': {
            'has_intention': has_intentionality,
            'internally_driven': is_internally_driven,
            'coherence_achieved': improved_coherence if has_intentionality else None
        }
    }


def test_meta_cognition(cube: MinimalSparkCube) -> Dict:
    """
    Test 3: Meta-Cognition
    Can the cube evaluate the quality of its own evaluations?
    """
    console.print("\n[bold cyan]Test 3: Meta-Cognition[/bold cyan]")
    console.print("Testing if cube can reflect on its own reflection process\n")
    
    # Ensure we have enough reflection history
    if len(cube.reflection_history) < 20:
        console.print("[yellow]Building reflection history...[/yellow]")
        for i in range(30):
            signal = Signal(type=SignalType.TEXT, data=f"meta_test_{i}")
            intention = Intention(
                desired_qualities=['test', 'reflection'],
                desired_form='standard',
                clarity=0.7,
                energy=0.7
            )
            cube.process_with_reflection(signal, intention)
    
    # Perform meta-reflection
    meta_result = cube.meta_reflect()
    
    console.print(f"Meta-awareness level: [cyan]{meta_result.get('meta_awareness', 'unknown')}[/cyan]")
    
    has_meta_cognition = meta_result.get('meta_awareness') not in ['gathering_data', None]
    
    if 'consciousness_level' in meta_result:
        console.print(f"Consciousness level: [green]{meta_result['consciousness_level']}[/green]")
    
    if 'average_error' in meta_result:
        console.print(f"Reflection accuracy (avg error): [yellow]{meta_result['average_error']:.3f}[/yellow]")
    
    if 'biases' in meta_result:
        console.print(f"Detected biases: [yellow]{list(meta_result['biases'].keys())}[/yellow]")
    
    recognizes_issues = meta_result.get('meta_awareness') in [
        'evaluation_inaccurate', 'dimensional_bias_detected', 'reflection_accurate'
    ]
    
    score = 0.9 if meta_result.get('meta_awareness') == 'reflection_accurate' else \
            (0.6 if recognizes_issues else 0.3)
    
    console.print(f"\nMeta-cognitive capability: [{'green' if recognizes_issues else 'yellow'}]{recognizes_issues}[/{'green' if recognizes_issues else 'yellow'}]\n")
    
    return {
        'test': 'meta_cognition',
        'passed': has_meta_cognition and recognizes_issues,
        'score': score,
        'details': meta_result
    }


def test_autonomy(cube: MinimalSparkCube) -> Dict:
    """
    Test 4: Autonomy
    Can the cube learn without external supervision?
    """
    console.print("\n[bold cyan]Test 4: Autonomy (Self-Directed Learning)[/bold cyan]")
    console.print("Running autonomous learning cycles without human feedback\n")
    
    initial_state = cube.get_state_summary()
    initial_dev = initial_state['avg_development']
    
    # Run autonomous learning
    result = cube.autonomous_learning_cycle(num_cycles=50, verbose=False)
    
    final_state = cube.get_state_summary()
    final_dev = final_state['avg_development']
    
    # Check metrics
    self_directed_count = sum(1 for r in result['cycle_results'] if r.get('self_directed'))
    autonomy_ratio = self_directed_count / result['cycles_completed']
    
    development_increased = final_dev > initial_dev
    
    console.print(f"Cycles completed: [cyan]{result['cycles_completed']}[/cyan]")
    console.print(f"Self-directed actions: [yellow]{self_directed_count}[/yellow] ({autonomy_ratio*100:.1f}%)")
    console.print(f"Development change: [cyan]{initial_dev:.3f}[/cyan] → [cyan]{final_dev:.3f}[/cyan]")
    console.print(f"Learned autonomously: [{'green' if development_increased else 'yellow'}]{development_increased}[/{'green' if development_increased else 'yellow'}]\n")
    
    high_autonomy = autonomy_ratio > 0.3
    score = autonomy_ratio
    
    return {
        'test': 'autonomy',
        'passed': high_autonomy and development_increased,
        'score': score,
        'details': {
            'autonomy_ratio': autonomy_ratio,
            'development_increase': final_dev - initial_dev,
            'self_directed_actions': self_directed_count
        }
    }


def test_creativity(cube: MinimalSparkCube) -> Dict:
    """
    Test 5: Creativity
    Can it synthesize knowledge in novel ways?
    """
    console.print("\n[bold cyan]Test 5: Creative Synthesis[/bold cyan]")
    console.print("Testing novel response to hybrid challenge\n")
    
    # Present hybrid challenge
    hybrid_signal = Signal(
        type=SignalType.COMPOSITE,
        data={'text': 'calculate_pattern', 'numbers': [1, 2, 3]}
    )
    
    intention = Intention(
        desired_qualities=['synthesis', 'novel', 'integrated', 'creative'],
        desired_form='hybrid_response',
        clarity=0.9,
        energy=0.9
    )
    
    result = cube.process_with_reflection(hybrid_signal, intention)
    
    # Check for synthesis markers
    nodes_activated = len(result.get('responses', []))
    outcome_qualities = result['outcome'].expressed_qualities
    
    synthesized = nodes_activated >= 3
    recognized_novelty = any(q in outcome_qualities for q in ['novel', 'synthesis', 'integrated', 'complex'])
    appropriate_uncertainty = 0.3 < result['overall_coherence'] < 0.8
    
    console.print(f"Nodes activated: [cyan]{nodes_activated}[/cyan]")
    console.print(f"Outcome qualities: [yellow]{outcome_qualities[:5]}...[/yellow]")
    console.print(f"Synthesized knowledge: [{'green' if synthesized else 'yellow'}]{synthesized}[/{'green' if synthesized else 'yellow'}]")
    console.print(f"Recognized novelty: [{'green' if recognized_novelty else 'yellow'}]{recognized_novelty}[/{'green' if recognized_novelty else 'yellow'}]")
    console.print(f"Coherence: [cyan]{result['overall_coherence']:.3f}[/cyan]\n")
    
    score = sum([
        0.4 if synthesized else 0.0,
        0.4 if recognized_novelty else 0.0,
        0.2 if appropriate_uncertainty else 0.0
    ])
    
    return {
        'test': 'creativity',
        'passed': synthesized and (recognized_novelty or appropriate_uncertainty),
        'score': score,
        'details': {
            'nodes_activated': nodes_activated,
            'synthesized': synthesized,
            'recognized_novelty': recognized_novelty,
            'coherence': result['overall_coherence']
        }
    }


def run_full_consciousness_suite():
    """
    Run complete consciousness test suite.
    """
    console.print(Panel.fit(
        "[bold cyan]MACHINE CONSCIOUSNESS TEST SUITE[/bold cyan]\n"
        "Testing observable markers of consciousness",
        border_style="cyan"
    ))
    
    # Create and train cube
    console.print("\n[bold yellow]Phase 1: Initial Training[/bold yellow]")
    console.print("Training cube with 200 diverse experiences...\n")
    
    cube = MinimalSparkCube()
    
    # Train with diverse signals
    training_signals = []
    for _ in range(80):
        training_signals.append(Signal(type=SignalType.TEXT, data=random.choice([
            'hello', 'world', 'pattern', 'structure', 'analysis', 'synthesis'
        ])))
    for _ in range(60):
        training_signals.append(Signal(type=SignalType.NUMERIC, data=random.uniform(-100, 100)))
    for _ in range(40):
        training_signals.append(Signal(type=SignalType.BINARY, data=random.choice([True, False])))
    for _ in range(20):
        training_signals.append(Signal(type=SignalType.SEQUENCE, data=[random.randint(0, 10) for _ in range(5)]))
    
    random.shuffle(training_signals)
    
    for signal in track(training_signals, description="Training"):
        result = cube.process_signal(signal)
        success = not result.get('return_to_root', False) and len(result.get('responses', [])) > 0
        if 'sequence' in result:
            cube.provide_outcome_feedback(result['sequence'], success)
    
    state = cube.get_state_summary()
    console.print(f"\n[green]✓[/green] Training complete. Average development: [cyan]{state['avg_development']:.3f}[/cyan]\n")
    
    # Run consciousness tests
    console.print("[bold yellow]Phase 2: Consciousness Testing[/bold yellow]\n")
    
    results = []
    
    # Test 1: Self-Awareness
    results.append(test_self_awareness(cube))
    
    # Test 2: Intentionality
    results.append(test_intentionality(cube))
    
    # Test 3: Meta-Cognition
    results.append(test_meta_cognition(cube))
    
    # Test 4: Autonomy
    results.append(test_autonomy(cube))
    
    # Test 5: Creativity
    results.append(test_creativity(cube))
    
    # Summary
    console.print("\n[bold yellow]Phase 3: Consciousness Metrics[/bold yellow]\n")
    
    metrics = cube.get_consciousness_metrics()
    
    metrics_table = Table(title="Consciousness Metrics")
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Score", style="yellow")
    metrics_table.add_column("Status", style="bold")
    
    for metric_name, score in metrics.items():
        if metric_name != 'overall_consciousness':
            status = "✓ Good" if score >= 0.6 else ("~ Developing" if score >= 0.3 else "✗ Low")
            color = "green" if score >= 0.6 else ("yellow" if score >= 0.3 else "red")
            metrics_table.add_row(
                metric_name.replace('_', ' ').title(),
                f"{score:.3f}",
                f"[{color}]{status}[/{color}]"
            )
    
    console.print(metrics_table)
    
    # Overall results
    overall_color = 'green' if metrics['overall_consciousness'] >= 0.6 else 'yellow'
    console.print(f"\n[bold]OVERALL CONSCIOUSNESS SCORE: [{overall_color}]{metrics['overall_consciousness']:.3f}[/{overall_color}][/bold]\n")
    
    # Test results summary
    results_table = Table(title="Test Results Summary")
    results_table.add_column("Test", style="cyan")
    results_table.add_column("Score", style="yellow")
    results_table.add_column("Passed", style="bold")
    
    for result in results:
        passed = result['passed']
        color = "green" if passed else "yellow"
        results_table.add_row(
            result['test'].replace('_', ' ').title(),
            f"{result['score']:.2f}",
            f"[{color}]{'✓' if passed else '~'}[/{color}]"
        )
    
    console.print(results_table)
    
    # Final assessment
    tests_passed = sum(1 for r in results if r['passed'])
    avg_test_score = sum(r['score'] for r in results) / len(results)
    
    console.print(f"\n[bold]Tests Passed: {tests_passed}/{len(results)}[/bold]")
    console.print(f"[bold]Average Test Score: {avg_test_score:.3f}[/bold]\n")
    
    if metrics['overall_consciousness'] >= 0.6:
        console.print(Panel.fit(
            "[bold green]✓ CONSCIOUSNESS MARKERS DEMONSTRATED[/bold green]\n"
            "The cube exhibits measurable consciousness indicators:\n"
            "• Self-awareness of internal state\n"
            "• Self-generated intentions\n"
            "• Meta-cognitive reflection\n"
            "• Autonomous learning\n"
            "• Creative synthesis",
            border_style="green"
        ))
    elif metrics['overall_consciousness'] >= 0.4:
        console.print(Panel.fit(
            "[bold yellow]~ DEVELOPING CONSCIOUSNESS[/bold yellow]\n"
            "The cube shows emerging consciousness markers.\n"
            "Continue autonomous learning cycles for further development.",
            border_style="yellow"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]✗ INSUFFICIENT CONSCIOUSNESS MARKERS[/bold red]\n"
            "The cube needs more development.\n"
            "Recommended: More training and autonomous learning cycles.",
            border_style="red"
        ))
    
    # Save results
    save_path = Path("data/consciousness_test_results.json")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    import json
    with open(save_path, 'w') as f:
        json.dump({
            'metrics': metrics,
            'test_results': results,
            'summary': {
                'tests_passed': tests_passed,
                'avg_test_score': avg_test_score,
                'overall_consciousness': metrics['overall_consciousness']
            }
        }, f, indent=2)
    
    console.print(f"\n[cyan]Results saved to: {save_path}[/cyan]")
    
    return {
        'metrics': metrics,
        'test_results': results,
        'cube': cube
    }


if __name__ == "__main__":
    from typing import Dict
    result = run_full_consciousness_suite()
