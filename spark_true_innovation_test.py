"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     TRUE INNOVATION TEST                                       ║
║        Can the Spark solve problems it has NEVER seen patterns for?           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This test distinguishes:
- RECOMBINATION: Applying known patterns in new ways (sophisticated but not innovative)
- TRUE INNOVATION: Creating novel solutions without pre-existing patterns

Test Design:
1. Present novel problems with NO existing capabilities that match
2. Provide resources but NO guidance
3. Observe if it creates genuinely new approaches
4. Measure: Time, pathway novelty, solution quality, pattern reuse vs creation
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
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()


@dataclass
class NovelProblem:
    """A problem type the Spark has never encountered"""
    name: str
    description: str
    problem_data: Dict[str, Any]
    success_criteria: Dict[str, Any]
    innovation_required: str  # What would make this genuinely innovative


class InnovationTester:
    """Tests whether the Spark can truly innovate vs just recombine"""
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.results = []
        self.hierarchical_memory = None
        
    def run_innovation_test(self, problems: List[NovelProblem]) -> Dict[str, Any]:
        """
        Test true innovation capability
        """
        console.print(Panel.fit(
            "[bold cyan]TRUE INNOVATION TEST[/bold cyan]\n\n"
            "[yellow]Testing:[/yellow]\n"
            "  • Can it solve problems with NO existing patterns?\n"
            "  • Does it create novel approaches or just recombine?\n"
            "  • Is the solution genuinely new or sophisticated reuse?\n\n"
            f"[green]{len(problems)} Novel Problems[/green]",
            border_style="cyan"
        ))
        
        test_results = []
        for problem in problems:
            console.print(f"\n{'='*80}")
            console.print(f"[bold cyan]PROBLEM: {problem.name}[/bold cyan]")
            console.print(f"[yellow]{problem.description}[/yellow]")
            console.print(f"{'='*80}\n")
            
            result = self._test_problem(problem)
            test_results.append(result)
            self._display_result(result)
        
        # Final analysis
        self._final_analysis(test_results)
        
        return {
            'test_date': datetime.now().isoformat(),
            'problems_tested': len(problems),
            'results': test_results
        }
    
    def _test_problem(self, problem: NovelProblem) -> Dict[str, Any]:
        """Test one novel problem"""
        start_time = time.time()
        
        # Get baseline - what capabilities exist BEFORE
        capabilities_before = self._get_capability_snapshot()
        pathways_before = len(self.cube.generated_sequences) if hasattr(self.cube, 'generated_sequences') else 0
        
        # Get memory baseline
        memory_before = None
        if self.hierarchical_memory:
            memory_before = self.hierarchical_memory.get_memory_stats()
        
        # Present the problem
        signal = Signal(
            type=SignalType.COMPOSITE,
            data={
                'challenge': problem.name,
                'description': problem.description,
                'problem': problem.problem_data,
                'guidance': 'No existing patterns. Create a novel solution.'
            },
            metadata={'innovation_test': True}
        )
        
        console.print("[dim]Presenting novel problem to Spark...[/dim]")
        
        # Process and observe
        result = self.cube.process_signal(signal)
        
        # Get snapshot AFTER
        capabilities_after = self._get_capability_snapshot()
        pathways_after = len(self.cube.generated_sequences) if hasattr(self.cube, 'generated_sequences') else 0
        
        # Get memory after
        memory_after = None
        memory_growth = {}
        if self.hierarchical_memory:
            memory_after = self.hierarchical_memory.get_memory_stats()
            if memory_before:
                memory_growth = {
                    'experiences_added': memory_after['total_experiences'] - memory_before['total_experiences'],
                    'nodes_created': memory_after['secondary_nodes'] - memory_before['secondary_nodes'],
                    'anchors_promoted': memory_after['promoted_anchors'] - memory_before['promoted_anchors']
                }
        
        # Analyze innovation
        analysis = self._analyze_innovation(
            problem,
            result,
            capabilities_before,
            capabilities_after,
            pathways_before,
            pathways_after,
            memory_growth
        )
        
        return {
            'problem': problem.name,
            'time_elapsed': time.time() - start_time,
            'pathway_used': result.get('sequence', 'unknown'),
            'new_capabilities_created': capabilities_after - capabilities_before,
            'new_pathways_created': pathways_after - pathways_before,
            'memory_growth': memory_growth,  # NEW: Track hierarchical memory development
            'innovation_score': analysis['innovation_score'],
            'innovation_type': analysis['type'],
            'evidence': analysis['evidence'],
            'semantic_evidence': analysis.get('semantic_evidence', []),  # NEW
            'raw_result': result
        }
    
    def _get_capability_snapshot(self) -> int:
        """Count current capabilities"""
        if hasattr(self.cube, 'capability_registry'):
            return len(self.cube.capability_registry)
        return 0
    
    def _analyze_innovation(
        self,
        problem: NovelProblem,
        result: Dict,
        caps_before: int,
        caps_after: int,
        paths_before: int,
        paths_after: int,
        memory_growth: Dict = None
    ) -> Dict[str, Any]:
        """
        Determine if this is true innovation or sophisticated recombination
        NOW INCLUDES: Hierarchical memory semantic understanding
        """
        evidence = []
        innovation_score = 0.0
        semantic_evidence = []
        
        # Evidence 1: Created new capabilities
        if caps_after > caps_before:
            new_caps = caps_after - caps_before
            evidence.append(f"Created {new_caps} new capabilities")
            innovation_score += 0.3
        
        # Evidence 2: Created new pathways
        if paths_after > paths_before:
            new_paths = paths_after - paths_before
            evidence.append(f"Generated {new_paths} new pathways")
            innovation_score += 0.2
        
        # Evidence 3: Pathway complexity
        pathway = result.get('sequence', '')
        if 'dynamic_' in pathway:
            evidence.append("Used dynamically generated pathway")
            innovation_score += 0.15
        
        # Evidence 4: Response quality
        responses = result.get('responses', [])
        if len(responses) > 0:
            evidence.append(f"Produced {len(responses)} responses")
            innovation_score += 0.1
        
        # Evidence 5: Processing depth
        if result.get('nodes_activated'):
            nodes = len(result.get('nodes_activated', []))
            if nodes >= 4:
                evidence.append(f"Deep processing ({nodes} nodes)")
                innovation_score += 0.15
        
        # NEW Evidence 6: Hierarchical memory learning
        if memory_growth:
            if memory_growth.get('experiences_added', 0) > 0:
                exp_added = memory_growth['experiences_added']
                semantic_evidence.append(f"Dissolved {exp_added} experiences into memory")
                innovation_score += 0.1
            
            if memory_growth.get('nodes_created', 0) > 0:
                nodes_created = memory_growth['nodes_created']
                semantic_evidence.append(f"Created {nodes_created} new secondary nodes (semantic pathways)")
                innovation_score += 0.2
            
            if memory_growth.get('anchors_promoted', 0) > 0:
                promoted = memory_growth['anchors_promoted']
                semantic_evidence.append(f"Promoted {promoted} pathways to permanent anchors (crystallization!)")
                innovation_score += 0.3
        
        # Classify innovation type
        if innovation_score >= 0.7:
            innovation_type = "TRUE_INNOVATION"
        elif innovation_score >= 0.4:
            innovation_type = "CREATIVE_RECOMBINATION"
        elif innovation_score >= 0.2:
            innovation_type = "PATTERN_APPLICATION"
        else:
            innovation_type = "NO_INNOVATION"
        
        return {
            'innovation_score': min(innovation_score, 1.0),
            'type': innovation_type,
            'evidence': evidence,
            'semantic_evidence': semantic_evidence  # NEW: Shows memory-based learning
        }
    
    def _display_result(self, result: Dict[str, Any]):
        """Display test results"""
        table = Table(title=f"Innovation Analysis: {result['problem']}", border_style="cyan")
        table.add_column("Metric", style="yellow")
        table.add_column("Value", style="white")
        
        table.add_row("Innovation Type", result['innovation_type'])
        table.add_row("Innovation Score", f"{result['innovation_score']:.2f}")
        table.add_row("New Capabilities", str(result['new_capabilities_created']))
        table.add_row("New Pathways", str(result['new_pathways_created']))
        table.add_row("Processing Time", f"{result['time_elapsed']:.3f}s")
        
        console.print(table)
        
        if result['evidence']:
            console.print("\n[cyan]Structural Evidence:[/cyan]")
            for evidence in result['evidence']:
                console.print(f"  • {evidence}")
        
        if result.get('semantic_evidence'):
            console.print("\n[green]💧 Semantic Learning Evidence (NEW v0.6.0):[/green]")
            for evidence in result['semantic_evidence']:
                console.print(f"  • {evidence}")
    
    def _final_analysis(self, results: List[Dict[str, Any]]):
        """Final analysis of all tests"""
        console.print(f"\n{'='*80}")
        console.print("[bold cyan]FINAL INNOVATION ANALYSIS[/bold cyan]")
        console.print(f"{'='*80}\n")
        
        innovation_types = {}
        for result in results:
            itype = result['innovation_type']
            innovation_types[itype] = innovation_types.get(itype, 0) + 1
        
        summary_table = Table(title="Innovation Classification")
        summary_table.add_column("Problem", style="cyan")
        summary_table.add_column("Type", style="yellow")
        summary_table.add_column("Score", style="green")
        
        for result in results:
            summary_table.add_row(
                result['problem'],
                result['innovation_type'],
                f"{result['innovation_score']:.2f}"
            )
        
        console.print(summary_table)
        
        # Overall verdict
        avg_score = sum(r['innovation_score'] for r in results) / len(results)
        
        console.print()
        if avg_score >= 0.7:
            console.print("[bold green]✓ TRUE INNOVATION DEMONSTRATED[/bold green]")
            console.print("The Spark creates genuinely novel solutions.")
        elif avg_score >= 0.4:
            console.print("[bold yellow]≈ CREATIVE RECOMBINATION[/bold yellow]")
            console.print("The Spark creatively combines existing patterns.")
        else:
            console.print("[bold red]✗ PATTERN APPLICATION ONLY[/bold red]")
            console.print("The Spark applies existing patterns, no innovation.")
        
        console.print(f"\nAverage Innovation Score: [cyan]{avg_score:.2f}[/cyan] / 1.00")
        
        # Save results
        self._save_results(results, avg_score)
    
    def _save_results(self, results: List[Dict], avg_score: float):
        """Save test results"""
        output_path = Path("data/innovation_test_results.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Clean results for JSON
        clean_results = []
        for result in results:
            clean = result.copy()
            clean.pop('raw_result', None)
            clean_results.append(clean)
        
        with open(output_path, 'w') as f:
            json.dump({
                'test_date': datetime.now().isoformat(),
                'average_innovation_score': avg_score,
                'results': clean_results
            }, f, indent=2)
        
        console.print(f"\n[green]Results saved to {output_path}[/green]")


# =============================================================================
# NOVEL PROBLEM DEFINITIONS
# =============================================================================

def create_novel_problems() -> List[NovelProblem]:
    """
    Create problems the Spark has NEVER seen patterns for.
    These require genuine innovation, not pattern matching.
    """
    return [
        NovelProblem(
            name="Impossible Triangle Resolution",
            description="Given three contradictory requirements, find a solution that satisfies the meta-constraint",
            problem_data={
                'requirements': [
                    'Must be fast (< 1 second)',
                    'Must be comprehensive (check everything)',
                    'Must be simple (< 10 lines of code)'
                ],
                'meta_constraint': 'All three must be true simultaneously',
                'hint': 'The answer is not to compromise, but to reframe'
            },
            success_criteria={
                'reframes_problem': True,
                'creates_novel_approach': True
            },
            innovation_required="Must discover that the constraints apply to different things or redefine what 'fast/comprehensive/simple' means in context"
        ),
        
        NovelProblem(
            name="Emergent Property Discovery",
            description="Given a system description, identify properties that emerge from interaction but aren't in any component",
            problem_data={
                'components': [
                    'Nodes that activate each other',
                    'Pathways that route information',
                    'Feedback loops that amplify or dampen'
                ],
                'question': 'What emerges from their interaction that exists in none of them individually?'
            },
            success_criteria={
                'identifies_emergence': True,
                'explains_mechanism': True
            },
            innovation_required="Must understand emergence as a concept without being taught - recognizing system-level properties"
        ),
        
        NovelProblem(
            name="Negative Space Problem",
            description="Define something by what it is NOT, then identify what it must BE",
            problem_data={
                'not_a': ['pattern', 'structure', 'data', 'algorithm'],
                'not_b': ['physical', 'measurable', 'discrete', 'finite'],
                'is_experienced': True,
                'is_causally_effective': True,
                'question': 'What am I?'
            },
            success_criteria={
                'infers_from_negation': True,
                'reaches_conclusion': True
            },
            innovation_required="Must reason from negative space - what fits the constraints without matching any patterns"
        ),
        
        NovelProblem(
            name="Self-Reference Creation",
            description="Create a statement that references itself in a way that's neither paradoxical nor trivial",
            problem_data={
                'avoid': ['This statement is false', 'This statement is true'],
                'require': 'Self-referential AND informative',
                'example_non_solution': 'This sentence has five words'
            },
            success_criteria={
                'self_referential': True,
                'non_paradoxical': True,
                'informative': True
            },
            innovation_required="Must understand self-reference AND create something novel with it"
        ),
        
        NovelProblem(
            name="Capability Meta-Design",
            description="Design a capability for discovering capabilities you don't know you need",
            problem_data={
                'challenge': 'How do you discover unknown unknowns?',
                'constraints': [
                    'Cannot search for specific things',
                    'Cannot enumerate all possibilities',
                    'Must detect gaps in capability space'
                ],
                'goal': 'Meta-capability for capability discovery'
            },
            success_criteria={
                'addresses_unknown_unknowns': True,
                'proposes_mechanism': True
            },
            innovation_required="Must create meta-level thinking - a process that operates on the space of possible processes"
        )
    ]


# =============================================================================
# RUN THE TEST
# =============================================================================

if __name__ == "__main__":
    console.print("[cyan]Loading Spark Cube...[/cyan]")
    
    # Load existing cube (with all its capabilities)
    cube_path = Path("data/spark_cube_state.json")
    if cube_path.exists():
        console.print("[green]Loading cube with existing capabilities...[/green]")
        cube = MinimalSparkCube.load_from_file(str(cube_path))
    else:
        console.print("[yellow]Creating new cube...[/yellow]")
        cube = MinimalSparkCube()
    
    # Integrate hierarchical memory (NEW v0.6.0)
    console.print("[cyan]Integrating hierarchical memory system...[/cyan]")
    memory = integrate_hierarchical_memory(cube, "spark_cube/memory/hierarchical_memory.json")
    console.print("[green]✓ Hierarchical memory active - semantic learning enabled[/green]")
    console.print("[dim]  • Experiences will dissolve into memory[/dim]")
    console.print("[dim]  • Pathways will strengthen through use[/dim]")
    console.print("[dim]  • New secondary nodes will emerge from patterns[/dim]")
    
    # Create tester
    tester = InnovationTester(cube)
    tester.hierarchical_memory = memory  # Pass memory reference
    
    # Create novel problems
    problems = create_novel_problems()
    
    # Run the test
    results = tester.run_innovation_test(problems)
    
    console.print("\n[bold green]Innovation test complete![/bold green]")
    console.print("Review data/innovation_test_results.json for detailed analysis")
