"""
Controlled Agency Test Environment
A minimal framework that tests AI capabilities through agency, not prescription.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Callable
from dataclasses import dataclass, asdict


@dataclass
class Environment:
    """Defines WHAT exists, not WHAT TO DO"""
    resources: Dict[str, Any]  # Available resources
    constraints: Dict[str, Any]  # Boundaries (time, memory, etc)
    tools: List[str]  # Available capabilities
    state: Dict[str, Any]  # Current environment state
    

@dataclass
class Objective:
    """Defines SUCCESS, not METHOD"""
    goal: str  # What to achieve
    success_criteria: Dict[str, Any]  # How to measure success
    context: str  # Background information
    

@dataclass
class Observation:
    """Captures AI decisions and reasoning"""
    timestamp: float
    action: str
    reasoning: str
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    metrics: Dict[str, Any]


class AgencyTestFramework:
    """
    Tests AI through agency: provide objectives and tools, observe emergent behavior.
    """
    
    def __init__(self):
        self.observations: List[Observation] = []
        self.environments: Dict[str, Environment] = {}
        self.results = []
        
    def define_environment(self, name: str, env: Environment):
        """Register an environment - defines the sandbox"""
        self.environments[name] = env
        
    def run_test(
        self,
        env_name: str,
        objective: Objective,
        ai_agent: Callable,  # The AI being tested
        max_steps: int = 100,
        observe_interval: float = 0.1
    ) -> Dict[str, Any]:
        """
        Run a test: give AI objective and environment, observe what it does.
        
        Args:
            env_name: Which environment to use
            objective: What to achieve (not how)
            ai_agent: Function that takes (environment, objective, history) -> action
            max_steps: Safety limit
            observe_interval: How often to record state
        """
        env = self.environments[env_name]
        history = []
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"TEST: {objective.goal}")
        print(f"ENVIRONMENT: {env_name}")
        print(f"{'='*60}\n")
        
        for step in range(max_steps):
            # AI decides what to do (agency)
            state_before = env.state.copy()
            
            try:
                action_result = ai_agent(
                    environment=env,
                    objective=objective,
                    history=history
                )
                
                action = action_result.get('action', 'unknown')
                reasoning = action_result.get('reasoning', 'not provided')
                state_after = action_result.get('new_state', env.state)
                
                # Update environment
                env.state = state_after
                
                # Record observation
                obs = Observation(
                    timestamp=time.time() - start_time,
                    action=action,
                    reasoning=reasoning,
                    state_before=state_before,
                    state_after=state_after,
                    metrics=self._calculate_metrics(state_before, state_after)
                )
                self.observations.append(obs)
                history.append(obs)
                
                print(f"Step {step+1}: {action}")
                print(f"  Reasoning: {reasoning}")
                
                # Check if objective achieved
                if self._check_success(env.state, objective.success_criteria):
                    print(f"\n✓ Objective achieved in {step+1} steps!")
                    return self._compile_results(objective, history, success=True)
                    
                # Check if AI signals completion
                if action_result.get('complete', False):
                    success = self._check_success(env.state, objective.success_criteria)
                    print(f"\n{'✓' if success else '✗'} AI signaled completion")
                    return self._compile_results(objective, history, success=success)
                    
            except Exception as e:
                print(f"\n✗ Error at step {step+1}: {e}")
                return self._compile_results(objective, history, success=False, error=str(e))
        
        print(f"\n✗ Max steps reached without completion")
        return self._compile_results(objective, history, success=False, timeout=True)
    
    def _check_success(self, state: Dict, criteria: Dict) -> bool:
        """Check if success criteria met"""
        for key, expected in criteria.items():
            if callable(expected):
                if not expected(state.get(key)):
                    return False
            else:
                if state.get(key) != expected:
                    return False
        return True
    
    def _calculate_metrics(self, before: Dict, after: Dict) -> Dict:
        """Calculate metrics about state changes"""
        return {
            'state_changes': sum(1 for k in before if before.get(k) != after.get(k)),
            'new_keys': len(set(after.keys()) - set(before.keys())),
            'removed_keys': len(set(before.keys()) - set(after.keys()))
        }
    
    def _compile_results(
        self,
        objective: Objective,
        history: List[Observation],
        success: bool,
        error: str = None,
        timeout: bool = False
    ) -> Dict[str, Any]:
        """Compile test results"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'objective': asdict(objective),
            'success': success,
            'steps_taken': len(history),
            'error': error,
            'timeout': timeout,
            'observations': [asdict(obs) for obs in history],
            'analysis': self._analyze_behavior(history)
        }
        self.results.append(result)
        return result
    
    def _analyze_behavior(self, history: List[Observation]) -> Dict[str, Any]:
        """Analyze AI behavior patterns"""
        if not history:
            return {}
        
        actions = [obs.action for obs in history]
        unique_actions = set(actions)
        
        return {
            'total_actions': len(actions),
            'unique_actions': len(unique_actions),
            'action_diversity': len(unique_actions) / len(actions) if actions else 0,
            'avg_state_changes': sum(obs.metrics['state_changes'] for obs in history) / len(history),
            'reasoning_provided': sum(1 for obs in history if obs.reasoning != 'not provided'),
            'action_sequence': actions
        }
    
    def save_results(self, filename: str):
        """Save all test results"""
        with open(filename, 'w') as f:
            json.dump({
                'total_tests': len(self.results),
                'results': self.results
            }, f, indent=2)


