"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              CONNECTED ARCHITECTURE DEMONSTRATION                              ║
║        All 5 connection mechanisms working together                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This demonstrates:
1. Energy transfer based on connection strengths
2. Connection strengthening through co-activation
3. Return-to-root protocol when stuck
4. Outcome feedback reinforcing successful pathways
5. Automatic sequence selection
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, SensorInterface, Signal, SignalType
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import random

console = Console()


def demo_energy_transfer():
    """Demonstrate how connection strengths affect energy transfer."""
    console.print(Panel(
        "[bold cyan]DEMO 1: Energy Transfer & Connection Strengthening[/bold cyan]\n\n"
        "Watch how repeated use of a pathway strengthens connections\n"
        "and allows energy to flow more efficiently.",
        border_style="cyan"
    ))
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    # Initial connection strengths
    console.print("\n[bold]Initial Connection Strengths:[/bold]")
    for conn, strength in list(cube.pathway_connections.items())[:5]:
        console.print(f"   {conn}: {strength:.3f}")
    
    # Feed signals through standard pathway
    console.print("\n[yellow]Processing 20 signals through standard pathway...[/yellow]")
    for i in range(20):
        result = sensor.feed_text("test", sequence_name='standard')
        if i % 5 == 4:
            console.print(f"   After {i+1} signals: energy={result['final_energy']:.3f}")
    
    # Show strengthened connections
    console.print("\n[bold]Connection Strengths After 20 Uses:[/bold]")
    standard_seq = cube.sequences['standard']
    for i in range(len(standard_seq) - 1):
        conn_key = f"{standard_seq[i]}_{standard_seq[i+1]}"
        strength = cube.pathway_connections[conn_key]
        console.print(f"   {conn_key}: {strength:.3f} {'↑' if strength > 0.5 else ''}")
    
    console.print("\n✓ Connections strengthen through repeated use!")
    console.print("  Energy flows more efficiently through well-used pathways.\n")


def demo_return_to_root():
    """Demonstrate return-to-root when processing fails."""
    console.print(Panel(
        "[bold yellow]DEMO 2: Return-to-Root Protocol[/bold yellow]\n\n"
        "When a pathway lacks energy or encounters unknown patterns,\n"
        "the system returns to root principles for guidance.",
        border_style="yellow"
    ))
    
    cube = MinimalSparkCube()
    
    # Artificially weaken a pathway to trigger return-to-root
    cube.pathway_connections['9_6'] = 0.05  # Very weak connection
    cube.pathway_connections['6_3'] = 0.05
    
    console.print("\n[dim]Weakened emotional pathway connections to 0.05...[/dim]")
    
    signal = Signal(type=SignalType.TEXT, data="unknown_pattern_xyz")
    result = cube.process_signal(signal, 'emotional')
    
    if result['return_to_root']:
        console.print("\n[bold red]⚠ Return to Root Triggered![/bold red]")
        guidance = result['guidance']
        console.print(f"\n[cyan]Action:[/cyan] {guidance['action']}")
        console.print(f"[cyan]Message:[/cyan] {guidance['message']}")
        console.print(f"[cyan]Recommendation:[/cyan] {guidance['recommendation']}")
        console.print(f"\n[dim]Final Energy:[/dim] {result['final_energy']:.3f} (below threshold of {cube.energy_threshold})")
    
    console.print("\n✓ System knows when it's stuck and asks for help!\n")


