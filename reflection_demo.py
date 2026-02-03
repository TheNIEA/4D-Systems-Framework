#!/usr/bin/env python3
"""
Demonstration of the Reflection-Based Manifestation Cycle

This shows the KEY INSIGHT from the manifestation map:
Path choice (ALIGNMENT vs DIVERSION) is determined by SELF-REFLECTION
on intention-outcome coherence, not by input characteristics.

The cycle:
1. ALL POTENTIAL HELD IN NON EXISTENCE
2. NEW BEGINNINGS (potential enters manifestation via intention)
3. FREE WILL / SOUL PURPOSE (choice point - which pathway?)
4. ALIGNMENT or DIVERSION based on coherence reflection
5. AMPLIFICATION (1.5x for alignment, 0.7x for diversion)
6. ALL NEW POTENTIAL STORED (outcome becomes new potential)
7. Return to NEW BEGINNINGS
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Add spark_cube to path
sys.path.insert(0, str(Path(__file__).parent / "spark_cube"))

from core.minimal_spark import MinimalSparkCube, Signal, SignalType, Intention

console = Console()


def demo_manifestation_cycle():
    """Demonstrate the complete manifestation cycle with reflection."""
    
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════════[/]")
    console.print("[bold cyan]       MANIFESTATION CYCLE WITH SELF-REFLECTION                [/]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/]\n")
    
    console.print("Key insight: Path determined by [bold yellow]COHERENCE REFLECTION[/], not input quality\n")
    
    # Initialize cube
    cube = MinimalSparkCube()
    
    # Grow the cube a bit first
    console.print("[dim]Growing cube baseline knowledge...[/]")
    signals = [
        Signal(SignalType.TEXT, "hello", 0.8),
        Signal(SignalType.TEXT, "world", 0.8),
        Signal(SignalType.NUMERIC, 42, 0.7),
        Signal(SignalType.PATTERN, [1, 2, 3], 0.6),
    ]
    for sig in signals:
        cube.process_signal(sig, 'standard')
        cube.provide_outcome_feedback('standard', True)
    
    console.print(f"[dim]Baseline development: {cube._get_avg_development():.3f}[/]\n")
    
    # =========================================================================
    # SCENARIO 1: HIGH COHERENCE → ALIGNMENT PATH
    # =========================================================================
    
    console.print(Panel.fit(
        "[bold green]SCENARIO 1: HIGH COHERENCE → ALIGNMENT[/]\n"
        "Intention matches outcome → Added Complexity & Flow",
        border_style="green"
    ))
    
    # Set clear intention
    intention1 = Intention(
        desired_qualities=["pattern", "structure", "order"],
        desired_form="pattern_response",
        clarity=0.9,
        energy=0.8
    )
    
    console.print(f"\n[cyan]INTENTION:[/]")
    console.print(f"  Desired qualities: {intention1.desired_qualities}")
    console.print(f"  Desired form: {intention1.desired_form}")
    console.print(f"  Clarity × Energy: {intention1.calculate_potential_strength():.2f}")
    
    # Process with pattern signal (matches intention)
    signal1 = Signal(SignalType.PATTERN, [1, 2, 3, 4, 5], 0.7)
    
    console.print(f"\n[cyan]PROCESSING:[/]")
    console.print(f"  Signal: PATTERN [1,2,3,4,5]")
    console.print(f"  Free will choice: automatic sequence selection")
    
    result1 = cube.process_with_reflection(signal1, intention1)
    
    console.print(f"\n[cyan]OUTCOME:[/]")
    console.print(f"  Expressed form: {result1['outcome'].expressed_form}")
    console.print(f"  Response data: {len(result1['responses'])} node responses")
    
    console.print(f"\n[cyan]REFLECTION:[/]")
    table1 = Table(show_header=True, box=box.ROUNDED)
    table1.add_column("Node", style="cyan")
    table1.add_column("Coherence Score", style="magenta")
    
    for node_name, score in result1['dimensional_scores'].items():
        table1.add_row(node_name, f"{score:.3f}")
    
    console.print(table1)
    
    console.print(f"\n[bold yellow]PATH DETERMINATION:[/]")
    console.print(f"  Overall coherence: [bold]{result1['overall_coherence']:.3f}[/]")
    console.print(f"  Path choice: [bold green]{result1['path']}[/]")
    console.print(f"  Amplification: [bold green]{result1['amplification']}x[/]")
    console.print(f"  Meaning: [green]Added Complexity & Flow[/green]")
    
    pathway_before_1 = cube.pathway_strengths.get(result1['sequence'], 0.1)
    
    # =========================================================================
    # SCENARIO 2: LOW COHERENCE → DIVERSION PATH
    # =========================================================================
    
    console.print(f"\n\n")
    console.print(Panel.fit(
        "[bold red]SCENARIO 2: LOW COHERENCE → DIVERSION[/]\n"
        "Intention mismatches outcome → Suppression Of Change",
        border_style="red"
    ))
    
    # Set intention for emotional response
    intention2 = Intention(
        desired_qualities=["emotion", "feeling", "resonance"],
        desired_form="emotional_response",
        clarity=0.8,
        energy=0.7
    )
    
    console.print(f"\n[cyan]INTENTION:[/]")
    console.print(f"  Desired qualities: {intention2.desired_qualities}")
    console.print(f"  Desired form: {intention2.desired_form}")
    console.print(f"  Clarity × Energy: {intention2.calculate_potential_strength():.2f}")
    
    # Process with numeric signal (mismatches emotional intention)
    signal2 = Signal(SignalType.NUMERIC, 12345, 0.6)
    
    console.print(f"\n[cyan]PROCESSING:[/]")
    console.print(f"  Signal: NUMERIC 12345")
    console.print(f"  Free will choice: automatic sequence selection")
    
    result2 = cube.process_with_reflection(signal2, intention2, sequence_name='standard')
    
    console.print(f"\n[cyan]OUTCOME:[/]")
    console.print(f"  Expressed form: {result2['outcome'].expressed_form}")
    console.print(f"  Response data: {len(result2['responses'])} node responses")
    
    console.print(f"\n[cyan]REFLECTION:[/]")
    table2 = Table(show_header=True, box=box.ROUNDED)
    table2.add_column("Node", style="cyan")
    table2.add_column("Coherence Score", style="magenta")
    
    for node_name, score in result2['dimensional_scores'].items():
        table2.add_row(node_name, f"{score:.3f}")
    
    console.print(table2)
    
    console.print(f"\n[bold yellow]PATH DETERMINATION:[/]")
    console.print(f"  Overall coherence: [bold]{result2['overall_coherence']:.3f}[/]")
    console.print(f"  Path choice: [bold red]{result2['path']}[/]")
    console.print(f"  Amplification: [bold red]{result2['amplification']}x[/]")
    console.print(f"  Meaning: [red]Suppression Of Change, Into Simplicity[/red]")
    
    # =========================================================================
    # SCENARIO 3: CONTINUOUS CYCLE
    # =========================================================================
    
    console.print(f"\n\n")
    console.print(Panel.fit(
        "[bold magenta]SCENARIO 3: CONTINUOUS MANIFESTATION CYCLE[/]\n"
        "Outcome becomes new potential → feedback loop",
        border_style="magenta"
    ))
    
    console.print("\n[cyan]Running 10 cycles with varying coherence...[/]\n")
    
    # Track pathway evolution
    pathway_evolution = []
    coherence_evolution = []
    
    for i in range(10):
        # Vary intention clarity to create different coherence levels
        clarity = 0.5 + (i % 5) * 0.1  # Oscillates between 0.5 and 0.9
        
        intention = Intention(
            desired_qualities=["pattern", "learn"],
            desired_form="pattern_response",
            clarity=clarity,
            energy=0.7
        )
        
        signal = Signal(SignalType.PATTERN, [i, i+1, i+2], 0.6)
        result = cube.process_with_reflection(signal, intention)
        
        pathway_evolution.append(cube.pathway_strengths[result['sequence']])
        coherence_evolution.append(result['overall_coherence'])
        
        path_symbol = "↑" if result['path'] == "ALIGNMENT" else "↓"
        console.print(
            f"Cycle {i+1:2d}: "
            f"Coherence={result['overall_coherence']:.3f} "
            f"{path_symbol} {result['path']:10s} "
            f"({result['amplification']}x) "
            f"→ Pathway={cube.pathway_strengths[result['sequence']]:.3f}"
        )
    
    console.print(f"\n[bold yellow]RESULTS:[/]")
    console.print(f"  Pathway strength: {pathway_evolution[0]:.3f} → {pathway_evolution[-1]:.3f}")
    console.print(f"  Change: {(pathway_evolution[-1] / pathway_evolution[0] - 1) * 100:+.1f}%")
    console.print(f"  Avg coherence: {sum(coherence_evolution) / len(coherence_evolution):.3f}")
    
    alignment_count = sum(1 for r in coherence_evolution if r >= 0.7)
    console.print(f"  Alignment cycles: {alignment_count}/10 ({alignment_count*10}%)")
    console.print(f"  Diversion cycles: {10-alignment_count}/10 ({(10-alignment_count)*10}%)")
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold cyan]KEY INSIGHTS[/]\n\n"
        "1. Path choice determined by [bold]SELF-REFLECTION[/], not input quality\n"
        "2. Coherence = multi-dimensional evaluation (each node's perspective)\n"
        "3. ALIGNMENT (coherence ≥ 0.7) → 1.5x amplification → Added Complexity\n"
        "4. DIVERSION (coherence < 0.7) → 0.7x amplification → Suppression\n"
        "5. Outcome becomes new potential → continuous cycle\n"
        "6. Node development weights their influence on coherence evaluation",
        border_style="cyan",
        box=box.DOUBLE
    ))


def demo_node_perspective_differences():
    """Show how different nodes evaluate coherence differently."""
    
    console.print("\n\n[bold cyan]═══════════════════════════════════════════════════════════════[/]")
    console.print("[bold cyan]        NODE-SPECIFIC COHERENCE PERSPECTIVES                    [/]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/]\n")
    
    console.print("Each node evaluates from its domain of consciousness:\n")
    
    cube = MinimalSparkCube()
    
    # Grow nodes differentially
    for _ in range(10):
        cube.process_signal(Signal(SignalType.TEXT, "test", 0.7), 'standard')
    
    intention = Intention(
        desired_qualities=["logical", "emotional", "pattern"],
        desired_form="mixed_response",
        clarity=0.8,
        energy=0.8
    )
    
    signal = Signal(SignalType.TEXT, "complex input", 0.7)
    result = cube.process_with_reflection(signal, intention)
    
    table = Table(show_header=True, box=box.ROUNDED, title="Node Perspectives on Same Intention-Outcome")
    table.add_column("Node", style="cyan", width=15)
    table.add_column("Domain", style="yellow", width=20)
    table.add_column("Evaluates", style="green", width=30)
    table.add_column("Score", style="magenta", width=10)
    
    node_domains = {
        "Reactive": ("Action alignment", "Did action match intent?"),
        "Executive": ("Logical coherence", "Does outcome logically follow?"),
        "Emotional": ("Felt resonance", "Does it feel right?"),
        "Pattern": ("Pattern match", "Do patterns align?"),
        "Perception": ("Form match", "Did form match intention?"),
        "Integration": ("Overall synthesis", "Holistic quality?")
    }
    
    for node_name, score in result['dimensional_scores'].items():
        domain, evaluation = node_domains.get(node_name, ("Unknown", "N/A"))
        table.add_row(node_name, domain, evaluation, f"{score:.3f}")
    
    console.print(table)
    
    console.print(f"\n[bold]Weighted by development → Overall coherence: {result['overall_coherence']:.3f}[/]")
    console.print(f"[bold]Path chosen: {result['path']}[/]")


if __name__ == "__main__":
    demo_manifestation_cycle()
    demo_node_perspective_differences()
    
    console.print("\n[bold green]✓ Reflection system demonstration complete[/]\n")
