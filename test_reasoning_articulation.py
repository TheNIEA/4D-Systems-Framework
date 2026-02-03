#!/usr/bin/env python3
"""
Focused test: Does the semantic response capability enable reasoning articulation?

Tests the specific capabilities that were missing:
- Reasoning articulation (can it explain WHY in language?)
- Semantic innovation for language-based outputs
"""
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_reasoning_articulation():
    """Can the system articulate its reasoning in language?"""
    console.print(Panel.fit(
        "[bold cyan]REASONING ARTICULATION TEST[/bold cyan]\n"
        "Testing if semantic capability enables language-based reasoning",
        border_style="cyan"
    ))
    
    cube = MinimalSparkCube()
    
    # Test cases that require reasoning explanation
    test_cases = [
        {
            'question': 'What comes next: 2, 4, 8, 16? Explain your reasoning.',
            'should_contain': ['pattern', 'double', 'multiply', 'reasoning', 'because']
        },
        {
            'question': 'Why is pattern recognition important?',
            'should_contain': ['pattern', 'recognize', 'important', 'because', 'help']
        },
        {
            'question': 'How would you solve: if A=1, B=2, then what is C?',
            'should_contain': ['sequence', 'pattern', 'follow', 'next', '3']
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        console.print(f"\n[yellow]Test {i}:[/yellow] {test['question']}")
        
        signal = Signal(type=SignalType.TEXT, data={'question': test['question']})
        result = cube.process_with_synthesis(signal)
        
        response = result.get('semantic_response', '')
        
        if response:
            console.print(f"[green]✓ Response:[/green] {response}")
            
            # Check if response shows reasoning
            response_lower = response.lower()
            keywords_found = [kw for kw in test['should_contain'] if kw in response_lower]
            
            has_reasoning = len(keywords_found) >= 2  # At least 2 reasoning keywords
            
            results.append({
                'test': i,
                'has_response': True,
                'has_reasoning': has_reasoning,
                'keywords_found': keywords_found,
                'response_length': len(response)
            })
            
            if has_reasoning:
                console.print(f"[green]  ✓ Shows reasoning (keywords: {', '.join(keywords_found)})[/green]")
            else:
                console.print(f"[yellow]  ⚠ Response exists but lacks reasoning articulation[/yellow]")
        else:
            console.print(f"[red]✗ No response generated[/red]")
            results.append({
                'test': i,
                'has_response': False,
                'has_reasoning': False
            })
    
    # Summary
    console.print("\n" + "="*70)
    console.print("[bold]RESULTS SUMMARY[/bold]")
    console.print("="*70)
    
    responses_generated = sum(1 for r in results if r['has_response'])
    reasoning_articulated = sum(1 for r in results if r.get('has_reasoning', False))
    
    console.print(f"Responses generated: {responses_generated}/{len(test_cases)}")
    console.print(f"Reasoning articulated: {reasoning_articulated}/{len(test_cases)}")
    
    if reasoning_articulated > 0:
        console.print("\n[bold green]✓ SEMANTIC CAPABILITY ENABLED REASONING ARTICULATION[/bold green]")
        console.print("The system can now explain its reasoning in natural language!")
    elif responses_generated > 0:
        console.print("\n[yellow]⚠ Responses generated but reasoning needs improvement[/yellow]")
        console.print("The capability exists but may need refinement.")
    else:
        console.print("\n[red]✗ No semantic responses generated[/red]")
    
    # Check capability status
    console.print(f"\n[dim]Capability status:[/dim]")
    console.print(f"[dim]  - Semantic response: {hasattr(cube.nodes[10], 'semantic_response')}[/dim]")
    console.print(f"[dim]  - Total capabilities: {len(cube.nodes[12].capability_registry)}[/dim]")
    
    return results

if __name__ == '__main__':
    test_reasoning_articulation()
