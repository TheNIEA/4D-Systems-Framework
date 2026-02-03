"""
Hierarchical Memory Architecture for Spark Cube

This implements:
1. Secondary nodes that store experience along pathways
2. Node promotion when secondary nodes become anchors
3. Semantic memory through experience association
"""

import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import Counter
import json
import os


@dataclass
class Experience:
    """A single experience stored in a secondary node"""
    timestamp: str
    signal_summary: str  # What was the input
    outcome: str  # What happened
    success: bool
    pathway_used: str
    associated_concepts: List[str]
    embedding: Optional[List[float]] = None  # Semantic vector
    
    def similarity_to(self, other: 'Experience') -> float:
        """Calculate semantic similarity between experiences"""
        if self.embedding and other.embedding:
            # Cosine similarity
            a = np.array(self.embedding)
            b = np.array(other.embedding)
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
        else:
            # Fallback: concept overlap
            overlap = set(self.associated_concepts) & set(other.associated_concepts)
            total = set(self.associated_concepts) | set(other.associated_concepts)
            return len(overlap) / len(total) if total else 0.0


@dataclass
class SecondaryNode:
    """A secondary node that stores experiences along a pathway"""
    id: str
    parent_node_id: int  # Which main node this branches from
    domain: str  # What type of processing this specializes in
    experiences: List[Experience] = field(default_factory=list)
    strength: float = 0.1  # Starts weak, grows with use
    creation_time: str = field(default_factory=lambda: datetime.now().isoformat())
    activation_count: int = 0
    success_rate: float = 0.5
    
    # Promotion tracking
    promotion_threshold: float = 0.85  # Strength needed to become anchor
    is_promoted: bool = False
    
    # Sub-nodes (tertiary level)
    children: Dict[str, 'SecondaryNode'] = field(default_factory=dict)
    
    def add_experience(self, experience: Experience):
        """Add an experience and update strength"""
        self.experiences.append(experience)
        self.activation_count += 1
        
        # Update success rate
        successes = sum(1 for e in self.experiences if e.success)
        self.success_rate = successes / len(self.experiences)
        
        # Strengthen based on use and success
        if experience.success:
            self.strength = min(1.0, self.strength * 1.05 + 0.02)
        else:
            self.strength = max(0.1, self.strength * 0.98)
    
    def retrieve_relevant_experiences(self, query_experience: Experience, top_k: int = 5) -> List[Experience]:
        """Find experiences most relevant to current situation"""
        if not self.experiences:
            return []
        
        scored = []
        for exp in self.experiences:
            similarity = query_experience.similarity_to(exp)
            # Weight by recency and success
            score = similarity * (1.5 if exp.success else 0.5)
            scored.append((score, exp))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [exp for _, exp in scored[:top_k]]
    
    def should_promote(self) -> bool:
        """Check if this node should become an anchor"""
        return (
            self.strength >= self.promotion_threshold and
            len(self.experiences) >= 20 and
            self.success_rate >= 0.7 and
            not self.is_promoted
        )
    
    def create_child(self, domain: str) -> 'SecondaryNode':
        """Create a tertiary node under this one"""
        child_id = f"{self.id}.{len(self.children)}"
        child = SecondaryNode(
            id=child_id,
            parent_node_id=self.parent_node_id,
            domain=domain
        )
        self.children[domain] = child
        return child


