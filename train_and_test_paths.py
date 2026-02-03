"""
Train the Spark Cube extensively before testing path differentiation.

The key insight: The cube needs substantial development before clear
ALIGNMENT paths will emerge. Early on, everything looks like INTEGRATION
because the cube is learning from everything.

Training Strategy:
1. 200+ diverse experiences across all signal types
2. Mix of successful and challenging patterns
3. Outcome feedback to reinforce successful pathways
4. Then test with clear intention-outcome scenarios

This should produce:
- ALIGNMENT: High coherence when intention matches developed capabilities
- INTEGRATION: Medium coherence when partial match exists (learning zone)
- DIVERSION: Low coherence when intention completely mismatches output
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "spark_cube" / "core"))

from minimal_spark import MinimalSparkCube, Signal, SignalType, Intention
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import random

console = Console()


def train_cube_extensively(cube: MinimalSparkCube, num_experiences: int = 200):
    """
    Train the cube with diverse experiences to build up node development.
    """
    console.print(f"\n[bold cyan]Training cube with {num_experiences} diverse experiences...[/bold cyan]")
    
    training_data = []
    
    # Text patterns (40%)
    text_samples = [
        "hello", "world", "pattern", "recognition", "structure",
        "analysis", "synthesis", "integration", "development", "growth",
        "learning", "adaptation", "response", "processing", "coherence"
    ]
    for _ in range(int(num_experiences * 0.4)):
        text = random.choice(text_samples)
        training_data.append(('text', text))
    
    # Numeric patterns (30%)
    for _ in range(int(num_experiences * 0.3)):
        value = random.uniform(-100, 100)
        training_data.append(('numeric', value))
    
    # Binary patterns (15%)
    for _ in range(int(num_experiences * 0.15)):
        value = random.choice([True, False])
        training_data.append(('binary', value))
    
    # Sequences (15%)
    for _ in range(int(num_experiences * 0.15)):
        seq = [random.randint(0, 10) for _ in range(random.randint(3, 7))]
        training_data.append(('sequence', seq))
    
    # Shuffle for variety
    random.shuffle(training_data)
    
    # Process all training data
    for signal_type, data in track(training_data, description="Processing signals"):
        if signal_type == 'text':
            signal = Signal(type=SignalType.TEXT, data=data)
        elif signal_type == 'numeric':
            signal = Signal(type=SignalType.NUMERIC, data=data)
        elif signal_type == 'binary':
            signal = Signal(type=SignalType.BINARY, data=data)
        elif signal_type == 'sequence':
            signal = Signal(type=SignalType.SEQUENCE, data=data)
        
        result = cube.process_signal(signal)
        
        # Provide outcome feedback
        # Success if: processing completed and nodes activated
        success = not result.get('return_to_root', False) and len(result.get('responses', [])) > 0
        if 'sequence' in result:
            cube.provide_outcome_feedback(result['sequence'], success)
    
    state = cube.get_state_summary()
    
    console.print("\n[bold green]✓ Training complete![/bold green]")
    console.print(f"Average node development: [cyan]{state['avg_development']:.3f}[/cyan]")
    
    # Show node development table
    table = Table(title="Node Development After Training")
    table.add_column("Node", style="cyan")
    table.add_column("Development", style="green")
    table.add_column("Patterns", style="yellow")
    table.add_column("Activations", style="blue")
    
    for node_state in state['node_states'].values():
        table.add_row(
            node_state['name'],
            f"{node_state['development']:.3f}",
            str(node_state['patterns_learned']),
            str(node_state['activations'])
        )
    
    console.print(table)
    return state


def test_path_differentiation(cube: MinimalSparkCube):
    """
    Test the three-tier path system with clear scenarios.
    """
    console.print("\n[bold magenta]Testing Path Differentiation[/bold magenta]")
    console.print("After training, the cube should show different paths for different scenarios.\n")
    
    test_cases = []
    
    # Test 1: ALIGNMENT scenario
    # Intention matches cube's developed capabilities
    console.print("[bold yellow]Test 1: ALIGNMENT Scenario[/bold yellow]")
    console.print("Intention: Recognize a text pattern the cube has learned")
    
    intention1 = cube.set_intention(
        desired_qualities=['text', 'pattern', 'recognized', 'complete'],
        desired_form='standard',
        clarity=0.9,
        energy=0.9
    )
    
    signal1 = Signal(type=SignalType.TEXT, data="hello")
    result1 = cube.process_with_reflection(signal1, intention1, sequence_name='deep')
    
    test_cases.append(('ALIGNMENT', result1))
    
    console.print(f"Path: [{'green' if result1['path'] == 'ALIGNMENT' else 'yellow'}]{result1['path']}[/{'green' if result1['path'] == 'ALIGNMENT' else 'yellow'}]")
    console.print(f"Coherence: {result1['overall_coherence']:.3f}")
    console.print(f"Amplification: {result1['amplification']:.1f}x")
    console.print(f"Expressed qualities: {result1['outcome'].expressed_qualities}\n")
    
    # Test 2: INTEGRATION scenario
    # Intention partially matches - good learning opportunity
    console.print("[bold yellow]Test 2: INTEGRATION Scenario[/bold yellow]")
    console.print("Intention: Structure analysis (partially developed capability)")
    
    intention2 = cube.set_intention(
        desired_qualities=['pattern', 'analysis', 'structure', 'developing'],
        desired_form='deep',
        clarity=0.7,
        energy=0.8
    )
    
    signal2 = Signal(type=SignalType.TEXT, data="synthesis")
    result2 = cube.process_with_reflection(signal2, intention2, sequence_name='deep')
    
    test_cases.append(('INTEGRATION', result2))
    
    console.print(f"Path: [{'yellow' if result2['path'] == 'INTEGRATION' else 'cyan'}]{result2['path']}[/{'yellow' if result2['path'] == 'INTEGRATION' else 'cyan'}]")
    console.print(f"Coherence: {result2['overall_coherence']:.3f}")
    console.print(f"Amplification: {result2['amplification']:.1f}x")
    console.print(f"Expressed qualities: {result2['outcome'].expressed_qualities}\n")
    
    # Test 3: DIVERSION scenario
    # Intention completely mismatches cube's capabilities
    console.print("[bold yellow]Test 3: DIVERSION Scenario[/bold yellow]")
    console.print("Intention: Precise numeric calculation (undeveloped for text input)")
    
    intention3 = cube.set_intention(
        desired_qualities=['calculation', 'numeric', 'precise', 'mathematical'],
        desired_form='calculation_result',
        clarity=0.8,
        energy=0.7
    )
    
    signal3 = Signal(type=SignalType.TEXT, data="not a number")
    result3 = cube.process_with_reflection(signal3, intention3, sequence_name='standard')
    
    test_cases.append(('DIVERSION', result3))
    
    console.print(f"Path: [{'red' if result3['path'] == 'DIVERSION' else 'cyan'}]{result3['path']}[/{'red' if result3['path'] == 'DIVERSION' else 'cyan'}]")
    console.print(f"Coherence: {result3['overall_coherence']:.3f}")
    console.print(f"Amplification: {result3['amplification']:.1f}x")
    console.print(f"Expressed qualities: {result3['outcome'].expressed_qualities}\n")
    
    # Test 4: Another ALIGNMENT scenario with numeric
    console.print("[bold yellow]Test 4: ALIGNMENT Scenario (Numeric)[/bold yellow]")
    console.print("Intention: Process numeric value (trained capability)")
    
    intention4 = cube.set_intention(
        desired_qualities=['numeric', 'processed', 'complete', 'recognized'],
        desired_form='standard',
        clarity=0.9,
        energy=0.8
    )
    
    signal4 = Signal(type=SignalType.NUMERIC, data=42.0)
    result4 = cube.process_with_reflection(signal4, intention4, sequence_name='standard')
    
    test_cases.append(('ALIGNMENT', result4))
    
    console.print(f"Path: [{'green' if result4['path'] == 'ALIGNMENT' else 'yellow'}]{result4['path']}[/{'green' if result4['path'] == 'ALIGNMENT' else 'yellow'}]")
    console.print(f"Coherence: {result4['overall_coherence']:.3f}")
    console.print(f"Amplification: {result4['amplification']:.1f}x")
    console.print(f"Expressed qualities: {result4['outcome'].expressed_qualities}\n")
    
    # Summary table
    summary_table = Table(title="Path Differentiation Summary")
    summary_table.add_column("Expected", style="cyan")
    summary_table.add_column("Actual", style="yellow")
    summary_table.add_column("Coherence", style="green")
    summary_table.add_column("Amplification", style="magenta")
    summary_table.add_column("Match", style="bold")
    
    matches = 0
    for expected, result in test_cases:
        actual = result['path']
        match = "✓" if expected == actual else "✗"
        if expected == actual:
            matches += 1
        
        summary_table.add_row(
            expected,
            actual,
            f"{result['overall_coherence']:.3f}",
            f"{result['amplification']:.1f}x",
            match
        )
    
    console.print(summary_table)
    console.print(f"\n[bold]Path Prediction Accuracy: {matches}/{len(test_cases)} ({matches/len(test_cases)*100:.0f}%)[/bold]")
    
    # Show dimensional coherence for most interesting case
    console.print("\n[bold cyan]Dimensional Coherence Breakdown (Test 1 - ALIGNMENT):[/bold cyan]")
    dim_table = Table()
    dim_table.add_column("Node", style="cyan")
    dim_table.add_column("Coherence Score", style="green")
    
    for node_name, score in result1['dimensional_scores'].items():
        dim_table.add_row(node_name, f"{score:.3f}")
    
    console.print(dim_table)
    
    # Show emotional valence patterns learned
    emotional_node = cube.nodes.get(6)
    if emotional_node and emotional_node.pattern_weights:
        console.print("\n[bold cyan]Emotional Valence Patterns Learned:[/bold cyan]")
        valence_table = Table()
        valence_table.add_column("Pattern", style="yellow")
        valence_table.add_column("Valence", style="green")
        
        for pattern, valence in sorted(emotional_node.pattern_weights.items(), 
                                       key=lambda x: x[1], reverse=True)[:10]:
            valence_table.add_row(pattern, f"{valence:.3f}")
        
        console.print(valence_table)
        console.print(f"Total patterns learned: {len(emotional_node.pattern_weights)}")
    
    return test_cases


def main():
    """
    Main training and testing flow.
    """
    console.print(Panel.fit(
        "[bold cyan]THREE-TIER PATH SYSTEM VALIDATION[/bold cyan]\n"
        "Training extensively before testing path differentiation",
        border_style="cyan"
    ))
    
    # Create fresh cube
    cube = MinimalSparkCube()
    
    # Train extensively
    train_cube_extensively(cube, num_experiences=200)
    
    # Test path differentiation
    test_cases = test_path_differentiation(cube)
    
    # Save trained cube
    save_path = Path("data/trained_cube_200exp.json")
    cube.save_structure(save_path)
    
    console.print(f"\n[bold green]✓ Complete![/bold green]")
    console.print(f"Trained cube saved to: {save_path}")
    
    console.print("\n[bold cyan]Key Insights:[/bold cyan]")
    console.print("• ALIGNMENT emerges when intention matches developed capabilities")
    console.print("• INTEGRATION appears when partial match exists (learning opportunity)")
    console.print("• DIVERSION occurs when intention completely mismatches output")
    console.print("• Richer outcome extraction enables meaningful coherence comparison")
    console.print("• All nodes contribute to reflection, enabling holistic learning")


if __name__ == "__main__":
    main()
