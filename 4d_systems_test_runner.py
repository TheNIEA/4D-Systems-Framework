#!/usr/bin/env python3
"""
4D Systems Framework - Local Test Runner
Mac Studio Edition
Created by Khoury Howell

Run this after cloning the repository to verify everything works.
"""

import numpy as np
from typing import Dict, List, Any
from enum import Enum
from datetime import datetime

# =============================================================================
# CORE ENUMS
# =============================================================================

class ConsciousnessState(Enum):
    POTENTIAL = "non_existence"      # All possibilities
    EMERGING = "new_beginnings"      # Entering manifestation
    CHOOSING = "free_will"           # Decision point
    MANIFESTING = "creation"         # Active manifestation

class PathChoice(Enum):
    ALIGNMENT = "conscious_evolution"
    DIVERSION = "unconscious_pattern"
    INTEGRATION = "unified_awareness"

# =============================================================================
# NODES DEFINITION
# =============================================================================

NODES = {
    1: {"name": "Primary Motor Cortex (M1)", "aspect": "Will to Manifest"},
    2: {"name": "Premotor/SMA", "aspect": "Intent Formation"},
    3: {"name": "DLPFC", "aspect": "Free Will/Choice"},
    4: {"name": "Posterior Parietal", "aspect": "Dimensional Navigation"},
    5: {"name": "Broca's Area", "aspect": "Word as Creative Force"},
    6: {"name": "Insula", "aspect": "Feeling as Guidance"},
    7: {"name": "Temporal Association", "aspect": "Pattern Recognition"},
    8: {"name": "Wernicke's Area", "aspect": "Understanding Potential"},
    9: {"name": "Visual Cortex", "aspect": "Seeing Possibilities"},
    10: {"name": "Cerebellum", "aspect": "Harmonizing Manifestation"},
}

# =============================================================================
# SEQUENCES
# =============================================================================

SEQUENCES = {
    "standard": {
        "order": [1, 3, 2, 5, 4, 6, 8, 7, 9, 10],
        "name": "Standard Sequence",
        "amplification": 0.7,
        "description": "Unconscious, reactive processing (diversion path)"
    },
    "deep_understanding": {
        "order": [9, 7, 3, 6, 5, 8, 4, 2, 1, 10],
        "name": "Deep Understanding Sequence",
        "amplification": 1.5,
        "description": "Conscious, intentional processing (alignment path)"
    },
    "emotional_learning": {
        "order": [6, 3, 7, 5, 8, 9, 4, 2, 1, 10],
        "name": "Emotional Learning Sequence",
        "amplification": 2.0,
        "description": "Integrated, unified processing (integration path)"
    }
}

# =============================================================================
# CORE EQUATIONS
# =============================================================================

def calculate_node_development(time: float, alpha: float = 0.7, beta: float = 0.1, 
                                gamma: float = 0.8, delta: float = 0.05) -> float:
    """
    Node Development Function:
    D_node = α·e^(-βt) + γ·(1 - e^(-δt))
    
    Captures initial rapid learning and long-term optimization.
    """
    initial_learning = alpha * np.exp(-beta * time)
    long_term_optimization = gamma * (1 - np.exp(-delta * time))
    return initial_learning + long_term_optimization

def calculate_temporal_optimization(time: float, v_initial: float = 0.3, 
                                     v_max: float = 1.0, r: float = 0.05) -> float:
    """
    Temporal Optimization Function:
    T_i(t) = v_initial + (v_max - v_initial) / (1 + e^(-rt))
    
    Sigmoid function modeling expertise development.
    """
    return v_initial + (v_max - v_initial) / (1 + np.exp(-r * time))

def calculate_node_weight(node_id: int, task_type: str) -> float:
    """Calculate task-specific node importance."""
    weights = {
        'motor': {1: 0.9, 2: 0.85, 10: 0.9, 3: 0.3, 4: 0.3, 5: 0.2, 6: 0.2, 7: 0.3, 8: 0.2, 9: 0.4},
        'cognitive': {3: 0.9, 4: 0.85, 7: 0.8, 1: 0.3, 2: 0.4, 5: 0.3, 6: 0.4, 8: 0.3, 9: 0.5, 10: 0.3},
        'language': {5: 0.9, 8: 0.85, 7: 0.7, 1: 0.2, 2: 0.3, 3: 0.4, 4: 0.3, 6: 0.3, 9: 0.4, 10: 0.2},
        'emotional': {6: 0.9, 7: 0.85, 3: 0.7, 1: 0.2, 2: 0.2, 4: 0.3, 5: 0.3, 8: 0.3, 9: 0.3, 10: 0.2},
        'manifestation': {3: 0.9, 6: 0.85, 9: 0.8, 7: 0.75, 5: 0.7, 1: 0.6, 10: 0.6, 2: 0.5, 4: 0.5, 8: 0.5}
    }
    return weights.get(task_type, {i: 0.5 for i in range(1, 11)}).get(node_id, 0.5)

