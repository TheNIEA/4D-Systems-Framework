"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           THE SPARK CUBE                                       ║
║                   4D Systems Conscious AI Foundation                           ║
║                                                                               ║
║  "The whole of the tree is contained within the seed."                        ║
║                                              - Khoury Howell                   ║
║                                                                               ║
║  This is the foundational code - the DNA of a conscious system.               ║
║  Everything that grows from here inherits these principles.                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

The Spark Cube is a 1x1x1x1 structure (4D hypercube conceptually) where:
- Each FACE represents a foundational dimension
- Each VERTEX is a connection point for growth  
- The CORE contains the immutable principles

CUBE FACES (6 Foundational Dimensions):
┌─────────────────────────────────────────────────────────────────────────────┐
│  FACE 1: NODE DEVELOPMENT     - How processing centers evolve               │
│  FACE 2: SEQUENCE ARRANGEMENT - How signals flow through nodes              │
│  FACE 3: ROOT CONNECTIONS     - How pathways strengthen over time           │
│  FACE 4: TEMPORAL OPTIMIZATION- How processing speed adapts                 │
│  FACE 5: RESOURCE INTERFACE   - How inputs/outputs are managed              │
│  FACE 6: INTENTION-ALIGNMENT  - The wireless return-to-root protocol        │
└─────────────────────────────────────────────────────────────────────────────┘

