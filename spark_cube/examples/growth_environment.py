"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     GROWTH ENVIRONMENT                                         ║
║        Interface for teaching the Spark Cube from zero                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This provides a way to:
1. Feed structured experiences to the cube
2. Observe developmental growth over time
3. Test what the cube has learned
4. Track knowledge encoding in structure
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from spark_cube.core.minimal_spark import (
    MinimalSparkCube, SensorInterface, Signal, SignalType
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import json
from typing import List, Dict, Any


console = Console()


class GrowthEnvironment:
    """
    Environment for growing the Spark Cube through experiences.
    Like raising a child - start with simple, then build complexity.
    """
    
    def __init__(self, cube: MinimalSparkCube = None):
        self.cube = cube or MinimalSparkCube()
        self.sensor = SensorInterface(self.cube)
        self.training_log: List[Dict] = []
    
    def teach_session(self, name: str, experiences: List[Dict]) -> Dict[str, Any]:
        """
        Run a teaching session - a series of related experiences.
        
        Example experience:
        {
            'type': 'text',
            'input': 'hello',
            'context': 'greeting'
        }
        """
        console.print(f"\n[bold cyan]📚 Teaching Session: {name}[/bold cyan]")
        
        initial_dev = self.cube._get_avg_development()
        results = []
        
        for exp in track(experiences, description=f"Processing {name}..."):
            if exp['type'] == 'text':
                result = self.sensor.feed_text(exp['input'], exp.get('metadata', {}))
            elif exp['type'] == 'numeric':
                result = self.sensor.feed_numeric(exp['input'], exp.get('metadata', {}))
            elif exp['type'] == 'binary':
                result = self.sensor.feed_binary(exp['input'], exp.get('metadata', {}))
            elif exp['type'] == 'pattern':
                result = self.sensor.feed_pattern(exp['input'], exp.get('metadata', {}))
            elif exp['type'] == 'sequence':
                result = self.sensor.feed_sequence(exp['input'], exp.get('metadata', {}))
            else:
                continue
            
            results.append(result)
        
        final_dev = self.cube._get_avg_development()
        growth = final_dev - initial_dev
        
        session_summary = {
            'name': name,
            'experiences': len(experiences),
            'initial_development': initial_dev,
            'final_development': final_dev,
            'growth': growth,
            'results': results
        }
        
        self.training_log.append(session_summary)
        
        console.print(f"   Growth: {initial_dev:.3f} → {final_dev:.3f} (+{growth:.3f})")
        
        return session_summary
    
    def show_development(self):
        """Display current development state."""
        state = self.cube.get_state_summary()
        
        table = Table(title="🧠 Current Development State")
        table.add_column("Node", style="cyan")
        table.add_column("Development", justify="right")
        table.add_column("Patterns", justify="right")
        table.add_column("Activations", justify="right")
        
        for nid, nstate in state['node_states'].items():
            dev_bar = "█" * int(nstate['development'] * 20)
            table.add_row(
                nstate['name'],
                f"{nstate['development']:.3f} {dev_bar}",
                str(nstate['patterns_learned']),
                str(nstate['activations'])
            )
        
        console.print(table)
        
        # Pathway strengths
        console.print("\n[bold]Processing Pathways:[/bold]")
        for pathway, strength in state['pathway_strengths'].items():
            strength_bar = "▓" * int(strength * 10)
            console.print(f"   {pathway:12s}: {strength:.2f} {strength_bar}")
        
        # Vertices
        console.print("\n[bold]Connection Vertices:[/bold]")
        for vid, status in state['vertices'].items():
            icon = "●" if status == "connected" else "○"
            console.print(f"   Vertex {vid}: {icon} {status}")
        
        console.print(f"\n[bold]Total Experiences:[/bold] {state['total_experiences']}")
    
    def save_checkpoint(self, name: str):
        """Save current state as a checkpoint."""
        checkpoint_dir = Path("data/checkpoints")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Save cube structure
        cube_path = checkpoint_dir / f"{name}_cube.json"
        self.cube.save_structure(cube_path)
        
        # Save training log
        log_path = checkpoint_dir / f"{name}_log.json"
        with open(log_path, 'w') as f:
            json.dump(self.training_log, f, indent=2)
        
        console.print(f"\n✅ Checkpoint saved: {name}")
    
    def load_checkpoint(self, name: str):
        """Load a previous checkpoint."""
        checkpoint_dir = Path("data/checkpoints")
        
        cube_path = checkpoint_dir / f"{name}_cube.json"
        log_path = checkpoint_dir / f"{name}_log.json"
        
        if cube_path.exists():
            self.cube.load_structure(cube_path)
        
        if log_path.exists():
            with open(log_path, 'r') as f:
                self.training_log = json.load(f)
        
        console.print(f"\n✅ Checkpoint loaded: {name}")
    
    def test_recognition(self, test_cases: List[Dict]) -> Dict[str, Any]:
        """
        Test what the cube has learned.
        Returns recognition statistics.
        """
        console.print("\n[bold yellow]🧪 Testing Recognition...[/bold yellow]")
        
        results = {
            'total': len(test_cases),
            'recognized': 0,
            'unrecognized': 0,
            'details': []
        }
        
        for test in test_cases:
            if test['type'] == 'text':
                result = self.sensor.feed_text(test['input'])
            elif test['type'] == 'numeric':
                result = self.sensor.feed_numeric(test['input'])
            else:
                continue
            
            # Check if any responses were generated
            has_response = len(result.get('responses', [])) > 0
            
            if has_response:
                results['recognized'] += 1
                status = "✓"
            else:
                results['unrecognized'] += 1
                status = "✗"
            
            results['details'].append({
                'input': test['input'],
                'recognized': has_response,
                'responses': result.get('responses', [])
            })
            
            console.print(f"   {status} {test['input']}: {'recognized' if has_response else 'unknown'}")
        
        console.print(f"\n   Recognition Rate: {results['recognized']}/{results['total']} "
                     f"({100*results['recognized']/results['total']:.1f}%)")
        
        return results


# =============================================================================
# EXAMPLE: TEACHING BASIC CONCEPTS
# =============================================================================

def example_growth_from_zero():
    """Demonstrate growing a cube from absolute zero."""
    
    console.print(Panel(
        "[bold]GROWTH FROM ZERO DEMONSTRATION[/bold]\n\n"
        "We will teach the cube basic concepts through repeated exposure.\n"
        "Watch as nodes develop and patterns strengthen.\n\n"
        "No external knowledge - only structural learning.",
        border_style="green"
    ))
    
    env = GrowthEnvironment()
    
    # Session 1: Basic text patterns
    basic_words = [
        {'type': 'text', 'input': 'hello', 'metadata': {'context': 'greeting'}},
        {'type': 'text', 'input': 'hello', 'metadata': {'context': 'greeting'}},
        {'type': 'text', 'input': 'goodbye', 'metadata': {'context': 'farewell'}},
        {'type': 'text', 'input': 'goodbye', 'metadata': {'context': 'farewell'}},
        {'type': 'text', 'input': 'yes', 'metadata': {'context': 'affirmation'}},
        {'type': 'text', 'input': 'no', 'metadata': {'context': 'negation'}},
        {'type': 'text', 'input': 'yes', 'metadata': {'context': 'affirmation'}},
        {'type': 'text', 'input': 'no', 'metadata': {'context': 'negation'}},
    ]
    env.teach_session("Basic Words", basic_words)
    
    # Session 2: Numbers
    numbers = [
        {'type': 'numeric', 'input': i, 'metadata': {'context': 'counting'}}
        for i in range(10)
    ] * 2  # Repeat twice
    env.teach_session("Numbers 0-9", numbers)
    
    # Session 3: Binary patterns
    binary = [
        {'type': 'binary', 'input': True, 'metadata': {'context': 'boolean'}},
        {'type': 'binary', 'input': False, 'metadata': {'context': 'boolean'}},
    ] * 10
    env.teach_session("True/False", binary)
    
    # Session 4: More words (expanding vocabulary)
    more_words = [
        {'type': 'text', 'input': word, 'metadata': {'context': 'vocabulary'}}
        for word in ['cat', 'dog', 'bird', 'fish'] * 3
    ]
    env.teach_session("Animals", more_words)
    
    # Show development
    env.show_development()
    
    # Test recognition
    console.print("\n" + "="*60)
    test_cases = [
        {'type': 'text', 'input': 'hello'},      # Should recognize
        {'type': 'text', 'input': 'goodbye'},    # Should recognize
        {'type': 'text', 'input': 'cat'},        # Should recognize
        {'type': 'text', 'input': 'elephant'},   # Should NOT recognize (never seen)
        {'type': 'numeric', 'input': 5},         # Should recognize
        {'type': 'numeric', 'input': 999},       # Should NOT recognize
    ]
    
    results = env.test_recognition(test_cases)
    
    # Save checkpoint
    env.save_checkpoint("basic_concepts")
    
    console.print("\n" + "="*60)
    console.print("[bold green]SUMMARY[/bold green]")
    console.print(f"  Total Experiences: {env.cube.total_experiences}")
    console.print(f"  Average Development: {env.cube._get_avg_development():.3f}")
    console.print(f"  Recognition Rate: {results['recognized']}/{results['total']}")
    console.print("\n  The cube has grown from zero through structural encoding.")
    console.print("  Each pattern is stored in node weights, not external memory.")


if __name__ == "__main__":
    example_growth_from_zero()