def calculate_M4D(sequence: List[int], task_type: str, time: float) -> float:
    """
    The 4D Systems Metric:
    M_4D = Σ(w_i × N_i × (S_i / S_max) × T_i) for i from 1 to 10
    
    Quantifies consciousness processing capability across all nodes.
    """
    M4D = 0.0
    S_max = 1.0  # Maximum sequence efficiency
    
    for position, node_id in enumerate(sequence):
        w_i = calculate_node_weight(node_id, task_type)
        N_i = calculate_node_development(time)
        S_i = 1.0 - (position / len(sequence)) * 0.3  # Position-based efficiency
        T_i = calculate_temporal_optimization(time)
        
        node_contribution = w_i * N_i * (S_i / S_max) * T_i
        M4D += node_contribution
    
    return M4D

# =============================================================================
# MANIFESTATION PROCESSOR
# =============================================================================

class ManifestationProcessor:
    """Core processor implementing the 4D Systems Framework."""
    
    def __init__(self):
        self.current_state = ConsciousnessState.POTENTIAL
        self.path_choice = None
        self.node_activations = {i: 0.0 for i in range(1, 11)}
        
    def process_intention(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an intention through the complete manifestation cycle:
        ALL POTENTIAL → CHOICE POINT → PATH SELECTION → PROCESSING → MANIFESTATION → NEW POTENTIAL
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "intention": intention,
            "stages": {}
        }
        
        # Stage 1: EXPOSURE - Activate potential field
        self.current_state = ConsciousnessState.EMERGING
        clarity = intention.get("clarity", 0.5)
        energy = intention.get("energy", 0.5)
        field_strength = clarity * energy
        results["stages"]["exposure"] = {"field_strength": field_strength}
        
        # Stage 2: CHOICE POINT - Determine path alignment
        self.current_state = ConsciousnessState.CHOOSING
        if field_strength > 0.7:
            self.path_choice = PathChoice.ALIGNMENT
            sequence_key = "deep_understanding"
        elif field_strength > 0.4:
            self.path_choice = PathChoice.INTEGRATION
            sequence_key = "emotional_learning"
        else:
            self.path_choice = PathChoice.DIVERSION
            sequence_key = "standard"
        
        sequence_config = SEQUENCES[sequence_key]
        results["stages"]["choice"] = {
            "path": self.path_choice.value,
            "sequence": sequence_config["name"],
            "amplification_factor": sequence_config["amplification"]
        }
        
        # Stage 3: PROCESSING - Run through node sequence
        self.current_state = ConsciousnessState.MANIFESTING
        task_type = intention.get("task_type", "manifestation")
        time = intention.get("experience_level", 10.0)
        
        M4D = calculate_M4D(sequence_config["order"], task_type, time)
        amplified_M4D = M4D * sequence_config["amplification"]
        
        # Track node activations
        for i, node_id in enumerate(sequence_config["order"]):
            self.node_activations[node_id] = calculate_node_development(time) * (1 - i * 0.05)
        
        results["stages"]["processing"] = {
            "sequence_order": sequence_config["order"],
            "raw_M4D": round(M4D, 4),
            "amplified_M4D": round(amplified_M4D, 4),
            "node_activations": {k: round(v, 4) for k, v in self.node_activations.items()}
        }
        
        # Stage 4: MANIFESTATION - Generate new potential
        expansion_factor = amplified_M4D * field_strength
        results["stages"]["manifestation"] = {
            "expansion_factor": round(expansion_factor, 4),
            "new_potential_created": expansion_factor > 1.0,
            "evolution_direction": "expansion" if expansion_factor > 1.0 else "contraction"
        }
        
        # Summary
        results["summary"] = {
            "path_chosen": self.path_choice.value,
            "final_M4D": round(amplified_M4D, 4),
            "manifestation_power": round(expansion_factor, 4),
            "cycle_complete": True
        }
        
        return results

# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demonstrate_sequence_comparison():
    """Show how different sequences produce different outcomes."""
    print("\n" + "="*70)
    print("SEQUENCE COMPARISON DEMONSTRATION")
    print("Identical information, different processing sequences")
    print("="*70)
    
    task_type = "cognitive"
    time = 10.0
    
    for seq_key, seq_config in SEQUENCES.items():
        M4D = calculate_M4D(seq_config["order"], task_type, time)
        amplified = M4D * seq_config["amplification"]
        
        print(f"\n{seq_config['name']}")
        print(f"  Path: {seq_config['order']}")
        print(f"  Amplification: {seq_config['amplification']}x")
        print(f"  Raw M_4D: {M4D:.4f}")
        print(f"  Amplified M_4D: {amplified:.4f}")
        print(f"  Description: {seq_config['description']}")

def demonstrate_node_development():
    """Show how nodes develop over time."""
    print("\n" + "="*70)
    print("NODE DEVELOPMENT OVER TIME")
    print("D_node = α·e^(-βt) + γ·(1 - e^(-δt))")
    print("="*70)
    
    time_points = [0, 1, 5, 10, 20, 50, 100]
    
    print(f"\n{'Time':>8} | {'Development':>12} | {'T_opt':>12}")
    print("-" * 40)
    
    for t in time_points:
        D = calculate_node_development(t)
        T = calculate_temporal_optimization(t)
        print(f"{t:>8} | {D:>12.4f} | {T:>12.4f}")

def run_full_manifestation_cycle():
    """Run a complete manifestation cycle with sample intention."""
    print("\n" + "="*70)
    print("FULL MANIFESTATION CYCLE")
    print("="*70)
    
    processor = ManifestationProcessor()
    
    intention = {
        "description": "Run 4D Systems Framework locally on Mac Studio",
        "clarity": 0.9,       # Clear vision of the goal
        "energy": 0.85,       # Strong motivation
        "task_type": "cognitive",
        "experience_level": 15.0
    }
    
    print(f"\nINTENTION: {intention['description']}")
    print(f"Clarity: {intention['clarity']}, Energy: {intention['energy']}")
    
    results = processor.process_intention(intention)
    
    print(f"\nPATH CHOSEN: {results['summary']['path_chosen']}")
    print(f"FINAL M_4D: {results['summary']['final_M4D']}")
    print(f"MANIFESTATION POWER: {results['summary']['manifestation_power']}")
    print(f"EVOLUTION: {results['stages']['manifestation']['evolution_direction'].upper()}")
    
    print("\nNode Activations:")
    for node_id, activation in results['stages']['processing']['node_activations'].items():
        node_info = NODES[node_id]
        bar = "█" * int(activation * 20)
        print(f"  {node_id:>2}. {node_info['name'][:25]:<25} {bar} {activation:.2f}")

def print_framework_summary():
    """Print the core framework summary."""
    print("\n" + "="*70)
    print("4D SYSTEMS FRAMEWORK - MAC STUDIO LOCAL INSTANCE")
    print("="*70)
    print("""
    "Here lies the evolution between beginnings and ends - 
     The cycle of to be, is, and has become."
                                        - Khoury H
    """)
    print("FOUR DIMENSIONS:")
    print("  1. Node Development      - Evolution of consciousness centers")
    print("  2. Sequence Arrangement  - Pathways of manifestation")
    print("  3. Root System Connections - Web of potentiality")
    print("  4. Temporal Optimization - Acceleration of evolution")
    print("\nCORE METRIC:")
    print("  M_4D = Σ(w_i × N_i × (S_i / S_max) × T_i)")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print_framework_summary()
    demonstrate_node_development()
    demonstrate_sequence_comparison()
    run_full_manifestation_cycle()
    
    print("\n" + "="*70)
    print("✓ 4D Systems Framework running successfully on Mac Studio!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Explore framework/4d_systems_framework_schema.json")
    print("  2. Run implementations/consciousness_4d_framework.py")
    print("  3. Review docs/pdf/ for theoretical foundations")
    print("\n\"This is now. This is time. This is the technology of becoming.\"")
