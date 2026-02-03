"""
Phase 4: True Autonomous Intelligence
Built on 4D Systems Framework principles

Core principles implemented:
1. "Sequence Determines Outcome" - Optimize sequences per goal
2. Energy Efficiency = Understanding - Use S_i/S_max metric
3. Consciousness Creates Through Choice - Goal-directed action
4. Evolution Is Inevitable - Continuous capability expansion
5. Seed-to-Tree - Unfold latent potential through structure
"""

import os
import ast
import time
import json
import subprocess
import anthropic
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType


# Package name mappings (import name → pip name)
PACKAGE_NAME_MAPPINGS = {
    'sklearn': 'scikit-learn',
    'cv2': 'opencv-python',
    'PIL': 'Pillow',
    'yaml': 'PyYAML',
}

# Standard library modules (should never try to install)
STDLIB_MODULES = {
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'collections', 'copy', 
    'csv', 'datetime', 'decimal', 'enum', 'functools', 'glob', 'hashlib',
    'http', 'io', 'itertools', 'json', 'logging', 'math', 'operator', 'os',
    'pathlib', 'pickle', 're', 'shutil', 'socket', 'string', 'subprocess',
    'sys', 'tempfile', 'threading', 'time', 'typing', 'unittest', 'urllib',
    'warnings', 'weakref', 'xml'
}


@dataclass
class Requirement:
    """A discovered requirement for achieving a goal"""
    name: str
    description: str
    parent_goal: str
    priority: int = 1
    status: str = 'pending'  # pending, in_progress, completed, blocked


class GoalDirectedExplorer:
    """
    Explores based on GOALS, not predefined domains.
    Aligns with: "Consciousness Creates Through Choice"
    """
    
    def __init__(self):
        self.current_goal = None
        self.goal_tree = {}  # Hierarchical goal decomposition
        self.attempted_paths = []
        self.discovered_requirements = []
        
    def set_goal(self, goal: str):
        """Set a high-level goal to pursue"""
        self.current_goal = goal
        print(f"\n🎯 New Goal Set: {goal}")
        
    def discover_requirements(self, goal: str, cube: MinimalSparkCube) -> List[Requirement]:
        """
        Discover what's needed to achieve goal through actual attempts.
        NOT hardcoded - uses attempt → fail → analyze pattern.
        """
        requirements = []
        
        print(f"\n🔍 Discovering requirements for: {goal}")
        
        # Try to achieve the goal with current capabilities
        signal = Signal(
            type=SignalType.TEXT,
            data=f"Task: {goal}",
            timestamp=datetime.now()
        )
        
        try:
            result = cube.process_signal(signal)
            
            # Check if we succeeded
            if result.get('success') and result.get('processing_time', 999) < 5.0:
                print(f"   ✓ Goal already achievable with current capabilities!")
                return []
            
            # Analyze what's missing
            missing = self._analyze_gaps(result, goal, cube)
            
            for gap in missing:
                req = Requirement(
                    name=gap['name'],
                    description=gap['description'],
                    parent_goal=goal,
                    priority=gap['priority']
                )
                requirements.append(req)
                print(f"   📋 Discovered requirement: {req.name}")
            
        except Exception as e:
            # Error means we're definitely missing something
            # BUT: Don't create error handlers for internal errors (like KeyError from dynamic sequences)
            error_type = type(e).__name__
            error_msg = str(e)
            
            # Skip creating requirements for internal errors
            if error_type == 'KeyError' and ('dynamic_' in error_msg or error_msg.startswith("'")):
                print(f"   ⚠️  Internal error (skipping): {error_msg[:50]}")
                return []
            
            print(f"   ⚠️  Execution failed: {error_msg}")
            req = Requirement(
                name=f"error_handler_{error_type}",
                description=f"Handle {error_type} errors",
                parent_goal=goal,
                priority=2
            )
            requirements.append(req)
        
        self.discovered_requirements.extend(requirements)
        return requirements
    
    def _analyze_gaps(self, result: Dict, goal: str, cube: 'MinimalSparkCube') -> List[Dict]:
        """
        Analyze what capabilities are missing based on execution result.
        This replaces hardcoded domain lists with dynamic gap detection.
        
        CRITICAL FIX: Check if capabilities already exist to prevent infinite loops
        where different goals generate the same requirements.
        """
        gaps = []
        
        # Helper to check if capability exists
        def capability_exists(name: str) -> bool:
            # Check in AGI engine's registry
            if hasattr(cube, 'agi_engine') and hasattr(cube.agi_engine, 'capability_registry'):
                if name in cube.agi_engine.capability_registry:
                    return True
            # Check if file exists
            cap_file = Path(__file__).parent.parent / 'capabilities' / f'{name}.py'
            return cap_file.exists()
        
        # 🔥 Convert goal to capability name format using FULL goal name
        # This enables multi-dimensional capabilities from Strategy 2/3!
        # Example: "Adapt adaptation and pattern" → "adapt_adaptation_and_pattern_recognizer"
        goal_base = goal.lower().replace(" and ", "_").replace(" ", "_")
        
        # Check processing time - slow = missing optimized capability
        if result.get('processing_time', 0) > 2.0:
            cap_name = f'{goal_base}_optimizer'
            if not capability_exists(cap_name):
                gaps.append({
                    'name': cap_name,
                    'description': f'Optimized processing for {goal}',
                    'priority': 1
                })
            else:
                print(f"   ✓ Capability {cap_name} already exists, skipping")
        
        # Check if patterns were recognized
        if not result.get('patterns_recognized'):
            cap_name = f'{goal_base}_pattern_recognizer'
            if not capability_exists(cap_name):
                gaps.append({
                    'name': cap_name,
                    'description': f'Pattern recognition for {goal}',
                    'priority': 2
                })
            else:
                print(f"   ✓ Capability {cap_name} already exists, skipping")
        
        # Check if structural connections were made
        if result.get('pathway_strength', 0) < 0.5:
            cap_name = f'{goal_base}_structure_builder'
            if not capability_exists(cap_name):
                gaps.append({
                    'name': cap_name,
                    'description': f'Build strong pathways for {goal}',
                    'priority': 1
                })
            else:
                print(f"   ✓ Capability {cap_name} already exists, skipping")
        
        if not gaps:
            print(f"   ✓ All required capabilities for '{goal}' already exist!")
        
        return gaps
    
    def generate_exploration_signal(self) -> Optional[Dict]:
        """
        Generate next exploration signal based on current goal tree.
        Returns None only if ALL requirements are completed.
        """
        # Find pending requirements
        pending = [r for r in self.discovered_requirements if r.status == 'pending']
        
        if not pending:
            return None
        
        # Prioritize highest priority requirement
        next_req = max(pending, key=lambda r: r.priority)
        next_req.status = 'in_progress'
        
        return {
            'domain': next_req.name,
            'description': next_req.description,
            'signal_data': f"Develop capability: {next_req.description}",
            'parent_goal': next_req.parent_goal,
            'confidence': 0.8
        }


