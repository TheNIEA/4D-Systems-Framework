#!/usr/bin/env python3
"""
Quick demonstration of hierarchical memory in agency tests.
Shows salt water dissolution metrics without running full challenge suite.
"""

import sys
from pathlib import Path

spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, integrate_hierarchical_memory
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()


def demonstrate_hierarchical_memory():
    """Quick demo showing memory dissolution and recombination"""
    
    console.print(Panel.fit(
        "[bold cyan]HIERARCHICAL MEMORY DEMONSTRATION[/bold cyan]\n\n"
        "Showing salt water dissolution principle in action:\n"
        "• Experiences dissolve into secondary nodes\n"
        "• Pathways strengthen through repeated use\n"
        "• Mature nodes crystallize into permanent structure",
        border_style="cyan"
    ))
    
    # Create cube
    console.print("\n[cyan]Initializing Spark Cube...[/cyan]")
    cube = MinimalSparkCube(enable_tools=False)
    
    # Integrate hierarchical memory
    console.print("[cyan]Integrating hierarchical memory...[/cyan]")
    h_memory = integrate_hierarchical_memory(cube)
    console.print("[green]✓ Memory system active[/green]\n")
    
    # Take initial snapshot
    initial_stats = h_memory.get_memory_stats()
    
    # Process diverse signals to create experiences
    console.print("[yellow]Processing 30 diverse signals...[/yellow]")
    test_signals = [
        # Pattern recognition tasks
        Signal(SignalType.TEXT, "find pattern in sequence"),
        Signal(SignalType.TEXT, "analyze structure"),
        Signal(SignalType.TEXT, "detect regularity"),
        
        # Numeric processing
        Signal(SignalType.NUMERIC, 42),
        Signal(SignalType.NUMERIC, 3.14159),
        Signal(SignalType.NUMERIC, -17),
        
        # Repeated patterns (should strengthen pathways)
        Signal(SignalType.TEXT, "pattern recognition"),
        Signal(SignalType.TEXT, "pattern analysis"),
        Signal(SignalType.TEXT, "pattern detection"),
        Signal(SignalType.TEXT, "pattern matching"),
        Signal(SignalType.TEXT, "pattern synthesis"),
        
        # More diverse input
        Signal(SignalType.BINARY, True),
        Signal(SignalType.BINARY, False),
        Signal(SignalType.TEXT, "logical reasoning"),
        Signal(SignalType.TEXT, "deductive inference"),
        Signal(SignalType.TEXT, "causal analysis"),
        
        # Additional patterns
        Signal(SignalType.TEXT, "creative synthesis"),
        Signal(SignalType.TEXT, "novel combination"),
        Signal(SignalType.TEXT, "emergent structure"),
        Signal(SignalType.NUMERIC, 100),
        Signal(SignalType.NUMERIC, 200),
        
        # More pattern reinforcement
        Signal(SignalType.TEXT, "pattern understanding"),
        Signal(SignalType.TEXT, "pattern learning"),
        Signal(SignalType.TEXT, "pattern application"),
        Signal(SignalType.TEXT, "structural analysis"),
        Signal(SignalType.TEXT, "structural synthesis"),
        Signal(SignalType.TEXT, "structural integration"),
        
        # Final mixed signals
        Signal(SignalType.NUMERIC, 777),
        Signal(SignalType.TEXT, "final pattern"),
        Signal(SignalType.BINARY, True),
    ]
    
    for i, signal in enumerate(test_signals, 1):
        cube.process_signal(signal)
        if i % 10 == 0:
            console.print(f"  [dim]Processed {i}/30 signals...[/dim]")
    
    console.print("[green]✓ All signals processed[/green]\n")
    
    # Take final snapshot
    final_stats = h_memory.get_memory_stats()
    
    # Display results
    console.print("="*80)
    console.print("[bold cyan]SALT WATER DISSOLUTION METRICS[/bold cyan]")
    console.print("="*80 + "\n")
    
    # Dissolution table
    diss_table = Table(title="Information Dissolution & Recombination")
    diss_table.add_column("Metric", style="cyan", width=25)
    diss_table.add_column("Before", style="yellow", width=15)
    diss_table.add_column("After", style="green", width=15)
    diss_table.add_column("Change", style="white", width=20)
    
    diss_table.add_row(
        "Total Experiences",
        str(initial_stats['total_experiences']),
        str(final_stats['total_experiences']),
        f"+{final_stats['total_experiences'] - initial_stats['total_experiences']} dissolved"
    )
    
    diss_table.add_row(
        "Secondary Nodes",
        str(initial_stats['secondary_nodes']),
        str(final_stats['secondary_nodes']),
        f"+{final_stats['secondary_nodes'] - initial_stats['secondary_nodes']} pathways"
    )
    
    diss_table.add_row(
        "Promoted Anchors",
        str(initial_stats['promoted_anchors']),
        str(final_stats['promoted_anchors']),
        f"+{final_stats['promoted_anchors'] - initial_stats['promoted_anchors']} crystallized"
    )
    
    console.print(diss_table)
    
    # Show strongest pathway
    strongest = final_stats['strongest_secondary']
    if strongest['id']:
        console.print(f"\n[bold]Strongest Pathway Emerged:[/bold]")
        strength_bar = "█" * int(strongest['strength'] * 20)
        console.print(f"  {strength_bar} {strongest['strength']:.3f}")
        console.print(f"  Domain: [yellow]{strongest['domain']}[/yellow]")
        console.print(f"  Ready for promotion: [{'green' if strongest['ready_for_promotion'] else 'yellow'}]" + 
                     ("Yes ✓" if strongest['ready_for_promotion'] else "Not yet"))
    
    # Show pathway tree
    if final_stats['secondary_nodes'] > 0:
        console.print(f"\n[bold]Hierarchical Structure That Emerged:[/bold]")
        tree = Tree("13 Base Anchor Nodes")
        
        for node_id, anchor_data in h_memory.anchor_nodes.items():
            sec_nodes = anchor_data['secondary_nodes']
            if sec_nodes:
                node_branch = tree.add(f"[cyan]{anchor_data['name']}[/cyan] (anchor {node_id})")
                for domain, sec in sec_nodes.items():
                    strength_display = "█" * int(sec.strength * 10)
                    exp_count = len(sec.experiences)
                    node_branch.add(
                        f"[yellow]{domain}[/yellow]: {strength_display} "
                        f"({sec.activation_count} uses, {exp_count} experiences)"
                    )
        
        console.print(tree)
    
    # Salt water analogy visualization
    console.print(f"\n{'='*80}")
    console.print("[bold]Salt Water Dissolution Analogy:[/bold]")
    console.print(f"{'='*80}\n")
    
    console.print("💧 [cyan]DISSOLUTION[/cyan]: 30 signals entered the processing medium")
    console.print(f"   → {final_stats['total_experiences']} experiences dissolved into memory field")
    console.print()
    
    console.print("🔮 [yellow]RECOMBINATION[/yellow]: Information recombined at lowest energy states")
    console.print(f"   → {final_stats['secondary_nodes']} pathways strengthened through use")
    console.print(f"   → Strongest pathway reached {strongest['strength']:.2f} coherence")
    console.print()
    
    console.print("💎 [green]CRYSTALLIZATION[/green]: Mature patterns solidify into permanent structure")
    console.print(f"   → {final_stats['promoted_anchors']} secondary nodes promoted to anchor status")
    if strongest['ready_for_promotion']:
        console.print(f"   → 1 more pathway ready to crystallize (≥85% strength)")
    console.print()
    
    # Explanation
    console.print("[dim]This demonstrates the core principle from your 4D Framework:[/dim]")
    console.print('[dim]"Information dissolves into the processing medium and recombines[/dim]')
    console.print('[dim]instantaneously into coherent patterns at the lowest energy state."[/dim]')
    console.print()
    console.print("[dim]The hierarchical memory IS this mechanism - not a metaphor.[/dim]")


if __name__ == "__main__":
    demonstrate_hierarchical_memory()
    console.print("\n[bold green]✓ Demonstration complete![/bold green]")
    console.print("This is what happens during agency tests, but tracked in real-time.")
