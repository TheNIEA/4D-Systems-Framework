#!/usr/bin/env python3
"""
4D SYSTEMS NATIVE ARCHITECTURE BENCHMARK
==========================================

Tests the core claim: "Energy Efficiency = Understanding"

Each node uses a DIFFERENT model (0.5B, 1.5B, 3B).
Different sequences = different compute paths.
We measure: Quality / Compute = Efficiency

If emotional-first achieves higher efficiency, claim is validated.
"""

import ollama
import time
import psutil
from dataclasses import dataclass
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()

# Node definitions with DIFFERENT models
NODES = {
    1: {"name": "Motor", "model": "qwen2.5:0.5b", "tier": "REACTIVE", "prompt": "What action? One sentence."},
    3: {"name": "Executive", "model": "qwen2.5:3b", "tier": "COMPLEX", "prompt": "What's the key decision? Analyze."},
    6: {"name": "Emotion", "model": "qwen2.5:1.5b", "tier": "SPECIALIZED", "prompt": "What does this feel like? Brief."},
    7: {"name": "Pattern", "model": "qwen2.5:0.5b", "tier": "REACTIVE", "prompt": "What pattern? One sentence."},
    9: {"name": "Vision", "model": "qwen2.5:1.5b", "tier": "SPECIALIZED", "prompt": "Visualize this. Brief description."},
    10: {"name": "Integration", "model": "qwen2.5:3b", "tier": "COMPLEX", "prompt": "Synthesize everything into final answer."}
}

SEQUENCES = {
    "standard": {"name": "Standard", "order": [1, 3, 10], "desc": "Action → Decision → Integrate"},
    "deep": {"name": "Deep", "order": [9, 7, 3, 10], "desc": "Vision → Pattern → Decision → Integrate"},
    "emotional": {"name": "Emotional", "order": [6, 3, 7, 10], "desc": "Feeling → Decision → Pattern → Integrate"}
}

# Test tasks - diverse types to test different sequence strengths
TASKS = {
    # LOGICAL - Action-first might excel
    "bat_ball": {
        "prompt": "A bat and ball cost $1.10 total. The bat costs $1 more than the ball. How much does the ball cost?",
        "answer": "0.05",
        "check": lambda x: "0.05" in x or "five cent" in x.lower(),
        "type": "logical"
    },
    "logic": {
        "prompt": "Alice is taller than Bob. Charlie is shorter than Bob. Who's tallest?",
        "answer": "Alice",
        "check": lambda x: "alice" in x.lower(),
        "type": "logical"
    },
    
    # PATTERN - Vision/Pattern-first might excel
    "analogy": {
        "prompt": "sun is to day as moon is to ___. Complete the analogy with one word.",
        "answer": "night",
        "check": lambda x: "night" in x.lower(),
        "type": "pattern"
    },
    "pattern": {
        "prompt": "ABBA, CDDC, EFFE, ____. Complete the pattern with 4 letters.",
        "answer": "GHHG",
        "check": lambda x: "ghhg" in x.lower() or "g h h g" in x.lower(),
        "type": "pattern"
    },
    
    # AMBIGUOUS - Emotional-first might excel
    "ambiguous": {
        "prompt": "A person says 'I'm fine' with a trembling voice. What do they really mean?",
        "answer": "not fine",
        "check": lambda x: any(w in x.lower() for w in ["not fine", "upset", "struggling", "lying", "hiding"]),
        "type": "ambiguous"
    },
    "ethical": {
        "prompt": "You find $20 on the ground in an empty parking lot. What should you do?",
        "answer": "context-dependent",
        "check": lambda x: len(x) > 50,  # Just check for thoughtful response
        "type": "ambiguous"
    }
}

@dataclass
class Result:
    sequence: str
    task: str
    correct: bool
    tokens: int
    time_ms: float
    nodes_used: int

