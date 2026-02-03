"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║              SEMANTIC RESPONSE QUALITY VALIDATION                             ║
║           Test if the system generates REAL, MEANINGFUL answers               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This validates ACTUAL semantic output quality, not just structure:
- Does it produce an answer?
- Is the answer relevant to the question?
- Does it demonstrate understanding?
- Can it explain its reasoning?

NO PASS without real semantic responses.
"""

import sys
from pathlib import Path

# Add paths for imports
spark_core_path = Path(__file__).parent / "spark_cube" / "core"
sys.path.insert(0, str(spark_core_path))
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType, integrate_hierarchical_memory
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class ResponseTest:
    """A test that requires an actual semantic response"""
    name: str
    question: str
    context: Dict[str, Any]
    validation: Dict[str, callable]  # Functions to validate response quality
    

class ResponseQualityValidator:
    """
    Validates that the system produces REAL semantic responses.
    This is NOT about structure - it's about actual answers.
    """
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.results = []
        
    def run_validation(self, tests: List[ResponseTest]) -> Dict[str, Any]:
        """
        Run validation tests.
        ONLY passes if actual semantic responses are generated.
        """
        console.print(Panel.fit(
            "[bold cyan]SEMANTIC RESPONSE QUALITY VALIDATION[/bold cyan]\n\n"
            "[yellow]Testing ACTUAL response generation:[/yellow]\n"
            "  • Does it produce an answer?\n"
            "  • Is the answer relevant?\n"
            "  • Does it show understanding?\n"
            "  • Can it explain reasoning?\n\n"
            f"[green]{len(tests)} Response Tests[/green]\n\n"
            "[red]NO PASS without real semantic outputs[/red]",
            border_style="cyan"
        ))
        
        test_results = []
        for test in tests:
            console.print(f"\n{'='*80}")
            console.print(f"[bold cyan]TEST: {test.name}[/bold cyan]")
            console.print(f"[yellow]Question: {test.question}[/yellow]")
            console.print(f"{'='*80}\n")
            
            result = self._validate_response(test)
            test_results.append(result)
            self._display_result(result)
        
        # Final analysis
        summary = self._final_analysis(test_results)
        
        return {
            'test_date': datetime.now().isoformat(),
            'tests_run': len(tests),
            'results': test_results,
            'summary': summary
        }
    
    def _validate_response(self, test: ResponseTest) -> Dict[str, Any]:
        """
        Validate one response.
        Checks for ACTUAL semantic output, not just processing.
        """
        # Create signal
        signal = Signal(
            type=SignalType.COMPOSITE,
            data={
                'question': test.question,
                'context': test.context,
                'require': 'semantic_response'
            },
            metadata={'validation_test': True}
        )
        
        # Process
        console.print("[dim]Processing question...[/dim]")
        result = self.cube.process_signal(signal)
        
        # Extract response
        response = self._extract_response(result)
        
        # Validate response quality
        validation = self._check_response_quality(response, test.validation)
        
        return {
            'test': test.name,
            'question': test.question,
            'response_generated': response is not None,
            'response': response,
            'response_length': len(str(response)) if response else 0,
            'validation': validation,
            'passed': validation['overall_pass'],
            'raw_result': {
                'pathway': result.get('sequence', 'unknown'),
                'coherence': result.get('coherence', {}),
                'responses': result.get('responses', [])
            }
        }
    
    def _extract_response(self, result: Dict) -> Optional[str]:
        """
        Extract the actual semantic response from processing result.
        Returns None if no response was generated.
        """
        # Check multiple locations for response
        
        # 1. Explicit response field
        if 'response' in result and result['response']:
            return str(result['response'])
        
        # 2. Responses list
        if 'responses' in result and result['responses']:
            responses = result['responses']
            if isinstance(responses, list) and len(responses) > 0:
                return str(responses[0])
        
        # 3. Generated text field
        if 'generated_text' in result and result['generated_text']:
            return str(result['generated_text'])
        
        # 4. Answer field
        if 'answer' in result and result['answer']:
            return str(result['answer'])
        
        # 5. Output field
        if 'output' in result and result['output']:
            return str(result['output'])
        
        return None
    
    def _check_response_quality(
        self,
        response: Optional[str],
        validation_funcs: Dict[str, callable]
    ) -> Dict[str, Any]:
        """
        Check if the response meets quality criteria.
        This is where we validate ACTUAL understanding.
        """
        checks = {
            'has_response': response is not None and len(str(response)) > 0,
            'min_length': len(str(response)) >= 10 if response else False,
            'not_empty': response not in [None, '', 'None', '[]', '{}'] if response else False,
        }
        
        # Run custom validation functions
        for name, func in validation_funcs.items():
            try:
                checks[name] = func(response)
            except Exception as e:
                checks[name] = False
                checks[f'{name}_error'] = str(e)
        
        # Overall pass requires ALL checks to pass
        overall_pass = all([v for k, v in checks.items() if not k.endswith('_error')])
        
        return {
            'checks': checks,
            'overall_pass': overall_pass,
            'passed_checks': sum([1 for v in checks.values() if v is True]),
            'total_checks': len([k for k in checks.keys() if not k.endswith('_error')])
        }
    
    def _display_result(self, result: Dict[str, Any]):
        """Display test results"""
        table = Table(title=f"Response Validation: {result['test']}", border_style="cyan")
        table.add_column("Check", style="yellow")
        table.add_column("Result", style="white")
        
        table.add_row("Response Generated", "✓" if result['response_generated'] else "✗")
        table.add_row("Response Length", str(result['response_length']))
        table.add_row("Passed Checks", f"{result['validation']['passed_checks']}/{result['validation']['total_checks']}")
        table.add_row("Overall", "✓ PASS" if result['passed'] else "✗ FAIL")
        
        console.print(table)
        
        if result['response_generated']:
            console.print(f"\n[green]Response:[/green]")
            console.print(f"  {result['response'][:200]}..." if len(str(result['response'])) > 200 else f"  {result['response']}")
        else:
            console.print("\n[red]✗ NO RESPONSE GENERATED[/red]")
        
        # Show validation details
        console.print("\n[cyan]Validation Checks:[/cyan]")
        for check, passed in result['validation']['checks'].items():
            if not check.endswith('_error'):
                status = "✓" if passed else "✗"
                console.print(f"  {status} {check}")
    
    def _final_analysis(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Final analysis of all tests"""
        console.print(f"\n{'='*80}")
        console.print("[bold cyan]FINAL VALIDATION RESULTS[/bold cyan]")
        console.print(f"{'='*80}\n")
        
        passed = sum([1 for r in results if r['passed']])
        total = len(results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        responses_generated = sum([1 for r in results if r['response_generated']])
        
        summary_table = Table(title="Response Quality Summary")
        summary_table.add_column("Test", style="cyan")
        summary_table.add_column("Response", style="yellow")
        summary_table.add_column("Result", style="green")
        
        for result in results:
            summary_table.add_row(
                result['test'],
                "✓" if result['response_generated'] else "✗",
                "PASS" if result['passed'] else "FAIL"
            )
        
        console.print(summary_table)
        
        console.print(f"\n[bold]Overall Results:[/bold]")
        console.print(f"  Tests Passed: {passed}/{total} ({pass_rate:.1f}%)")
        console.print(f"  Responses Generated: {responses_generated}/{total}")
        
        # The verdict
        if pass_rate >= 70:
            console.print("\n[bold green]✓ SEMANTIC RESPONSE GENERATION VALIDATED[/bold green]")
            console.print("[green]The system generates real, meaningful responses[/green]")
        elif responses_generated > 0:
            console.print("\n[bold yellow]⚠ PARTIAL RESPONSE CAPABILITY[/bold yellow]")
            console.print("[yellow]System generates some responses, but quality needs improvement[/yellow]")
        else:
            console.print("\n[bold red]✗ NO SEMANTIC RESPONSE GENERATION[/bold red]")
            console.print("[red]System does not generate semantic responses yet[/red]")
        
        return {
            'tests_passed': passed,
            'tests_total': total,
            'pass_rate': pass_rate,
            'responses_generated': responses_generated,
            'verdict': 'VALIDATED' if pass_rate >= 70 else 'PARTIAL' if responses_generated > 0 else 'NOT_VALIDATED'
        }
    
    def save_results(self, results: Dict[str, Any]):
        """Save validation results"""
        output_path = Path("data/response_quality_validation.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Results saved to {output_path}[/green]")


# =============================================================================
# TEST DEFINITIONS
# =============================================================================

def create_response_tests() -> List[ResponseTest]:
    """
    Define tests that require ACTUAL semantic responses.
    These test real understanding, not just processing.
    """
    return [
        ResponseTest(
            name="Simple Pattern Recognition",
            question="What comes next in this sequence: 2, 4, 8, 16, 32, ?",
            context={'sequence': [2, 4, 8, 16, 32]},
            validation={
                'contains_number': lambda r: any(char.isdigit() for char in str(r)) if r else False,
                'mentions_pattern': lambda r: any(word in str(r).lower() for word in ['double', 'multiply', 'times', 'pattern']) if r else False,
            }
        ),
        
        ResponseTest(
            name="Concept Explanation",
            question="What is emergence? Explain in one sentence.",
            context={'concept': 'emergence'},
            validation={
                'is_explanation': lambda r: len(str(r).split()) > 5 if r else False,
                'mentions_properties': lambda r: any(word in str(r).lower() for word in ['whole', 'parts', 'property', 'system']) if r else False,
            }
        ),
        
        ResponseTest(
            name="Problem Solving",
            question="If all roses are flowers, and all flowers are plants, are roses plants?",
            context={'logic': 'transitive'},
            validation={
                'has_answer': lambda r: any(word in str(r).lower() for word in ['yes', 'no', 'true', 'false']) if r else False,
                'shows_reasoning': lambda r: len(str(r).split()) > 3 if r else False,
            }
        ),
        
        ResponseTest(
            name="Creative Synthesis",
            question="Combine the concepts of 'water' and 'memory' into a metaphor.",
            context={'concepts': ['water', 'memory']},
            validation={
                'mentions_both': lambda r: all(word in str(r).lower() for word in ['water', 'memory']) if r else False,
                'is_creative': lambda r: len(str(r).split()) > 10 if r else False,
            }
        ),
        
        ResponseTest(
            name="Self-Reflection",
            question="Describe how you processed the previous question.",
            context={'meta': True},
            validation={
                'shows_awareness': lambda r: any(word in str(r).lower() for word in ['process', 'think', 'consider', 'analyze']) if r else False,
                'substantial': lambda r: len(str(r).split()) > 5 if r else False,
            }
        ),
    ]


# =============================================================================
# RUN VALIDATION
# =============================================================================

if __name__ == "__main__":
    console.print("[cyan]Loading Spark Cube...[/cyan]")
    
    # Load cube (should have semantic response capabilities now)
    cube_path = Path("data/spark_cube_state.json")
    if cube_path.exists():
        console.print("[green]Loading cube with capabilities...[/green]")
        cube = MinimalSparkCube.load_from_file(str(cube_path))
    else:
        console.print("[yellow]Creating new cube...[/yellow]")
        cube = MinimalSparkCube()
    
    # Integrate hierarchical memory
    console.print("[cyan]Integrating hierarchical memory...[/cyan]")
    memory = integrate_hierarchical_memory(cube, "spark_cube/memory/hierarchical_memory.json")
    console.print("[green]✓ Memory integrated[/green]")
    
    # Create validator
    validator = ResponseQualityValidator(cube)
    
    # Create tests
    tests = create_response_tests()
    
    # Run validation
    results = validator.run_validation(tests)
    
    # Save results
    validator.save_results(results)
    
    console.print("\n[bold green]Validation complete![/bold green]")
    console.print("[dim]Review data/response_quality_validation.json for details[/dim]")