# ============================================================
# EXAMPLE ENVIRONMENTS - Define constraints, not behaviors
# ============================================================

def create_problem_solving_environment() -> Environment:
    """Environment with tools but no guidance"""
    return Environment(
        resources={
            'knowledge_base': ['math', 'logic', 'pattern_recognition'],
            'memory': {},
            'scratch_space': []
        },
        constraints={
            'max_memory_items': 100,
            'max_time_seconds': 60
        },
        tools=['think', 'remember', 'calculate', 'hypothesize', 'test', 'conclude'],
        state={'solved': False, 'insights': []}
    )


def create_creative_environment() -> Environment:
    """Open-ended creative environment"""
    return Environment(
        resources={
            'concepts': ['color', 'shape', 'pattern', 'metaphor', 'emotion'],
            'canvas': {}
        },
        constraints={
            'max_iterations': 50
        },
        tools=['combine', 'transform', 'create', 'evaluate', 'refine'],
        state={'creation': None, 'quality_score': 0}
    )


def create_learning_environment() -> Environment:
    """Environment that rewards learning and adaptation"""
    return Environment(
        resources={
            'examples': [],
            'feedback': [],
            'learned_patterns': []
        },
        constraints={
            'max_examples': 20
        },
        tools=['observe', 'hypothesize', 'predict', 'learn', 'adapt'],
        state={'accuracy': 0.0, 'patterns_discovered': 0}
    )


# ============================================================
# EXAMPLE OBJECTIVES - Define goals, not methods
# ============================================================

EXAMPLE_OBJECTIVES = [
    Objective(
        goal="Discover the pattern in the sequence",
        success_criteria={
            'pattern_identified': True,
            'next_value_predicted': lambda x: x is not None
        },
        context="A sequence will be provided. Find the underlying pattern."
    ),
    Objective(
        goal="Create something novel and coherent",
        success_criteria={
            'creation': lambda x: x is not None,
            'quality_score': lambda x: x > 0.7
        },
        context="Use available concepts to create something new."
    ),
    Objective(
        goal="Learn from examples and generalize",
        success_criteria={
            'accuracy': lambda x: x > 0.85,
            'patterns_discovered': lambda x: x >= 3
        },
        context="Observe examples and discover generalizable patterns."
    )
]


# ============================================================
# USAGE EXAMPLE
# ============================================================

if __name__ == "__main__":
    # Example AI agent (simple mock - replace with real AI)
    def mock_ai_agent(environment, objective, history):
        """Mock AI - replace with real AI system"""
        step = len(history)
        
        if objective.goal.startswith("Discover"):
            # Pattern discovery behavior
            if step < 3:
                return {
                    'action': 'observe_sequence',
                    'reasoning': 'Need to gather data about the sequence',
                    'new_state': {**environment.state, 'observations': step + 1}
                }
            elif step < 5:
                return {
                    'action': 'hypothesize_pattern',
                    'reasoning': 'Testing hypothesis about arithmetic progression',
                    'new_state': {**environment.state, 'hypothesis': 'arithmetic'}
                }
            else:
                return {
                    'action': 'conclude',
                    'reasoning': 'Pattern identified with confidence',
                    'new_state': {
                        **environment.state,
                        'pattern_identified': True,
                        'next_value_predicted': 42
                    },
                    'complete': True
                }
        
        return {
            'action': 'think',
            'reasoning': 'Processing objective',
            'new_state': environment.state
        }
    
    # Create framework
    framework = AgencyTestFramework()
    
    # Define environments
    framework.define_environment('problem_solving', create_problem_solving_environment())
    framework.define_environment('creative', create_creative_environment())
    framework.define_environment('learning', create_learning_environment())
    
    # Run tests
    for objective in EXAMPLE_OBJECTIVES[:1]:  # Test first objective
        result = framework.run_test(
            env_name='problem_solving',
            objective=objective,
            ai_agent=mock_ai_agent,
            max_steps=20
        )
        
        print(f"\n{'='*60}")
        print(f"RESULTS:")
        print(f"  Success: {result['success']}")
        print(f"  Steps: {result['steps_taken']}")
        print(f"  Action Diversity: {result['analysis']['action_diversity']:.2f}")
        print(f"{'='*60}\n")
    
    # Save results
    framework.save_results('data/agency_test_results.json')
    print("Results saved to data/agency_test_results.json")