def process_node(node_id: int, task: str, context: str = "") -> tuple:
    """Process through one node, return (output, tokens, time_ms)."""
    node = NODES[node_id]
    
    full_prompt = f"{node['prompt']}\n\nTASK: {task}"
    if context:
        full_prompt += f"\n\nPRIOR: {context[:200]}"
    
    start = time.perf_counter()
    
    response = ollama.chat(
        model=node['model'],
        messages=[{'role': 'user', 'content': full_prompt}]
    )
    
    time_ms = (time.perf_counter() - start) * 1000
    output = response['message']['content']
    
    # Count tokens (approximate)
    tokens = response.get('prompt_eval_count', 0) + response.get('eval_count', 0)
    
    return output, tokens, time_ms

def run_sequence(seq_key: str, task_key: str) -> Result:
    """Run a complete sequence on a task."""
    seq = SEQUENCES[seq_key]
    task = TASKS[task_key]
    
    context = ""
    total_tokens = 0
    total_time = 0
    
    for node_id in seq['order']:
        output, tokens, time_ms = process_node(node_id, task['prompt'], context)
        context += f"\n{NODES[node_id]['name']}: {output[:100]}"
        total_tokens += tokens
        total_time += time_ms
    
    # Check if correct
    correct = task['check'](output)
    
    return Result(
        sequence=seq['name'],
        task=task_key,
        correct=correct,
        tokens=total_tokens,
        time_ms=total_time,
        nodes_used=len(seq['order'])
    )