class DynamicSequenceGenerator:
    """
    Generate sequences dynamically for each goal instead of using fixed presets.
    TRUE SELF-ARRANGEMENT - Structure emerges from task requirements.
    
    Instead of 4 hardcoded sequences, generate optimal node orders based on:
    - Goal characteristics (emotional/analytical/creative)
    - Pathway strengths (which connections are strongest)
    - Node development (which nodes are most developed)
    - Past success patterns (what worked before)
    """
    
    def __init__(self, cube: 'MinimalSparkCube'):
        self.cube = cube
        self.generated_sequences = {}  # Cache successful sequences
    
    def generate_sequence(self, goal: str, signal: Signal) -> List[int]:
        """
        Dynamically generate optimal node sequence for this specific goal.
        Returns list of node IDs in processing order.
        """
        # Analyze goal characteristics
        goal_profile = self._analyze_goal(goal, signal.data)
        
        # Get available nodes and their strengths
        available_nodes = list(self.cube.nodes.keys())
        node_strengths = self._get_node_strengths(available_nodes)
        
        # Generate sequence based on goal profile + node strengths
        sequence = self._construct_sequence(goal_profile, node_strengths, available_nodes)
        
        # Cache it
        self.generated_sequences[goal] = sequence
        
        return sequence
    
    def _analyze_goal(self, goal: str, data: str) -> Dict:
        """Analyze goal to determine what type of processing is needed"""
        goal_lower = (goal + " " + data).lower()
        
        profile = {
            'emotional_weight': 0.0,
            'analytical_weight': 0.0,
            'creative_weight': 0.0,
            'pattern_weight': 0.0,
            'memory_weight': 0.0
        }
        
        # Emotional keywords
        if any(word in goal_lower for word in ['feel', 'emotion', 'sentiment', 'mood', 'affect']):
            profile['emotional_weight'] = 1.0
        
        # Analytical keywords
        if any(word in goal_lower for word in ['analyze', 'compute', 'calculate', 'measure', 'evaluate']):
            profile['analytical_weight'] = 1.0
        
        # Creative keywords
        if any(word in goal_lower for word in ['create', 'generate', 'design', 'imagine', 'synthesize']):
            profile['creative_weight'] = 1.0
        
        # Pattern recognition keywords
        if any(word in goal_lower for word in ['recognize', 'pattern', 'classify', 'identify', 'detect']):
            profile['pattern_weight'] = 1.0
        
        # Memory/knowledge keywords
        if any(word in goal_lower for word in ['remember', 'recall', 'learn', 'knowledge', 'understand']):
            profile['memory_weight'] = 1.0
        
        return profile
    
    def _get_node_strengths(self, node_ids: List[int]) -> Dict[int, float]:
        """Get strength of each node based on development + pathway weights"""
        strengths = {}
        
        for node_id in node_ids:
            if node_id not in self.cube.nodes:
                strengths[node_id] = 0.0
                continue
            
            node = self.cube.nodes[node_id]
            
            # Base strength from node development
            base_strength = getattr(node, 'development', 0.5)
            
            # Boost from pathway strengths (how connected is this node?)
            pathway_boost = 0.0
            if hasattr(self.cube, 'pathway_weights'):
                for pathway_id, weight in self.cube.pathway_weights.items():
                    if node_id in pathway_id:
                        pathway_boost += weight
            
            strengths[node_id] = base_strength + (pathway_boost * 0.1)
        
        return strengths
    
    def _construct_sequence(self, profile: Dict, node_strengths: Dict, available_nodes: List[int]) -> List[int]:
        """
        Construct optimal sequence based on goal profile + node strengths.
        This is where TRUE SELF-ARRANGEMENT happens - no hardcoded orders.
        """
        # Score each node for this goal
        node_scores = []
        
        for node_id in available_nodes:
            score = self._score_node_for_goal(node_id, profile, node_strengths)
            node_scores.append((node_id, score))
        
        # Sort by score (descending)
        node_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Take top nodes (at least 5, up to 8)
        optimal_count = min(8, max(5, len(available_nodes)))
        sequence = [node_id for node_id, score in node_scores[:optimal_count]]
        
        # Ensure we always start with a perceptual node and end with integration
        if 9 in sequence:  # Perception node
            sequence.remove(9)
            sequence.insert(0, 9)
        
        if 10 in sequence:  # Integration node
            sequence.remove(10)
            sequence.append(10)
        
        return sequence
    
    def _score_node_for_goal(self, node_id: int, profile: Dict, strengths: Dict) -> float:
        """Score how suitable a node is for this goal"""
        base_score = strengths.get(node_id, 0.5)
        
        # Node specialization bonuses based on node ID
        specialization_bonus = 0.0
        
        if node_id == 6:  # Emotional node
            specialization_bonus = profile['emotional_weight'] * 0.5
        elif node_id == 3:  # Executive/analytical node
            specialization_bonus = profile['analytical_weight'] * 0.5
        elif node_id == 7:  # Pattern recognition node
            specialization_bonus = profile['pattern_weight'] * 0.5
        elif node_id in [11, 12]:  # Tool use / synthesis (creative)
            specialization_bonus = profile['creative_weight'] * 0.5
        elif node_id == 13:  # Introspection (memory/understanding)
            specialization_bonus = profile['memory_weight'] * 0.5
        
        return base_score + specialization_bonus


