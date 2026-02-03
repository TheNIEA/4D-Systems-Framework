"""
SIMPLE SEMANTIC RESPONSE TEST
Just run the validation to see current state
"""

import sys
from pathlib import Path

# Add paths for imports
spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, integrate_hierarchical_memory
from rich.console import Console

console = Console()

console.print("[cyan]Loading Spark Cube...[/cyan]")
cube = MinimalSparkCube()

console.print("[cyan]Integrating hierarchical memory...[/cyan]")
memory = integrate_hierarchical_memory(cube, "spark_cube/memory/hierarchical_memory.json")

console.print("[green]✓ Setup complete[/green]\n")

# Test one question
test_question = "What comes next in this sequence: 2, 4, 8, 16, 32, ?"
console.print(f"[bold yellow]Test Question:[/bold yellow] {test_question}\n")

signal = Signal(
    type=SignalType.COMPOSITE,
    data={
        'question': test_question,
        'context': {'sequence': [2, 4, 8, 16, 32]},
        'require_response': True
    },
    metadata={'test': True}
)

console.print("[dim]Processing with synthesis enabled...[/dim]")
result = cube.process_with_synthesis(signal)

console.print("\n[bold cyan]Result:[/bold cyan]")
console.print(f"  Pathway: {result.get('sequence', 'none')}")
console.print(f"  Coherence: {result.get('coherence', {}).get('base_coherence', 0):.2f}")
console.print(f"  Responses: {result.get('responses', [])}")
console.print(f"  Synthesis: {result.get('synthesis', {})}")

# Check for semantic response
if 'semantic_response' in result:
    console.print(f"\n[green]✓ Semantic Response:[/green]")
    console.print(f"  {result['semantic_response']}")

# Check for actual response
response_found = False
for field in ['response', 'responses', 'answer', 'output', 'semantic_response']:
    if field in result and result[field]:
        if field == 'responses' and isinstance(result[field], list) and len(result[field]) > 0:
            console.print(f"\n[green]✓ Found responses:[/green]")
            for i, resp in enumerate(result[field]):
                console.print(f"  {i+1}. {resp}")
            response_found = True
            break
        elif field != 'responses':
            console.print(f"\n[green]✓ Found {field}:[/green]")
            console.print(f"  {result[field]}")
            response_found = True
            break

if not response_found:
    console.print("\n[red]✗ No semantic response generated[/red]")
    console.print("\n[yellow]This confirms the system needs semantic response capabilities[/yellow]")
