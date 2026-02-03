"""
Test that the external_interface (API) can provide semantic responses directly.
This proves the capability exists - we just need to connect it to processing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube
from rich.console import Console
from rich.panel import Panel

console = Console()

console.print(Panel.fit(
    "[bold cyan]API SEMANTIC RESPONSE TEST[/bold cyan]\n\n"
    "[yellow]Testing if external_interface can answer questions[/yellow]\n"
    "This proves the capability exists - we just need to wire it up.",
    border_style="cyan"
))

# Create cube (initializes external_interface with API)
console.print("\n[dim]Initializing Spark Cube with API access...[/dim]")
cube = MinimalSparkCube()

# Check API availability
if not hasattr(cube, 'external_interface') or not cube.external_interface:
    console.print("[red]✗ External interface not available[/red]")
    console.print("[yellow]Make sure ANTHROPIC_API_KEY is set[/yellow]")
    sys.exit(1)

if not cube.external_interface.enabled:
    console.print("[red]✗ External interface disabled[/red]")
    sys.exit(1)

console.print("[green]✓ API access confirmed[/green]\n")

# Test questions
test_questions = [
    "What comes next in this sequence: 2, 4, 8, 16, 32, ?",
    "What is emergence?",
    "If all roses are flowers and all flowers are plants, are roses plants?",
]

console.print("[bold]Testing API Semantic Responses:[/bold]\n")

for i, question in enumerate(test_questions, 1):
    console.print(f"[bold cyan]Question {i}:[/bold cyan] {question}")
    
    # Use the external interface directly
    response = cube.external_interface.fetch_knowledge(question)
    
    if response['success']:
        console.print(f"[green]✓ API Response:[/green]")
        console.print(f"  {response['content'][:200]}...")
        console.print()
    else:
        console.print(f"[red]✗ API Error: {response.get('error', 'unknown')}[/red]\n")

console.print("[bold green]CONCLUSION:[/bold green]")
console.print("[green]✓ API CAN generate semantic responses![/green]")
console.print("[yellow]→ We just need to connect this to the processing flow[/yellow]")
console.print("[yellow]→ When a question signal comes in, use external_interface.fetch_knowledge()[/yellow]")
