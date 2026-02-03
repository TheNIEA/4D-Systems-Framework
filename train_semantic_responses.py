"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║           SEMANTIC RESPONSE TRAINING                                          ║
║     Train the system to generate responses through ACTUAL EXAMPLES            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Instead of trying to synthesize capabilities directly, we:
1. Process real questions that REQUIRE responses
2. Let the AGI engine detect the gap
3. Allow it to synthesize needed capabilities
4. Repeat with variations to strengthen pathways

This is directed learning through exercise, not manufacturing.
"""

import sys
from pathlib import Path

# Add paths for imports
spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, integrate_hierarchical_memory
from dataclasses import dataclass
from typing import Dict, List, Any
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


@dataclass
class TrainingExample:
    """A training example that requires semantic response"""
    question: str
    context: Dict[str, Any]
    category: str
    expected_features: List[str]  # Features we expect in a good response


class SemanticResponseTrainer:
    """
    Trains the system to generate semantic responses by processing examples.
    This triggers the AGI engine to synthesize needed capabilities.
    """
    
    def __init__(self, cube: MinimalSparkCube, memory):
        self.cube = cube
        self.memory = memory
        self.training_log = []
        
    def train(self, examples: List[TrainingExample], iterations: int = 3) -> Dict[str, Any]:
        """
        Train on examples multiple times to strengthen response pathways.
        The AGI engine should detect gaps and synthesize capabilities.
        """
        console.print(Panel.fit(
            "[bold cyan]SEMANTIC RESPONSE TRAINING[/bold cyan]\n\n"
            "[yellow]Training Strategy:[/yellow]\n"
            "  • Process questions that REQUIRE semantic responses\n"
            "  • AGI engine detects capability gaps\n"
            "  • System synthesizes needed response capabilities\n"
            "  • Hierarchical memory strengthens successful patterns\n\n"
            f"[green]{len(examples)} Training Examples × {iterations} Iterations[/green]\n"
            f"[green]= {len(examples) * iterations} Total Training Steps[/green]",
            border_style="cyan"
        ))
        
        # Track capability growth
        start_secondary_nodes = sum(
            1 for anchor in self.memory.anchor_nodes.values()
            for _ in anchor.get('secondary_nodes', {})
        )
        start_promoted = len(self.memory.promoted_anchors)
        
        # Training loop
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            
            task = progress.add_task(
                "[cyan]Training semantic responses...",
                total=len(examples) * iterations
            )
            
            for iteration in range(iterations):
                console.print(f"\n[bold yellow]Iteration {iteration + 1}/{iterations}[/bold yellow]")
                
                for example in examples:
                    result = self._train_on_example(example, iteration)
                    self.training_log.append(result)
                    progress.update(task, advance=1)
        
        # Analyze results
        end_secondary_nodes = sum(
            1 for anchor in self.memory.anchor_nodes.values()
            for _ in anchor.get('secondary_nodes', {})
        )
        end_promoted = len(self.memory.promoted_anchors)
        
        summary = self._analyze_training(
            start_secondary_nodes,
            end_secondary_nodes,
            start_promoted,
            end_promoted
        )
        
        return summary
    
    def _train_on_example(self, example: TrainingExample, iteration: int) -> Dict[str, Any]:
        """
        Train on one example.
        Processing should trigger capability synthesis if needed.
        """
        # Create signal
        signal = Signal(
            type=SignalType.COMPOSITE,
            data={
                'question': example.question,
                'context': example.context,
                'require_response': True,
                'training': True,
                'iteration': iteration
            },
            metadata={
                'training_example': True,
                'category': example.category
            }
        )
        
        # Process
        result = self.cube.process_signal(signal)
        
        # Check for response
        response = self._extract_response(result)
        
        # Log
        return {
            'iteration': iteration,
            'category': example.category,
            'question': example.question,
            'response_generated': response is not None,
            'response': response,
            'pathway': result.get('sequence', 'unknown'),
            'coherence': result.get('coherence', {}),
            'capabilities_after': len(self.cube.capabilities)
        }
    
    def _extract_response(self, result: Dict) -> Any:
        """Extract response from processing result"""
        # Check multiple fields
        for field in ['response', 'responses', 'answer', 'output', 'generated_text']:
            if field in result and result[field]:
                value = result[field]
                if isinstance(value, list) and len(value) > 0:
                    return value[0]
                return value
        return None
    
    def _analyze_training(
        self,
        start_cap: int,
        end_cap: int,
        start_nodes: int,
        end_nodes: int
    ) -> Dict[str, Any]:
        """Analyze training results"""
        console.print(f"\n{'='*80}")
        console.print("[bold cyan]TRAINING ANALYSIS[/bold cyan]")
        console.print(f"{'='*80}\n")
        
        # Calculate metrics
        new_capabilities = end_cap - start_cap
        new_nodes = end_nodes - start_nodes
        responses_generated = sum([1 for log in self.training_log if log['response_generated']])
        total_steps = len(self.training_log)
        response_rate = (responses_generated / total_steps * 100) if total_steps > 0 else 0
        
        # Display metrics
        metrics_table = Table(title="Training Results", border_style="cyan")
        metrics_table.add_column("Metric", style="yellow")
        metrics_table.add_column("Before", style="dim")
        metrics_table.add_column("After", style="green")
        metrics_table.add_column("Change", style="bold green")
        
        metrics_table.add_row(
            "Capabilities",
            str(start_cap),
            str(end_cap),
            f"+{new_capabilities}"
        )
        
        metrics_table.add_row(
            "Secondary Nodes",
            str(start_nodes),
            str(end_nodes),
            f"+{new_nodes}"
        )
        
        metrics_table.add_row(
            "Response Rate",
            "0%",
            f"{response_rate:.1f}%",
            f"+{response_rate:.1f}%"
        )
        
        console.print(metrics_table)
        
        # Show sample responses
        console.print("\n[bold]Sample Responses:[/bold]")
        samples = [log for log in self.training_log if log['response_generated']]
        if samples:
            for i, sample in enumerate(samples[:3], 1):
                console.print(f"\n[cyan]{i}. {sample['question'][:60]}...[/cyan]")
                console.print(f"   Response: {str(sample['response'])[:100]}...")
        else:
            console.print("[red]  No responses generated during training[/red]")
        
        # Verdict
        console.print(f"\n[bold]Training Verdict:[/bold]")
        if new_capabilities > 0:
            console.print(f"[green]✓ {new_capabilities} new capabilities synthesized![/green]")
        else:
            console.print("[yellow]⚠ No new capabilities synthesized[/yellow]")
        
        if new_nodes > 0:
            console.print(f"[green]✓ {new_nodes} new secondary nodes created![/green]")
        else:
            console.print("[yellow]⚠ No new secondary nodes[/yellow]")
        
        if response_rate > 0:
            console.print(f"[green]✓ Response generation: {response_rate:.1f}%[/green]")
        else:
            console.print("[red]✗ No semantic responses generated[/red]")
        
        return {
            'training_steps': total_steps,
            'capabilities_before': start_cap,
            'capabilities_after': end_cap,
            'new_capabilities': new_capabilities,
            'secondary_nodes_before': start_nodes,
            'secondary_nodes_after': end_nodes,
            'new_nodes': new_nodes,
            'responses_generated': responses_generated,
            'response_rate': response_rate,
            'training_log': self.training_log
        }
    
    def save_results(self, summary: Dict[str, Any]):
        """Save training results"""
        output_path = Path("data/semantic_response_training.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        console.print(f"\n[green]Training results saved to {output_path}[/green]")


# =============================================================================
# TRAINING EXAMPLES
# =============================================================================

def create_training_examples() -> List[TrainingExample]:
    """
    Create training examples that require semantic responses.
    These should trigger the AGI engine to synthesize response capabilities.
    """
    return [
        # Pattern recognition
        TrainingExample(
            question="What comes next: 2, 4, 8, 16, 32, ?",
            context={'sequence': [2, 4, 8, 16, 32], 'type': 'pattern'},
            category="pattern_recognition",
            expected_features=['number', 'pattern', 'double']
        ),
        
        TrainingExample(
            question="Complete the pattern: A, B, C, D, E, ?",
            context={'sequence': ['A', 'B', 'C', 'D', 'E'], 'type': 'sequence'},
            category="pattern_recognition",
            expected_features=['letter', 'alphabet', 'next']
        ),
        
        # Concept explanation
        TrainingExample(
            question="What is emergence?",
            context={'concept': 'emergence', 'domain': 'systems_theory'},
            category="concept_explanation",
            expected_features=['property', 'whole', 'parts', 'system']
        ),
        
        TrainingExample(
            question="Explain what a neural network is",
            context={'concept': 'neural_network', 'domain': 'ai'},
            category="concept_explanation",
            expected_features=['network', 'nodes', 'learning', 'connections']
        ),
        
        # Problem solving
        TrainingExample(
            question="If all roses are flowers and all flowers are plants, are roses plants?",
            context={'type': 'logic', 'reasoning': 'transitive'},
            category="problem_solving",
            expected_features=['yes', 'transitive', 'logic']
        ),
        
        TrainingExample(
            question="How many legs do 3 cats have in total?",
            context={'type': 'arithmetic', 'calculation': 'multiplication'},
            category="problem_solving",
            expected_features=['12', 'multiply', 'legs']
        ),
        
        # Creative synthesis
        TrainingExample(
            question="Combine water and memory into a metaphor",
            context={'concepts': ['water', 'memory'], 'task': 'metaphor'},
            category="creative_synthesis",
            expected_features=['water', 'memory', 'metaphor']
        ),
        
        TrainingExample(
            question="Create an analogy between a tree and knowledge",
            context={'concepts': ['tree', 'knowledge'], 'task': 'analogy'},
            category="creative_synthesis",
            expected_features=['tree', 'knowledge', 'growth', 'roots']
        ),
        
        # Self-reflection
        TrainingExample(
            question="How did you process the previous question?",
            context={'type': 'meta', 'reflection': True},
            category="self_reflection",
            expected_features=['process', 'pathway', 'nodes', 'reasoning']
        ),
        
        TrainingExample(
            question="Describe your reasoning for your last answer",
            context={'type': 'meta', 'reflection': True},
            category="self_reflection",
            expected_features=['reasoning', 'because', 'analyzed', 'considered']
        ),
    ]


# =============================================================================
# RUN TRAINING
# =============================================================================

if __name__ == "__main__":
    console.print("[cyan]Loading Spark Cube...[/cyan]")
    
    # Load or create cube
    cube_path = Path("data/spark_cube_state.json")
    if cube_path.exists():
        console.print("[green]Loading existing cube...[/green]")
        with open(cube_path, 'r') as f:
            cube_data = json.load(f)
        console.print(f"[dim]  Capabilities in saved state: {len(cube_data.get('capabilities', []))}[/dim]")
        # Note: MinimalSparkCube doesn't have load_from_file method
        # We'll create fresh and let AGI synthesize
    
    console.print("[yellow]Creating fresh cube with AGI engine...[/yellow]")
    cube = MinimalSparkCube()
    
    # Integrate hierarchical memory
    console.print("[cyan]Integrating hierarchical memory...[/cyan]")
    memory = integrate_hierarchical_memory(cube, "spark_cube/memory/hierarchical_memory.json")
    total_exp = len(memory.experience_index)
    console.print(f"[green]✓ Memory integrated ({total_exp} experiences)[/green]")
    
    # Create trainer
    trainer = SemanticResponseTrainer(cube, memory)
    
    # Create training examples
    examples = create_training_examples()
    console.print(f"[green]✓ {len(examples)} training examples created[/green]\n")
    
    # Train
    summary = trainer.train(examples, iterations=3)
    
    # Save results
    trainer.save_results(summary)
    
    console.print("\n[bold green]Training complete![/bold green]")
    console.print("[dim]Run validate_response_quality.py to test results[/dim]")