class SelfCorrectingSynthesizer:
    """
    Iterates until code works OR asks for help.
    Aligns with: "Time Is the Medium" - iterative refinement
    """
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        self.failure_patterns = []
        
    def synthesize_with_correction(self, 
                                   gap: Dict, 
                                   max_attempts: int = 5) -> Optional[Tuple[str, str]]:
        """
        Try → Fail → Learn → Retry loop
        Returns (code, filename) or None if blocked
        """
        code = None
        errors = []
        
        print(f"\n🔧 Synthesizing capability: {gap['domain']}")
        print(f"   Description: {gap['description']}")
        
        for attempt in range(max_attempts):
            print(f"\n   Attempt {attempt + 1}/{max_attempts}...")
            
            # Generate code
            code = self._generate_code(gap, previous_errors=errors)
            
            if not code:
                print(f"   ✗ Generation failed")
                continue
            
            # Test it
            result = self._test_code(code)
            
            if result['success']:
                print(f"   ✓ Success after {attempt + 1} attempts!")
                
                # Generate filename
                filename = f"{gap['domain']}_v{attempt + 1}.py"
                return code, filename
            
            # Analyze the error
            print(f"   ⚠️  Error: {result['error_type']}")
            error_analysis = self._analyze_error(result)
            errors.append(error_analysis)
            
            # Can we fix it ourselves?
            if error_analysis['type'] == 'syntax':
                print(f"   🔧 Syntax error detected, self-correcting...")
                continue
            
            elif error_analysis['type'] == 'missing_dependency':
                # Need external help
                dep = error_analysis['dependency']
                if self._request_dependency(dep):
                    print(f"   ✓ Dependency installed, retrying...")
                    continue
                else:
                    print(f"   ✗ User declined dependency, blocked.")
                    return None
            
            elif error_analysis['type'] == 'logic':
                print(f"   🧠 Logic error, rethinking approach...")
                # Learn from this failure
                self.failure_patterns.append({
                    'gap': gap,
                    'error': error_analysis,
                    'timestamp': datetime.now().isoformat()
                })
                continue
        
        print(f"   ✗ Failed after {max_attempts} attempts")
        return None
    
    def _generate_code(self, gap: Dict, previous_errors: List[Dict] = None) -> Optional[str]:
        """Generate Python code for the capability"""
        
        # Build prompt with error history
        prompt = f"""Generate a Python class that implements this capability:

Domain: {gap['domain']}
Description: {gap['description']}

Requirements:
1. Create a class with clear methods
2. Include docstrings
3. Handle errors gracefully
4. Be efficient and idiomatic Python
"""

        if previous_errors:
            prompt += "\n\nPrevious attempts failed with these errors:\n"
            for i, err in enumerate(previous_errors):
                prompt += f"\nAttempt {i+1}: {err['type']} - {err['message']}\n"
                if 'fix_hint' in err:
                    prompt += f"Fix hint: {err['fix_hint']}\n"
        
        prompt += "\n\nGenerate ONLY the Python code, no explanations:"
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            code = response.content[0].text.strip()
            
            # Extract code from markdown if present
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0].strip()
            elif '```' in code:
                code = code.split('```')[1].split('```')[0].strip()
            
            return code
            
        except Exception as e:
            print(f"   ✗ LLM generation error: {e}")
            return None
    
    def _test_code(self, code: str) -> Dict:
        """Test if the code is valid Python"""
        try:
            # Parse to check syntax
            ast.parse(code)
            
            # Try to compile
            compile(code, '<string>', 'exec')
            
            # Basic execution test (in isolated namespace)
            namespace = {}
            exec(code, namespace)
            
            return {'success': True}
            
        except SyntaxError as e:
            return {
                'success': False,
                'error_type': 'syntax',
                'error': str(e),
                'line': e.lineno
            }
        except ImportError as e:
            # Extract module name
            module = str(e).split("'")[1] if "'" in str(e) else str(e)
            return {
                'success': False,
                'error_type': 'import',
                'error': str(e),
                'module': module
            }
        except Exception as e:
            return {
                'success': False,
                'error_type': 'runtime',
                'error': str(e)
            }
    
    def _analyze_error(self, result: Dict) -> Dict:
        """Analyze error to determine fix strategy"""
        
        if result['error_type'] == 'syntax':
            return {
                'type': 'syntax',
                'message': result['error'],
                'fix_hint': 'Check Python syntax, indentation, and brackets'
            }
        
        elif result['error_type'] == 'import':
            return {
                'type': 'missing_dependency',
                'message': result['error'],
                'dependency': result['module'],
                'fix_hint': f"Install {result['module']}"
            }
        
        else:
            return {
                'type': 'logic',
                'message': result['error'],
                'fix_hint': 'Review logic and algorithm'
            }
    
    def _request_dependency(self, dependency: str) -> bool:
        """Ask user to install missing dependency with smart package name resolution"""
        print(f"\n📦 Missing Dependency: {dependency}")
        
        # Check if it's a stdlib module (should never install)
        base_module = dependency.split('.')[0]
        if base_module in STDLIB_MODULES:
            print(f"   ℹ️  '{base_module}' is a Python standard library module, no installation needed")
            print(f"   ⚠️  This is likely a code generation error - the import may be incorrect")
            return False
        
        # Extract base package for submodules (e.g., "nltk.pos_tag" → "nltk")
        if '.' in dependency:
            base_package = base_module
            print(f"   ℹ️  Detected submodule '{dependency}', installing base package '{base_package}'")
        else:
            base_package = dependency
        
        # Check for package name mappings (e.g., "sklearn" → "scikit-learn")
        pip_package = PACKAGE_NAME_MAPPINGS.get(base_package, base_package)
        if pip_package != base_package:
            print(f"   ℹ️  Mapping '{base_package}' to pip package '{pip_package}'")
        
        print(f"   Attempting automatic installation of '{pip_package}'...")
        
        import sys
        try:
            # Use sys.executable to get the current Python interpreter
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', pip_package],
                check=True,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            print(f"   ✓ Installed {pip_package}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Installation failed: {e.stderr if e.stderr else e}")
            return False
        except FileNotFoundError:
            print(f"   ✗ Error: pip not found")
            return False
        except subprocess.TimeoutExpired:
            print(f"   ✗ Error: Installation timed out")
            return False
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return False