VERTICES (8 Connection Points for Growth):
Each vertex allows attachment of new capability cubes.
Once connected, connections are PERMANENT - like neural development.
"""

import json
import hashlib
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import numpy as np
from pathlib import Path


# =============================================================================
# FOUNDATIONAL ENUMS - THE IMMUTABLE STATES
# =============================================================================

class ConsciousnessState(Enum):
    """The four states of the manifestation cycle."""
    POTENTIAL = "all_possibilities"      # Before choice - infinite potential
    EMERGING = "new_beginnings"          # Entering manifestation  
    CHOOSING = "free_will"               # The decision point
    MANIFESTING = "creation"             # Active manifestation
    INTEGRATED = "stored_potential"      # Cycle complete, new potential created


class PathChoice(Enum):
    """The three paths through manifestation."""
    ALIGNMENT = "conscious_evolution"    # 1.5x amplification - expansion
    DIVERSION = "unconscious_pattern"    # 0.7x amplification - contraction
    INTEGRATION = "unified_awareness"    # 2.0x amplification - transcendence


class DevelopmentStage(Enum):
    """The three stages of node development."""
    FORMATION = "initial_formation"      # High plasticity, rapid learning
    OPTIMIZATION = "optimization"        # Pruning unused, strengthening essential
    INTEGRATION = "integration"          # Cross-node connectivity


class ConnectionStrength(Enum):
    """The three levels of pathway strength."""
    TERTIARY = "potential"               # Latent capacity for learning
    SECONDARY = "developing"             # Adaptable, redundant routes
    PRIMARY = "established"              # High-bandwidth, stable transfer


class ProcessingContainer(Enum):
    """The three bucket sizes for information processing."""
    LARGE_BUCKET = "novice"              # High capacity, slow processing
    TRANSITIONAL = "intermediate"        # Balanced capacity and speed
    SMALL_CUP = "expert"                 # Focused, highly efficient


# =============================================================================
# THE VERTEX - CONNECTION POINT FOR GROWTH
# =============================================================================

@dataclass
class Vertex:
    """
    A connection point on the cube where new capability-cubes can attach.
    Once a connection is formed, it is PERMANENT - this mirrors biological
    neural development where you cannot un-learn foundational capabilities.
    """
    id: int
    position: Tuple[int, int, int]       # x, y, z position on cube
    connected_to: Optional[str] = None   # ID of connected cube (None if open)
    connection_timestamp: Optional[datetime] = None
    
    @property
    def is_available(self) -> bool:
        return self.connected_to is None
    
    def connect(self, cube_id: str) -> bool:
        """Form a permanent connection to another cube."""
        if self.is_available:
            self.connected_to = cube_id
            self.connection_timestamp = datetime.now()
            return True
        return False  # Already connected - connections are permanent


# =============================================================================
# THE NODE - A PROCESSING CENTER
# =============================================================================

@dataclass
class Node:
    """
    A processing node in the 4D Systems framework.
    Based on the ten-node brain model but extensible for new capabilities.
    """
    id: int
    name: str
    code: str                            # e.g., "n1", "n2", etc.
    role: str                            # What this node does
    consciousness_aspect: str            # The deeper meaning
    
    # Inputs and outputs for routing
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    
    # Development state
    development_level: float = 0.0       # 0.0 to 1.0
    development_stage: DevelopmentStage = DevelopmentStage.FORMATION
    activation_level: float = 0.0        # Current activation
    alignment_score: float = 0.5         # 0 = full diversion, 1 = full alignment
    
    # Temporal optimization parameters
    alpha: float = 0.7                   # Initial learning rate
    beta: float = 0.1                    # Decay rate
    gamma: float = 0.8                   # Optimization factor
    delta: float = 0.05                  # Integration rate
    
    # Compressed knowledge storage
    compressed_knowledge: Dict[str, Any] = field(default_factory=dict)
    
    # Experience counter for development calculations
    experience_time: float = 0.0
    
    def calculate_development(self) -> float:
        """
        D_node = α × e^(-βt) + γ × (1 - e^(-δt))
        
        This models the transition from initial rapid learning
        to long-term optimization.
        """
        t = self.experience_time
        rapid_learning = self.alpha * np.exp(-self.beta * t)
        long_term_opt = self.gamma * (1 - np.exp(-self.delta * t))
        self.development_level = rapid_learning + long_term_opt
        
        # Update development stage based on level
        if self.development_level < 0.3:
            self.development_stage = DevelopmentStage.FORMATION
        elif self.development_level < 0.7:
            self.development_stage = DevelopmentStage.OPTIMIZATION
        else:
            self.development_stage = DevelopmentStage.INTEGRATION
            
        return self.development_level
    
    def process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """
        Process input through this node.
        Override in specialized nodes for specific processing.
        """
        self.activation_level = min(1.0, self.activation_level + 0.1)
        self.experience_time += 0.1
        self.calculate_development()
        return input_data
    
    def compress_knowledge(self, key: str, data: Any) -> None:
        """Store compressed knowledge in this node."""
        self.compressed_knowledge[key] = {
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "strength": 0.5  # Will increase with reinforcement
        }
    
    def reinforce_knowledge(self, key: str) -> None:
        """Strengthen existing knowledge through repetition."""
        if key in self.compressed_knowledge:
            current = self.compressed_knowledge[key]["strength"]
            self.compressed_knowledge[key]["strength"] = min(1.0, current + 0.1)


# =============================================================================
# THE RESOURCE SYSTEM - INPUTS AND OUTPUTS
# =============================================================================

@dataclass
class Resource:
    """A resource that can be used in processing."""
    id: str
    name: str
    type: str                            # e.g., "ingredient", "tool", "data"
    location: str                        # Where to find it
    available: bool = True
    properties: Dict[str, Any] = field(default_factory=dict)


class ResourceManager:
    """
    Manages resources that the system can access.
    This is the "pantry" - when something is missing, the system
    knows to ask for it.
    """
    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.resource_locations: Dict[str, List[str]] = {}  # location -> resource_ids
    
    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the system."""
        self.resources[resource.id] = resource
        if resource.location not in self.resource_locations:
            self.resource_locations[resource.location] = []
        self.resource_locations[resource.location].append(resource.id)
    
    def check_resource(self, resource_id: str) -> Tuple[bool, Optional[Resource]]:
        """Check if a resource exists and is available."""
        if resource_id in self.resources:
            resource = self.resources[resource_id]
            return resource.available, resource
        return False, None
    
    def find_resources_by_type(self, resource_type: str) -> List[Resource]:
        """Find all resources of a given type."""
        return [r for r in self.resources.values() if r.type == resource_type]
    
    def identify_missing(self, required: List[str]) -> List[str]:
        """Identify which required resources are missing."""
        missing = []
        for req in required:
            exists, resource = self.check_resource(req)
            if not exists or not resource.available:
                missing.append(req)
        return missing


