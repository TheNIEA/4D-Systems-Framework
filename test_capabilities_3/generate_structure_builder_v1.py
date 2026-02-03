import random
import json
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class PathwayType(Enum):
    SEQUENTIAL = "sequential"
    BRANCHING = "branching"
    PARALLEL = "parallel"
    CYCLICAL = "cyclical"

@dataclass
class CreativeNode:
    id: str
    content: str
    triggers: List[str]
    weight: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class GenerativeStructureBuilder:
    """
    Build strong pathways for generating creative responses through structured
    node networks and pathway management.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the structure builder.
        
        Args:
            seed: Random seed for reproducible generation
        """
        self.nodes: Dict[str, CreativeNode] = {}
        self.pathways: Dict[str, List[str]] = {}
        self.triggers: Dict[str, List[str]] = {}
        self.generators: Dict[str, Callable] = {}
        self._rng = random.Random(seed)
        self._initialize_default_generators()
    
    def _initialize_default_generators(self) -> None:
        """Initialize default content generators."""
        self.generators.update({
            'concept': lambda: f"concept_{self._rng.randint(1000, 9999)}",
            'action': lambda: f"action_{self._rng.randint(1000, 9999)}",
            'descriptor': lambda: f"desc_{self._rng.randint(1000, 9999)}"
        })
    
    def add_node(self, node_id: str, content: str, triggers: List[str], 
                 weight: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a creative node to the structure.
        
        Args:
            node_id: Unique identifier for the node
            content: Content or template for the node
            triggers: List of trigger keywords
            weight: Weight for pathway selection (higher = more likely)
            metadata: Additional node metadata
            
        Returns:
            bool: Success status
        """
        try:
            if node_id in self.nodes:
                raise ValueError(f"Node {node_id} already exists")
            
            node = CreativeNode(node_id, content, triggers, weight, metadata or {})
            self.nodes[node_id] = node
            
            # Update trigger index
            for trigger in triggers:
                if trigger not in self.triggers:
                    self.triggers[trigger] = []
                self.triggers[trigger].append(node_id)
            
            return True
            
        except Exception as e:
            print(f"Error adding node {node_id}: {e}")
            return False
    
    def create_pathway(self, pathway_id: str, node_sequence: List[str], 
                      pathway_type: PathwayType = PathwayType.SEQUENTIAL) -> bool:
        """
        Create a pathway connecting nodes.
        
        Args:
            pathway_id: Unique pathway identifier
            node_sequence: List of node IDs in pathway
            pathway_type: Type of pathway structure
            
        Returns:
            bool: Success status
        """
        try:
            # Validate nodes exist
            for node_id in node_sequence:
                if node_id not in self.nodes:
                    raise ValueError(f"Node {node_id} does not exist")
            
            if len(node_sequence) < 2:
                raise ValueError("Pathway must contain at least 2 nodes")
            
            self.pathways[pathway_id] = {
                'nodes': node_sequence,
                'type': pathway_type,
                'created_at': self._rng.random()  # Simple timestamp substitute
            }
            
            return True
            
        except Exception as e:
            print(f"Error creating pathway {pathway_id}: {e}")
            return False
    
    def find_pathways_by_trigger(self, trigger: str, max_results: int = 5) -> List[str]:
        """
        Find pathways that contain nodes matching the trigger.
        
        Args:
            trigger: Trigger keyword to search for
            max_results: Maximum number of pathways to return
            
        Returns:
            List of pathway IDs
        """
        try:
            matching_nodes = self.triggers.get(trigger, [])
            if not matching_nodes:
                return []
            
            matching_pathways = []
            for pathway_id, pathway_data in self.pathways.items():
                if any(node_id in matching_nodes for node_id in pathway_data['nodes']):
                    matching_pathways.append(pathway_id)
            
            return matching_pathways[:max_results]
            
        except Exception as e:
            print(f"Error finding pathways for trigger {trigger}: {e}")
            return []
    
    def generate_response(self, triggers: List[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate creative response using pathways and triggers.
        
        Args:
            triggers: List of trigger keywords
            context: Additional context for generation
            
        Returns:
            Generated response data
        """
        try:
            context = context or {}
            response = {
                'content': [],
                'pathway_used': None,
                'nodes_activated': [],
                'confidence': 0.0
            }
            
            # Find best pathway
            pathway_candidates = []
            for trigger in triggers:
                pathway_candidates.extend(self.find_pathways_by_trigger(trigger))
            
            if not pathway_candidates:
                # Generate fallback response
                response['content'] = [self._generate_fallback_content(triggers)]
                response['confidence'] = 0.3
                return response
            
            # Select pathway by frequency and randomness
            pathway_id = self._select_best_pathway(pathway_candidates)
            pathway_data = self.pathways[pathway_id]
            
            # Generate content along pathway
            for node_id in pathway_data['nodes']:
                node = self.nodes[node_id]
                if any(trigger in node.triggers for trigger in triggers):
                    generated_content = self._generate_node_content(node, context)
                    response['content'].append(generated_content)
                    response['nodes_activated'].append(node_id)
            
            response['pathway_used'] = pathway_id
            response['confidence'] = min(len(response['nodes_activated']) / len(pathway_data['nodes']), 1.0)
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {'content': [], 'error': str(e), 'confidence': 0.0}
    
    def _select_best_pathway(self, candidates: List[str]) -> str:
        """Select best pathway from candidates using weighted selection."""
        try:
            if len(candidates) == 1:
                return candidates[0]
            
            # Weight by frequency and pathway strength
            pathway_weights = {}
            for pathway_id in set(candidates):
                frequency = candidates.count(pathway_id)
                pathway_nodes = self.pathways[pathway_id]['nodes']
                avg_weight = sum(self.nodes[node_id].weight for node_id in pathway_nodes) / len(pathway_nodes)
                pathway_weights[pathway_id] = frequency * avg_weight
            
            # Weighted random selection
            total_weight = sum(pathway_weights.values())
            if total_weight == 0:
                return self._rng.choice(list(pathway_weights.keys()))
            
            rand_val = self._rng.uniform(0, total_weight)
            cumulative = 0
            
            for pathway_id, weight in pathway_weights.items():
                cumulative += weight
                if rand_val <= cumulative:
                    return pathway_id
            
            return list(pathway_weights.keys())[-1]
            
        except Exception:
            return self._rng.choice(candidates)
    
    def _generate_node_content(self, node: CreativeNode, context: Dict[str, Any]) -> str:
        """Generate content for a specific node."""
        try:
            content = node.content
            
            # Simple template replacement
            for key, value in context.items():
                content = content.replace(f"{{{key}}}", str(value))
            
            # Apply any registered generators
            for gen_type, generator in self.generators.items():
                if f"{{{gen_type}}}" in content:
                    content = content.replace(f"{{{gen_type}}}", generator())
            
            return content
            
        except Exception:
            return node.content
    
    def _generate_fallback_content(self, triggers: List[str]) -> str:
        """Generate fallback content when no pathways match."""
        try:
            if not triggers:
                return "Creative response generated"
            
            trigger_text = ", ".join(triggers[:3])
            return f"Creative exploration of: {trigger_text}"
            
        except Exception:
            return "Generated creative response"
    
    def add_generator(self, name: str, generator_func: Callable) -> bool:
        """
        Add custom content generator function.
        
        Args:
            name: Generator name for template replacement
            generator_func: Function that returns generated content
            
        Returns:
            bool: Success status
        """
        try:
            self.generators[name] = generator_func
            return True
        except Exception as e:
            print(f"Error adding generator {name}: {e}")
            return False
    
    def export_structure(self) -> Dict[str, Any]:
        """
        Export the current structure configuration.
        
        Returns:
            Dictionary containing structure data
        """
        try:
            return {
                'nodes': {nid: {
                    'content': node.content,
                    'triggers': node.triggers,
                    'weight': node.weight,
                    'metadata': node.metadata
                } for nid, node in self.nodes.items()},
                'pathways': dict(self.pathways),
                'triggers': dict(self.triggers)
            }
        except Exception as e:
            print(f"Error exporting structure: {e}")
            return {}
    
    def import_structure(self, structure_data: Dict[str, Any]) -> bool:
        """
        Import structure configuration from data.
        
        Args:
            structure_data: Structure data dictionary
            
        Returns:
            bool: Success status
        """
        try:
            # Clear existing data
            self.nodes.clear()
            self.pathways.clear()
            self.triggers.clear()
            
            # Import nodes
            for node_id, node_data in structure_data.get('nodes', {}).items():
                self.add_node(
                    node_id,
                    node_data['content'],
                    node_data['triggers'],
                    node_data.get('weight', 1.0),
                    node_data.get('metadata', {})
                )
            
            # Import pathways
            for pathway_id, pathway_data in structure_data.get('pathways', {}).items():
                if isinstance(pathway_data, dict):
                    self.pathways[pathway_id] = pathway_data
                else:
                    # Legacy format support
                    self.pathways[pathway_id] = {
                        'nodes': pathway_data,
                        'type': PathwayType.SEQUENTIAL
                    }
            
            return True
            
        except Exception as e:
            print(f"Error importing structure: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current structure.
        
        Returns:
            Statistics dictionary
        """
        try:
            return {
                'total_nodes': len(self.nodes),
                'total_pathways': len(self.pathways),
                'total_triggers': len(self.triggers),
                'avg_node_weight': sum(node.weight for node in self.nodes.values()) / len(self.nodes) if self.nodes else 0,
                'pathway_types': list(set(
                    pathway.get('type', PathwayType.SEQUENTIAL) 
                    for pathway in self.pathways.values()
                ))
            }
        except Exception as e:
            print(f"Error calculating stats: {e}")
            return {}