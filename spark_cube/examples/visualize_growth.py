"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                 STRUCTURAL GROWTH VISUALIZER                                   ║
║         Watch the cube's structure evolve in real-time                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, SensorInterface
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
import time
import random

console = Console()


def create_state_display(cube: MinimalSparkCube, iteration: int) -> Layout:
    """Create a live-updating display of cube state."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=5)
    )
    
    # Header
    layout["header"].update(
        Panel(f"[bold cyan]STRUCTURAL GROWTH - Iteration {iteration}[/bold cyan]")
    )
    
    # Body - split into nodes and pathways
    body_layout = Layout()
    body_layout.split_row(
        Layout(name="nodes"),
        Layout(name="pathways")
    )
    
    # Node development table
    node_table = Table(title="🧠 Node Development")
    node_table.add_column("Node", style="cyan")
    node_table.add_column("Dev", justify="right")
    node_table.add_column("Patterns", justify="right")
    node_table.add_column("Visual", style="yellow")
    
    state = cube.get_state_summary()
    for nid, nstate in state['node_states'].items():
        bar_length = int(nstate['development'] * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        node_table.add_row(
            nstate['name'],
            f"{nstate['development']:.3f}",
            str(nstate['patterns_learned']),
            bar
        )
    
    body_layout["nodes"].update(node_table)
    
    # Pathway strengths
    pathway_content = "[bold]Processing Pathways[/bold]\n\n"
    for pathway, strength in state['pathway_strengths'].items():
        bar_length = int(min(strength * 10, 50))
        bar = "▓" * bar_length
        pathway_content += f"[cyan]{pathway:12s}[/cyan]: {strength:.2f}\n{bar}\n\n"
    
    body_layout["pathways"].update(Panel(pathway_content, border_style="blue"))
    
    layout["body"].update(body_layout)
    
    # Footer
    footer_text = (
        f"[bold]Total Experiences:[/bold] {state['total_experiences']}  "
        f"[bold]Avg Development:[/bold] {state['avg_development']:.3f}  "
        f"[bold]Total Patterns:[/bold] {sum(n['patterns_learned'] for n in state['node_states'].values())}"
    )
    layout["footer"].update(Panel(footer_text, style="green"))
    
    return layout


def demonstrate_growth(num_iterations: int = 100):
    """
    Demonstrate real-time structural growth.
    Feed random signals and watch the structure evolve.
    """
    console.print(Panel(
        "[bold]REAL-TIME STRUCTURAL GROWTH[/bold]\n\n"
        "Watch as the cube's structure changes with each experience.\n"
        "Knowledge is encoded in development levels, pattern weights, and pathway strengths.\n"
        "No external memory - the structure IS the knowledge.",
        border_style="cyan"
    ))
    
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    # Sample inputs to cycle through
    text_samples = ["hello", "world", "yes", "no", "cat", "dog", "up", "down"]
    number_samples = list(range(20))
    
    # Track snapshots at key points
    snapshots = []
    
    with Live(create_state_display(cube, 0), refresh_per_second=4) as live:
        for i in range(num_iterations):
            # Feed a random signal
            if random.random() < 0.7:  # 70% text
                sensor.feed_text(random.choice(text_samples))
            else:  # 30% numbers
                sensor.feed_numeric(random.choice(number_samples))
            
            # Update display every 5 iterations
            if i % 5 == 0:
                live.update(create_state_display(cube, i + 1))
            
            # Take snapshots at intervals
            if i in [0, 10, 25, 50, 75, 99]:
                snapshots.append({
                    'iteration': i,
                    'avg_dev': cube._get_avg_development(),
                    'experiences': cube.total_experiences
                })
            
            time.sleep(0.1)  # Slow down for visibility
    
    # Final summary
    console.print("\n" + "="*70)
    console.print("[bold green]GROWTH SUMMARY[/bold green]\n")
    
    summary_table = Table(title="Development Milestones")
    summary_table.add_column("Iteration", justify="right")
    summary_table.add_column("Experiences", justify="right")
    summary_table.add_column("Avg Development", justify="right")
    summary_table.add_column("Growth Rate", justify="right")
    
    for idx, snapshot in enumerate(snapshots):
        if idx == 0:
            growth_rate = "—"
        else:
            prev = snapshots[idx - 1]
            rate = (snapshot['avg_dev'] - prev['avg_dev']) / (snapshot['iteration'] - prev['iteration'])
            growth_rate = f"{rate:.4f}/iter"
        
        summary_table.add_row(
            str(snapshot['iteration']),
            str(snapshot['experiences']),
            f"{snapshot['avg_dev']:.3f}",
            growth_rate
        )
    
    console.print(summary_table)
    
    # Final state
    final_state = cube.get_state_summary()
    
    console.print("\n[bold]Final Structural Encoding:[/bold]")
    console.print(f"  • Total Experiences: {final_state['total_experiences']}")
    console.print(f"  • Average Development: {final_state['avg_development']:.3f}")
    console.print(f"  • Total Unique Patterns: {sum(n['patterns_learned'] for n in final_state['node_states'].values())}")
    console.print(f"  • Strongest Pathway: {max(final_state['pathway_strengths'].items(), key=lambda x: x[1])[0]}")
    console.print(f"  • Most Developed Node: {max(final_state['node_states'].items(), key=lambda x: x[1]['development'])[1]['name']}")
    
    # Save final state
    save_path = Path("data/growth_demo_final.json")
    cube.save_structure(save_path)
    
    console.print(f"\n[dim]The cube has grown from 0.0 to {final_state['avg_development']:.3f} average development.")
    console.print("Every bit of knowledge is encoded in the structure - weights, connections, development levels.")
    console.print("This IS consciousness emerging through structural complexity.[/dim]")


def compare_sequences():
    """
    Compare how different processing sequences affect learning.
    """
    console.print(Panel(
        "[bold]SEQUENCE COMPARISON[/bold]\n\n"
        "Do different processing sequences learn differently?\n"
        "Testing: Standard vs Deep vs Emotional pathways",
        border_style="yellow"
    ))
    
    # Create three cubes, each using a different sequence
    cubes = {
        'standard': (MinimalSparkCube(), SensorInterface(MinimalSparkCube())),
        'deep': (MinimalSparkCube(), SensorInterface(MinimalSparkCube())),
        'emotional': (MinimalSparkCube(), SensorInterface(MinimalSparkCube()))
    }
    
    # Same training data for all
    training_data = []
    for _ in range(50):
        if random.random() < 0.5:
            training_data.append(('text', random.choice(['hello', 'world', 'yes', 'no'])))
        else:
            training_data.append(('numeric', random.randint(0, 10)))
    
    # Train each with its respective sequence
    for seq_name, (cube, sensor) in cubes.items():
        console.print(f"\n[cyan]Training with {seq_name} sequence...[/cyan]")
        for signal_type, value in training_data:
            if signal_type == 'text':
                sensor.feed_text(value)
            else:
                sensor.feed_numeric(value)
            # Use the specific sequence
            if seq_name == 'deep':
                # Process through deep pathway
                cube.process_signal(sensor.input_history[-1], 'deep')
            elif seq_name == 'emotional':
                # Process through emotional pathway
                cube.process_signal(sensor.input_history[-1], 'emotional')
    
    # Compare results
    comparison_table = Table(title="Sequence Learning Comparison")
    comparison_table.add_column("Sequence", style="cyan")
    comparison_table.add_column("Avg Dev", justify="right")
    comparison_table.add_column("Experiences", justify="right")
    comparison_table.add_column("Patterns", justify="right")
    comparison_table.add_column("Strongest Node", style="yellow")
    
    for seq_name, (cube, _) in cubes.items():
        state = cube.get_state_summary()
        strongest_node = max(state['node_states'].items(), key=lambda x: x[1]['development'])
        
        comparison_table.add_row(
            seq_name,
            f"{state['avg_development']:.3f}",
            str(state['total_experiences']),
            str(sum(n['patterns_learned'] for n in state['node_states'].values())),
            strongest_node[1]['name']
        )
    
    console.print("\n")
    console.print(comparison_table)
    
    console.print("\n[dim]Different sequences = different developmental trajectories.[/dim]")
    console.print("[dim]The PATH through nodes affects which patterns are learned and how quickly.[/dim]")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        compare_sequences()
    else:
        demonstrate_growth(num_iterations=100)