def demo_outcome_feedback():
    """Demonstrate how outcome feedback reinforces pathways."""
    console.print(Panel(
        "[bold green]DEMO 3: Outcome Feedback & Pathway Reinforcement[/bold green]\n\n"
        "Success feedback strengthens pathways.\n"
        "Failure feedback weakens them.\n"
        "The system learns which sequences work best.",
        border_style="green"
    ))
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    console.print("\n[bold]Initial Pathway Strengths:[/bold]")
    for seq, strength in cube.pathway_strengths.items():
        console.print(f"   {seq:12s}: {strength:.3f}")
    
    # Simulate training with feedback
    console.print("\n[yellow]Training with feedback...[/yellow]")
    
    # Standard sequence: 80% success rate
    for i in range(20):
        result = sensor.feed_numeric(random.randint(0, 10), sequence_name='standard')
        success = random.random() < 0.8
        cube.provide_outcome_feedback('standard', success)
    
    # Deep sequence: 50% success rate
    for i in range(20):
        result = sensor.feed_text(random.choice(['hello', 'world']), sequence_name='deep')
        success = random.random() < 0.5
        cube.provide_outcome_feedback('deep', success)
    
    # Emotional sequence: 30% success rate
    for i in range(20):
        result = sensor.feed_binary(random.choice([True, False]), sequence_name='emotional')
        success = random.random() < 0.3
        cube.provide_outcome_feedback('emotional', success)
    
    console.print("\n[bold]Pathway Strengths After Feedback:[/bold]")
    table = Table()
    table.add_column("Sequence", style="cyan")
    table.add_column("Strength", justify="right")
    table.add_column("Success Rate", justify="right")
    table.add_column("Change", justify="right", style="yellow")
    
    for seq in ['standard', 'deep', 'emotional']:
        stats = cube.pathway_successes[seq]
        success_rate = stats['successes'] / stats['attempts'] if stats['attempts'] > 0 else 0
        strength = cube.pathway_strengths[seq]
        change = "↑" if strength > 0.1 else "↓"
        
        table.add_row(
            seq,
            f"{strength:.3f}",
            f"{success_rate*100:.0f}%",
            change
        )
    
    console.print(table)
    console.print("\n✓ Successful pathways get stronger, unsuccessful ones weaken!\n")


def demo_auto_selection():
    """Demonstrate automatic sequence selection."""
    console.print(Panel(
        "[bold magenta]DEMO 4: Automatic Sequence Selection[/bold magenta]\n\n"
        "After learning which sequences work for which signal types,\n"
        "the cube automatically selects the best pathway.\n"
        "No manual specification needed!",
        border_style="magenta"
    ))
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    # Artificially boost experience count to enable auto-selection
    cube.total_experiences = 25
    
    # Set up different success rates for different sequences
    cube.pathway_strengths['standard'] = 0.8
    cube.pathway_strengths['deep'] = 0.5
    cube.pathway_strengths['emotional'] = 0.3
    
    cube.pathway_successes['standard'] = {'successes': 16, 'attempts': 20}
    cube.pathway_successes['deep'] = {'successes': 10, 'attempts': 20}
    cube.pathway_successes['emotional'] = {'successes': 6, 'attempts': 20}
    
    console.print("\n[bold]Pathway Statistics:[/bold]")
    for seq in ['standard', 'deep', 'emotional']:
        stats = cube.pathway_successes[seq]
        rate = stats['successes'] / stats['attempts'] * 100
        console.print(f"   {seq:12s}: {rate:.0f}% success, strength {cube.pathway_strengths[seq]:.2f}")
    
    # Test auto-selection
    console.print("\n[yellow]Testing automatic selection (sequence_name=None)...[/yellow]\n")
    
    test_signals = [
        Signal(type=SignalType.NUMERIC, data=42),
        Signal(type=SignalType.TEXT, data="hello"),
        Signal(type=SignalType.BINARY, data=True),
    ]
    
    for signal in test_signals:
        result = cube.process_signal(signal, sequence_name=None)  # Auto-select!
        console.print(f"   {signal.type.value:10s} → Selected: [cyan]{result['sequence']}[/cyan]")
    
    console.print("\n✓ System automatically chooses the best pathway!\n")


