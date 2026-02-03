import time
import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

# --- Core Definitions ---

@dataclass
class RootEntity:
    """
    Represents a verified concept in the 4D Root System.
    Unlike a standard token, a RootEntity has 'Mass' (Significance) 
    and 'TemporalPosition' (When it became true).
    """
    id: str
    name: str
    creation_timestamp: float  # Unix timestamp
    strength: float = 1.0      # 0.0 to 1.0 (How established is this fact?)
    decay_rate: float = 0.01   # How fast this truth becomes irrelevant

class StructuralResistanceError(Exception):
    """
    The 'Spark'. 
    Raised when the system encounters too much friction to proceed safely.
    This prevents hallucination by stopping the flow.
    """
    def __init__(self, message, friction_level, node_id):
        self.friction_level = friction_level
        self.node_id = node_id
        super().__init__(f"[RESISTANCE {friction_level:.2f}] {message}")

class RootNode:
    """
    The Physics Engine of the 4D Framework.
    
    Role:
    1. Check if a concept exists in the Root System.
    2. Calculate 'Friction' (Energy cost to process this concept).
    3. Enforce the 'Truth Constraint' (Stop vs. Flow).
    """
    
    def __init__(self, tolerance_threshold: float = 0.7):
        # In a real system, this would connect to a Vector Database or Knowledge Graph.
        # Here, we mock the 'Universal Record'.
        self.root_registry: Dict[str, RootEntity] = {}
        self.tolerance_threshold = tolerance_threshold # Maximum allowed friction before 'Spark'

        # Seed with some 'Truths' for the simulation
        self._seed_reality()

    def _seed_reality(self):
        """Populate the system with established facts (Roots)."""
        current_time = time.time()
        
        # Establishing a root for 'Mars' (The Planet)
        self.root_registry["mars_planet"] = RootEntity(
            id="mars_001", 
            name="Mars", 
            creation_timestamp=current_time - 1000000, 
            strength=0.99 # Hard fact
        )
        
        # Establishing a root for 'SpaceX' (The Company)
        self.root_registry["spacex"] = RootEntity(
            id="spx_001", 
            name="SpaceX", 
            creation_timestamp=current_time - 50000, 
            strength=0.90
        )

        # NOTE: 'Treaty of Mars 2029' is intentionally MISSING.

    def _calculate_temporal_stability(self, root: RootEntity) -> float:
        """
        Calculates how 'stable' a root is based on time.
        Older roots (Gravity, Math) are more stable than new ones (News).
        """
        age = time.time() - root.creation_timestamp
        # Simple logistic function for stability: older = stronger
        stability = 1.0 / (1.0 + math.exp(-0.001 * age)) 
        return stability * root.strength

    def calculate_friction(self, concept_key: str) -> float:
        """
        The Core Equation:
        Friction = 1.0 - (RootStability)
        
        Returns:
            0.0 = Superconductivity (Perfect Truth / Flow)
            1.0 = Infinite Resistance (Total Fabrication)
        """
        root = self.root_registry.get(concept_key)
        
        if not root:
            # Concept does not exist in Root System.
            # In standard AI, this would be a "guess". 
            # In 4D, this is Maximum Friction.
            return 1.0
        
        stability = self._calculate_temporal_stability(root)
        friction = 1.0 - stability
        return max(0.0, friction)

    def process_impulse(self, input_concept: str):
        """
        Simulates the flow of a thought through the Root Node.
        """
        print(f"[*] Processing Impulse: '{input_concept}'")
        
        # 1. Normalize input (Mocking NLP extraction)
        key = input_concept.lower().replace(" ", "_")
        
        # 2. Calculate Physics
        friction = self.calculate_friction(key)
        print(f"    -> Semantic Friction Coefficient: {friction:.4f}")

        # 3. Check against Threshold (The 'Spark' Logic)
        if friction > self.tolerance_threshold:
            # TRIGGER THE SPARK
            raise StructuralResistanceError(
                message=f"Root connection failed for '{input_concept}'. No path to ground.",
                friction_level=friction,
                node_id="ROOT_DIM_3"
            )
            
        # 4. Success - Superconductivity
        print(f"    -> [FLOW STATE] Impulse grounded. Energy cost: {friction * 10} J\n")
        return True

# --- SIMULATION EXECUTION ---

def run_simulation():
    system = RootNode(tolerance_threshold=0.6)
    
    print("--- 4D SYSTEM INITIALIZED: ROOT LAYER ACTIVE ---\n")

    # Test Case 1: Valid Reality
    try:
        system.process_impulse("Mars Planet")
    except StructuralResistanceError as e:
        print(f"    [!] SPARK DETECTED: {e}")

    # Test Case 2: The Hallucination Attempt
    try:
        system.process_impulse("Treaty of Mars 2029")
    except StructuralResistanceError as e:
        print(f"    [!] SPARK DETECTED: {e}")
        print("    [!] SYSTEM HALT: Energy preservation protocol active.")

if __name__ == "__main__":
    run_simulation()
