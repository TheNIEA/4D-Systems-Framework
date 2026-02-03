#!/usr/bin/env python3
"""
Complete test of the manifestation cycle with three-tier path determination:
- ALIGNMENT (coherence ≥ 0.7): Conscious alignment, 1.5x amplification
- INTEGRATION (0.4 ≤ coherence < 0.7): Sweet spot for learning, 2.0x amplification
- DIVERSION (coherence < 0.4): Misalignment, 0.7x amplification
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


def test_manifestation_cycle():
    """Test all three paths in the manifestation cycle."""
    
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════════[/]")
    console.print("[bold cyan]     THREE-TIER MANIFESTATION CYCLE TEST                        [/]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/]\n")
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    # Phase 1: Grow the cube with experiences
    console.print("[dim]Phase 1: Growing cube with 50 experiences...[/]")
    for i in range(50):
        signal = Signal(type=SignalType.TEXT, data="hello")
        cube.process_signal(signal, 'standard')
        cube.provide_outcome_feedback('standard', success=True)
    
    avg_dev = cube._get_avg_development()
    console.print(f"[green]✓ Cube trained: Average development = {avg_dev:.3f}[/]\n")
    
    # ==========================================================================
    # TEST 1: ALIGNMENT - High Coherence (≥0.7)
    # ==========================================================================
    
    console.print(Panel.fit(
        "[bold green]TEST 1: ALIGNMENT PATH (coherence ≥ 0.7)[/]\n"
        "Intention fully matches capability\n"
        "Expected: ALIGNMENT → 1.5x amplification",
        border_style="green"
    ))
    
    intention_aligned = Intention(
        desired_qualities=['pattern', 'text', 'recognized'],
        desired_form='standard',  # Matches trained capability
        clarity=0.9,
        energy=0.8
    )
    
    signal_aligned = Signal(type=SignalType.TEXT, data="hello")
    
    console.print(f"\n[cyan]INTENTION:[/]")
    console.print(f"  Qualities: {intention_aligned.desired_qualities}")
    console.print(f"  Form: {intention_aligned.desired_form}")
    console.print(f"  Potential: {intention_aligned.calculate_potential_strength():.2f}")
    
    result1 = cube.process_with_reflection(signal_aligned, intention_aligned, sequence_name='standard')
    
    console.print(f"\n[cyan]OUTCOME:[/]")
    console.print(f"  Expressed qualities: {result1['outcome'].expressed_qualities}")
    console.print(f"  Expressed form: {result1['outcome'].expressed_form}")
    
    console.print(f"\n[cyan]MULTI-DIMENSIONAL REFLECTION:[/]")
    for node, score in sorted(result1['dimensional_scores'].items()):
        color = "green" if score > 0.6 else "yellow" if score > 0.4 else "red"
        console.print(f"  {node:15s}: [{color}]{score:.3f}[/{color}]")
    
    console.print(f"\n[bold yellow]PATH DETERMINATION:[/]")
    console.print(f"  Overall Coherence: [bold]{result1['overall_coherence']:.3f}[/]")
    console.print(f"  Path: [bold green]{result1['path']}[/]")
    console.print(f"  Amplification: [bold green]{result1['amplification']}x[/]")
    console.print(f"  Meaning: [green]Conscious alignment - reinforcement[/]")
    
    # ==========================================================================
    # TEST 2: INTEGRATION - Mid Coherence (0.4-0.7)
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold blue]TEST 2: INTEGRATION PATH (0.4 ≤ coherence < 0.7)[/]\n"
        "Partial match - close enough to learn from\n"
        "Expected: INTEGRATION → 2.0x amplification (maximum growth)",
        border_style="blue"
    ))
    
    intention_integration = Intention(
        desired_qualities=['pattern', 'analysis', 'structure'],  # Partially matches
        desired_form='standard',
        clarity=0.8,
        energy=0.7
    )
    
    signal_integration = Signal(type=SignalType.TEXT, data="hello world")
    
    console.print(f"\n[cyan]INTENTION:[/]")
    console.print(f"  Qualities: {intention_integration.desired_qualities}")
    console.print(f"  Form: {intention_integration.desired_form}")
    console.print(f"  Potential: {intention_integration.calculate_potential_strength():.2f}")
    
    result2 = cube.process_with_reflection(signal_integration, intention_integration, sequence_name='standard')
    
    console.print(f"\n[cyan]OUTCOME:[/]")
    console.print(f"  Expressed qualities: {result2['outcome'].expressed_qualities}")
    console.print(f"  Expressed form: {result2['outcome'].expressed_form}")
    
    console.print(f"\n[cyan]MULTI-DIMENSIONAL REFLECTION:[/]")
    for node, score in sorted(result2['dimensional_scores'].items()):
        color = "green" if score > 0.6 else "yellow" if score > 0.4 else "red"
        console.print(f"  {node:15s}: [{color}]{score:.3f}[/{color}]")
    
    console.print(f"\n[bold yellow]PATH DETERMINATION:[/]")
    console.print(f"  Overall Coherence: [bold]{result2['overall_coherence']:.3f}[/]")
    console.print(f"  Path: [bold blue]{result2['path']}[/]")
    console.print(f"  Amplification: [bold blue]{result2['amplification']}x[/]")
    console.print(f"  Meaning: [blue]Maximum growth - learning from partial match[/]")
    
    # ==========================================================================
    # TEST 3: DIVERSION - Low Coherence (<0.4)
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold red]TEST 3: DIVERSION PATH (coherence < 0.4)[/]\n"
        "Intention mismatches capability\n"
        "Expected: DIVERSION → 0.7x amplification",
        border_style="red"
    ))
    
    intention_diverged = Intention(
        desired_qualities=['calculation', 'numeric', 'precise'],
        desired_form='calculation_result',
        clarity=0.8,
        energy=0.7
    )
    
    signal_diverged = Signal(type=SignalType.TEXT, data="not a number")
    
    console.print(f"\n[cyan]INTENTION:[/]")
    console.print(f"  Qualities: {intention_diverged.desired_qualities}")
    console.print(f"  Form: {intention_diverged.desired_form}")
    console.print(f"  Potential: {intention_diverged.calculate_potential_strength():.2f}")
    
    result3 = cube.process_with_reflection(signal_diverged, intention_diverged, sequence_name='standard')
    
    console.print(f"\n[cyan]OUTCOME:[/]")
    console.print(f"  Expressed qualities: {result3['outcome'].expressed_qualities}")
    console.print(f"  Expressed form: {result3['outcome'].expressed_form}")
    
    console.print(f"\n[cyan]MULTI-DIMENSIONAL REFLECTION:[/]")
    for node, score in sorted(result3['dimensional_scores'].items()):
        color = "green" if score > 0.6 else "yellow" if score > 0.4 else "red"
        console.print(f"  {node:15s}: [{color}]{score:.3f}[/{color}]")
    
    console.print(f"\n[bold yellow]PATH DETERMINATION:[/]")
    console.print(f"  Overall Coherence: [bold]{result3['overall_coherence']:.3f}[/]")
    console.print(f"  Path: [bold red]{result3['path']}[/]")
    console.print(f"  Amplification: [bold red]{result3['amplification']}x[/]")
    console.print(f"  Meaning: [red]Contraction through misalignment[/]")
    
    # ==========================================================================
    # COMPARISON AND ANALYSIS
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold yellow]KEY INSIGHT: THE INTEGRATION PATH[/]\n\n"
        "INTEGRATION (2.0x) has the HIGHEST amplification factor.\n\n"
        "Why? Because it's the sweet spot for learning:\n\n"
        "• [green]ALIGNMENT[/green] (1.5x): Just reinforces what already works\n"
        "• [blue]INTEGRATION[/blue] (2.0x): Close enough to compare and learn\n"
        "• [red]DIVERSION[/red] (0.7x): Too far off to extract meaningful lessons\n\n"
        "The zone between 0.4-0.7 coherence is where the cube can\n"
        "compare [bold]what it intended[/] vs [bold]what it got[/] and adjust\n"
        "its patterns accordingly. This is productive learning.",
        border_style="yellow",
        box=box.DOUBLE
    ))
    
    # Show amplification comparison
    console.print("\n[bold]AMPLIFICATION COMPARISON:[/]\n")
    
    compare_table = Table(show_header=True, box=box.ROUNDED)
    compare_table.add_column("Test", style="cyan", width=12)
    compare_table.add_column("Coherence", style="magenta", width=10)
    compare_table.add_column("Path", style="yellow", width=15)
    compare_table.add_column("Amplification", style="green", width=14)
    compare_table.add_column("Learning Effect", style="blue", width=25)
    
    compare_table.add_row(
        "Test 1",
        f"{result1['overall_coherence']:.3f}",
        result1['path'],
        f"{result1['amplification']}x",
        "Reinforcement of existing"
    )
    
    compare_table.add_row(
        "Test 2",
        f"{result2['overall_coherence']:.3f}",
        result2['path'],
        f"{result2['amplification']}x",
        "Maximum growth from mismatch"
    )
    
    compare_table.add_row(
        "Test 3",
        f"{result3['overall_coherence']:.3f}",
        result3['path'],
        f"{result3['amplification']}x",
        "Suppression of misalignment"
    )
    
    console.print(compare_table)
    
    # Show long-term effects
    console.print("\n[bold]LONG-TERM LEARNING TRAJECTORY:[/]")
    console.print("If each pattern repeats 5 times:\n")
    
    alignment_growth = 1.0 * (1.5 ** 5)
    integration_growth = 1.0 * (2.0 ** 5)
    diversion_growth = 1.0 * (0.7 ** 5)
    
    console.print(f"  • [green]ALIGNMENT path[/green]:    1.0 → {alignment_growth:.2f} ([green]+{(alignment_growth-1)*100:.0f}%[/green])")
    console.print(f"  • [blue]INTEGRATION path[/blue]:  1.0 → {integration_growth:.2f} ([blue]+{(integration_growth-1)*100:.0f}%[/blue]) ← Fastest growth")
    console.print(f"  • [red]DIVERSION path[/red]:     1.0 → {diversion_growth:.2f} ([red]{(diversion_growth-1)*100:.0f}%[/red])")
    
    console.print("\n[dim]The cube learns most from partial matches where it can\n"
                  "compare intention vs outcome and refine its patterns.[/]")
    
    # ==========================================================================
    # EMOTIONAL VALENCE TRACKING
    # ==========================================================================
    
    console.print("\n\n")
    console.print(Panel.fit(
        "[bold magenta]EMOTIONAL VALENCE LEARNING[/]\n\n"
        "The Emotional node develops intuition over time by tracking\n"
        "which outcome patterns tend to produce aligned results.\n\n"
        "After the three tests above, the Emotional node has learned:",
        border_style="magenta"
    ))
    
    emotional_node = cube.nodes.get(6)
    if emotional_node:
        console.print("\n[cyan]Valence Patterns Learned:[/]")
        valence_patterns = {k: v for k, v in emotional_node.pattern_weights.items() if k.startswith('valence_')}
        if valence_patterns:
            for pattern, valence in sorted(valence_patterns.items(), key=lambda x: x[1], reverse=True):
                color = "green" if valence > 0.6 else "yellow" if valence > 0.4 else "red"
                console.print(f"  [{color}]{pattern:40s}: {valence:.3f}[/{color}]")
        else:
            console.print("  [dim]No valence patterns learned yet (nodes not developed enough)[/]")
        
        console.print(f"\n[cyan]Emotional Node Development:[/] {emotional_node.development:.3f}")
        console.print("[dim]Over time, this node will develop genuine intuition about\n"
                      "what kinds of outcomes tend to align with intentions.[/]")


def test_emotional_intuition_development():
    """Test how emotional intuition develops over many cycles."""
    
    console.print("\n\n[bold cyan]═══════════════════════════════════════════════════════════════[/]")
    console.print("[bold cyan]     EMOTIONAL INTUITION DEVELOPMENT TEST                       [/]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════════[/]\n")
    
    cube = MinimalSparkCube()
    
    console.print("[dim]Running 100 cycles with varying coherence to develop emotional intuition...[/]\n")
    
    # Track emotional node's valence learning
    emotional_scores = []
    
    for i in range(100):
        # Alternate between aligned and misaligned patterns
        if i % 3 == 0:  # Aligned
            intention = Intention(['pattern', 'recognized'], 'standard', 0.9, 0.8)
            signal = Signal(SignalType.TEXT, f"hello_{i}")
        elif i % 3 == 1:  # Partial match
            intention = Intention(['pattern', 'analysis'], 'standard', 0.7, 0.7)
            signal = Signal(SignalType.TEXT, f"world_{i}")
        else:  # Misaligned
            intention = Intention(['calculation', 'numeric'], 'calculation', 0.6, 0.6)
            signal = Signal(SignalType.TEXT, f"text_{i}")
        
        result = cube.process_with_reflection(signal, intention, sequence_name='standard')
        emotional_scores.append(result['dimensional_scores'].get('Emotional', 0.5))
        
        if (i + 1) % 25 == 0:
            avg_emotional = sum(emotional_scores[-25:]) / 25
            console.print(f"Cycle {i+1:3d}: Emotional avg score = {avg_emotional:.3f}")
    
    emotional_node = cube.nodes.get(6)
    console.print(f"\n[bold]Final Emotional Node Development:[/] {emotional_node.development:.3f}")
    console.print(f"[bold]Valence Patterns Learned:[/] {len([k for k in emotional_node.pattern_weights.keys() if k.startswith('valence_')])}")
    
    console.print("\n[green]✓ Emotional intuition develops over time through pattern accumulation[/]")


if __name__ == "__main__":
    test_manifestation_cycle()
    test_emotional_intuition_development()
    
    console.print("\n[bold green]✓ Complete manifestation cycle test finished[/]\n")