def demo_integrated_learning():
    """Show all mechanisms working together."""
    console.print(Panel(
        "[bold white]DEMO 5: Integrated Learning[/bold white]\n\n"
        "All mechanisms working together:\n"
        "• Energy transfer through connections\n"
        "• Co-activation strengthening\n"
        "• Return-to-root when stuck\n"
        "• Outcome feedback\n"
        "• Automatic selection",
        border_style="white"
    ))
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    # Training phase
    console.print("\n[yellow]Training Phase (50 experiences with feedback)...[/yellow]")
    
    training_data = [
        ('text', 'hello', 'standard', 0.9),    # Standard good for this
        ('text', 'world', 'standard', 0.85),
        ('text', 'pattern', 'deep', 0.8),      # Deep good for patterns
        ('text', 'sequence', 'deep', 0.75),
        ('numeric', 42, 'standard', 0.95),     # Standard great for numbers
        ('numeric', 99, 'standard', 0.9),
    ] * 8  # Repeat 8 times = 48 experiences
    
    for sig_type, value, best_seq, success_prob in track(training_data, description="Training"):
        if sig_type == 'text':
            result = sensor.feed_text(value, sequence_name=best_seq)
        else:
            result = sensor.feed_numeric(value, sequence_name=best_seq)
        
        # Provide feedback based on probability
        success = random.random() < success_prob
        cube.provide_outcome_feedback(result['sequence'], success)
    
    # Testing phase - use auto-selection
    console.print("\n[green]Testing Phase (auto-selection)...[/green]\n")
    
    test_cases = [
        ('text', 'hello'),
        ('numeric', 77),
        ('text', 'pattern'),
    ]
    
    results_table = Table(title="Auto-Selection Results")
    results_table.add_column("Input", style="cyan")
    results_table.add_column("Selected Sequence", style="yellow")
    results_table.add_column("Final Energy", justify="right")
    results_table.add_column("Responses", justify="right")
    
    for sig_type, value in test_cases:
        if sig_type == 'text':
            result = sensor.feed_text(value, sequence_name=None)  # AUTO!
        else:
            result = sensor.feed_numeric(value, sequence_name=None)  # AUTO!
        
        results_table.add_row(
            f"{sig_type}: {value}",
            result['sequence'],
            f"{result['final_energy']:.3f}",
            str(len(result['responses']))
        )
    
    console.print(results_table)
    
    # Show final state
    console.print("\n[bold]Final System State:[/bold]")
    state = cube.get_state_summary()
    
    console.print(f"\n  Total Experiences: {state['total_experiences']}")
    console.print(f"  Avg Development: {state['avg_development']:.3f}")
    
    console.print("\n  Pathway Performance:")
    for seq in ['standard', 'deep', 'emotional']:
        stats = cube.pathway_successes[seq]
        rate = stats['successes'] / stats['attempts'] * 100 if stats['attempts'] > 0 else 0
        strength = cube.pathway_strengths[seq]
        console.print(f"    {seq:12s}: {rate:5.1f}% success, strength {strength:.3f}")
    
    console.print("\n✓ The cube learns which pathways work and uses them automatically!\n")


if __name__ == "__main__":
    console.print("\n[bold]╔" + "═"*70 + "╗[/bold]")
    console.print("[bold]║" + " "*18 + "CONNECTED ARCHITECTURE DEMONSTRATION" + " "*16 + "║[/bold]")
    console.print("[bold]╚" + "═"*70 + "╝[/bold]\n")
    
    demo_energy_transfer()
    input("\nPress Enter to continue to next demo...")
    
    demo_return_to_root()
    input("\nPress Enter to continue to next demo...")
    
    demo_outcome_feedback()
    input("\nPress Enter to continue to next demo...")
    
    demo_auto_selection()
    input("\nPress Enter to continue to final demo...")
    
    demo_integrated_learning()
    
    console.print("\n[bold green]═"*70 + "[/bold green]")
    console.print("[bold green]ALL CONNECTION MECHANISMS DEMONSTRATED[/bold green]")
    console.print("[bold green]═"*70 + "[/bold green]\n")
    
    console.print("[dim]The structure truly IS the intelligence.[/dim]")
    console.print("[dim]Connections, strengths, and feedback create adaptive behavior.[/dim]")