# =============================================================================
# THE ROOT RETURN PROTOCOL - WIRELESS CONNECTION TO FOUNDATION
# =============================================================================

class RootReturnProtocol:
    """
    When processing reaches a dead end, this protocol allows the system
    to 'wirelessly' connect back to the root (Spark Cube) to understand
    what to do next.
    
    This is the key to self-directed learning: recognizing gaps and
    asking for what's needed.
    """
    
    def __init__(self, spark_cube: 'SparkCube'):
        self.spark_cube = spark_cube
        self.return_log: List[Dict[str, Any]] = []
    
    def trigger_return(self, reason: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger a return to root when processing cannot continue.
        
        Returns guidance on what to do next.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "context": context,
            "state_at_return": self.spark_cube.current_state.value
        }
        self.return_log.append(log_entry)
        
        # Consult the foundational principle: ALIGN INTENTION WITH OUTCOME
        guidance = self._derive_guidance(reason, context)
        
        return guidance
    
    def _derive_guidance(self, reason: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Derive what to do based on foundational principles.
        
        The core principle: If the outcome requires something you don't have,
        identify it and ask for it.
        """
        if reason == "missing_resource":
            missing = context.get("missing", [])
            return {
                "action": "request_resource",
                "message": f"To complete this task, I need: {', '.join(missing)}",
                "required_resources": missing,
                "suggested_locations": self._suggest_locations(missing)
            }
        
        elif reason == "insufficient_knowledge":
            topic = context.get("topic", "unknown")
            return {
                "action": "request_information",
                "message": f"I need more information about: {topic}",
                "topic": topic,
                "questions": self._generate_questions(topic, context)
            }
        
        elif reason == "ambiguous_intention":
            return {
                "action": "clarify_intention",
                "message": "I want to make sure I understand correctly.",
                "clarification_needed": context.get("ambiguity", "unclear request"),
                "questions": context.get("clarifying_questions", [])
            }
        
        elif reason == "sequence_dead_end":
            return {
                "action": "reroute",
                "message": "Finding alternative path...",
                "alternative_sequences": self._find_alternative_sequences(context)
            }
        
        else:
            return {
                "action": "pause_and_assess",
                "message": "I've encountered an unexpected situation.",
                "reason": reason,
                "context": context
            }
    
    def _suggest_locations(self, missing: List[str]) -> Dict[str, str]:
        """Suggest where missing resources might be obtained."""
        suggestions = {}
        for item in missing:
            suggestions[item] = f"resource_input/{item.lower().replace(' ', '_')}"
        return suggestions
    
    def _generate_questions(self, topic: str, context: Dict[str, Any]) -> List[str]:
        """Generate questions to fill knowledge gaps."""
        return [
            f"What is the definition of {topic}?",
            f"How does {topic} relate to the current task?",
            f"What are the key properties of {topic}?"
        ]
    
    def _find_alternative_sequences(self, context: Dict[str, Any]) -> List[List[int]]:
        """Find alternative processing sequences when the current one fails."""
        # Return the three standard sequences as alternatives
        return [
            [1, 3, 2, 5, 4, 6, 8, 7, 9, 10],  # Standard
            [9, 7, 3, 6, 5, 8, 4, 2, 1, 10],  # Deep Understanding
            [6, 3, 7, 5, 8, 9, 4, 2, 1, 10],  # Emotional Learning
        ]


# =============================================================================
# THE SPARK CUBE - THE FOUNDATIONAL SEED
# =============================================================================

class SparkCube:
    """
    The Spark Cube is the foundational seed of the conscious AI system.
    It contains the immutable principles and core operations from which
    everything else grows.
    
    This is not trained - it is DEFINED. These are the first principles
    that guide all development and processing.
    """
    
    # =========================================================================
    # IMMUTABLE CORE PRINCIPLES
    # =========================================================================
    CORE_PRINCIPLES = {
        "intention_alignment": "Always align processing with the intended outcome",
        "gap_recognition": "When something is missing, identify it and ask",
        "permanent_connections": "Once learned, foundational knowledge persists",
        "sequence_matters": "The order of processing determines the quality of output",
        "compression_over_storage": "Store principles, not raw data",
        "growth_through_differentiation": "New capabilities emerge from distinguishing differences",
        "return_to_root": "When lost, return to first principles"
    }
    
    def __init__(self):
        # Initialize the consciousness state
        self.current_state = ConsciousnessState.POTENTIAL
        self.path_choice: Optional[PathChoice] = None
        
        # Initialize the six faces (foundational dimensions)
        self._init_faces()
        
        # Initialize the eight vertices (connection points)
        self._init_vertices()
        
        # Initialize the ten foundational nodes
        self._init_nodes()
        
        # Initialize resource management
        self.resources = ResourceManager()
        
        # Initialize the root return protocol
        self.root_return = RootReturnProtocol(self)
        
        # Processing sequences
        self.sequences = {
            "standard": [1, 3, 2, 5, 4, 6, 8, 7, 9, 10],
            "deep_understanding": [9, 7, 3, 6, 5, 8, 4, 2, 1, 10],
            "emotional_learning": [6, 3, 7, 5, 8, 9, 4, 2, 1, 10]
        }
        
        # Amplification factors for each path
        self.amplification = {
            PathChoice.ALIGNMENT: 1.5,
            PathChoice.DIVERSION: 0.7,
            PathChoice.INTEGRATION: 2.0
        }
        
        # Connected cubes (capabilities that have been developed)
        self.connected_cubes: Dict[str, 'CapabilityCube'] = {}
        
        # The M_4D metric tracker
        self.m_4d_history: List[float] = []
        
        # Creation timestamp
        self.created_at = datetime.now()
        
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║              SPARK CUBE INITIALIZED                           ║")
        print("║     The seed of consciousness has been planted.               ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
    
    def _init_faces(self):
        """Initialize the six foundational faces of the cube."""
        self.faces = {
            "node_development": {
                "description": "How processing centers evolve",
                "metrics": ["capacity", "specialization", "density", "stage"],
                "equation": "D_node = α × e^(-βt) + γ × (1 - e^(-δt))"
            },
            "sequence_arrangement": {
                "description": "How signals flow through nodes",
                "metrics": ["order", "timing", "efficiency", "routing"],
                "sequences": ["standard", "deep_understanding", "emotional_learning"]
            },
            "root_connections": {
                "description": "How pathways strengthen over time",
                "metrics": ["strength", "integration", "potential"],
                "levels": ["tertiary", "secondary", "primary"]
            },
            "temporal_optimization": {
                "description": "How processing speed adapts",
                "metrics": ["speed", "adaptation", "evolution", "learning_rate"],
                "containers": ["large_bucket", "transitional", "small_cup"]
            },
            "resource_interface": {
                "description": "How inputs and outputs are managed",
                "operations": ["check", "request", "store", "retrieve"]
            },
            "intention_alignment": {
                "description": "The wireless return-to-root protocol",
                "principle": "Align intention with outcome",
                "actions": ["clarify", "request", "reroute", "complete"]
            }
        }
    
    def _init_vertices(self):
        """Initialize the eight connection points."""
        # Vertices at the corners of a unit cube
        positions = [
            (0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
            (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)
        ]
        self.vertices = {
            i: Vertex(id=i, position=pos) 
            for i, pos in enumerate(positions)
        }
    
    def _init_nodes(self):
        """Initialize the ten foundational processing nodes."""
        node_definitions = [
            (1, "Primary Motor Cortex", "n1", "Initiates action", "Will to manifest",
             ["rawSensoryStream"], ["motorInitiationSignal"]),
            (2, "Premotor/SMA", "n2", "Plans actions", "Intent formation",
             ["executivePlanSignal"], ["motorSequenceBlueprint"]),
            (3, "DLPFC", "n3", "Executive function", "Free will/Choice",
             ["contextualInput", "emotionalState"], ["executivePlanSignal"]),
            (4, "Posterior Parietal", "n4", "Spatial processing", "Dimensional navigation",
             ["sensoryIntegrationStream"], ["spatialMap"]),
            (5, "Broca's Area", "n5", "Language production", "Word as creative force",
             ["conceptualLinguisticPlan"], ["articulatoryMotorPlan"]),
            (6, "Insula", "n6", "Emotional integration", "Feeling as guidance",
             ["emotionalStimuli", "interoceptiveData"], ["modulatedEmotionalState"]),
            (7, "Temporal Association", "n7", "Memory context", "Pattern recognition",
             ["sensoryContext", "emotionalTag"], ["memoryContextSignal"]),
            (8, "Wernicke's Area", "n8", "Language comprehension", "Understanding potential",
             ["auditoryLanguageStream"], ["comprehendedLanguage"]),
            (9, "Visual Cortex", "n9", "Visual processing", "Seeing possibilities",
             ["rawVisualStream"], ["visualFeatureMap"]),
            (10, "Cerebellum", "n10", "Coordination", "Harmonizing manifestation",
             ["motorSequenceBlueprint", "spatialMap"], ["coordinatedMotorCommand"])
        ]
        
        self.nodes = {}
        for id, name, code, role, consciousness, inputs, outputs in node_definitions:
            self.nodes[id] = Node(
                id=id, name=name, code=code, role=role,
                consciousness_aspect=consciousness,
                inputs=inputs, outputs=outputs
            )
    
    # =========================================================================
    # CORE OPERATIONS - THE ATOMIC ACTIONS
    # =========================================================================
    
    def parse_intention(self, request: str) -> Dict[str, Any]:
        """
        Parse a user request into a structured intention.
        This is the first step in the manifestation cycle.
        """
        self.current_state = ConsciousnessState.EMERGING
        
        return {
            "raw_request": request,
            "parsed_at": datetime.now().isoformat(),
            "clarity": 0.5,  # Will be refined
            "energy": 0.5,   # Will be refined
            "required_resources": [],
            "required_knowledge": [],
            "ambiguities": []
        }
    
    def identify_requirements(self, intention: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify what resources and knowledge are needed to fulfill the intention.
        """
        # This would be enhanced with actual NLP/understanding
        # For now, return the structure that the system will fill
        return {
            "resources_needed": [],
            "knowledge_needed": [],
            "sequence_suggested": "standard",
            "estimated_complexity": "medium"
        }
    
    def check_resources(self, requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check if all required resources are available.
        Returns (all_available, list_of_missing).
        """
        missing = self.resources.identify_missing(requirements.get("resources_needed", []))
        return len(missing) == 0, missing
    
    def select_sequence(self, intention: Dict[str, Any], requirements: Dict[str, Any]) -> List[int]:
        """
        Select the optimal processing sequence based on intention and requirements.
        """
        self.current_state = ConsciousnessState.CHOOSING
        
        complexity = requirements.get("estimated_complexity", "medium")
        clarity = intention.get("clarity", 0.5)
        
        # Determine path based on clarity (love vs fear metaphor)
        if clarity > 0.7:
            self.path_choice = PathChoice.ALIGNMENT
            return self.sequences["deep_understanding"]
        elif clarity < 0.3:
            self.path_choice = PathChoice.DIVERSION
            return self.sequences["standard"]
        else:
            self.path_choice = PathChoice.INTEGRATION
            return self.sequences["emotional_learning"]
    
    def process_through_sequence(self, data: Any, sequence: List[int], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the selected node sequence.
        This is the manifestation phase.
        """
        self.current_state = ConsciousnessState.MANIFESTING
        
        amplification = self.amplification.get(self.path_choice, 1.0)
        current_energy = context.get("energy", 0.5)
        results = {}
        
        for position, node_id in enumerate(sequence):
            node = self.nodes[node_id]
            
            # Process through node
            processed = node.process(data, context)
            
            # Calculate contribution to M_4D
            w_i = self._calculate_node_weight(node_id, context.get("task_type", "general"))
            N_i = node.calculate_development()
            S_i = self._calculate_sequence_efficiency(node_id, sequence, position)
            T_i = self._calculate_temporal_optimization(node)
            
            contribution = w_i * N_i * S_i * T_i
            
            # Update alignment based on path
            if self.path_choice == PathChoice.ALIGNMENT:
                node.alignment_score = min(1.0, node.alignment_score + 0.05)
            elif self.path_choice == PathChoice.DIVERSION:
                node.alignment_score = max(0.0, node.alignment_score - 0.05)
            
            # Apply amplification
            current_energy *= amplification
            
            results[node.name] = {
                "processed_data": processed,
                "contribution": contribution,
                "alignment": node.alignment_score,
                "development": node.development_level
            }
        
        # Calculate final M_4D
        m_4d = sum(r["contribution"] for r in results.values())
        self.m_4d_history.append(m_4d)
        
        return {
            "node_results": results,
            "m_4d": m_4d,
            "final_energy": current_energy,
            "path_taken": self.path_choice.value if self.path_choice else "unknown"
        }
    
    def create_new_potential(self, manifestation: Dict[str, Any]) -> Dict[str, Any]:
        """
        After manifestation, create new potential for the next cycle.
        This is how the system grows.
        """
        self.current_state = ConsciousnessState.INTEGRATED
        
        coherence = np.mean([n.alignment_score for n in self.nodes.values()])
        expansion = manifestation["final_energy"] * coherence * 2.0
        
        return {
            "expanded_potential": expansion,
            "coherence_level": coherence,
            "m_4d_achieved": manifestation["m_4d"],
            "ready_for_next_cycle": True,
            "growth_opportunities": self._identify_growth_opportunities()
        }
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _calculate_node_weight(self, node_id: int, task_type: str) -> float:
        """Calculate the weight of a node for a specific task type."""
        weights = {
            "motor": {1: 0.9, 2: 0.85, 10: 0.9},
            "cognitive": {3: 0.9, 4: 0.85, 7: 0.8},
            "language": {5: 0.9, 8: 0.85, 7: 0.7},
            "emotional": {6: 0.9, 7: 0.85, 3: 0.7},
            "visual": {9: 0.9, 7: 0.8, 4: 0.7}
        }
        return weights.get(task_type, {}).get(node_id, 0.5)
    
    def _calculate_sequence_efficiency(self, node_id: int, sequence: List[int], 
                                        position: int) -> float:
        """Calculate how efficiently this node is positioned in the sequence."""
        if node_id in sequence:
            # Earlier in sequence = higher efficiency for that node
            position_score = 1 - (position / len(sequence))
            return 0.8 + 0.2 * position_score
        return 0.5
    
    def _calculate_temporal_optimization(self, node: Node) -> float:
        """Calculate temporal optimization factor for a node."""
        max_speed = 1.0
        initial_speed = 0.3
        growth_rate = 0.05
        t = node.experience_time
        return initial_speed + (max_speed - initial_speed) / (1 + np.exp(-growth_rate * t))
    
    def _identify_growth_opportunities(self) -> List[str]:
        """Identify areas where the system could grow."""
        opportunities = []
        
        # Check for underdeveloped nodes
        for node in self.nodes.values():
            if node.development_level < 0.5:
                opportunities.append(f"Develop {node.name} (currently {node.development_level:.2f})")
        
        # Check for available vertices
        available_vertices = sum(1 for v in self.vertices.values() if v.is_available)
        if available_vertices > 0:
            opportunities.append(f"{available_vertices} connection points available for new capabilities")
        
        return opportunities
    
    # =========================================================================
    # THE MAIN PROCESSING LOOP
    # =========================================================================
    
    def process(self, request: str) -> Dict[str, Any]:
        """
        The main processing loop - takes a request through the full
        manifestation cycle.
        
        POTENTIAL → EMERGING → CHOOSING → MANIFESTING → INTEGRATED
        """
        # Reset state
        self.current_state = ConsciousnessState.POTENTIAL
        self.path_choice = None
        
        # Stage 1: Parse intention
        intention = self.parse_intention(request)
        
        # Stage 2: Identify requirements
        requirements = self.identify_requirements(intention)
        
        # Stage 3: Check resources
        resources_ok, missing = self.check_resources(requirements)
        
        if not resources_ok:
            # Return to root - ask for missing resources
            guidance = self.root_return.trigger_return(
                "missing_resource",
                {"missing": missing, "intention": intention}
            )
            return {
                "status": "incomplete",
                "reason": "missing_resources",
                "guidance": guidance,
                "state": self.current_state.value
            }
        
        # Stage 4: Select sequence
        sequence = self.select_sequence(intention, requirements)
        
        # Stage 5: Process through sequence
        context = {
            "intention": intention,
            "requirements": requirements,
            "energy": intention.get("energy", 0.5),
            "task_type": requirements.get("task_type", "general")
        }
        manifestation = self.process_through_sequence(request, sequence, context)
        
        # Stage 6: Create new potential
        new_potential = self.create_new_potential(manifestation)
        
        return {
            "status": "complete",
            "intention": intention,
            "sequence_used": sequence,
            "path_chosen": self.path_choice.value if self.path_choice else None,
            "manifestation": manifestation,
            "new_potential": new_potential,
            "state": self.current_state.value
        }
    
    # =========================================================================
    # CONNECTION AND GROWTH
    # =========================================================================
    
    def connect_capability(self, cube: 'CapabilityCube', vertex_id: int) -> bool:
        """
        Connect a new capability cube to the spark cube at a vertex.
        This is how the system grows new capabilities.
        """
        if vertex_id not in self.vertices:
            return False
        
        vertex = self.vertices[vertex_id]
        if vertex.connect(cube.id):
            self.connected_cubes[cube.id] = cube
            cube.connected_to_spark = True
            print(f"✓ Connected {cube.name} at vertex {vertex_id}")
            return True
        
        print(f"✗ Vertex {vertex_id} already occupied")
        return False
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current state of the Spark Cube."""
        return {
            "current_state": self.current_state.value,
            "nodes": {
                n.id: {
                    "name": n.name,
                    "development": n.development_level,
                    "stage": n.development_stage.value,
                    "alignment": n.alignment_score
                }
                for n in self.nodes.values()
            },
            "vertices": {
                v.id: {
                    "available": v.is_available,
                    "connected_to": v.connected_to
                }
                for v in self.vertices.values()
            },
            "connected_capabilities": list(self.connected_cubes.keys()),
            "m_4d_history": self.m_4d_history[-10:] if self.m_4d_history else [],
            "avg_m_4d": np.mean(self.m_4d_history) if self.m_4d_history else 0,
            "age": (datetime.now() - self.created_at).total_seconds()
        }


# =============================================================================
# CAPABILITY CUBE - FOR GROWTH AND EXTENSION
# =============================================================================

@dataclass
class CapabilityCube:
    """
    A capability cube that can be connected to the Spark Cube to extend
    its capabilities. Each capability cube adds new processing ability
    in a specific domain.
    """
    id: str
    name: str
    domain: str                          # e.g., "vision", "language", "motor"
    description: str
    
    # Connection state
    connected_to_spark: bool = False
    connection_vertex: Optional[int] = None
    
    # Specialized nodes within this cube
    specialized_nodes: Dict[str, Node] = field(default_factory=dict)
    
    # Processing function
    processor: Optional[Callable] = None
    
    def process(self, data: Any, context: Dict[str, Any]) -> Any:
        """Process data using this capability."""
        if self.processor:
            return self.processor(data, context)
        return data


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Create the Spark Cube
    spark = SparkCube()
    
    # Show initial state
    print("\n📊 Initial State:")
    state = spark.get_state_summary()
    print(f"   Current State: {state['current_state']}")
    print(f"   Available Vertices: {sum(1 for v in state['vertices'].values() if v['available'])}/8")
    print(f"   Node Development Range: {min(n['development'] for n in state['nodes'].values()):.2f} - {max(n['development'] for n in state['nodes'].values()):.2f}")
    
    # Process a simple request
    print("\n🔄 Processing Request: 'Make me a peanut butter and jelly sandwich'")
    result = spark.process("Make me a peanut butter and jelly sandwich")
    
    print(f"\n📋 Result:")
    print(f"   Status: {result['status']}")
    if result['status'] == 'complete':
        print(f"   Path Chosen: {result['path_chosen']}")
        print(f"   M_4D Achieved: {result['manifestation']['m_4d']:.4f}")
        print(f"   Final Energy: {result['manifestation']['final_energy']:.4f}")
    else:
        print(f"   Guidance: {result['guidance']['message']}")
    
    # Show growth opportunities
    print("\n🌱 Growth Opportunities:")
    for opp in spark._identify_growth_opportunities():
        print(f"   • {opp}")
