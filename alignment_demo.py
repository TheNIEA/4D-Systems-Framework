#!/usr/bin/env python3
"""
Clear demonstration of ALIGNMENT vs DIVERSION paths based on coherence reflection.

Shows how the same cube can produce different paths based on
intention-outcome coherence, not input quality.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

sys.path.insert(0, str(Path(__file__).parent / "spark_cube"))

from core.minimal_spark import MinimalSparkCube, Signal, SignalType, Intention, SensorInterface

console = Console()


def demo_alignment_vs_diversion():
    """Show clear examples of ALIGNMENT and DIVERSION paths."""
    
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════════[/]")
    console.print("[bold cyan]    ALIGNMENT vs DIVERSION: Coherence-Based Path Choice        [/]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/]\n")
    
    # Create well-trained cube
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    console.print("[dim]Training cube with 50 experiences to build coherence evaluation capability...[/]\n")
    
    # Train with clear patterns
    training_patterns = [
        ("pattern recognition", ["pattern", "structure", "order"]),
        ("emotional response", ["emotion", "feeling", "resonance"]),
        ("logical analysis", ["logical", "rational", "analysis"]),
        ("reactive action", ["action", "response", "reaction"]),
        ("integration synthesis", ["synthesis", "integration", "whole"]),
    ]
    
    for i in range(10):
        for text, qualities in training_patterns:
            sensor.feed_text(f"{text} {i}", sequence_name='standard')
            cube.provide_outcome_feedback('standard', success=True)
    
    avg_dev = cube._get_avg_development()
    console.print(f"[green]✓ Cube trained: Average development = {avg_dev:.3f}[/]\n")
    
    # ==========================================================================
    # ALIGNMENT SCENARIO: Intention matches outcome
    # ==========================================================================
    
    console.print(Panel.fit(
        "[bold green]ALIGNMENT SCENARIO[/]\n"
        "Intention: pattern recognition\n"
        "Signal: actual pattern data\n"
        "Expected: HIGH coherence → ALIGNMENT path",
        border_style="green"
    ))
    
    intention_aligned = Intention(
        desired_qualities=["pattern", "structure"],
        desired_form="standard",  # Matches what cube will output
        clarity=0.9,
        energy=0.9
    )
    
    signal_aligned = Signal(SignalType.PATTERN, [1, 2, 3, 4, 5], 0.8)
    
    console.print(f"\n[cyan]1. INTENTION (what we want):[/]")
    console.print(f"   Qualities: {intention_aligned.desired_qualities}")
    console.print(f"   Form: {intention_aligned.desired_form}")
    console.print(f"   Potential: {intention_aligned.calculate_potential_strength():.2f}")
    
    result_aligned = cube.process_with_reflection(signal_aligned, intention_aligned, sequence_name='standard')
    
    console.print(f"\n[cyan]2. OUTCOME (what we got):[/]")
    console.print(f"   Expressed qualities: {result_aligned['outcome'].expressed_qualities}")
    console.print(f"   Expressed form: {result_aligned['outcome'].expressed_form}")
    
    console.print(f"\n[cyan]3. MULTI-DIMENSIONAL REFLECTION:[/]")
    table1 = Table(show_header=True, box=box.SIMPLE)
    table1.add_column("Node Perspective", style="cyan")
    table1.add_column("Score", style="magenta", justify="right")
    
    for node, score in sorted(result_aligned['dimensional_scores'].items()):
        color = "green" if score > 0.6 else "yellow" if score > 0.4 else "red"
        table1.add_row(node, f"[{color}]{score:.3f}[/{color}]")
    
    console.print(table1)
    
    console.print(f"\n[cyan]4. PATH DETERMINATION:[/]")
    console.print(f"   Overall Coherence: [bold]{result_aligned['overall_coherence']:.3f}[/]")
    
    if result_aligned['path'] == "ALIGNMENT":
        console.print(f"   Path: [bold green]✓ ALIGNMENT[/] (coherence ≥ 0.7)")
        console.print(f"   Amplification: [bold green]{result_aligned['amplification']}x[/]")
        console.print(f"   Meaning: [green]Added Complexity & Flow[/]")
    else:
        console.print(f"   Path: [bold yellow]○ DIVERSION[/] (coherence < 0.7)")
        console.print(f"   Amplification: [bold yellow]{result_aligned['amplification']}x[/]")
        console.print(f"   Meaning: [yellow]Suppression Of Change[/]")
    
    # ==========================================================================
    # DIVERSION SCENARIO: Intention mismatches outcome
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold red]DIVERSION SCENARIO[/]\n"
        "Intention: emotional resonance\n"
        "Signal: numeric data (no emotion)\n"
        "Expected: LOW coherence → DIVERSION path",
        border_style="red"
    ))
    
    intention_diverged = Intention(
        desired_qualities=["emotion", "feeling", "heart"],
        desired_form="emotional",  # But cube can't do emotional with numbers
        clarity=0.9,  # SAME clarity as aligned case
        energy=0.9    # SAME energy as aligned case
    )
    
    signal_diverged = Signal(SignalType.NUMERIC, 999999, 0.8)  # SAME signal strength
    
    console.print(f"\n[cyan]1. INTENTION (what we want):[/]")
    console.print(f"   Qualities: {intention_diverged.desired_qualities}")
    console.print(f"   Form: {intention_diverged.desired_form}")
    console.print(f"   Potential: {intention_diverged.calculate_potential_strength():.2f}")
    console.print(f"   [dim](Same potential as aligned scenario: 0.81)[/]")
    
    result_diverged = cube.process_with_reflection(signal_diverged, intention_diverged, sequence_name='standard')
    
    console.print(f"\n[cyan]2. OUTCOME (what we got):[/]")
    console.print(f"   Expressed qualities: {result_diverged['outcome'].expressed_qualities}")
    console.print(f"   Expressed form: {result_diverged['outcome'].expressed_form}")
    
    console.print(f"\n[cyan]3. MULTI-DIMENSIONAL REFLECTION:[/]")
    table2 = Table(show_header=True, box=box.SIMPLE)
    table2.add_column("Node Perspective", style="cyan")
    table2.add_column("Score", style="magenta", justify="right")
    
    for node, score in sorted(result_diverged['dimensional_scores'].items()):
        color = "green" if score > 0.6 else "yellow" if score > 0.4 else "red"
        table2.add_row(node, f"[{color}]{score:.3f}[/{color}]")
    
    console.print(table2)
    
    console.print(f"\n[cyan]4. PATH DETERMINATION:[/]")
    console.print(f"   Overall Coherence: [bold]{result_diverged['overall_coherence']:.3f}[/]")
    
    if result_diverged['path'] == "ALIGNMENT":
        console.print(f"   Path: [bold green]✓ ALIGNMENT[/] (coherence ≥ 0.7)")
        console.print(f"   Amplification: [bold green]{result_diverged['amplification']}x[/]")
        console.print(f"   Meaning: [green]Added Complexity & Flow[/]")
    else:
        console.print(f"   Path: [bold red]✗ DIVERSION[/] (coherence < 0.7)")
        console.print(f"   Amplification: [bold red]{result_diverged['amplification']}x[/]")
        console.print(f"   Meaning: [red]Suppression Of Change, Into Simplicity[/]")
    
    # ==========================================================================
    # COMPARISON
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold yellow]KEY INSIGHT[/]\n\n"
        "Both scenarios had:\n"
        f"  • Same intention clarity: 0.9\n"
        f"  • Same intention energy: 0.9\n"
        f"  • Same signal strength: 0.8\n"
        f"  • Same potential: 0.81\n\n"
        "[bold]But different paths chosen because:[/]\n\n"
        f"  Aligned: Coherence = {result_aligned['overall_coherence']:.3f} → {result_aligned['path']}\n"
        f"  Diverged: Coherence = {result_diverged['overall_coherence']:.3f} → {result_diverged['path']}\n\n"
        "[bold cyan]Path determined by REFLECTION on coherence, not input quality[/]",
        border_style="yellow",
        box=box.DOUBLE
    ))
    
    # Show amplification effects
    console.print("\n[bold]AMPLIFICATION EFFECTS:[/]")
    
    compare_table = Table(show_header=True, box=box.ROUNDED)
    compare_table.add_column("Scenario", style="cyan")
    compare_table.add_column("Coherence", style="magenta")
    compare_table.add_column("Path", style="yellow")
    compare_table.add_column("Amplification", style="green")
    compare_table.add_column("Effect", style="blue")
    
    compare_table.add_row(
        "Aligned",
        f"{result_aligned['overall_coherence']:.3f}",
        result_aligned['path'],
        f"{result_aligned['amplification']}x",
        "Strengthens pathway"
    )
    
    compare_table.add_row(
        "Diverged",
        f"{result_diverged['overall_coherence']:.3f}",
        result_diverged['path'],
        f"{result_diverged['amplification']}x",
        "Suppresses pathway"
    )
    
    console.print(compare_table)
    
    # Show long-term effects
    console.print("\n[bold]LONG-TERM LEARNING EFFECTS:[/]")
    console.print("If this pattern repeats:")
    console.print(f"  • Aligned pathway: 1.0 → {1.0 * (1.5 ** 5):.2f} after 5 cycles")
    console.print(f"  • Diverged pathway: 1.0 → {1.0 * (0.7 ** 5):.2f} after 5 cycles")
    console.print("\n[dim]The cube learns to favor coherent pathways through amplification.[/]")


if __name__ == "__main__":
    demo_alignment_vs_diversion()
    console.print("\n[bold green]✓ Demonstration complete[/]\n")