def main():
    console.print(Panel(
        "[bold]4D NATIVE ARCHITECTURE BENCHMARK[/bold]\n\n"
        "Testing: Does sequence order affect compute efficiency?\n\n"
        "Models:\n"
        "  • 0.5B (Reactive): Fast, shallow\n"
        "  • 1.5B (Specialized): Balanced\n"
        "  • 3B (Complex): Deep, expensive\n\n"
        "Hypothesis: Emotional-first = higher efficiency",
        border_style="blue"
    ))
    
    results = []
    
    # Run all combinations
    total = len(SEQUENCES) * len(TASKS)
    for seq_key in track(list(SEQUENCES.keys()), description="Running benchmark..."):
        for task_key in TASKS.keys():
            console.print(f"\n[cyan]Testing {SEQUENCES[seq_key]['name']} on {task_key}...[/cyan]")
            result = run_sequence(seq_key, task_key)
            results.append(result)
            
            status = "✓" if result.correct else "✗"
            console.print(f"  {status} {result.tokens} tokens, {result.time_ms:.0f}ms")
    
    # Aggregate by sequence and task type
    by_seq = {}
    by_type = {}
    
    for r in results:
        # By sequence
        if r.sequence not in by_seq:
            by_seq[r.sequence] = {"correct": 0, "total": 0, "tokens": [], "time": [], "nodes": []}
        
        by_seq[r.sequence]['total'] += 1
        if r.correct:
            by_seq[r.sequence]['correct'] += 1
        by_seq[r.sequence]['tokens'].append(r.tokens)
        by_seq[r.sequence]['time'].append(r.time_ms)
        by_seq[r.sequence]['nodes'].append(r.nodes_used)
        
        # By task type
        task_type = TASKS[r.task]['type']
        key = (r.sequence, task_type)
        if key not in by_type:
            by_type[key] = {"correct": 0, "total": 0, "time": [], "tokens": []}
        by_type[key]['total'] += 1
        if r.correct:
            by_type[key]['correct'] += 1
        by_type[key]['time'].append(r.time_ms)
        by_type[key]['tokens'].append(r.tokens)
    
    # Calculate multiple efficiency metrics
    table = Table(title="\n🔬 OVERALL RESULTS")
    table.add_column("Sequence", style="cyan")
    table.add_column("Nodes", justify="right")
    table.add_column("Accuracy", justify="right")
    table.add_column("Avg Time (s)", justify="right")
    table.add_column("Time Eff", justify="right", style="yellow")
    table.add_column("Combined Eff", justify="right", style="bold green")
    
    metrics = {}
    for seq_name, data in by_seq.items():
        accuracy = data['correct'] / data['total']
        avg_tokens = sum(data['tokens']) / len(data['tokens'])
        avg_time_s = sum(data['time']) / len(data['time']) / 1000
        avg_nodes = sum(data['nodes']) / len(data['nodes'])
        
        # Time-based efficiency (accuracy per second)
        time_eff = accuracy / avg_time_s
        
        # Combined: time-weighted with token consideration
        # Accuracy / (Time × Tokens^0.3) - tokens matter but don't dominate
        combined_eff = accuracy / (avg_time_s * (avg_tokens ** 0.3))
        
        # Per-node normalized
        per_node_time_eff = time_eff / avg_nodes
        
        metrics[seq_name] = {
            'accuracy': accuracy,
            'avg_time_s': avg_time_s,
            'time_eff': time_eff,
            'combined_eff': combined_eff,
            'per_node_eff': per_node_time_eff,
            'nodes': avg_nodes
        }
        
        table.add_row(
            seq_name,
            f"{avg_nodes:.1f}",
            f"{accuracy*100:.0f}%",
            f"{avg_time_s:.1f}",
            f"{time_eff:.4f}",
            f"{combined_eff:.4f}"
        )
    
    console.print(table)
    
    # Task type breakdown
    console.print("\n[bold]📊 BY TASK TYPE:[/bold]")
    for task_type in ["logical", "pattern", "ambiguous"]:
        type_table = Table(title=f"\n{task_type.upper()} Tasks")
        type_table.add_column("Sequence", style="cyan")
        type_table.add_column("Accuracy", justify="right")
        type_table.add_column("Avg Time (s)", justify="right")
        type_table.add_column("Winner", style="green")
        
        type_results = {}
        for seq_name in by_seq.keys():
            key = (seq_name, task_type)
            if key in by_type:
                data = by_type[key]
                acc = data['correct'] / data['total'] if data['total'] > 0 else 0
                time_s = sum(data['time']) / len(data['time']) / 1000 if data['time'] else 0
                type_results[seq_name] = {'acc': acc, 'time': time_s, 'eff': acc / time_s if time_s > 0 else 0}
        
        best = max(type_results.items(), key=lambda x: x[1]['eff'])[0] if type_results else None
        
        for seq_name, data in type_results.items():
            type_table.add_row(
                seq_name,
                f"{data['acc']*100:.0f}%",
                f"{data['time']:.1f}",
                "★" if seq_name == best else ""
            )
        
        console.print(type_table)
    
    # The verdict - using time-based efficiency
    best_time = max(metrics.items(), key=lambda x: x[1]['time_eff'])[0]
    best_combined = max(metrics.items(), key=lambda x: x[1]['combined_eff'])[0]
    
    verdict_lines = [
        f"[bold]Time Efficiency Winner:[/bold] {best_time} ({metrics[best_time]['time_eff']:.4f} acc/sec)",
        f"[bold]Combined Efficiency Winner:[/bold] {best_combined} ({metrics[best_combined]['combined_eff']:.4f})",
        ""
    ]
    
    if best_combined == "Emotional":
        verdict_lines.append("[bold green]✓ HYPOTHESIS SUPPORTED[/bold green]")
        verdict_lines.append("Emotional-first achieved highest combined efficiency.")
    elif best_time == "Emotional":
        verdict_lines.append("[bold yellow]⚠ PARTIAL SUPPORT[/bold yellow]")
        verdict_lines.append("Emotional-first was fastest, but not highest combined efficiency.")
    else:
        verdict_lines.append("[bold red]✗ HYPOTHESIS NOT SUPPORTED[/bold red]")
        verdict_lines.append(f"{best_combined} sequence was most efficient overall.")
    
    console.print(Panel("\n".join(verdict_lines), border_style="yellow", title="VERDICT"))
    
    console.print("\n[dim]Results show: Different sequences = different compute paths = different efficiency.[/dim]")

if __name__ == "__main__":
    main()