class HierarchicalMemory:
    """
    Manages the hierarchical memory structure for Spark Cube.
    
    Structure:
    - 13 Main Anchor Nodes (fixed)
    - Secondary Nodes (grow from experience)
    - Tertiary Nodes (specializations of secondary)
    - Promoted Nodes (secondary → anchor)
    """
    
    def __init__(self, cube, storage_path: str = "spark_cube/memory"):
        self.cube = cube
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # Main anchor nodes (the original 13)
        self.anchor_nodes: Dict[int, Dict] = {
            i: {
                'name': self._get_node_name(i),
                'development': 0.5,
                'secondary_nodes': {}
            }
            for i in range(1, 14)
        }
        
        # Promoted nodes (secondary nodes that became anchors)
        self.promoted_anchors: Dict[str, SecondaryNode] = {}
        
        # Next available anchor ID
        self.next_anchor_id = 14
        
        # Global experience index for semantic search
        self.experience_index: List[Tuple[str, Experience]] = []  # (node_id, experience)
        
        # Load existing memory
        self._load_memory()
    
    def _get_node_name(self, node_id: int) -> str:
        """Get the name of a main node"""
        names = {
            1: "Reactive",
            2: "Habit",
            3: "Executive",
            4: "Temporal",
            5: "Social",
            6: "Emotional",
            7: "Pattern",
            8: "Language",
            9: "Perception",
            10: "Integration",
            11: "Memory",
            12: "ToolUse",
            13: "Learning"
        }
        return names.get(node_id, f"Node_{node_id}")
    
    def record_pathway_experience(
        self,
        pathway: List[int],
        signal: dict,
        outcome: dict,
        success: bool
    ):
        """
        Record an experience along a pathway.
        This creates/updates secondary nodes for each step.
        """
        pathway_name = f"pathway_{'_'.join(map(str, pathway))}"
        
        # Create experience object
        experience = Experience(
            timestamp=datetime.now().isoformat(),
            signal_summary=self._summarize_signal(signal),
            outcome=str(outcome.get('result', ''))[:200],
            success=success,
            pathway_used=pathway_name,
            associated_concepts=self._extract_concepts(signal)
        )
        
        # Record at each node along the pathway
        for i, node_id in enumerate(pathway):
            if node_id not in self.anchor_nodes:
                continue  # Skip if not a valid anchor node
            
            # Determine domain based on position and context
            domain = self._infer_domain(signal, node_id, pathway, i)
            
            # Get or create secondary node
            secondary = self._get_or_create_secondary(node_id, domain)
            
            # Add experience
            secondary.add_experience(experience)
            
            # Index for global search
            self.experience_index.append((secondary.id, experience))
            
            # Check for promotion
            if secondary.should_promote():
                self._promote_node(secondary)
        
        # Periodic save
        if len(self.experience_index) % 100 == 0:
            self._save_memory()
    
    def _get_or_create_secondary(self, node_id: int, domain: str) -> SecondaryNode:
        """Get existing or create new secondary node"""
        anchor = self.anchor_nodes[node_id]
        
        if domain not in anchor['secondary_nodes']:
            secondary_id = f"node_{node_id}_sec_{len(anchor['secondary_nodes'])}"
            anchor['secondary_nodes'][domain] = SecondaryNode(
                id=secondary_id,
                parent_node_id=node_id,
                domain=domain
            )
        
        return anchor['secondary_nodes'][domain]
    
    def _infer_domain(self, signal: dict, node_id: int, pathway: List[int], position: int) -> str:
        """Infer the domain/specialization based on context"""
        concepts = self._extract_concepts(signal)
        
        # Combine node function with signal concepts
        node_name = self._get_node_name(node_id).lower()
        
        # Find most relevant concept for this node
        if concepts:
            # Use first concept as domain specialization
            return f"{node_name}_{concepts[0]}"
        else:
            return f"{node_name}_general"
    
    def _extract_concepts(self, signal: dict) -> List[str]:
        """Extract semantic concepts from signal"""
        concepts = []
        
        # From goal/challenge
        if 'goal' in signal:
            words = str(signal['goal']).lower().split()
            concepts.extend([w for w in words if len(w) > 3])
        
        if 'challenge' in signal:
            words = str(signal['challenge']).lower().split()
            concepts.extend([w for w in words if len(w) > 3])
        
        if 'data' in signal and isinstance(signal['data'], dict):
            concepts.extend(str(k) for k in signal['data'].keys())
        
        # Remove duplicates, keep order
        seen = set()
        return [c for c in concepts if not (c in seen or seen.add(c))][:10]
    
    def _summarize_signal(self, signal: dict) -> str:
        """Create a summary of the signal for storage"""
        parts = []
        if 'goal' in signal:
            parts.append(f"Goal: {signal['goal']}")
        if 'challenge' in signal:
            parts.append(f"Challenge: {signal['challenge']}")
        if 'type' in signal:
            parts.append(f"Type: {signal['type']}")
        return "; ".join(parts)[:500]
    
    def _promote_node(self, secondary: SecondaryNode):
        """Promote a secondary node to anchor status"""
        if secondary.is_promoted:
            return
        
        secondary.is_promoted = True
        self.promoted_anchors[secondary.id] = secondary
        
        # Assign new anchor ID
        new_node_id = self.next_anchor_id
        self.next_anchor_id += 1
        
        # Create new anchor entry
        self.anchor_nodes[new_node_id] = {
            'name': secondary.domain,
            'development': secondary.strength,
            'secondary_nodes': {},
            'promoted_from': secondary.parent_node_id,
            'promotion_date': datetime.now().isoformat()
        }
        
        print(f"\n🌟 NODE PROMOTION: {secondary.domain}")
        print(f"   Secondary node '{secondary.id}' → Anchor Node {new_node_id}")
        print(f"   Strength: {secondary.strength:.2f}")
        print(f"   Experiences: {len(secondary.experiences)}")
        print(f"   Success Rate: {secondary.success_rate:.1%}")
        print(f"   This node can now be part of main processing sequences!\n")
        
        # Register with cube's available nodes
        if hasattr(self.cube, 'nodes'):
            self.cube.nodes[new_node_id] = {
                'name': secondary.domain,
                'development': secondary.strength,
                'function': self._create_node_function(secondary)
            }
    
    def _create_node_function(self, secondary: SecondaryNode):
        """Create a processing function for a promoted node"""
        def process(signal, context):
            # Use accumulated experience to process
            query_exp = Experience(
                timestamp=datetime.now().isoformat(),
                signal_summary=self._summarize_signal(signal),
                outcome="",
                success=True,
                pathway_used="query",
                associated_concepts=self._extract_concepts(signal)
            )
            
            relevant = secondary.retrieve_relevant_experiences(query_exp, top_k=3)
            
            # Apply learned patterns
            result = {
                'processed_by': secondary.domain,
                'relevant_experiences': len(relevant),
                'confidence': secondary.success_rate,
                'suggested_approach': self._synthesize_approach(relevant)
            }
            
            return result
        
        return process
    
    def _synthesize_approach(self, experiences: List[Experience]) -> str:
        """Synthesize an approach from relevant experiences"""
        if not experiences:
            return "No prior experience to draw from"
        
        successful = [e for e in experiences if e.success]
        if successful:
            # Return concepts from successful experiences
            all_concepts = []
            for e in successful:
                all_concepts.extend(e.associated_concepts)
            
            # Most common concepts
            common = Counter(all_concepts).most_common(3)
            return f"Apply patterns from: {', '.join(c for c, _ in common)}"
        else:
            return "Previous attempts unsuccessful - try alternative approach"
    
    def query_relevant_memory(self, signal: dict, top_k: int = 10) -> List[Tuple[str, Experience]]:
        """Find most relevant experiences across all memory"""
        query_exp = Experience(
            timestamp=datetime.now().isoformat(),
            signal_summary=self._summarize_signal(signal),
            outcome="",
            success=True,
            pathway_used="query",
            associated_concepts=self._extract_concepts(signal)
        )
        
        scored = []
        for node_id, exp in self.experience_index:
            similarity = query_exp.similarity_to(exp)
            scored.append((similarity, node_id, exp))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [(node_id, exp) for _, node_id, exp in scored[:top_k]]
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about the memory structure"""
        total_secondary = sum(
            len(anchor['secondary_nodes'])
            for anchor in self.anchor_nodes.values()
        )
        
        total_experiences = len(self.experience_index)
        
        strongest_secondary = None
        max_strength = 0
        for anchor in self.anchor_nodes.values():
            for sec in anchor['secondary_nodes'].values():
                if sec.strength > max_strength:
                    max_strength = sec.strength
                    strongest_secondary = sec
        
        return {
            'anchor_nodes': 13,
            'promoted_anchors': len(self.promoted_anchors),
            'total_anchors': 13 + len(self.promoted_anchors),
            'secondary_nodes': total_secondary,
            'total_experiences': total_experiences,
            'strongest_secondary': {
                'id': strongest_secondary.id if strongest_secondary else None,
                'domain': strongest_secondary.domain if strongest_secondary else None,
                'strength': max_strength,
                'ready_for_promotion': strongest_secondary.should_promote() if strongest_secondary else False
            }
        }
    
    def _save_memory(self):
        """Persist memory to disk"""
        # Save anchor nodes and their secondary nodes
        data = {
            'anchor_nodes': {},
            'promoted_anchors': {},
            'next_anchor_id': self.next_anchor_id,
            'experience_count': len(self.experience_index)
        }
        
        for node_id, anchor in self.anchor_nodes.items():
            data['anchor_nodes'][str(node_id)] = {
                'name': anchor['name'],
                'development': anchor['development'],
                'secondary_nodes': {
                    domain: {
                        'id': sec.id,
                        'domain': sec.domain,
                        'strength': sec.strength,
                        'activation_count': sec.activation_count,
                        'success_rate': sec.success_rate,
                        'experience_count': len(sec.experiences),
                        'is_promoted': sec.is_promoted
                    }
                    for domain, sec in anchor['secondary_nodes'].items()
                }
            }
        
        for node_id, sec in self.promoted_anchors.items():
            data['promoted_anchors'][node_id] = {
                'domain': sec.domain,
                'strength': sec.strength,
                'parent_node_id': sec.parent_node_id
            }
        
        path = os.path.join(self.storage_path, 'hierarchical_memory.json')
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_memory(self):
        """Load memory from disk"""
        path = os.path.join(self.storage_path, 'hierarchical_memory.json')
        if not os.path.exists(path):
            return
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            # Restore next anchor ID
            self.next_anchor_id = data.get('next_anchor_id', 14)
            
            # Restore secondary nodes
            for node_id_str, anchor_data in data.get('anchor_nodes', {}).items():
                node_id = int(node_id_str)
                if node_id in self.anchor_nodes:
                    for domain, sec_data in anchor_data.get('secondary_nodes', {}).items():
                        secondary = SecondaryNode(
                            id=sec_data['id'],
                            parent_node_id=node_id,
                            domain=sec_data['domain'],
                            strength=sec_data['strength'],
                            activation_count=sec_data['activation_count'],
                            success_rate=sec_data['success_rate'],
                            is_promoted=sec_data.get('is_promoted', False)
                        )
                        self.anchor_nodes[node_id]['secondary_nodes'][domain] = secondary
            
            print(f"✓ Loaded hierarchical memory: {data.get('experience_count', 0)} experiences")
        
        except Exception as e:
            print(f"Warning: Could not load memory: {e}")


def integrate_with_cube(cube):
    """
    Integrate hierarchical memory with existing Spark Cube.
    Call this after cube initialization.
    """
    memory = HierarchicalMemory(cube)
    
    # Store reference on cube
    cube.hierarchical_memory = memory
    
    # Wrap the process_signal method to record experiences
    if hasattr(cube, 'process_signal'):
        original_process = cube.process_signal
        
        def process_with_memory(signal, sequence_name=None, **kwargs):
            # Process normally
            result = original_process(signal, sequence_name=sequence_name, **kwargs)
            
            # Get the pathway that was actually used (from result or sequences)
            pathway = None
            actual_sequence = result.get('sequence', sequence_name)
            
            if actual_sequence:
                # Try generated sequences first, then base sequences
                if hasattr(cube, 'generated_sequences') and actual_sequence in cube.generated_sequences:
                    pathway = cube.generated_sequences[actual_sequence]
                elif hasattr(cube, 'sequences') and actual_sequence in cube.sequences:
                    pathway = cube.sequences[actual_sequence]
            
            # Record the experience if we have a pathway
            if pathway:
                success = result.get('overall_coherence', result.get('coherence', 0.5)) > 0.5
                signal_dict = signal.__dict__ if hasattr(signal, '__dict__') else {'data': str(signal)}
                memory.record_pathway_experience(
                    pathway=pathway,
                    signal=signal_dict,
                    outcome=result,
                    success=success
                )
            
            return result
        
        cube.process_signal = process_with_memory
    
    return memory
