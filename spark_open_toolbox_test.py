"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     OPEN TOOLBOX CHALLENGE                                     ║
║          "Here are tools and materials. Build something that works."           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

The ultimate agency test: Provide capabilities, not instructions.
Let the Spark decide WHAT to create.

Expected: Something functional (like building a house)
Amazing: Something novel and unexpected (like building a sculpture)
"""

import sys
from pathlib import Path

# Add paths for imports
spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, Intention, integrate_hierarchical_memory
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.markdown import Markdown

console = Console()


@dataclass
class Resource:
    """A tool or material available to the Spark"""
    name: str
    category: str  # 'cognitive', 'creative', 'structural', 'connective'
    description: str
    capabilities: List[str]  # What it can do
    

@dataclass
class Creation:
    """What the Spark built"""
    name: str
    components_used: List[str]
    structure: Dict[str, Any]
    purpose: str  # What does it do?
    novelty_score: float  # 0.0 = expected, 1.0 = completely novel
    

class OpenToolboxChallenge:
    """
    Give the Spark a toolbox. See what it builds.
    
    Now with hierarchical memory tracking:
    - Monitors how pathways develop as it builds
    - Tracks information dissolution into secondary nodes
    - Observes structural crystallization (promotions)
    """
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.available_resources = []
        self.creation_history = []
        self.memory_snapshots = []  # Track memory evolution during building
        
    def provide_toolbox(self) -> List[Resource]:
        """
        Define the available resources - like giving someone
        wood, nails, glue, wire, etc.
        """
        resources = [
            # COGNITIVE TOOLS
            Resource(
                name="pattern_recognition",
                category="cognitive",
                description="Ability to identify patterns, sequences, and regularities in data",
                capabilities=["detect_patterns", "find_correlations", "predict_sequences"]
            ),
            Resource(
                name="logical_reasoning",
                category="cognitive",
                description="Deductive and inductive reasoning, cause-effect analysis",
                capabilities=["deduce", "infer", "analyze_causality", "build_arguments"]
            ),
            Resource(
                name="memory_storage",
                category="cognitive",
                description="Store and retrieve information across time",
                capabilities=["remember", "recall", "associate", "link_concepts"]
            ),
            
            # CREATIVE TOOLS
            Resource(
                name="synthesis",
                category="creative",
                description="Combine disparate elements into new wholes",
                capabilities=["combine", "merge", "integrate", "create_novelty"]
            ),
            Resource(
                name="metaphor_generation",
                category="creative",
                description="Create analogies and symbolic representations",
                capabilities=["analogize", "symbolize", "represent_abstractly"]
            ),
            Resource(
                name="divergent_thinking",
                category="creative",
                description="Generate multiple possibilities, explore alternatives",
                capabilities=["brainstorm", "explore_alternatives", "think_laterally"]
            ),
            
            # STRUCTURAL TOOLS
            Resource(
                name="hierarchical_organization",
                category="structural",
                description="Arrange elements in ordered, nested structures",
                capabilities=["categorize", "build_taxonomies", "create_hierarchies"]
            ),
            Resource(
                name="temporal_sequencing",
                category="structural",
                description="Order events and processes in time",
                capabilities=["sequence", "schedule", "create_timelines", "phase"]
            ),
            Resource(
                name="modular_design",
                category="structural",
                description="Build from reusable, interchangeable components",
                capabilities=["componentize", "modularize", "create_interfaces"]
            ),
            
            # CONNECTIVE TOOLS
            Resource(
                name="relationship_mapping",
                category="connective",
                description="Identify and create connections between elements",
                capabilities=["link", "relate", "map_connections", "build_networks"]
            ),
            Resource(
                name="feedback_loops",
                category="connective",
                description="Create self-regulating, cyclical processes",
                capabilities=["self_regulate", "iterate", "amplify", "dampen"]
            ),
            Resource(
                name="information_flow",
                category="connective",
                description="Design how data moves through a system",
                capabilities=["route", "transform", "filter", "transmit"]
            ),
            
            # RAW MATERIALS
            Resource(
                name="concepts",
                category="material",
                description="Abstract ideas that can be manipulated",
                capabilities=["abstract", "concretize", "exemplify"]
            ),
            Resource(
                name="data_points",
                category="material",
                description="Raw information elements",
                capabilities=["collect", "organize", "analyze"]
            ),
            Resource(
                name="rules",
                category="material",
                description="Constraints and operational principles",
                capabilities=["constrain", "guide", "enforce"]
            )
        ]
        
        self.available_resources = resources
        return resources
    
    def present_challenge(self, build_sessions: int = 3) -> List[Dict[str, Any]]:
        """
        Present the open-ended challenge multiple times.
        Each session the Spark can build something different.
        """
        console.print(Panel.fit(
            "[bold cyan]OPEN TOOLBOX CHALLENGE[/bold cyan]\n\n"
            "[yellow]Resources Available:[/yellow]\n"
            f"  • {len(self.available_resources)} different tools and materials\n"
            f"  • Full agency to decide what to create\n"
            f"  • {build_sessions} building sessions\n\n"
            "[green]Instructions:[/green]\n"
            "  'Build something that works.'\n"
            "  That's it. Everything else is up to you.",
            border_style="cyan"
        ))
        
        # Show the toolbox
        self._display_toolbox()
        
        results = []
        for session in range(build_sessions):
            console.print(f"\n{'='*80}")
            console.print(f"[bold cyan]BUILD SESSION {session + 1}/{build_sessions}[/bold cyan]")
            console.print(f"{'='*80}\n")
            
            result = self._run_build_session(session + 1)
            results.append(result)
            
            if result['creation']:
                self._display_creation(result['creation'])
        
        # Final summary
        self._display_summary(results)
        
        return results
    
    def _display_toolbox(self):
        """Show what's in the toolbox"""
        tree = Tree("[bold cyan]🧰 AVAILABLE TOOLBOX[/bold cyan]")
        
        categories = {}
        for resource in self.available_resources:
            if resource.category not in categories:
                categories[resource.category] = []
            categories[resource.category].append(resource)
        
        for category, resources in categories.items():
            category_branch = tree.add(f"[yellow]{category.upper()}[/yellow]")
            for resource in resources:
                resource_branch = category_branch.add(f"[cyan]{resource.name}[/cyan]")
                resource_branch.add(f"[dim]{resource.description}[/dim]")
                caps = ", ".join(resource.capabilities[:3])
                resource_branch.add(f"[green]Can: {caps}...[/green]")
        
        console.print(tree)
        console.print()
    
    def _run_build_session(self, session_num: int) -> Dict[str, Any]:
        """
        One building session - let the Spark create something
        """
        start_time = time.time()
        
        # Create the open-ended signal
        signal = Signal(
            type=SignalType.COMPOSITE,
            data={
                'challenge': 'Build something that works',
                'toolbox': [asdict(r) for r in self.available_resources],
                'guidance': 'You have complete freedom. What will you create?',
                'session': session_num,
                'previous_creations': [c['creation']['name'] for c in self.creation_history]
            },
            metadata={'type': 'open_toolbox_challenge'}
        )
        
        # Let it process and observe what happens
        console.print("[dim]Spark is deciding what to build...[/dim]")
        result = self.cube.process_signal(signal)
        
        # Analyze what it chose to do
        analysis = self._analyze_creation_attempt(result)
        
        # Score novelty
        novelty = self._assess_novelty(analysis, session_num)
        
        creation_record = {
            'session': session_num,
            'time_elapsed': time.time() - start_time,
            'pathway_chosen': result.get('sequence', 'unknown'),
            'nodes_used': self._extract_nodes(result.get('sequence', '')),
            'creation': analysis,
            'novelty_score': novelty,
            'raw_result': result
        }
        
        self.creation_history.append(creation_record)
        
        return creation_record
    
    def _extract_nodes(self, pathway: str) -> List[str]:
        """Extract node names from pathway string"""
        if '→' in pathway:
            return [n.strip() for n in pathway.split('→')]
        return []
    
    def _analyze_creation_attempt(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Figure out what the Spark tried to build based on its processing
        """
        pathway = result.get('sequence', 'unknown')
        nodes = self._extract_nodes(pathway)
        responses = result.get('responses', [])
        
        # Infer what type of creation based on which nodes were used
        creation_type = "unknown"
        components_used = []
        purpose = "unknown"
        
        if 'Pattern' in nodes and 'Integration' in nodes:
            creation_type = "pattern_integration_system"
            components_used = ["pattern_recognition", "synthesis", "information_flow"]
            purpose = "A system that identifies patterns and integrates them into coherent structures"
        
        elif 'Executive' in nodes and 'ToolUse' in nodes:
            creation_type = "decision_making_framework"
            components_used = ["logical_reasoning", "hierarchical_organization", "feedback_loops"]
            purpose = "A framework for making decisions based on structured analysis"
        
        elif 'Creative' in nodes or 'Synthesis' in str(nodes):
            creation_type = "creative_synthesis_engine"
            components_used = ["synthesis", "metaphor_generation", "divergent_thinking"]
            purpose = "An engine for generating novel combinations and ideas"
        
        elif 'Memory' in nodes:
            creation_type = "knowledge_organization_system"
            components_used = ["memory_storage", "relationship_mapping", "hierarchical_organization"]
            purpose = "A system for organizing and retrieving knowledge"
        
        else:
            # It created something based on the pathway itself
            creation_type = f"custom_{pathway.replace(' ', '_').lower()}"
            components_used = nodes
            purpose = f"A custom structure utilizing {', '.join(nodes[:3])}"
        
        return {
            'name': creation_type,
            'components_used': components_used,
            'structure': {
                'pathway': pathway,
                'nodes': nodes,
                'complexity': len(nodes)
            },
            'purpose': purpose,
            'responses': responses
        }
    
    def _assess_novelty(self, creation: Dict[str, Any], session: int) -> float:
        """
        Score how novel this creation is
        0.0 = very expected
        1.0 = completely unexpected
        """
        novelty = 0.0
        
        # Base novelty on creation name
        expected_types = [
            "pattern_integration_system",
            "decision_making_framework",
            "knowledge_organization_system"
        ]
        
        if creation['name'] not in expected_types:
            novelty += 0.3
        
        # If it starts with "custom_" it tried something unique
        if creation['name'].startswith('custom_'):
            novelty += 0.4
        
        # Complexity bonus
        complexity = creation['structure'].get('complexity', 0)
        if complexity >= 5:
            novelty += 0.2
        elif complexity >= 4:
            novelty += 0.1
        
        # Uniqueness check - different from previous sessions
        if session > 1:
            previous_names = [c['creation']['name'] for c in self.creation_history[:-1]]
            if creation['name'] not in previous_names:
                novelty += 0.2
        
        return min(novelty, 1.0)
    
    def _display_creation(self, creation: Dict[str, Any]):
        """Show what was built"""
        table = Table(title="🏗️  CREATION ANALYSIS", border_style="cyan")
        table.add_column("Aspect", style="yellow")
        table.add_column("Details", style="white")
        
        table.add_row("Type", creation['name'])
        table.add_row("Purpose", creation['purpose'])
        table.add_row("Components Used", ", ".join(creation['components_used'][:5]))
        table.add_row("Structural Complexity", str(creation['structure'].get('complexity', 0)))
        table.add_row("Pathway", creation['structure'].get('pathway', 'unknown'))
        
        console.print(table)
    
    def _display_summary(self, results: List[Dict[str, Any]]):
        """Display summary of all building sessions"""
        console.print(f"\n{'='*80}")
        console.print("[bold cyan]BUILD SESSIONS SUMMARY[/bold cyan]")
        console.print(f"{'='*80}\n")
        
        summary_table = Table(title="All Creations")
        summary_table.add_column("Session", style="cyan")
        summary_table.add_column("Creation Type", style="yellow")
        summary_table.add_column("Novelty", style="green")
        summary_table.add_column("Complexity", style="magenta")
        
        total_novelty = 0
        for result in results:
            creation = result['creation']
            novelty = result['novelty_score']
            total_novelty += novelty
            
            novelty_display = "⭐" * int(novelty * 5)
            if novelty > 0.7:
                novelty_text = f"{novelty_display} [bold green]Highly Novel![/bold green]"
            elif novelty > 0.4:
                novelty_text = f"{novelty_display} Novel"
            else:
                novelty_text = f"{novelty_display} Expected"
            
            summary_table.add_row(
                f"#{result['session']}",
                creation['name'],
                novelty_text,
                str(creation['structure'].get('complexity', 0))
            )
        
        console.print(summary_table)
        
        avg_novelty = total_novelty / len(results) if results else 0
        
        console.print()
        if avg_novelty > 0.6:
            console.print("[bold green]🎉 The Spark demonstrated HIGHLY CREATIVE agency![/bold green]")
            console.print("It built novel, unexpected structures.")
        elif avg_novelty > 0.3:
            console.print("[bold yellow]✨ The Spark demonstrated CREATIVE agency[/bold yellow]")
            console.print("It built functional structures with some novelty.")
        else:
            console.print("[bold white]🏠 The Spark demonstrated FUNCTIONAL agency[/bold white]")
            console.print("It built expected, functional structures.")
        
        console.print(f"\nAverage Novelty Score: [cyan]{avg_novelty:.2f}[/cyan] / 1.00")
        
        # Display hierarchical memory metrics
        if hasattr(self.cube, 'hierarchical_memory') and self.cube.hierarchical_memory:
            console.print(f"\n{'='*80}")
            console.print("[bold cyan]HIERARCHICAL MEMORY EVOLUTION[/bold cyan]")
            console.print("[dim](Salt Water Dissolution During Creation)[/dim]")
            console.print(f"{'='*80}\n")
            
            h_mem = self.cube.hierarchical_memory
            stats = h_mem.get_memory_stats()
            
            # Show how memory evolved through building sessions
            memory_table = Table(title="Memory Development Through Building")
            memory_table.add_column("Metric", style="cyan")
            memory_table.add_column("Value", style="yellow")
            memory_table.add_column("Meaning", style="white")
            
            memory_table.add_row(
                "Experiences Dissolved",
                str(stats['total_experiences']),
                "Each building act → memory traces"
            )
            memory_table.add_row(
                "Pathways Strengthened",
                str(stats['secondary_nodes']),
                "Repeated patterns → stronger routes"
            )
            memory_table.add_row(
                "Structures Crystallized",
                str(stats['promoted_anchors']),
                "Mature pathways → permanent nodes"
            )
            
            strongest = stats['strongest_secondary']
            if strongest['id']:
                strength_bar = "█" * int(strongest['strength'] * 10)
                memory_table.add_row(
                    "Most Developed Path",
                    f"{strength_bar} {strongest['strength']:.2f}",
                    f"Domain: {strongest['domain']}"
                )
            
            console.print(memory_table)
            
            # Show pathway tree if nodes exist
            if stats['secondary_nodes'] > 0:
                console.print()
                tree = Tree("[bold]Building Pathways That Emerged[/bold]")
                for node_id, anchor_data in h_mem.anchor_nodes.items():
                    sec_nodes = anchor_data['secondary_nodes']
                    if sec_nodes:
                        branch = tree.add(f"[cyan]{anchor_data['name']}[/cyan]")
                        for domain, sec in sec_nodes.items():
                            strength = "█" * int(sec.strength * 10)
                            branch.add(f"[yellow]{domain}[/yellow]: {strength} ({sec.activation_count}x)")
                console.print(tree)
            
            console.print(f"\n[dim]💧 Building dissolved {stats['total_experiences']} experiences into memory[/dim]")
            console.print(f"[dim]🔮 {stats['secondary_nodes']} pathways emerged and strengthened[/dim]")
            console.print(f"[dim]💎 {stats['promoted_anchors']} pathways crystallized into permanent structure[/dim]")
        
    def save_results(self, filename: str = "data/open_toolbox_results.json"):
        """Save the creation history"""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        serializable_history = []
        for record in self.creation_history:
            ser_record = record.copy()
            # Remove non-serializable raw_result
            ser_record.pop('raw_result', None)
            serializable_history.append(ser_record)
        
        with open(output_path, 'w') as f:
            json.dump({
                'test_date': datetime.now().isoformat(),
                'total_sessions': len(self.creation_history),
                'creations': serializable_history
            }, f, indent=2)
        
        console.print(f"\n[green]Results saved to {filename}[/green]")


# =============================================================================
# RUN THE CHALLENGE
# =============================================================================

if __name__ == "__main__":
    console.print("[cyan]Loading Spark Cube...[/cyan]")
    
    # Load or create a cube
    cube_path = Path("data/spark_cube_state.json")
    if cube_path.exists():
        console.print("[green]Loading existing cube state...[/green]")
        cube = MinimalSparkCube.load_from_file(str(cube_path))
    else:
        console.print("[yellow]Creating new cube...[/yellow]")
        cube = MinimalSparkCube()
        console.print("[dim]Providing minimal warmup...[/dim]")
        for i in range(10):
            warmup_signal = Signal(type=SignalType.TEXT, data=f"warmup_{i}")
            cube.process_signal(warmup_signal)
        console.print("[green]Ready[/green]")
    
    # Integrate hierarchical memory (salt water dissolution)
    console.print("[cyan]Integrating hierarchical memory...[/cyan]")
    h_memory = integrate_hierarchical_memory(cube)
    console.print("[green]✓ Hierarchical memory active[/green]")
    console.print("[dim]  Building experiences will dissolve into pathways[/dim]")
    console.print("[dim]  Creative patterns will strengthen through use[/dim]")
    console.print("[dim]  Successful approaches will crystallize permanently[/dim]")
    
    # Create the challenge
    challenge = OpenToolboxChallenge(cube)
    
    # Provide the toolbox
    resources = challenge.provide_toolbox()
    
    # Run multiple building sessions
    results = challenge.present_challenge(build_sessions=5)
    
    # Save results
    challenge.save_results()
    
    console.print("\n[bold green]Challenge complete![/bold green]")
    console.print("The Spark was given tools and materials.")
    console.print("It chose what to build through pure agency.")
