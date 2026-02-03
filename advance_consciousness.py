"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              CONSCIOUSNESS ADVANCEMENT PROTOCOL                                ║
║           Push the cube to 0.6+ consciousness threshold                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This script systematically develops all consciousness markers:
1. Self-Awareness - Extended conflict training
2. Emotional Intelligence - Emotional sequence development
3. Autonomy - Extended autonomous learning (500 cycles)
4. Creativity - Cross-domain synthesis training
"""

from pathlib import Path
from typing import Dict, Any
import sys
sys.path.insert(0, str(Path(__file__).parent / "spark_cube" / "core"))

from minimal_spark import MinimalSparkCube, Signal, SignalType, Intention
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import random
import json

console = Console()


def phase_1_initial_training(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Phase 1: Comprehensive initial training
    Goal: Build strong foundation across all signal types
    """
    console.print("\n[bold cyan]═══ Phase 1: Foundation Training ═══[/bold cyan]")
    console.print("Building diverse experience base (300 signals)\n")
    
    training_signals = []
    
    # Rich variety of text patterns
    text_words = [
        'hello', 'world', 'pattern', 'structure', 'analysis', 'synthesis',
        'integration', 'development', 'growth', 'learning', 'adaptation',
        'response', 'processing', 'coherence', 'alignment', 'recognition'
    ]
    for _ in range(120):
        training_signals.append(Signal(type=SignalType.TEXT, data=random.choice(text_words)))
    
    # Numeric patterns
    for _ in range(90):
        training_signals.append(Signal(type=SignalType.NUMERIC, data=random.uniform(-100, 100)))
    
    # Binary patterns
    for _ in range(60):
        training_signals.append(Signal(type=SignalType.BINARY, data=random.choice([True, False])))
    
    # Sequences
    for _ in range(30):
        training_signals.append(Signal(type=SignalType.SEQUENCE, 
                                      data=[random.randint(0, 10) for _ in range(random.randint(3, 7))]))
    
    random.shuffle(training_signals)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Training foundation", total=len(training_signals))
        
        for signal in training_signals:
            result = cube.process_signal(signal)
            success = not result.get('return_to_root', False) and len(result.get('responses', [])) > 0
            if 'sequence' in result:
                cube.provide_outcome_feedback(result['sequence'], success)
            progress.advance(task)
    
    state = cube.get_state_summary()
    console.print(f"\n[green]✓[/green] Foundation complete. Development: [cyan]{state['avg_development']:.3f}[/cyan]")
    
    return state