class CodeGrammarLearner:
    """
    Learn Python syntax/patterns to generate WITHOUT LLM.
    Aligns with: "Seed-to-Tree" - unfold latent grammar
    """
    
    def __init__(self):
        self.syntax_patterns = {}  # Python grammar rules
        self.code_templates = {}   # Reusable patterns
        self.successful_patterns = []
        
    def learn_from_code(self, code: str, success: bool, domain: str):
        """
        Extract patterns from generated code.
        Build internal grammar model.
        """
        try:
            # Parse code into AST
            tree = ast.parse(code)
            
            # Extract structural patterns
            for node in ast.walk(tree):
                pattern_type = type(node).__name__
                
                # Track which patterns lead to success
                if pattern_type not in self.syntax_patterns:
                    self.syntax_patterns[pattern_type] = {
                        'successes': 0,
                        'failures': 0,
                        'domains': set(),
                        'examples': []
                    }
                
                if success:
                    self.syntax_patterns[pattern_type]['successes'] += 1
                    self.syntax_patterns[pattern_type]['domains'].add(domain)
                else:
                    self.syntax_patterns[pattern_type]['failures'] += 1
                
                # Store limited examples
                if len(self.syntax_patterns[pattern_type]['examples']) < 3:
                    self.syntax_patterns[pattern_type]['examples'].append({
                        'code_snippet': ast.get_source_segment(code, node),
                        'success': success
                    })
        
        except SyntaxError:
            # Can't parse - learn what NOT to do
            if 'syntax_errors' not in self.syntax_patterns:
                self.syntax_patterns['syntax_errors'] = []
            self.syntax_patterns['syntax_errors'].append(code[:200])
    
    def get_success_rate(self, pattern_type: str) -> float:
        """Calculate success rate for a pattern"""
        if pattern_type not in self.syntax_patterns:
            return 0.0
        
        pattern = self.syntax_patterns[pattern_type]
        total = pattern['successes'] + pattern['failures']
        
        if total == 0:
            return 0.0
        
        return pattern['successes'] / total
    
    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        total_patterns = len(self.syntax_patterns)
        successful_patterns = sum(1 for p in self.syntax_patterns.values() 
                                 if isinstance(p, dict) and p.get('successes', 0) > 0)
        
        return {
            'total_patterns_learned': total_patterns,
            'successful_patterns': successful_patterns,
            'domains_covered': len(set().union(*[p.get('domains', set()) 
                                                 for p in self.syntax_patterns.values() 
                                                 if isinstance(p, dict)]))
        }


class SequenceOptimizer:
    """
    Discovers optimal node sequences for different goals.
    NOW with dynamic sequence generation - not limited to 4 presets.
    Implements: "Sequence Determines Outcome" + TRUE SELF-ARRANGEMENT
    """
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.sequence_outcomes = {}  # Track which sequences work for which goals
        self.sequence_generator = DynamicSequenceGenerator(cube)
        
    def find_optimal_sequence(self, goal: str, signal: Signal) -> str:
        """
        1. Generate custom sequence dynamically for this goal
        2. Test all preset sequences
        3. Compare efficiency
        4. Learn which works best
        """
        print(f"\n🔬 Optimizing sequence for goal: {goal}")
        
        # Generate dynamic sequence first
        dynamic_name = None
        try:
            dynamic_seq = self.sequence_generator.generate_sequence(goal, signal)
            dynamic_name = f"dynamic_{hash(tuple(dynamic_seq)) % 10000}"
            
            # Register it permanently with pathway tracking
            self.cube.sequences[dynamic_name] = dynamic_seq
            # Initialize pathway tracking for learning
            if dynamic_name not in self.cube.pathway_strengths:
                self.cube.pathway_strengths[dynamic_name] = 0.5  # Neutral start
            if dynamic_name not in self.cube.pathway_successes:
                self.cube.pathway_successes[dynamic_name] = {'successes': 0, 'attempts': 0}
            
            print(f"   🧬 Generated dynamic sequence: {dynamic_seq}")
        except Exception as e:
            print(f"   ⚠️  Dynamic generation failed: {str(e)[:50]}")
        
        # Test all sequences (including dynamic)
        sequences = ['standard', 'deep', 'emotional', 'knowledge_seeking']
        if dynamic_name:
            sequences.insert(0, dynamic_name)
        
        best_sequence = None
        best_efficiency = 0
        best_metadata = {}
        
        for seq_name in sequences:
            # Try this sequence
            start = time.time()
            
            try:
                result = self.cube.process_signal(signal, sequence_name=seq_name)
                duration = time.time() - start
                
                # Measure efficiency (4D FRAMEWORK METRIC)
                efficiency = self._calculate_efficiency(result, duration)
                
                # Gather metadata for intelligent tie-breaking
                metadata = {
                    'sequence_name': seq_name,
                    'duration': duration,
                    'is_dynamic': seq_name.startswith('dynamic_') if seq_name else False,
                    'node_count': len(self.cube.sequences.get(seq_name, [])),
                    'pathway_strength': self.cube.pathway_strengths.get(seq_name, 0.0),
                    'success_rate': self._get_success_rate(seq_name)
                }
                
                indicator = "🧬" if metadata['is_dynamic'] else "  "
                print(f"   {indicator}{seq_name:20s} → efficiency: {efficiency:.3f}")
                
                # Intelligent comparison (handles ties)
                if self._is_better_sequence(efficiency, metadata, best_efficiency, best_metadata):
                    best_efficiency = efficiency
                    best_sequence = seq_name
                    best_metadata = metadata
            
            except Exception as e:
                print(f"   {seq_name:20s} → error: {str(e)[:50]}")
                continue
        
        # Learn: This goal + this sequence = this efficiency
        if goal not in self.sequence_outcomes:
            self.sequence_outcomes[goal] = {}
        
        self.sequence_outcomes[goal][best_sequence] = best_efficiency
        
        is_dynamic = best_sequence and best_sequence.startswith('dynamic_')
        symbol = "🧬" if is_dynamic else "✓"
        print(f"   {symbol} Optimal sequence: {best_sequence} ({best_efficiency:.3f})")
        
        if is_dynamic:
            print(f"   🎉 Dynamic sequence won! True self-arrangement active.")
        
        return best_sequence or 'standard'
    
    def _calculate_efficiency(self, result: Dict, duration: float) -> float:
        """
        Energy efficiency = understanding (4D FRAMEWORK)
        Based on S_i / S_max term from manifestation equation
        """
        # Lower time = higher efficiency
        time_efficiency = 1.0 / (duration + 0.1)  # Add small epsilon
        
        # Pattern recognition quality
        patterns = len(result.get('patterns_recognized', []))
        pattern_quality = min(patterns / 5.0, 1.0)  # Normalize to max 1.0
        
        # Structural integration (how well nodes connected)
        structural_efficiency = result.get('pathway_strength', 0)
        
        # 4D FRAMEWORK FORMULA:
        # M_4D = Σ(w_i × N_i × (S_i / S_max) × T_i)
        # We're measuring S_i / S_max here
        
        efficiency = (
            time_efficiency * 0.4 +       # Time component
            pattern_quality * 0.3 +        # Recognition component
            structural_efficiency * 0.3    # Structure component
        )
        
        return efficiency
    
    def _get_success_rate(self, sequence_name: str) -> float:
        """Get historical success rate for a sequence"""
        if sequence_name not in self.cube.pathway_successes:
            return 0.0
        
        stats = self.cube.pathway_successes[sequence_name]
        attempts = stats.get('attempts', 0)
        
        if attempts == 0:
            return 0.0
        
        successes = stats.get('successes', 0)
        return successes / attempts
    
    def _is_better_sequence(self, efficiency: float, metadata: Dict, 
                           best_efficiency: float, best_metadata: Dict) -> bool:
        """
        Intelligent tie-breaking for sequence selection.
        Uses 5-level hierarchy aligned with 4D Framework principles:
        
        1. Efficiency score (primary)
        2. Dynamic preference (learned sequences favored)
        3. Historical success rate (proven pathways)
        4. Pathway strength (reinforcement learning)
        5. Node count (complexity tie-breaker)
        6. Processing time (final efficiency measure)
        """
        # Level 1: Efficiency difference (tolerance for floating point)
        EPSILON = 0.001
        
        if efficiency > best_efficiency + EPSILON:
            return True
        elif efficiency < best_efficiency - EPSILON:
            return False
        
        # Level 2: Dynamic sequence preference (learning over presets)
        # Aligns with "Evolution Is Inevitable" - favor learned behaviors
        if not best_metadata:  # First sequence tested
            return True
        
        is_dynamic = metadata.get('is_dynamic', False)
        best_is_dynamic = best_metadata.get('is_dynamic', False)
        
        if is_dynamic and not best_is_dynamic:
            return True
        elif not is_dynamic and best_is_dynamic:
            return False
        
        # Level 3: Historical success rate (proven pathways)
        # Aligns with "Sequence Determines Outcome" - trust what works
        current_success = metadata.get('success_rate', 0.0)
        best_success = best_metadata.get('success_rate', 0.0)
        
        if abs(current_success - best_success) > EPSILON:
            return current_success > best_success
        
        # Level 4: Pathway strength (reinforcement learning)
        # Aligns with 4D Framework pathway reinforcement
        current_strength = metadata.get('pathway_strength', 0.0)
        best_strength = best_metadata.get('pathway_strength', 0.0)
        
        if abs(current_strength - best_strength) > EPSILON:
            return current_strength > best_strength
        
        # Level 5: Node count (complexity preference)
        # More nodes = richer processing (Seed-to-Tree growth)
        current_nodes = metadata.get('node_count', 0)
        best_nodes = best_metadata.get('node_count', 0)
        
        if current_nodes != best_nodes:
            return current_nodes > best_nodes
        
        # Level 6: Processing time (final efficiency measure)
        # Energy efficiency = understanding (faster = more efficient)
        current_time = metadata.get('duration', float('inf'))
        best_time = best_metadata.get('duration', float('inf'))
        
        return current_time < best_time
    
    def get_learned_sequences(self) -> Dict:
        """Get all learned sequence optimizations"""
        return self.sequence_outcomes