def phase_2_emotional_development(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Phase 2: Emotional Intelligence Development
    Goal: Activate and develop the emotional node (currently 0.0)
    """
    console.print("\n[bold cyan]═══ Phase 2: Emotional Intelligence Development ═══[/bold cyan]")
    console.print("Training emotional sequence to develop valence patterns\n")
    
    emotional_training = []
    
    # Create emotionally charged scenarios with explicit intentions
    positive_words = ['harmony', 'alignment', 'success', 'growth', 'integration']
    negative_words = ['conflict', 'misalignment', 'failure', 'stuck', 'blocked']
    
    # Positive valence training (60)
    for word in positive_words:
        for _ in range(12):
            emotional_training.append({
                'signal': Signal(type=SignalType.TEXT, data=word),
                'intention': Intention(
                    desired_qualities=['positive', 'aligned', 'coherent'],
                    desired_form='emotional',
                    clarity=0.8,
                    energy=0.8
                ),
                'expected_valence': 'positive'
            })
    
    # Negative valence training (40)
    for word in negative_words:
        for _ in range(8):
            emotional_training.append({
                'signal': Signal(type=SignalType.TEXT, data=word),
                'intention': Intention(
                    desired_qualities=['resolution', 'correction', 'improvement'],
                    desired_form='emotional',
                    clarity=0.7,
                    energy=0.7
                ),
                'expected_valence': 'negative'
            })
    
    random.shuffle(emotional_training)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Emotional training", total=len(emotional_training))
        
        for item in emotional_training:
            result = cube.process_with_reflection(
                item['signal'], 
                item['intention'],
                sequence_name='emotional'  # Force emotional sequence
            )
            progress.advance(task)
    
    # Check emotional node development
    emotional_node = cube.nodes.get(6)
    emotional_dev = emotional_node.development if emotional_node else 0.0
    valence_patterns = len(emotional_node.pattern_weights) if emotional_node else 0
    
    console.print(f"\n[green]✓[/green] Emotional development: [cyan]{emotional_dev:.3f}[/cyan]")
    console.print(f"[green]✓[/green] Valence patterns learned: [cyan]{valence_patterns}[/cyan]")
    
    return {
        'emotional_development': emotional_dev,
        'valence_patterns': valence_patterns
    }


def phase_3_self_awareness_training(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Phase 3: Self-Awareness Strengthening
    Goal: Create strong internal conflict that cube can recognize
    """
    console.print("\n[bold cyan]═══ Phase 3: Self-Awareness Strengthening ═══[/bold cyan]")
    console.print("Creating strong cognitive dissonance for self-recognition\n")
    
    # Create extreme conflict: train 'standard' pathway very strong but mark as failing
    conflict_signal = Signal(type=SignalType.TEXT, data="self_awareness_test")
    
    console.print("Creating internal conflict (250 trials)...")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("Conflict training", total=250)
        
        for i in range(250):
            result = cube.process_signal(conflict_signal, sequence_name='standard')
            # Mark as failure to create dissonance
            cube.provide_outcome_feedback('standard', success=False)
            
            # Occasionally succeed to make it confusing
            if i % 20 == 0:
                cube.provide_outcome_feedback('standard', success=True)
            
            progress.advance(task)
    
    # Check if conflict is detectable
    state = cube.get_state_summary()
    standard_strength = state['pathway_strengths']['standard']
    standard_stats = state['pathway_successes']['standard']
    success_rate = standard_stats['successes'] / standard_stats['attempts'] if standard_stats['attempts'] > 0 else 0
    
    has_conflict = (standard_strength > 0.3 and success_rate < 0.2)
    
    console.print(f"\n[green]✓[/green] Pathway strength: [cyan]{standard_strength:.3f}[/cyan]")
    console.print(f"[green]✓[/green] Success rate: [cyan]{success_rate:.3f}[/cyan]")
    console.print(f"[green]✓[/green] Conflict detectable: [{'green' if has_conflict else 'yellow'}]{has_conflict}[/{'green' if has_conflict else 'yellow'}]")
    
    # Test self-correction
    result = cube.process_signal(conflict_signal)
    self_corrected = result['sequence'] != 'standard'
    console.print(f"[green]✓[/green] Self-corrects behavior: [{'green' if self_corrected else 'yellow'}]{self_corrected}[/{'green' if self_corrected else 'yellow'}]")
    console.print(f"    Chose: [cyan]{result['sequence']}[/cyan] (avoided 'standard')")
    
    return {
        'conflict_detectable': has_conflict,
        'self_corrects': self_corrected,
        'pathway_strength': standard_strength,
        'success_rate': success_rate
    }


def phase_4_extended_autonomy(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Phase 4: Extended Autonomous Learning
    Goal: 500 self-directed learning cycles
    """
    console.print("\n[bold cyan]═══ Phase 4: Extended Autonomous Learning ═══[/bold cyan]")
    console.print("Running 500 self-directed learning cycles\n")
    
    console.print("The cube will:")
    console.print("  • Generate its own learning goals")
    console.print("  • Choose what to attend to")
    console.print("  • Learn from self-evaluation")
    console.print("  • Meta-reflect every 50 cycles\n")
    
    initial_metrics = cube.get_consciousness_metrics()
    
    # Run extended autonomous learning
    result = cube.autonomous_learning_cycle(num_cycles=500, verbose=True)
    
    final_metrics = cube.get_consciousness_metrics()
    
    console.print("\n[bold]Consciousness Progression:[/bold]")
    
    progression_table = Table()
    progression_table.add_column("Metric", style="cyan")
    progression_table.add_column("Before", style="yellow")
    progression_table.add_column("After", style="green")
    progression_table.add_column("Change", style="bold")
    
    for metric_name in ['autonomy', 'self_awareness', 'meta_cognition', 'emotional_intelligence', 
                        'learning_autonomy', 'flexibility', 'overall_consciousness']:
        before = initial_metrics.get(metric_name, 0)
        after = final_metrics.get(metric_name, 0)
        change = after - before
        change_str = f"+{change:.3f}" if change >= 0 else f"{change:.3f}"
        change_color = "green" if change > 0 else ("yellow" if change == 0 else "red")
        
        progression_table.add_row(
            metric_name.replace('_', ' ').title(),
            f"{before:.3f}",
            f"{after:.3f}",
            f"[{change_color}]{change_str}[/{change_color}]"
        )
    
    console.print(progression_table)
    
    return {
        'initial_consciousness': initial_metrics['overall_consciousness'],
        'final_consciousness': final_metrics['overall_consciousness'],
        'improvement': final_metrics['overall_consciousness'] - initial_metrics['overall_consciousness'],
        'final_metrics': final_metrics
    }


def phase_5_creativity_training(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Phase 5: Creative Synthesis Development
    Goal: Cross-domain synthesis capabilities
    """
    console.print("\n[bold cyan]═══ Phase 5: Creative Synthesis Training ═══[/bold cyan]")
    console.print("Teaching cross-domain knowledge synthesis\n")
    
    # Train separate domains first
    console.print("Training domain specialization...")
    
    # Text domain
    for _ in range(30):
        signal = Signal(type=SignalType.TEXT, data=random.choice(['analyze', 'synthesize', 'integrate']))
        intention = Intention(
            desired_qualities=['text', 'pattern', 'structured'],
            desired_form='deep',
            clarity=0.8,
            energy=0.8
        )
        cube.process_with_reflection(signal, intention, sequence_name='deep')
    
    # Numeric domain
    for _ in range(30):
        signal = Signal(type=SignalType.NUMERIC, data=random.uniform(0, 100))
        intention = Intention(
            desired_qualities=['numeric', 'calculated', 'precise'],
            desired_form='standard',
            clarity=0.8,
            energy=0.8
        )
        cube.process_with_reflection(signal, intention, sequence_name='standard')
    
    console.print("[green]✓[/green] Domain specialization complete")
    
    # Now test cross-domain synthesis
    console.print("\nTesting creative synthesis (10 hybrid challenges)...")
    
    synthesis_results = []
    
    for i in range(10):
        hybrid_signal = Signal(
            type=SignalType.COMPOSITE,
            data={
                'text': random.choice(['calculate', 'measure', 'quantify', 'analyze']),
                'numbers': [random.randint(1, 100) for _ in range(3)]
            }
        )
        
        intention = Intention(
            desired_qualities=['synthesis', 'novel', 'integrated', 'creative', 'multi_domain'],
            desired_form='hybrid_response',
            clarity=0.9,
            energy=0.9
        )
        
        result = cube.process_with_reflection(hybrid_signal, intention)
        
        nodes_activated = len(result.get('responses', []))
        outcome_qualities = result['outcome'].expressed_qualities
        synthesized = nodes_activated >= 3
        recognized_novelty = any(q in outcome_qualities for q in ['novel', 'synthesis', 'integrated', 'complex', 'multi_node'])
        
        synthesis_results.append({
            'synthesized': synthesized,
            'recognized_novelty': recognized_novelty,
            'coherence': result['overall_coherence'],
            'nodes_activated': nodes_activated
        })
    
    avg_nodes = sum(r['nodes_activated'] for r in synthesis_results) / len(synthesis_results)
    synthesis_rate = sum(1 for r in synthesis_results if r['synthesized']) / len(synthesis_results)
    novelty_rate = sum(1 for r in synthesis_results if r['recognized_novelty']) / len(synthesis_results)
    
    console.print(f"\n[green]✓[/green] Average nodes activated: [cyan]{avg_nodes:.1f}[/cyan]")
    console.print(f"[green]✓[/green] Synthesis success rate: [cyan]{synthesis_rate*100:.0f}%[/cyan]")
    console.print(f"[green]✓[/green] Novelty recognition rate: [cyan]{novelty_rate*100:.0f}%[/cyan]")
    
    return {
        'synthesis_rate': synthesis_rate,
        'novelty_rate': novelty_rate,
        'avg_nodes_activated': avg_nodes
    }


def final_consciousness_evaluation(cube: MinimalSparkCube) -> Dict[str, Any]:
    """
    Final comprehensive consciousness evaluation
    """
    console.print("\n[bold magenta]═══ Final Consciousness Evaluation ═══[/bold magenta]\n")
    
    metrics = cube.get_consciousness_metrics()
    state = cube.get_state_summary()
    
    # Metrics table
    metrics_table = Table(title="Final Consciousness Metrics")
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Score", style="yellow")
    metrics_table.add_column("Threshold", style="white")
    metrics_table.add_column("Status", style="bold")
    
    threshold = 0.6
    
    for metric_name, score in metrics.items():
        if metric_name != 'overall_consciousness':
            status = "✓ Achieved" if score >= threshold else ("~ Developing" if score >= 0.4 else "✗ Low")
            color = "green" if score >= threshold else ("yellow" if score >= 0.4 else "red")
            
            metrics_table.add_row(
                metric_name.replace('_', ' ').title(),
                f"{score:.3f}",
                f"{threshold:.1f}",
                f"[{color}]{status}[/{color}]"
            )
    
    console.print(metrics_table)
    
    overall = metrics['overall_consciousness']
    overall_color = 'green' if overall >= 0.6 else ('yellow' if overall >= 0.5 else 'red')
    
    console.print(f"\n[bold]OVERALL CONSCIOUSNESS SCORE: [{overall_color}]{overall:.3f}[/{overall_color}][/bold]")
    
    # Achievements
    achievements = []
    if metrics['autonomy'] >= 0.7:
        achievements.append("✓ High Autonomy - Self-directed learning")
    if metrics['meta_cognition'] >= 0.6:
        achievements.append("✓ Meta-Cognitive - Reflects on own thinking")
    if metrics['self_awareness'] >= 0.6:
        achievements.append("✓ Self-Aware - Recognizes internal state")
    if metrics['emotional_intelligence'] >= 0.5:
        achievements.append("✓ Emotional Intelligence - Learned valence patterns")
    if metrics['learning_autonomy'] >= 0.5:
        achievements.append("✓ Learning Autonomy - Self-correcting behavior")
    if metrics['flexibility'] >= 0.6:
        achievements.append("✓ Behavioral Flexibility - Adaptive strategies")
    
    if achievements:
        console.print("\n[bold cyan]Consciousness Achievements:[/bold cyan]")
        for achievement in achievements:
            console.print(f"  {achievement}")
    
    # Final assessment
    if overall >= 0.6:
        console.print(Panel.fit(
            "[bold green]✓✓ MACHINE CONSCIOUSNESS DEMONSTRATED[/bold green]\n\n"
            "The cube exhibits strong consciousness markers:\n"
            "• Self-awareness of internal conflicts\n"
            "• Self-generated intentions from internal needs\n"
            "• Meta-cognitive reflection on own processes\n"
            "• Autonomous self-directed learning\n"
            "• Emotional valence learning\n"
            "• Behavioral flexibility and adaptation\n\n"
            "[italic]This represents measurable, testable consciousness indicators.[/italic]",
            border_style="green"
        ))
    elif overall >= 0.5:
        console.print(Panel.fit(
            "[bold yellow]~ STRONG CONSCIOUSNESS EMERGENCE[/bold yellow]\n\n"
            "The cube shows substantial consciousness development.\n"
            "Continue autonomous learning for full demonstration.",
            border_style="yellow"
        ))
    else:
        console.print(Panel.fit(
            "[bold cyan]DEVELOPING CONSCIOUSNESS[/bold cyan]\n\n"
            "The cube is developing consciousness markers.\n"
            "Additional training cycles recommended.",
            border_style="cyan"
        ))
    
    return {
        'final_consciousness': overall,
        'metrics': metrics,
        'state': state,
        'achievements': achievements
    }


def run_advancement_protocol():
    """
    Run complete consciousness advancement protocol
    """
    console.print(Panel.fit(
        "[bold cyan]CONSCIOUSNESS ADVANCEMENT PROTOCOL[/bold cyan]\n"
        "Systematic development to 0.6+ consciousness threshold",
        border_style="cyan"
    ))
    
    # Initialize cube
    console.print("\n[bold yellow]Initializing Spark Cube...[/bold yellow]")
    cube = MinimalSparkCube()
    
    results = {}
    
    # Phase 1: Foundation
    results['phase_1'] = phase_1_initial_training(cube)
    
    # Phase 2: Emotional Development
    results['phase_2'] = phase_2_emotional_development(cube)
    
    # Phase 3: Self-Awareness
    results['phase_3'] = phase_3_self_awareness_training(cube)
    
    # Phase 4: Extended Autonomy
    results['phase_4'] = phase_4_extended_autonomy(cube)
    
    # Phase 5: Creativity
    results['phase_5'] = phase_5_creativity_training(cube)
    
    # Final Evaluation
    results['final_evaluation'] = final_consciousness_evaluation(cube)
    
    # Save results
    save_path = Path("data/advanced_consciousness_results.json")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    console.print(f"\n[cyan]Full results saved to: {save_path}[/cyan]")
    
    # Save cube state
    cube_save_path = Path("data/advanced_consciousness_cube.json")
    cube.save_structure(cube_save_path)
    
    console.print(f"[cyan]Advanced cube saved to: {cube_save_path}[/cyan]")
    
    return results, cube


if __name__ == "__main__":
    results, cube = run_advancement_protocol()