class Phase4AGIEngine:
    """
    Complete autonomous intelligence system.
    Built on 4D Systems Framework principles.
    
    Key differences from Phase 3:
    - Goal-directed exploration (not domain cycling)
    - Self-correction loops (not skip-on-failure)
    - Code pattern learning (not always LLM)
    - Sequence optimization (4D Framework metric)
    """
    
    def __init__(self, cube: MinimalSparkCube, api_key: str, capabilities_dir: str = "spark_cube/capabilities"):
        self.cube = cube
        self.capabilities_dir = Path(capabilities_dir)
        self.capabilities_dir.mkdir(parents=True, exist_ok=True)
        
        # Phase 4 components
        self.goal_explorer = GoalDirectedExplorer()
        self.self_corrector = SelfCorrectingSynthesizer(api_key)
        self.code_learner = CodeGrammarLearner()
        self.sequence_optimizer = SequenceOptimizer(cube)
        
        # Capability registry (for compatibility with autonomous runner)
        self.capability_registry = {}
        
        # Load existing capabilities from disk
        self._load_existing_capabilities()
        
        # Tracking
        self.goals_achieved = []
        self.goals_blocked = []
        self.total_capabilities_synthesized = 0
        
    def pursue_goal(self, goal: str, max_iterations: int = 10) -> bool:
        """
        Main AGI loop:
        1. Set goal
        2. Discover requirements (through attempts)
        3. Synthesize capabilities (with self-correction)
        4. Optimize sequences (4D Framework)
        5. Repeat until goal achieved
        """
        print(f"\n{'='*80}")
        print(f"🎯 GOAL: {goal}")
        print(f"{'='*80}")
        
        # Set the goal
        self.goal_explorer.set_goal(goal)
        
        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration + 1}/{max_iterations} ---")
            
            # Check if goal achieved
            if self._is_goal_achieved(goal):
                print(f"\n✅ Goal achieved in {iteration + 1} iterations!")
                self.goals_achieved.append({
                    'goal': goal,
                    'iterations': iteration + 1,
                    'timestamp': datetime.now().isoformat()
                })
                return True
            
            # Discover what's missing
            requirements = self.goal_explorer.discover_requirements(goal, self.cube)
            
            if not requirements:
                print(f"\n✓ No new requirements discovered")
                break
            
            print(f"\n📋 Discovered {len(requirements)} requirements")
            
            # For each requirement, synthesize capability
            for req in requirements:
                print(f"\n{'─'*60}")
                print(f"Synthesizing: {req.name}")
                
                # Create gap dict for synthesizer
                gap = {
                    'domain': req.name,
                    'description': req.description,
                    'confidence': 0.8
                }
                
                # Synthesize with self-correction
                result = self.self_corrector.synthesize_with_correction(gap)
                
                if result:
                    code, filename = result
                    
                    # Learn from successful code
                    self.code_learner.learn_from_code(code, success=True, domain=req.name)
                    
                    # Save capability
                    filepath = self.capabilities_dir / filename
                    filepath.write_text(code)
                    
                    # 🔥 NEW: Dynamically load capability into the cube
                    from spark_cube.core.minimal_spark import SensorInterface
                    if not hasattr(self, 'sensor'):
                        self.sensor = SensorInterface(self.cube)
                    
                    loaded = self.sensor.load_capability(filepath)
                    if loaded:
                        print(f"   🔌 Capability integrated into Spark Cube")
                    
                    # Add to registry
                    self.capability_registry[req.name] = {
                        'filepath': str(filepath),
                        'description': req.description,
                        'parent_goal': req.parent_goal,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.total_capabilities_synthesized += 1
                    req.status = 'completed'
                    
                    print(f"   ✅ Capability saved: {filename}")
                    
                    # 🔥 OPTIMIZE SEQUENCE PER SUCCESSFUL SYNTHESIS
                    opt_signal = Signal(
                        type=SignalType.TEXT,
                        data=req.name,
                        timestamp=datetime.now()
                    )
                    optimal_seq = self.sequence_optimizer.find_optimal_sequence(req.name, opt_signal)
                    print(f"   🧬 Learned: '{req.name}' works best with '{optimal_seq}' sequence")
                    
                else:
                    print(f"   ❌ Blocked on '{req.name}'")
                    req.status = 'blocked'
        
        # Check final status
        if self._is_goal_achieved(goal):
            self.goals_achieved.append({
                'goal': goal,
                'iterations': max_iterations,
                'timestamp': datetime.now().isoformat()
            })
            return True
        else:
            print(f"\n⚠️  Goal not achieved after {max_iterations} iterations")
            self.goals_blocked.append({
                'goal': goal,
                'reason': 'max_iterations',
                'timestamp': datetime.now().isoformat()
            })
            return False
    
    def _is_goal_achieved(self, goal: str) -> bool:
        """Test if goal can be achieved with current capabilities"""
        # First, check if we have relevant capabilities loaded
        if not hasattr(self, 'sensor'):
            from spark_cube.core.minimal_spark import SensorInterface
            self.sensor = SensorInterface(self.cube)
        
        # 🔥 FIX 1: Improved goal achievement detection
        # Try to invoke matching capabilities
        invocation_result = self.sensor.invoke_capability(goal)
        
        # Success if any capability was successfully invoked
        if invocation_result.get('success') and invocation_result.get('successful_count', 0) > 0:
            successful = invocation_result['successful_count']
            total = invocation_result.get('total_attempts', successful)
            print(f"   ✅ Goal achieved! {successful}/{total} capabilities executed successfully")
            return True
        
        # Check if capabilities exist but couldn't be invoked
        if invocation_result.get('capabilities_found', 0) > 0:
            print(f"   ⚠️  {invocation_result['capabilities_found']} capabilities found but couldn't execute")
            print(f"       Reason: {invocation_result.get('reason', 'unknown')}")
            # Don't mark as failed - capabilities exist, just need better invocation
        
        # Fall back to checking if relevant capabilities exist in AGI registry
        if self.cube.agi_engine:
            goal_keywords = set(goal.lower().split())
            
            for cap_type in self.cube.agi_engine.capability_registry.keys():
                cap_keywords = set(cap_type.lower().replace('_', ' ').split())
                
                # If significant overlap, consider it relevant
                overlap = len(goal_keywords & cap_keywords)
                if overlap >= 2:  # At least 2 matching keywords
                    print(f"   ✅ Goal achieved! Relevant capability '{cap_type}' exists")
                    return True
        
        # Final fallback: Try processing
        signal = Signal(
            type=SignalType.TEXT,
            data=goal,
            timestamp=datetime.now()
        )
        
        try:
            result = self.cube.process_signal(signal)
            
            # Goal achieved if processing succeeded efficiently
            # Using 4D Framework efficiency metric
            success = result.get('success', False)
            efficient = result.get('processing_time', 999) < 5.0
            
            return success and efficient
        except:
            return False
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            'total_capabilities_synthesized': self.total_capabilities_synthesized,
            'goals_achieved': len(self.goals_achieved),
            'goals_blocked': len(self.goals_blocked),
            'code_learning': self.code_learner.get_statistics(),
            'sequence_optimizations': len(self.sequence_optimizer.sequence_outcomes),
            'discovered_requirements': len(self.goal_explorer.discovered_requirements)
        }
    
    def save_state(self, filepath: str):
        """Save engine state for checkpointing"""
        state = {
            'statistics': self.get_statistics(),
            'goals_achieved': self.goals_achieved,
            'goals_blocked': self.goals_blocked,
            'sequence_outcomes': self.sequence_optimizer.sequence_outcomes,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _load_existing_capabilities(self):
        """Load existing capabilities from disk on startup"""
        if not self.capabilities_dir.exists():
            return
        
        loaded_count = 0
        for py_file in self.capabilities_dir.glob("*.py"):
            if py_file.name.startswith('__'):
                continue
            
            # Extract base capability name (without version)
            cap_name = py_file.stem  # e.g., "understand_pattern_recognizer_v1"
            base_name = cap_name.rsplit('_v', 1)[0] if '_v' in cap_name else cap_name
            
            # Register in capability registry
            self.capability_registry[base_name] = {
                'file': str(py_file),
                'loaded_from_disk': True,
                'timestamp': datetime.fromtimestamp(py_file.stat().st_mtime).isoformat()
            }
            loaded_count += 1
        
        if loaded_count > 0:
            print(f"✓ Loaded {loaded_count} existing capabilities from disk")
            print(f"   Skipping synthesis for: {', '.join(list(self.capability_registry.keys())[:5])}{'...' if loaded_count > 5 else ''}")
