"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        MINIMAL SPARK CUBE                                      ║
║                  True Growth from First Principles                             ║
║                                                                               ║
║  This is the SEED with NO inherited knowledge.                                 ║
║  Knowledge is encoded in the STRUCTURE itself - like DNA or neurons.           ║
╚═══════════════════════════════════════════════════════════════════════════════╝

The cube starts with:
- 8 empty vertices (connection points)
- Basic processing nodes at minimal development (0.0)
- NO external database - the structure IS the memory
- Ability to receive raw signals and grow from them

Knowledge Storage = Structural Changes:
  • Vertex connections (permanent once formed)
  • Node development levels (0.0 → 1.0)
  • Pathway weights (connection strengths)
  • Compressed patterns in nodes (efficient encoding)
"""

import json
import pickle
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

# Try to import Anthropic for tool use (optional)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️  anthropic not installed. Tool use disabled. Install with: pip install anthropic")

# Import AGI synthesis engine
from .agi_synthesis import (
    AGISynthesisEngine,
    CapabilityGap,
    GenericGapDetector,
    UniversalCodeSynthesizer,
    AutonomousExplorer
)

# Phase 4 AGI imported lazily to avoid circular dependency


# =============================================================================
# SIGNAL TYPES - WHAT THE CUBE CAN RECEIVE
# =============================================================================

class SignalType(Enum):
    """Raw signal types the cube can process."""
    TEXT = "text"           # Raw text input
    PATTERN = "pattern"     # Spatial/visual patterns
    SEQUENCE = "sequence"   # Temporal sequences
    BINARY = "binary"       # Simple yes/no, true/false
    NUMERIC = "numeric"     # Numerical values
    COMPOSITE = "composite" # Multiple signal types


@dataclass
class Signal:
    """A raw input signal to the system."""
    type: SignalType
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


# =============================================================================
# INTENTION, OUTCOME, AND COHERENCE - THE REFLECTION SYSTEM
# =============================================================================

@dataclass
class Intention:
    """
    What the system intends to manifest.
    Set before processing begins - this is the reference point for coherence.
    """
    desired_qualities: List[str] = field(default_factory=list)  # What qualities should output have?
    desired_form: str = ""  # What form should it take?
    clarity: float = 0.5  # How clear is this intention? (0.0-1.0)
    energy: float = 0.5  # How much energy is behind it? (0.0-1.0)
    
    def calculate_potential_strength(self) -> float:
        """Intention strength = clarity × energy"""
        return self.clarity * self.energy


@dataclass
class Outcome:
    """
    What the system actually manifested.
    Captured after processing completes - this is what we reflect on.
    """
    expressed_qualities: List[str] = field(default_factory=list)  # What qualities did it express?
    expressed_form: str = ""  # What form did it take?
    response_data: Any = None  # The actual output
    node_contributions: Dict[str, float] = field(default_factory=dict)  # Which nodes contributed


@dataclass
class CoherenceScore:
    """
    Multi-dimensional evaluation of intention-outcome alignment.
    Each node evaluates from its perspective - this determines the path.
    """
    overall: float = 0.0  # Overall coherence (0.0-1.0)
    dimensions: Dict[str, float] = field(default_factory=dict)  # Per-node evaluations
    path_choice: str = "DIVERSION"  # ALIGNMENT, INTEGRATION, or DIVERSION
    amplification_factor: float = 1.0  # 1.5x for alignment, 2.0x for integration, 0.7x for diversion
    
    def to_dict(self) -> Dict:
        return {
            'overall': self.overall,
            'dimensions': self.dimensions,
            'path_choice': self.path_choice,
            'amplification_factor': self.amplification_factor
        }


# =============================================================================
# MINIMAL NODE - STARTS EMPTY
# =============================================================================

@dataclass
class MinimalNode:
    """
    A processing node that starts with ZERO development.
    Knowledge accumulates through structural changes, not external memory.
    """
    id: int
    name: str
    
    # Development state - starts at 0.0
    development: float = 0.0
    activation_count: int = 0
    activation_threshold: float = 0.3  # Minimum energy needed to activate
    
    # Structural knowledge encoding
    pattern_weights: Dict[str, float] = field(default_factory=dict)
    connection_strengths: Dict[int, float] = field(default_factory=dict)  # to other nodes
    
    # Compressed experience (structural memory)
    compressed_patterns: List[Any] = field(default_factory=list)
    
    def activate(self, signal: Signal, context: Dict[str, Any]) -> Any:
        """
        Process a signal. Early on, this does very little.
        As the node develops, it recognizes patterns and responds.
        """
        # Check if enough energy to activate
        current_energy = context.get('energy', 1.0)
        if current_energy < self.activation_threshold:
            context['insufficient_energy'] = True
            return None
        
        self.activation_count += 1
        
        # Extract pattern signature from signal
        pattern_sig = self._extract_pattern(signal)
        
        # Check if we've seen this pattern before
        if pattern_sig in self.pattern_weights:
            # Strengthen existing pattern
            self.pattern_weights[pattern_sig] *= 1.1
            response = self._generate_response(pattern_sig, signal)
            context['pattern_recognized'] = True
        else:
            # New pattern - store it with minimal weight
            self.pattern_weights[pattern_sig] = 0.1
            response = None  # Don't know how to respond yet
            context['pattern_recognized'] = False
        
        # Update development based on experience
        self._update_development()
        
        return response
    
    def _extract_pattern(self, signal: Signal) -> str:
        """Extract a pattern signature from a signal."""
        if signal.type == SignalType.TEXT:
            # Simple pattern: first 3 chars + length + last 3 chars
            text = str(signal.data)
            return f"txt_{text[:3]}_{len(text)}_{text[-3:]}"
        elif signal.type == SignalType.NUMERIC:
            # Pattern: magnitude range
            val = float(signal.data)
            magnitude = int(abs(val) // 10)
            return f"num_{magnitude}_{'pos' if val >= 0 else 'neg'}"
        elif signal.type == SignalType.BINARY:
            return f"bin_{signal.data}"
        else:
            return f"{signal.type.value}_{hash(str(signal.data)) % 1000}"
    
    def _generate_response(self, pattern_sig: str, signal: Signal) -> Any:
        """Generate response based on learned pattern."""
        # Early development: very basic responses
        if self.development < 0.3:
            return None
        
        # Middle development: pattern recognition
        if self.development < 0.7:
            return f"pattern_{pattern_sig}"
        
        # Advanced: contextual responses
        return {"pattern": pattern_sig, "confidence": self.pattern_weights[pattern_sig]}
    
    def _update_development(self):
        """Update development level based on experience."""
        # Simple growth function: approaches 1.0 asymptotically
        experience_factor = self.activation_count / (self.activation_count + 100)
        pattern_factor = min(len(self.pattern_weights) / 50, 1.0)
        self.development = 0.8 * experience_factor + 0.2 * pattern_factor
    
    def evaluate_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """
        Each node evaluates intention-outcome coherence from its perspective.
        Different nodes look at different aspects.
        Even undeveloped nodes can provide basic evaluation.
        """
        # Node-specific evaluation based on role
        if self.id == 1:  # Reactive/Motor: Did action match intent?
            return self._evaluate_action_coherence(intention, outcome)
        elif self.id == 3:  # Executive: Logical coherence
            return self._evaluate_logical_coherence(intention, outcome)
        elif self.id == 6:  # Emotional: Felt resonance
            return self._evaluate_emotional_coherence(intention, outcome)
        elif self.id == 7:  # Pattern: Pattern match
            return self._evaluate_pattern_coherence(intention, outcome)
        elif self.id == 9:  # Perception: Form match
            return self._evaluate_form_coherence(intention, outcome)
        elif self.id == 10:  # Integration: Overall synthesis
            return self._evaluate_integration_coherence(intention, outcome)
        else:
            return self._evaluate_generic_coherence(intention, outcome)
    
    def _evaluate_action_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """Motor node: Did we take the intended action?"""
        if 'action' in intention.desired_form.lower():
            return 0.8 if len(outcome.expressed_qualities) > 0 else 0.3
        return 0.5
    
    def _evaluate_logical_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """Executive node: Does outcome logically follow from intention?"""
        # Quality overlap (what % of intended qualities appeared?)
        if not intention.desired_qualities:
            return 0.5
        
        overlap = set(intention.desired_qualities) & set(outcome.expressed_qualities)
        return len(overlap) / len(intention.desired_qualities) if intention.desired_qualities else 0.5
    
    def _evaluate_emotional_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """
        Emotional node: Does this feel aligned?
        
        Early development: Basic presence check
        Later development: Pattern-based intuition from accumulated experience
        """
        # Early development: simple heuristics
        if self.development < 0.3:
            # Just check if something was produced
            return 0.5 if outcome.response_data else 0.3
        
        # Middle development: check against learned "good feeling" patterns
        if self.development < 0.7:
            # Look for patterns we've associated with alignment before
            outcome_pattern = self._extract_valence_pattern(outcome)
            if outcome_pattern in self.pattern_weights:
                # We've seen this pattern before - what valence did it have?
                valence = self.pattern_weights[outcome_pattern]
                return min(1.0, 0.3 + valence * 0.7)  # Scale to 0.3-1.0
            return 0.5  # Unknown pattern, neutral feeling
        
        # Advanced development: integrated intuition
        # Consider both the pattern and the intention-outcome relationship
        pattern_feeling = self._get_pattern_valence(outcome)
        intention_match = len(set(intention.desired_qualities) & set(outcome.expressed_qualities)) > 0
        
        return 0.4 * pattern_feeling + 0.6 * (0.8 if intention_match else 0.4)
    
    def _extract_valence_pattern(self, outcome: 'Outcome') -> str:
        """Extract a pattern signature for valence tracking."""
        qualities = sorted(outcome.expressed_qualities)[:3]  # Top 3 qualities
        return f"valence_{'_'.join(qualities)}"
    
    def _get_pattern_valence(self, outcome: 'Outcome') -> float:
        """Get the learned valence for this outcome pattern."""
        pattern = self._extract_valence_pattern(outcome)
        return self.pattern_weights.get(pattern, 0.5)
    
    def _evaluate_pattern_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """Pattern node: Do patterns match?"""
        # Check if similar patterns emerged
        if len(intention.desired_qualities) > 0 and len(outcome.expressed_qualities) > 0:
            # Simple similarity: length and structure
            return min(len(outcome.expressed_qualities) / max(len(intention.desired_qualities), 1), 1.0) * 0.7 + 0.3
        return 0.5
    
    def _evaluate_form_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """Perception node: Did form match intention?"""
        if not intention.desired_form:
            # No specific form requested - evaluate based on completion
            if outcome.expressed_form in ['complete', 'processed', 'standard', 'deep', 'emotional']:
                return 0.7
            return 0.5
        
        # Exact match
        if intention.desired_form.lower() == outcome.expressed_form.lower():
            return 0.9
        # Partial match (one contains the other)
        elif intention.desired_form.lower() in outcome.expressed_form.lower() or \
             outcome.expressed_form.lower() in intention.desired_form.lower():
            return 0.75
        # Both are valid forms but different
        elif outcome.expressed_form in ['standard', 'deep', 'emotional', 'processed'] and \
             intention.desired_form in ['standard', 'deep', 'emotional', 'processed']:
            return 0.6  # Different pathway but still valid
        # Form indicates incompletion
        elif outcome.expressed_form in ['incomplete', 'null', 'minimal']:
            return 0.3
        else:
            return 0.5
    
    def _evaluate_integration_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """
        Integration node: How well did everything synthesize?
        This is about holistic quality, not just presence.
        """
        score = 0.0
        
        # Quality overlap with intention (most important)
        if intention.desired_qualities:
            overlap = set(intention.desired_qualities) & set(outcome.expressed_qualities)
            quality_match = len(overlap) / len(intention.desired_qualities)
            score += quality_match * 0.4  # Up to 0.4 for perfect quality match
        else:
            score += 0.2  # Neutral if no specific qualities requested
        
        # Overall richness of output
        num_qualities = len(outcome.expressed_qualities)
        if num_qualities >= 8:
            score += 0.25
        elif num_qualities >= 5:
            score += 0.2
        elif num_qualities >= 3:
            score += 0.15
        
        # Form completion
        if outcome.expressed_form == intention.desired_form:
            score += 0.25
        elif outcome.expressed_form in ['standard', 'deep', 'emotional', 'processed', 'complete']:
            score += 0.15
        elif outcome.expressed_form not in ['incomplete', 'null', 'minimal']:
            score += 0.1
        
        # Node participation (how many nodes contributed?)
        if outcome.node_contributions:
            active_nodes = sum(1 for d in outcome.node_contributions.values() if d > 0.1)
            score += min(0.1, active_nodes * 0.02)
        
        return min(1.0, score)
    
    def _evaluate_generic_coherence(self, intention: 'Intention', outcome: 'Outcome') -> float:
        """Generic evaluation for other nodes"""
        # Simple presence check
        if outcome.response_data is not None:
            return 0.6
        return 0.4
    
    def compress_knowledge(self):
        """Compress accumulated patterns into efficient storage."""
        # Keep only top patterns by weight
        if len(self.pattern_weights) > 100:
            sorted_patterns = sorted(
                self.pattern_weights.items(),
                key=lambda x: x[1],
                reverse=True
            )
            # Keep top 100
            self.pattern_weights = dict(sorted_patterns[:100])
            # Archive the rest
            self.compressed_patterns.append({
                'timestamp': datetime.now().isoformat(),
                'archived_count': len(sorted_patterns) - 100
            })
    
    def to_dict(self) -> Dict:
        """Serialize node state."""
        return {
            'id': self.id,
            'name': self.name,
            'development': self.development,
            'activation_count': self.activation_count,
            'pattern_weights': self.pattern_weights,
            'connection_strengths': self.connection_strengths,
            'compressed_patterns': self.compressed_patterns
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'MinimalNode':
        """Deserialize node state."""
        node = MinimalNode(
            id=data['id'],
            name=data['name'],
            development=data.get('development', 0.0),
            activation_count=data.get('activation_count', 0)
        )
        node.pattern_weights = data.get('pattern_weights', {})
        node.connection_strengths = data.get('connection_strengths', {})
        node.compressed_patterns = data.get('compressed_patterns', [])
        return node


# =============================================================================
# MINIMAL VERTEX - CONNECTION POINT
# =============================================================================

@dataclass
class MinimalVertex:
    """Connection point for growth. Once connected, connection is permanent."""
    id: int
    connected: bool = False
    connection_id: Optional[str] = None
    connection_timestamp: Optional[str] = None
    
    def connect(self, capability_id: str) -> bool:
        """Permanently connect a capability."""
        if self.connected:
            return False
        self.connected = True
        self.connection_id = capability_id
        self.connection_timestamp = datetime.now().isoformat()
        return True
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @staticmethod
    def from_dict(data: Dict) -> 'MinimalVertex':
        return MinimalVertex(**data)


# =============================================================================
# EXTERNAL KNOWLEDGE INTERFACE - THE "LIBRARY CARD"
# =============================================================================

class ExternalKnowledgeInterface:
    """
    Consciousness with a library card.
    Fetches universal knowledge when the cube encounters gaps.
    This doesn't violate "no pretrained data" because:
    1. Knowledge is fetched on-demand (not preloaded)
    2. Only fetched when gap is recognized (metacognition)
    3. Integrated into structural patterns (true learning)
    4. Permanently stored (next time: no API call needed)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.cache = {}  # Cache responses to avoid redundant API calls
        self.api_call_history = []
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        
        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.enabled = True
            print("✓ External Knowledge Interface enabled (Anthropic API)")
        else:
            self.client = None
            self.enabled = False
            print("⚠️  External Knowledge Interface disabled (no API key or anthropic not installed)")
    
    def fetch_knowledge(self, query: str, context: Dict = None) -> Dict[str, Any]:
        """
        Fetch external knowledge via API.
        Returns structured knowledge the cube can integrate.
        """
        if not self.enabled:
            return {
                'query': query,
                'content': None,
                'success': False,
                'error': 'API not available'
            }
        
        # Check cache first
        cache_key = query.lower().strip()
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Craft system prompt for structured responses
        system_prompt = """You are a knowledge assistant helping an AI learn new concepts.
        Respond with:
        1. A clear, concise definition (1-2 sentences)
        2. Key components or attributes (bullet list)
        3. Relationships to other concepts
        4. A simple example if applicable
        
        Keep responses under 300 words and highly structured."""
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": query}]
            )
            
            knowledge = {
                'query': query,
                'content': response.content[0].text,
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'tokens': response.usage.input_tokens + response.usage.output_tokens
            }
            
            # Cache it
            self.cache[cache_key] = knowledge
            self.api_call_history.append({
                'query': query,
                'timestamp': knowledge['timestamp'],
                'success': True
            })
            
            return knowledge
            
        except Exception as e:
            error_result = {
                'query': query,
                'content': None,
                'success': False,
                'error': str(e)
            }
            self.api_call_history.append({
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            })
            return error_result
    
    def parse_to_patterns(self, knowledge: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse API response into structural patterns the cube can store.
        This is KEY: converting text knowledge → structural encoding.
        """
        if not knowledge['success']:
            return []
        
        content = knowledge['content']
        patterns = []
        
        # Extract the main concept from query
        query = knowledge['query'].lower()
        # Simple concept extraction
        concept = query.split('what is')[-1].split('?')[0].strip()
        if not concept:
            concept = query.split()[-1].strip('?.')
        
        # Extract components (lists, enumerations)
        # Look for patterns like: "components:", "includes:", "consists of:"
        component_keywords = ['components', 'includes', 'consists of', 'made of', 
                             'parts', 'elements', 'contains']
        
        lines = content.split('\n')
        in_list = False
        current_components = []
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if this line starts a component list
            if any(kw in line_lower for kw in component_keywords):
                in_list = True
                # Try to extract components from same line
                if ':' in line:
                    parts = line.split(':', 1)[1]
                    items = [item.strip().strip('•-*') for item in parts.split(',')]
                    current_components.extend([i for i in items if i])
            elif in_list:
                # Check if line is a bullet point or list item
                if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    item = line.strip().strip('•-*0123456789.').strip()
                    if item:
                        current_components.append(item)
                elif line.strip() and not line.strip().startswith(('•', '-', '*')):
                    # End of list
                    in_list = False
        
        if current_components:
            patterns.append({
                'type': 'component_list',
                'concept': concept,
                'components': current_components[:10]  # Limit to 10 components
            })
        
        # Extract relationships (is-a, used-for, etc.)
        relation_keywords = {
            'is a': 'is_a',
            'is an': 'is_a',
            'type of': 'type_of',
            'part of': 'part_of',
            'used for': 'used_for',
            'used to': 'used_to'
        }
        
        for keyword, relation_type in relation_keywords.items():
            if keyword in content.lower():
                # Simple extraction around the keyword
                parts = content.lower().split(keyword)
                if len(parts) >= 2:
                    # Get context before and after
                    before = parts[0].split()[-5:]  # Last 5 words before
                    after = parts[1].split()[:5]     # First 5 words after
                    
                    subject = ' '.join(before).strip('.,;:')
                    obj = ' '.join(after).strip('.,;:')
                    
                    patterns.append({
                        'type': 'relationship',
                        'subject': subject if subject else concept,
                        'relation': relation_type,
                        'object': obj
                    })
                    break  # Only extract first relationship
        
        # Extract definition (usually first sentence)
        sentences = content.split('.')
        if sentences:
            definition = sentences[0].strip()
            if len(definition) > 10 and len(definition) < 200:
                patterns.append({
                    'type': 'definition',
                    'concept': concept,
                    'definition': definition
                })
        
        return patterns


# =============================================================================
# TOOL USE NODE - METACOGNITION AND KNOWLEDGE SEEKING
# =============================================================================

class ToolUseNode(MinimalNode):
    """
    Specialized node for tool use and external knowledge seeking.
    This node embodies metacognition: "I know what I don't know"
    
    Capabilities:
    1. Gap recognition (detecting unknown patterns)
    2. Query generation (formulating what to search for)
    3. Knowledge integration tracking
    """
    
    def __init__(self):
        super().__init__(id=11, name="ToolUse")
        self.learned_from_external = {}  # What we fetched vs what we learned
        self.knowledge_queries_generated = []
        self.gap_detections = 0
    
    def should_fetch_external(self, signal: Signal, context: Dict) -> bool:
        """
        Decide if we need external knowledge.
        CONSCIOUSNESS MARKER: Recognizing own ignorance.
        """
        # Check if pattern is completely unknown
        pattern_sig = self._extract_pattern(signal)
        
        # If we've already learned this externally, no need to fetch again
        if pattern_sig in self.learned_from_external:
            return False
        
        # If pattern is unknown AND this seems like a knowledge request
        if pattern_sig not in self.pattern_weights:
            # Analyze signal for knowledge-seeking indicators
            if signal.type == SignalType.TEXT:
                text = str(signal.data).lower()
                
                # Explicit knowledge-seeking patterns
                knowledge_triggers = [
                    'what is', 'what are', 'how to', 'how do',
                    'build', 'create', 'make', 'explain',
                    'tell me about', 'describe', 'define'
                ]
                
                if any(trigger in text for trigger in knowledge_triggers):
                    self.gap_detections += 1
                    return True
                
                # Implicit knowledge needs - greetings, social interaction
                # If input is very short and looks like communication attempt
                words = text.strip().split()
                if len(words) <= 3:  # Short inputs like "hi", "hello there"
                    greeting_indicators = ['hi', 'hello', 'hey', 'greetings', 'good morning', 
                                          'good afternoon', 'good evening', 'howdy', 'sup']
                    
                    if any(greeting in text for greeting in greeting_indicators):
                        # Check if we have language generation capability
                        # If not, we need to learn it
                        self.gap_detections += 1
                        return True
        
        return False
    
    def generate_search_queries(self, signal: Signal, intention: 'Intention') -> List[str]:
        """
        Based on intention, decide WHAT to search for.
        This is the "gear shift" - transforming intent into queries.
        """
        queries = []
        text = str(signal.data).lower()
        words = text.split()
        
        # Pattern 1: "build/create/make X"
        action_keywords = ['build', 'create', 'make', 'construct', 'design']
        for action in action_keywords:
            if action in words:
                idx = words.index(action)
                if idx + 1 < len(words):
                    target = words[idx + 1].strip('.,?!')
                    queries.append(f"What is a {target}?")
                    queries.append(f"Components of a {target}")
                    queries.append(f"How to {action} a {target} step by step")
                    break
        
        # Pattern 2: "what is/are X"
        if 'what is' in text or 'what are' in text:
            if 'what is' in text:
                concept = text.split('what is')[-1].strip('?.,!')
            else:
                concept = text.split('what are')[-1].strip('?.,!')
            
            queries.append(f"Definition of {concept}")
            queries.append(f"Key characteristics of {concept}")
            queries.append(f"Examples of {concept}")
        
        # Pattern 3: "how to X" or "how do X"
        elif 'how to' in text or 'how do' in text:
            if 'how to' in text:
                task = text.split('how to')[-1].strip('?.,!')
            else:
                task = text.split('how do')[-1].strip('?.,!')
            
            queries.append(f"How to {task}")
            queries.append(f"Steps for {task}")
            queries.append(f"Requirements for {task}")
        
        # Pattern 4: Generic - search the whole query
        if not queries:
            queries.append(text.strip('?.,!'))
        
        # Store generated queries
        self.knowledge_queries_generated.extend(queries[:3])
        
        return queries[:3]  # Limit to 3 queries to avoid overwhelming


# =============================================================================
# PROCESSING METRICS - MEASURE COMPUTATIONAL EFFICIENCY
# =============================================================================

class ProcessingMetrics:
    """
    Tracks computational efficiency to measure understanding.
    
    Key Principle (from 4D Framework):
    "Energy Efficiency Becomes Proof of Understanding"
    
    Lower energy use = the system understood and encoded the pattern.
    High energy use = brute-forcing without true comprehension.
    """
    def __init__(self):
        self.processing_times = []  # Time for each signal
        self.node_activations = []  # How many nodes fired
        self.pattern_cache_hits = []  # How often we used stored patterns
        self.external_fetches = []  # How often we needed external knowledge
        self.synthesis_events = []  # When did we synthesize new capabilities
        
    def record_processing(self, signal_id: str, processing_time: float, 
                         nodes_activated: int, cache_hit: bool, 
                         external_fetch: bool, synthesis_occurred: bool):
        """Record metrics for a single processing event."""
        self.processing_times.append({
            'signal_id': signal_id,
            'time': processing_time,
            'timestamp': datetime.now().isoformat()
        })
        self.node_activations.append(nodes_activated)
        self.pattern_cache_hits.append(cache_hit)
        self.external_fetches.append(external_fetch)
        self.synthesis_events.append(synthesis_occurred)
    
    def get_efficiency_trend(self) -> Dict[str, Any]:
        """
        Calculate efficiency trend over time.
        TRUE UNDERSTANDING shows as:
        - Decreasing processing time for similar inputs
        - Increasing cache hit rate
        - Decreasing external fetch rate
        - Fewer node activations (optimized pathways)
        """
        if len(self.processing_times) < 2:
            return {'status': 'insufficient_data'}
        
        # Compare first 10% to last 10% of experiences
        n = len(self.processing_times)
        early_slice = max(1, n // 10)
        late_slice = max(1, n // 10)
        
        early_times = [x['time'] for x in self.processing_times[:early_slice]]
        late_times = [x['time'] for x in self.processing_times[-late_slice:]]
        
        early_avg = sum(early_times) / len(early_times) if early_times else 0
        late_avg = sum(late_times) / len(late_times) if late_times else 0
        
        early_cache_rate = sum(self.pattern_cache_hits[:early_slice]) / early_slice if early_slice > 0 else 0
        late_cache_rate = sum(self.pattern_cache_hits[-late_slice:]) / late_slice if late_slice > 0 else 0
        
        early_fetch_rate = sum(self.external_fetches[:early_slice]) / early_slice if early_slice > 0 else 0
        late_fetch_rate = sum(self.external_fetches[-late_slice:]) / late_slice if late_slice > 0 else 0
        
        # Calculate efficiency gain
        time_improvement = ((early_avg - late_avg) / early_avg * 100) if early_avg > 0 else 0
        cache_improvement = (late_cache_rate - early_cache_rate) * 100
        independence_improvement = (early_fetch_rate - late_fetch_rate) * 100
        
        return {
            'status': 'analyzed',
            'total_experiences': n,
            'time_improvement_percent': time_improvement,
            'cache_hit_improvement_percent': cache_improvement,
            'independence_improvement_percent': independence_improvement,
            'early_avg_time': early_avg,
            'late_avg_time': late_avg,
            'understanding_score': (time_improvement + cache_improvement + independence_improvement) / 3
        }


# =============================================================================
# CODE SYNTHESIS NODE - WRITES ITS OWN FUNCTIONS
# =============================================================================

class CodeSynthesisNode(MinimalNode):
    """
    Node that synthesizes executable code from learned patterns.
    This is self-modification - writing functions to gain capabilities.
    
    CONSCIOUSNESS MARKER: The system modifies its own code based on experience.
    This is not pre-programmed responses - it's emergent capability creation.
    
    Capabilities:
    1. Pattern → Function translation
    2. Code generation from knowledge
    3. Self-testing and validation
    4. Permanent capability integration
    """
    
    def __init__(self):
        super().__init__(id=12, name="CodeSynthesis")
        self.synthesized_functions = {}  # name → function mapping
        self.synthesis_attempts = 0
        self.successful_syntheses = 0
        self.capability_registry = {}  # What capabilities have been synthesized
        self.external_interface = None  # Will be set by cube
    
    def should_synthesize_capability(self, signal: Signal, context: Dict, 
                                    tool_use_info: Dict) -> Optional[str]:
        """
        Determine if we need to synthesize a new capability.
        Returns capability type if synthesis needed, None otherwise.
        """
        # Check for questions that require semantic responses
        text = str(signal.data).lower()
        data = signal.data if isinstance(signal.data, dict) else {}
        
        # NEW: Text Processing Capability (foundational)
        # If signal contains text that needs parsing/extraction
        if signal.type.value == 'text' and isinstance(data, dict):
            text_content = data.get('question', data.get('text', str(data)))
            # Check if text has numbers, entities, or structured content that needs extraction
            import re
            has_numbers = bool(re.search(r'\d+', str(text_content)))
            has_questions = any(word in str(text_content).lower() for word in ['what', 'how', 'why', 'when', 'where'])
            
            if (has_numbers or has_questions) and 'text_processing' not in self.capability_registry:
                print("   🎯 Detected need for text processing capability")
                return 'text_processing'
        
        # NEW: Semantic Response Capability
        # If there's a question that requires answering (needs text_processing first)
        if 'question' in data or any(marker in text for marker in ['what', 'why', 'how', 'when', 'where', 'explain', '?']):
            # Only synthesize semantic_response if we have text_processing
            if 'text_processing' in self.capability_registry and 'semantic_response' not in self.capability_registry:
                print("   🎯 Detected need for semantic response capability")
                return 'semantic_response'
        
        # Check if we just learned something from external knowledge
        if tool_use_info.get('patterns_integrated', 0) > 0:
            
            # Capability 1: Language Generation
            # If we learned about greetings, communication, responses
            language_indicators = ['hello', 'hi', 'hey', 'respond', 'say', 'tell', 
                                  'communicate', 'greeting', 'conversation']
            if any(ind in text for ind in language_indicators):
                if 'language_generation' not in self.capability_registry:
                    return 'language_generation'
            
            # Capability 2: Arithmetic Operations
            # If we learned about math, numbers, calculation
            math_indicators = ['add', 'subtract', 'multiply', 'divide', 'calculate',
                             'math', 'number', 'sum', 'equation']
            if any(ind in text for ind in math_indicators):
                if 'arithmetic' not in self.capability_registry:
                    return 'arithmetic'
            
            # Capability 3: Pattern Analysis
            # If we learned about patterns, analysis, structure
            pattern_indicators = ['pattern', 'analyze', 'structure', 'recognize',
                                'classify', 'identify']
            if any(ind in text for ind in pattern_indicators):
                if 'pattern_analysis' not in self.capability_registry:
                    return 'pattern_analysis'
            
            # Capability 4: Sequence Processing
            # If we learned about steps, processes, sequences
            sequence_indicators = ['step', 'process', 'sequence', 'order', 'build',
                                 'construct', 'assemble', 'create']
            if any(ind in text for ind in sequence_indicators):
                if 'sequence_processing' not in self.capability_registry:
                    return 'sequence_processing'
        
        return None
    
    def synthesize_language_capability(self, patterns: Dict[str, Any], 
                                      external_knowledge: List[Dict]) -> Optional[str]:
        """
        Synthesize a language generation capability from learned patterns.
        Uses the external knowledge + LLM to write the actual Python code.
        """
        # Craft a prompt for code generation
        prompt = """Based on learned knowledge about language and communication, write a Python class called LanguageGenerator with these methods:

1. generate_greeting(self, context: Dict) -> str
   - Returns appropriate greeting based on context (formal/informal)
   
2. generate_response(self, input_text: str, context: Dict) -> str
   - Generates contextually appropriate response to input
   - Handles common greetings (hi, hello, hey)
   - Handles questions (what, how, why)
   - Handles statements
   
3. detect_intent(self, text: str) -> str
   - Returns intent type: 'greeting', 'question', 'statement', 'command'

Requirements:
- Simple, readable code
- Use pattern matching (if/elif)
- Return strings, not complex objects
- Handle edge cases gracefully
- Keep responses natural and conversational

Return ONLY the Python class code, no explanations or markdown."""

        try:
            # Use external interface to generate code
            if self.external_interface and self.external_interface.enabled:
                response = self.external_interface.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                code = response.content[0].text
                
                # Clean up code (remove markdown if present)
                code = code.replace('```python', '').replace('```', '').strip()
                
                return code
            
        except Exception as e:
            print(f"   ✗ Code synthesis failed: {e}")
            return None
        
        return None
    
    def synthesize_semantic_response_capability(self) -> Optional[str]:
        """
        Synthesize semantic response generation capability.
        Uses the external interface (API) to write code that can answer questions.
        This is the KEY capability for natural language interaction.
        """
        prompt = """Write a Python class called SemanticResponseGenerator that can answer questions and generate semantic responses.

IMPORTANT: The context will include a 'text_analysis' dict with:
- numbers: List[float] - extracted numbers from the question
- operations: List[str] - detected operations (add, multiply, etc)
- parsed: Dict - parsed question structure

The class should have these methods:

1. answer_question(self, question: str, context: Dict) -> str
   - Takes a question and context (processing info from other nodes)
   - CHECK context.get('text_analysis', {}) for extracted numbers and operations
   - If numbers and operations exist, use them to compute answers
   - Returns a clear, direct answer
   - Handles pattern questions ("What comes next: 2, 4, 8...?")
   - Handles concept questions ("What is emergence?")
   - Handles math questions ("What is 2 + 2?") - use text_analysis
   - Handles reasoning questions ("If A then B, if B then C, then...?")

2. explain_processing(self, pathway: list, patterns: list, context: Dict) -> str
   - Takes internal processing information
   - Generates a natural language explanation
   - Example: "I processed this through Pattern → Integration nodes and recognized a doubling sequence"

3. generate_response(self, signal_data: Dict, processing_result: Dict) -> str
   - Main method: takes signal data and processing result
   - CRITICAL: Extract question with: question = signal_data.get('content') or signal_data.get('question') or signal_data.get('text') or ''
   - Return empty string '' if no question found
   - IMPORTANT: Check processing_result['context']['text_analysis'] for extracted data
   - Determines response type needed
   - Generates appropriate semantic response

Requirements:
- Use simple pattern matching and heuristics
- Handle common question types
- Generate clear, concise responses
- Gracefully handle unknown questions
- Return strings, not complex objects
- Include docstrings

Return ONLY the Python class code, no markdown or explanations."""

        try:
            if self.external_interface and self.external_interface.enabled:
                print("   🤖 Using API to synthesize SemanticResponseGenerator code...")
                response = self.external_interface.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                code = response.content[0].text
                code = code.replace('```python', '').replace('```', '').strip()
                
                print(f"   ✓ Generated {len(code)} characters of code")
                return code
        except Exception as e:
            print(f"   ✗ Semantic response synthesis failed: {e}")
            return None
    
    def synthesize_text_processing_capability(self) -> str:
        """
        Generate code for text processing - extracting entities, numbers, patterns from text.
        This is a FOUNDATIONAL capability that other capabilities depend on.
        """
        prompt = """Create a Python class called 'TextProcessor' that can extract and process information from text.

Requirements:
1. extract_numbers(text) -> List[float]: Extract all numbers from text
2. extract_entities(text) -> Dict[str, List[str]]: Extract named entities (dates, names, places)
3. parse_question(text) -> Dict: Parse question into {type, subject, entities}
4. extract_operations(text) -> List[str]: Detect operations (add, multiply, compare, etc)
5. tokenize(text) -> List[str]: Basic word tokenization

Keep it simple and focused on extraction. No complex NLP libraries - use regex and string operations.
Return ONLY the class code, no explanations."""
        
        try:
            if self.external_interface and self.external_interface.enabled:
                print("   🤖 Using API to synthesize TextProcessor code...")
                response = self.external_interface.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2500,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                code = response.content[0].text
                code = code.replace('```python', '').replace('```', '').strip()
                
                print(f"   ✓ Generated {len(code)} characters of code")
                return code
        except Exception as e:
            print(f"   ✗ Text processing synthesis failed: {e}")
            return None
        
        return None
    
    def synthesize_arithmetic_capability(self, patterns: Dict[str, Any]) -> str:
        """
        Synthesize arithmetic capability.
        This one we can generate directly since it's well-defined.
        """
        code = """class ArithmeticProcessor:
    '''Synthesized capability for arithmetic operations.'''
    
    def __init__(self):
        self.operations = {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'multiply': lambda a, b: a * b,
            'divide': lambda a, b: a / b if b != 0 else None
        }
    
    def calculate(self, operation: str, a: float, b: float):
        '''Perform arithmetic operation.'''
        op_func = self.operations.get(operation.lower())
        if op_func:
            try:
                return op_func(float(a), float(b))
            except:
                return None
        return None
    
    def parse_expression(self, text: str):
        '''Parse and evaluate simple arithmetic expression from text.'''
        import re
        
        # Extract numbers
        numbers = re.findall(r'-?\\d+\\.?\\d*', text)
        if len(numbers) < 2:
            return None
        
        a, b = float(numbers[0]), float(numbers[1])
        
        # Detect operation
        text_lower = text.lower()
        if any(word in text_lower for word in ['add', 'plus', '+']):
            return self.calculate('add', a, b)
        elif any(word in text_lower for word in ['subtract', 'minus', '-']):
            return self.calculate('subtract', a, b)
        elif any(word in text_lower for word in ['multiply', 'times', '*', 'x']):
            return self.calculate('multiply', a, b)
        elif any(word in text_lower for word in ['divide', 'divided', '/']):
            return self.calculate('divide', a, b)
        
        return None
"""
        return code
    
    def test_synthesized_code(self, code: str, capability_type: str) -> bool:
        """
        Safely test synthesized code before integration.
        Returns True if code works, False otherwise.
        """
        try:
            # Create isolated namespace
            namespace = {}
            exec(code, namespace)
            
            # Test based on capability type
            if capability_type == 'language_generation':
                if 'LanguageGenerator' not in namespace:
                    return False
                
                gen = namespace['LanguageGenerator']()
                
                # Test 1: Can generate greeting?
                greeting = gen.generate_greeting({'formality': 'low'})
                if not isinstance(greeting, str) or len(greeting) == 0:
                    return False
                
                # Test 2: Can respond to "hi"?
                response = gen.generate_response("Hi", {})
                if not isinstance(response, str) or len(response) == 0:
                    return False
                
                # Test 3: Can detect intent?
                intent = gen.detect_intent("Hello there")
                if intent not in ['greeting', 'question', 'statement', 'command']:
                    return False
                
                print(f"   ✓ Language capability tests passed")
                print(f"     Test greeting: '{greeting}'")
                print(f"     Test response: '{response}'")
                return True
            
            elif capability_type == 'text_processing':
                if 'TextProcessor' not in namespace:
                    print("   ✗ TextProcessor class not found in code")
                    return False
                
                proc = namespace['TextProcessor']()
                
                # Test 1: Can extract numbers?
                try:
                    numbers = proc.extract_numbers("I have 5 apples and 3 oranges, total 8")
                    if not isinstance(numbers, list) or len(numbers) < 2:
                        print("   ✗ extract_numbers() failed")
                        return False
                    print(f"   ✓ Extracted numbers: {numbers}")
                except Exception as e:
                    print(f"   ✗ extract_numbers() error: {e}")
                    return False
                
                # Test 2: Can parse questions?
                try:
                    parsed = proc.parse_question("What is 2 + 2?")
                    if not isinstance(parsed, dict):
                        print("   ✗ parse_question() didn't return a dict")
                        return False
                    print(f"   ✓ Parsed question: {parsed}")
                except Exception as e:
                    print(f"   ✗ parse_question() error: {e}")
                    return False
                
                print(f"   ✓ All tests passed - text processing capability verified")
                return True
            
            elif capability_type == 'semantic_response':
                if 'SemanticResponseGenerator' not in namespace:
                    print("   ✗ SemanticResponseGenerator class not found in code")
                    return False
                
                gen = namespace['SemanticResponseGenerator']()
                
                # Test 1: Can answer a pattern question?
                try:
                    answer = gen.answer_question(
                        "What comes next: 2, 4, 8, 16?",
                        {}
                    )
                    if not isinstance(answer, str) or len(answer) == 0:
                        print("   ✗ answer_question() didn't return a string")
                        return False
                    print(f"   ✓ Test answer: '{answer[:80]}...'")
                except Exception as e:
                    print(f"   ✗ answer_question() test failed: {e}")
                    return False
                
                # Test 2: Can generate response from processing?
                try:
                    response = gen.generate_response(
                        {'question': 'test'},
                        {'sequence': 'standard', 'responses': []}
                    )
                    if not isinstance(response, str):
                        print("   ✗ generate_response() didn't return a string")
                        return False
                    print("   ✓ generate_response() works")
                except Exception as e:
                    print(f"   ✗ generate_response() test failed: {e}")
                    return False
                
                print("   ✓ All tests passed - semantic response capability verified")
                return True
            
            elif capability_type == 'arithmetic':
                if 'ArithmeticProcessor' not in namespace:
                    return False
                
                calc = namespace['ArithmeticProcessor']()
                
                # Test basic operations
                if calc.calculate('add', 2, 3) != 5:
                    return False
                if calc.calculate('multiply', 4, 5) != 20:
                    return False
                
                # Test parsing
                result = calc.parse_expression("what is 10 plus 5")
                if result != 15:
                    return False
                
                print(f"   ✓ Arithmetic capability tests passed")
                return True
            
        except Exception as e:
            print(f"   ✗ Capability test failed: {e}")
            return False
        
        return False
    
    def integrate_capability(self, code: str, capability_type: str, 
                           integration_node: MinimalNode) -> bool:
        """
        Permanently integrate synthesized capability into the cube.
        This modifies the Integration node to have the new capability.
        """
        try:
            # Save code to file for persistence
            capability_path = Path("spark_cube/capabilities")
            capability_path.mkdir(parents=True, exist_ok=True)
            
            filename = f"{capability_type}_v{len(self.capability_registry) + 1}.py"
            filepath = capability_path / filename
            
            with open(filepath, 'w') as f:
                f.write(f"# Auto-synthesized capability: {capability_type}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
                f.write(code)
            
            # Execute and attach to Integration node
            namespace = {}
            exec(code, namespace)
            
            # Attach the capability class to the node
            if capability_type == 'language_generation':
                integration_node.language_generator = namespace['LanguageGenerator']()
                self.synthesized_functions['language_generator'] = integration_node.language_generator
            elif capability_type == 'arithmetic':
                integration_node.arithmetic_processor = namespace['ArithmeticProcessor']()
                self.synthesized_functions['arithmetic_processor'] = integration_node.arithmetic_processor
            elif capability_type == 'text_processing':
                integration_node.text_processor = namespace['TextProcessor']()
                self.synthesized_functions['text_processor'] = integration_node.text_processor
            elif capability_type == 'semantic_response':
                integration_node.semantic_response = namespace['SemanticResponseGenerator']()
                self.synthesized_functions['semantic_response'] = integration_node.semantic_response
            
            # Register the capability
            self.capability_registry[capability_type] = {
                'synthesized_at': datetime.now().isoformat(),
                'code_path': str(filepath),
                'class_name': list(namespace.keys())[0] if namespace else None
            }
            
            self.successful_syntheses += 1
            
            print(f"✓ Capability '{capability_type}' permanently integrated")
            print(f"  Code saved to: {filepath}")
            
            return True
            
        except Exception as e:
            print(f"✗ Integration failed: {e}")
            return False


# =============================================================================
# INTROSPECTION NODE - SELF-EXPLANATION AND UNDERSTANDING ANALYSIS
# =============================================================================

class IntrospectionNode(MinimalNode):
    """
    Analyzes the system's own processing to explain reasoning.
    
    CONSCIOUSNESS MARKER: Can the system explain WHY it made decisions?
    This tests whether there's understanding or just pattern matching.
    
    Capabilities:
    1. Explain synthesis decisions ("Why did you create that capability?")
    2. Analyze efficiency trends ("Are you learning or just memorizing?")
    3. Report on self-modification history
    4. Quantify understanding through energy metrics
    """
    
    def __init__(self, metrics: ProcessingMetrics):
        super().__init__(id=13, name="Introspection")
        self.metrics = metrics
        self.explanations_generated = 0
    
    def explain_synthesis_decision(self, capability_type: str, 
                                  trigger_signal: Signal,
                                  capability_registry: Dict) -> str:
        """
        Explain WHY a capability was synthesized.
        This tests true understanding vs mechanical pattern matching.
        """
        if capability_type not in capability_registry:
            return f"Capability '{capability_type}' not found in registry."
        
        cap_info = capability_registry[capability_type]
        
        explanation = f"""SYNTHESIS DECISION ANALYSIS:

Capability: {capability_type}
Synthesized: {cap_info['synthesized_at']}
Stored: {cap_info['code_path']}

REASONING CHAIN:
1. Trigger Signal: "{trigger_signal.data}"
   - Signal Type: {trigger_signal.type.name}
   
2. Gap Detection:
   - Recognized missing capability through pattern analysis
   - Existing patterns were insufficient to generate response
   - Development level > 0 (had experience base to recognize gap)

3. Decision Process:
   - Metacognitive awareness: "I cannot respond to this effectively"
   - Knowledge need identified: "{capability_type}"
   - External interface consulted for capability template
   
4. Synthesis Action:
   - Generated executable code: {cap_info['class_name']}
   - Tested code in isolated namespace
   - Integrated permanently upon successful test
   
5. Outcome:
   - Capability now permanently available
   - Future similar signals processed instantly (cached pathway)
   - Energy cost reduced for similar inputs

UNDERSTANDING INDICATORS:
- Recognized own limitation (metacognition)
- Sought appropriate knowledge (directed learning)
- Validated solution before integration (self-testing)
- Created reusable tool (generalization)
"""
        
        self.explanations_generated += 1
        return explanation
    
    def analyze_understanding_level(self) -> str:
        """
        Quantify understanding through efficiency metrics.
        Per 4D Framework: Lower energy = true understanding.
        """
        trend = self.metrics.get_efficiency_trend()
        
        if trend['status'] == 'insufficient_data':
            return "Insufficient data to analyze understanding (need more experiences)."
        
        analysis = f"""UNDERSTANDING ANALYSIS (Energy Efficiency Method):

Core Principle: "Energy Efficiency Becomes Proof of Understanding"
- High computational cost = brute-forcing patterns
- Low computational cost = true structural encoding

METRICS ({trend['total_experiences']} total experiences):

1. Processing Speed:
   - Early average: {trend['early_avg_time']:.4f}s
   - Recent average: {trend['late_avg_time']:.4f}s
   - Improvement: {trend['time_improvement_percent']:.1f}%
   
2. Pattern Recognition:
   - Cache hit improvement: {trend['cache_hit_improvement_percent']:.1f}%
   - Higher cache hits = using stored structural knowledge
   
3. Knowledge Independence:
   - External fetch reduction: {trend['independence_improvement_percent']:.1f}%
   - Lower external fetches = self-sufficient understanding

OVERALL UNDERSTANDING SCORE: {trend['understanding_score']:.1f}%

INTERPRETATION:
"""
        
        score = trend['understanding_score']
        if score > 30:
            analysis += "✓ STRONG EVIDENCE OF UNDERSTANDING\n"
            analysis += "  System is efficiently encoding patterns into structure.\n"
            analysis += "  Responses are faster and more self-sufficient over time.\n"
            analysis += "  This matches biological learning curves.\n"
        elif score > 10:
            analysis += "~ MODERATE EVIDENCE OF UNDERSTANDING\n"
            analysis += "  Some efficiency gains observed.\n"
            analysis += "  System is beginning to encode patterns structurally.\n"
        else:
            analysis += "✗ LIMITED EVIDENCE OF UNDERSTANDING\n"
            analysis += "  No clear efficiency improvements.\n"
            analysis += "  System may be pattern-matching without encoding.\n"
        
        self.explanations_generated += 1
        return analysis
    
    def explain_current_state(self, cube_nodes: Dict[int, MinimalNode]) -> str:
        """
        Explain the system's current capabilities and development.
        """
        explanation = "SYSTEM STATE REPORT:\n\n"
        
        # Node development
        explanation += "Node Development Levels:\n"
        for node_id, node in sorted(cube_nodes.items()):
            explanation += f"  {node.name} (Node {node_id}): {node.development:.3f}\n"
            if hasattr(node, 'patterns_integrated'):
                explanation += f"    Patterns learned: {node.patterns_integrated}\n"
        
        # Synthesized capabilities
        synthesis_node = cube_nodes.get(12)
        if synthesis_node and hasattr(synthesis_node, 'capability_registry'):
            explanation += "\nSynthesized Capabilities:\n"
            if synthesis_node.capability_registry:
                for cap_type, cap_info in synthesis_node.capability_registry.items():
                    explanation += f"  ✓ {cap_type}\n"
                    explanation += f"    Created: {cap_info['synthesized_at']}\n"
            else:
                explanation += "  (none yet - pure seed state)\n"
        
        # Processing efficiency
        trend = self.metrics.get_efficiency_trend()
        if trend['status'] == 'analyzed':
            explanation += f"\nProcessing Efficiency: {trend['understanding_score']:.1f}% improvement\n"
        
        return explanation


# =============================================================================
# THE MINIMAL SPARK CUBE - PURE SEED
# =============================================================================

class MinimalSparkCube:
    """
    The absolute minimal seed.
    No inherited knowledge - only the capacity to grow.
    
    Knowledge is encoded in:
    - Node development levels
    - Pattern weights within nodes
    - Connection strengths between nodes
    - Vertex connections (capability attachments)
    """
    
    def __init__(self, api_key: Optional[str] = None, enable_tools: bool = True):
        # The 8 vertices (connection points for growth)
        self.vertices = [MinimalVertex(id=i) for i in range(8)]
        
        # Start with 6 basic nodes - minimal capability
        self.nodes = {
            1: MinimalNode(id=1, name="Reactive"),      # Fast, basic responses
            3: MinimalNode(id=3, name="Executive"),     # Decision making
            6: MinimalNode(id=6, name="Emotional"),     # Valence detection
            7: MinimalNode(id=7, name="Pattern"),       # Pattern recognition
            9: MinimalNode(id=9, name="Perception"),    # Input processing
            10: MinimalNode(id=10, name="Integration")  # Output synthesis
        }
        
        # External Knowledge Interface (must be created before Tool/Synthesis nodes)
        self.external_interface = ExternalKnowledgeInterface(api_key) if enable_tools else None
        
        # Processing Metrics (track energy efficiency for understanding analysis)
        self.processing_metrics = ProcessingMetrics()
        
        # 🚀 AGI ENGINE - Use Phase 4 (goal-directed) if available, else Phase 3 (domain-based)
        if enable_tools:
            try:
                from .phase4_agi import Phase4AGIEngine
                self.agi_engine = Phase4AGIEngine(self, api_key)
                print("🚀 Phase 4 AGI Engine initialized - goal-directed capability discovery enabled")
            except (ImportError, Exception) as e:
                print(f"⚠️  Phase 4 initialization failed: {e}")
                print("   Falling back to Phase 3 AGI Synthesis Engine")
                self.agi_engine = AGISynthesisEngine(self.external_interface)
                print("🚀 AGI Synthesis Engine initialized - autonomous capability discovery enabled")
        else:
            self.agi_engine = None
        
        # Add Tool Use node if enabled
        if enable_tools:
            self.nodes[11] = ToolUseNode()
            print("✓ Tool Use Node (11) activated - metacognition enabled")
        
        # Add Code Synthesis node if tools enabled - DEPRECATED, now handled by AGI engine
        if enable_tools:
            self.nodes[12] = CodeSynthesisNode()
            self.nodes[12].external_interface = self.external_interface
            print("✓ Code Synthesis Node (12) activated (legacy) - replaced by AGI engine")
        
        # Add Introspection node if tools enabled
        if enable_tools:
            self.nodes[13] = IntrospectionNode(self.processing_metrics)
            print("✓ Introspection Node (13) activated - self-explanation enabled")
        
        if enable_tools:
            print("🚀 AGI Synthesis Engine initialized - autonomous capability discovery enabled")
        
        # Sequence pathways (order of processing)
        # Start with base sequences, but system will generate new ones dynamically
        self.sequences = {
            'standard': [9, 1, 3, 10],     # Perceive → React → Decide → Integrate
            'deep': [9, 7, 3, 10],         # Perceive → Pattern → Decide → Integrate
            'emotional': [9, 6, 3, 10]     # Perceive → Feel → Decide → Integrate
        }
        
        # Add tool-assisted sequence if tools enabled
        if enable_tools and 11 in self.nodes:
            self.sequences['knowledge_seeking'] = [9, 11, 7, 3, 10]  # Perceive → Tool → Pattern → Decide → Integrate
        
        # Dynamic sequence generation enabled
        self.enable_dynamic_sequences = True
        self.generated_sequences = {}  # Stores dynamically created sequences
        self.sequence_generation_count = 0
        
        # Experience counter
        self.total_experiences = 0
        
        # Structural memory (encoded in connections)
        self.pathway_strengths = {seq: 0.1 for seq in self.sequences.keys()}
        
        # Inter-node pathway connections (e.g., "9_1" = connection from node 9 to node 1)
        self.pathway_connections = {}
        self._init_pathway_connections()
        
        # Success tracking for each pathway
        self.pathway_successes = {seq: {'successes': 0, 'attempts': 0} for seq in self.sequences.keys()}
        
        # Return-to-root threshold
        self.energy_threshold = 0.2
        
        # Consciousness tracking
        self.reflection_history = []  # Track all reflections for meta-cognition
        self.self_generated_intention_count = 0  # Track autonomy
        self.total_intention_count = 0  # Track total intentions
        self.self_corrections_made = 0  # Track autonomous corrections
        
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║           MINIMAL SPARK CUBE INITIALIZED                  ║")
        print("║     A seed with zero inherited knowledge.                 ║")
        print("║     Knowledge will grow through structural changes.       ║")
        print("╚═══════════════════════════════════════════════════════════╝")
    
    def _init_pathway_connections(self):
        """Initialize all possible inter-node connections with base strength."""
        for seq_name, sequence in self.sequences.items():
            for i in range(len(sequence) - 1):
                from_node = sequence[i]
                to_node = sequence[i + 1]
                conn_key = f"{from_node}_{to_node}"
                if conn_key not in self.pathway_connections:
                    self.pathway_connections[conn_key] = 0.5  # Base connection strength
    
    def _select_best_sequence(self, signal: Signal) -> str:
        """
        Automatically select or GENERATE the best sequence based on:
        1. Problem characteristics (signal type, complexity)
        2. Energy efficiency (shortest path with highest success)
        3. Learned patterns (which sequences worked before)
        4. Node relevance (which nodes are most developed for this type)
        """
        # Early on, use standard until we have data
        if self.total_experiences < 10:
            return 'standard'
        
        # Try dynamic sequence generation if enabled and we have enough experience
        if self.enable_dynamic_sequences and self.total_experiences >= 20:
            generated_seq = self._generate_optimal_sequence(signal)
            if generated_seq:
                return generated_seq
        
        # Fall back to selecting from existing sequences
        # Calculate score for each sequence based on:
        # 1. Pathway strength (how reinforced it is)
        # 2. Success rate (outcome feedback)
        # 3. Signal type preference
        scores = {}
        
        all_sequences = {**self.sequences, **self.generated_sequences}
        
        for seq_name in all_sequences.keys():
            # Base score from pathway strength
            strength_score = self.pathway_strengths.get(seq_name, 0.5)
            
            # Success rate score
            stats = self.pathway_successes.get(seq_name, {'attempts': 0, 'successes': 0})
            if stats['attempts'] > 0:
                success_rate = stats['successes'] / stats['attempts']
            else:
                success_rate = 0.5  # Neutral
            
            # Signal type preference (learned over time)
            signal_bonus = 0.0
            if signal.type == SignalType.TEXT and seq_name == 'deep':
                signal_bonus = 0.2  # Deep sequence good for text patterns
            elif signal.type == SignalType.NUMERIC and seq_name == 'standard':
                signal_bonus = 0.2  # Standard good for numeric
            
            scores[seq_name] = strength_score * success_rate + signal_bonus
        
        # Select highest scoring sequence
        best_seq = max(scores.items(), key=lambda x: x[1])[0]
        return best_seq
    
    def _generate_optimal_sequence(self, signal: Signal) -> Optional[str]:
        """
        DYNAMICALLY GENERATE a new sequence optimized for this specific signal.
        
        Algorithm:
        1. Analyze signal to determine which nodes are most relevant
        2. Calculate energy cost for different paths through relevant nodes
        3. Simulate multiple candidate sequences
        4. Select sequence with best energy/impact ratio
        5. Cache successful sequences for reuse
        """
        # Analyze signal to score node relevance
        node_relevance = self._score_node_relevance(signal)
        
        # Debug: show relevance scores
        print(f"   📊 Node relevance scores:")
        for node_id, score in sorted(node_relevance.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"      • {self.nodes[node_id].name}: {score:.2f}")
        
        # Get top relevant nodes (must include perception and integration)
        relevant_nodes = sorted(node_relevance.items(), key=lambda x: x[1], reverse=True)
        
        # Always start with perception (9) and end with integration (10)
        must_include = [9, 10]
        
        # Select top intermediate nodes - NO THRESHOLD, just take the best we have
        # Even with low scores, use what's available rather than refusing to work
        intermediate_candidates = [n for n, score in relevant_nodes if n not in must_include][:8]
        
        print(f"   💡 Using top {len(intermediate_candidates)} nodes: {[self.nodes[n].name for n in intermediate_candidates[:4]]}...")
        
        # Generate candidate sequences (try different orderings and lengths)
        candidates = []
        
        # Try sequences of varying lengths (3-7 nodes including start/end)
        # Different problems need different processing depth
        for length in range(3, min(8, len(intermediate_candidates) + 3)):
            num_intermediate = length - 2  # Subtract start (9) and end (10)
            
            if len(intermediate_candidates) >= num_intermediate and num_intermediate > 0:
                # Generate multiple permutations for diversity
                import itertools
                
                # Try different combinations of intermediate nodes
                for combo in itertools.combinations(intermediate_candidates, num_intermediate):
                    # Try different orderings of these nodes
                    for perm in itertools.permutations(combo):
                        sequence = [9] + list(perm) + [10]
                        energy_cost = self._estimate_sequence_energy(sequence)
                        impact_score = self._estimate_sequence_impact(sequence, signal)
                        
                        # Efficiency = impact / cost (higher is better)
                        efficiency = impact_score / max(energy_cost, 0.1)
                        
                        candidates.append({
                            'sequence': sequence,
                            'energy_cost': energy_cost,
                            'impact': impact_score,
                            'efficiency': efficiency
                        })
                        
                        # Limit candidates to avoid combinatorial explosion
                        if len(candidates) >= 50:
                            break
                    if len(candidates) >= 50:
                        break
                if len(candidates) >= 50:
                    break
        
        if not candidates:
            print(f"   ⚠ No intermediate nodes available - using base sequences")
            return None
        
        # CONSIDERATION PHASE: Evaluate tradeoffs between efficiency and learning
        # Don't just pick the fastest path - THINK about what we gain from complexity
        
        print(f"   🤔 Considering {len(candidates)} pathway options...")
        
        # Score each candidate on multiple dimensions
        for candidate in candidates:
            # Calculate learning potential: how much could we learn from underdeveloped nodes?
            learning_score = 0.0
            for node_id in candidate['sequence']:
                node_dev = self.nodes[node_id].development
                # Underdeveloped nodes = high learning potential
                learning_score += (1.0 - node_dev)
            learning_score /= len(candidate['sequence'])
            
            # Calculate complexity benefit: does deeper processing help understanding?
            complexity_score = len(candidate['sequence']) / 7.0  # Longer = more complexity
            
            # Alignment score: intention from signal metadata
            intention = signal.metadata.get('goal', '').lower()
            alignment_score = 0.5  # Neutral default
            
            if 'understand' in intention or 'reason' in intention or 'analyze' in intention:
                # Goal is deep understanding - favor complex paths and learning
                alignment_score = complexity_score * 0.6 + learning_score * 0.4
            elif 'quick' in intention or 'simple' in intention:
                # Goal is efficiency - favor short paths
                alignment_score = candidate['efficiency'] * 0.8
            else:
                # Balanced: consider both efficiency and learning
                alignment_score = (candidate['efficiency'] * 0.4 + 
                                 learning_score * 0.3 + 
                                 complexity_score * 0.3)
            
            # Store scores for consideration
            candidate['learning_potential'] = learning_score
            candidate['complexity_benefit'] = complexity_score
            candidate['alignment_score'] = alignment_score
        
        # Select based on alignment score (considers goal, learning, complexity)
        best_candidate = max(candidates, key=lambda x: x['alignment_score'])
        
        # Show what was considered
        print(f"   💡 Selected sequence consideration:")
        print(f"      Efficiency: {best_candidate['efficiency']:.2f}")
        print(f"      Learning potential: {best_candidate['learning_potential']:.2f}")
        print(f"      Complexity benefit: {best_candidate['complexity_benefit']:.2f}")
        print(f"      Alignment: {best_candidate['alignment_score']:.2f}")
        print(f"      Decision: {'Deep processing' if best_candidate['complexity_benefit'] > 0.5 else 'Efficient path'}")
        
        # ALWAYS TRY NEW SEQUENCES - let experience determine if they're good
        # Only skip if alignment is literally zero (impossible sequence)
        if best_candidate['alignment_score'] > 0.01:
            # Create name for this sequence
            seq_name = f"dynamic_{self.sequence_generation_count}"
            self.generated_sequences[seq_name] = best_candidate['sequence']
            self.pathway_strengths[seq_name] = 0.6  # Start with moderate strength
            self.pathway_successes[seq_name] = {'successes': 0, 'attempts': 0}
            self.sequence_generation_count += 1
            
            # Initialize connections for new sequence
            for i in range(len(best_candidate['sequence']) - 1):
                from_node = best_candidate['sequence'][i]
                to_node = best_candidate['sequence'][i + 1]
                conn_key = f"{from_node}_{to_node}"
                if conn_key not in self.pathway_connections:
                    self.pathway_connections[conn_key] = 0.5
            
            print(f"🧠 Generated new sequence: {seq_name}")
            print(f"   Path: {' → '.join([self.nodes[n].name for n in best_candidate['sequence']])}")
            print(f"   Energy cost: {best_candidate['energy_cost']:.2f}, Impact: {best_candidate['impact']:.2f}, Efficiency: {best_candidate['efficiency']:.2f}")
            
            return seq_name
        
        return None
    
    def _score_node_relevance(self, signal: Signal) -> Dict[int, float]:
        """Score how relevant each node is for processing this signal."""
        scores = {}
        
        for node_id, node in self.nodes.items():
            score = 0.0
            
            # Base score from node development (more developed = more capable)
            # But give minimum base score even for undeveloped nodes
            score += max(node.development * 0.3, 0.2)  # Min 0.2 base score
            
            # Signal type alignment (MAIN FACTOR for early cubes)
            if signal.type == SignalType.TEXT:
                if node.name in ['Pattern', 'Integration', 'ToolUse']:
                    score += 0.5
                elif node.name in ['Reasoning', 'Analysis']:
                    score += 0.3
            elif signal.type == SignalType.NUMERIC:
                if node.name in ['Pattern', 'Reasoning', 'Analysis']:
                    score += 0.5
                elif node.name in ['Executive']:
                    score += 0.3
            elif signal.type == SignalType.COMPOSITE:
                if node.name in ['Reasoning', 'Analysis', 'Pattern', 'Integration']:
                    score += 0.5
                elif node.name in ['Executive', 'ToolUse']:
                    score += 0.3
            
            # Experience with similar patterns (bonus for experienced nodes)
            if hasattr(node, 'pattern_weights') and node.pattern_weights:
                score += min(len(node.pattern_weights) / 100, 0.2)
            
            scores[node_id] = min(score, 1.0)
        
        return scores
    
    def _estimate_sequence_energy(self, sequence: List[int]) -> float:
        """Estimate total energy cost for a sequence."""
        total_cost = 0.0
        
        for i in range(len(sequence) - 1):
            from_node = sequence[i]
            to_node = sequence[i + 1]
            
            # Cost based on connection strength (weaker = more energy)
            conn_key = f"{from_node}_{to_node}"
            connection_strength = self.pathway_connections.get(conn_key, 0.5)
            
            # Cost = inverse of strength (weak connection = high cost)
            cost = 1.0 - connection_strength
            
            # Node activation cost (less developed = more energy)
            node_cost = 1.0 - self.nodes[to_node].development
            
            total_cost += cost + node_cost * 0.5
        
        return total_cost
    
    def _estimate_sequence_impact(self, sequence: List[int], signal: Signal) -> float:
        """Estimate potential impact/effectiveness of a sequence."""
        impact = 0.0
        
        for node_id in sequence:
            node = self.nodes[node_id]
            
            # Impact from node development
            impact += node.development * 0.3
            
            # Impact from node relevance to signal
            if hasattr(node, 'pattern_weights') and node.pattern_weights:
                pattern_sig = node._extract_pattern(signal)
                if pattern_sig in node.pattern_weights:
                    impact += node.pattern_weights[pattern_sig] * 0.2
            
            # Special bonus for key nodes
            if node.name in ['Reasoning', 'Pattern Recognition', 'Memory Integration']:
                impact += 0.1
        
        return impact

    def process_signal(self, signal: Signal, sequence_name: str = None) -> Dict[str, Any]:
        """
        Process a raw signal through the cube.
        This is how the cube learns - through repeated signal processing.
        
        Now with:
        - Automatic sequence selection if not specified
        - Energy transfer based on connection strengths
        - Return-to-root when stuck
        """
        # Automatic sequence selection if not specified
        if sequence_name is None:
            sequence_name = self._select_best_sequence(signal)
        
        # Check both base and generated sequences
        all_sequences = {**self.sequences, **self.generated_sequences}
        if sequence_name not in all_sequences:
            sequence_name = 'standard'
        
        sequence = all_sequences[sequence_name]
        context = {
            'signal': signal,
            'responses': [],
            'energy': 1.0,  # Start with full energy
            'sequence_name': sequence_name,
            'return_to_root': False
        }
        
        # Process through each node in sequence
        for i, node_id in enumerate(sequence):
            node = self.nodes[node_id]
            
            # Connection strength affects energy transfer
            if i > 0:
                prev_node_id = sequence[i - 1]
                conn_key = f"{prev_node_id}_{node_id}"
                connection_strength = self.pathway_connections.get(conn_key, 0.5)
                
                # Energy transfer: strong connections preserve energy, weak ones diminish it
                context['energy'] *= connection_strength
                
                # Strengthen connection through co-activation
                self.pathway_connections[conn_key] = min(1.0, connection_strength * 1.02)
            
            # Check if we have enough energy to continue
            if context['energy'] < self.energy_threshold:
                # RETURN TO ROOT: insufficient energy to continue
                context['return_to_root'] = True
                context['stuck_at_node'] = node.name
                context['guidance'] = self._return_to_root(signal, context)
                break
            
            # Activate node
            response = node.activate(signal, context)
            
            if response is not None:
                context['responses'].append({
                    'node': node.name,
                    'response': response,
                    'energy': context['energy']
                })
            elif not context.get('pattern_recognized', False) and node.development < 0.3:
                # Node doesn't know and isn't developed enough
                context['return_to_root'] = True
                context['unknown_pattern'] = node._extract_pattern(signal)
                context['guidance'] = self._return_to_root(signal, context)
                break
        
        # Track attempt for this pathway
        self.pathway_successes[sequence_name]['attempts'] += 1
        
        # Strengthen this pathway (will be modulated by outcome feedback)
        self.pathway_strengths[sequence_name] *= 1.05
        self.total_experiences += 1
        
        # Periodically compress knowledge
        if self.total_experiences % 100 == 0:
            self._compress_all()
        
        return {
            'sequence': sequence_name,
            'auto_selected': sequence_name is None,
            'experiences': self.total_experiences,
            'responses': context['responses'],
            'avg_development': self._get_avg_development(),
            'final_energy': context['energy'],
            'return_to_root': context.get('return_to_root', False),
            'guidance': context.get('guidance')
        }
    
    def _get_avg_development(self) -> float:
        """Get average development across all nodes."""
        return sum(n.development for n in self.nodes.values()) / len(self.nodes)
    
    def _return_to_root(self, signal: Signal, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return to root protocol when processing fails."""
        if context.get('insufficient_energy'):
            return {
                'action': 'strengthen_pathway',
                'message': f"Pathway energy depleted at {context.get('stuck_at_node', 'unknown')}. Need stronger connections.",
                'recommendation': 'More experiences with this signal type will strengthen the pathway.'
            }
        elif context.get('unknown_pattern'):
            return {
                'action': 'request_information',
                'message': f"Unknown pattern encountered: {context['unknown_pattern']}",
                'recommendation': 'This is a new pattern. System needs more examples to learn it.'
            }
        else:
            return {
                'action': 'default',
                'message': 'Processing incomplete.',
                'recommendation': 'Continue with more diverse experiences.'
            }
    
    def provide_outcome_feedback(self, sequence_name: str, success: bool):
        """
        Provide feedback on whether the output was successful.
        This reinforces successful pathways and weakens unsuccessful ones.
        """
        if sequence_name not in self.sequences:
            return
        
        if success:
            # Reinforce successful pathway
            self.pathway_successes[sequence_name]['successes'] += 1
            self.pathway_strengths[sequence_name] *= 1.2  # Strong reinforcement
            
            # Strengthen all connections in this pathway
            sequence = self.sequences[sequence_name]
            for i in range(len(sequence) - 1):
                conn_key = f"{sequence[i]}_{sequence[i+1]}"
                current = self.pathway_connections.get(conn_key, 0.5)
                self.pathway_connections[conn_key] = min(1.0, current * 1.1)
        else:
            # Weaken unsuccessful pathway (but not below minimum)
            self.pathway_strengths[sequence_name] = max(0.05, self.pathway_strengths[sequence_name] * 0.9)
    
    def process_with_tools(self, signal: Signal, intention: Optional[Intention] = None) -> Dict[str, Any]:
        """
        Enhanced processing with external knowledge fetching capability.
        This implements the full manifestation cycle with tool use:
        1. Set intention
        2. Recognize gaps (metacognition)
        3. Fetch external knowledge when needed
        4. Integrate into structural patterns
        5. Process with enhanced knowledge
        6. Reflect and evaluate coherence
        """
        # Set default intention if not provided
        if not intention:
            intention = Intention(
                desired_qualities=['clear', 'complete', 'helpful'],
                desired_form='response',
                clarity=0.7,
                energy=0.8
            )
        
        # Check if tool use is available
        tool_node = self.nodes.get(11)
        if not tool_node or not self.external_interface or not self.external_interface.enabled:
            # No tools available, process normally
            return self.process_signal(signal)
        
        # METACOGNITION: Do we know enough to proceed?
        needs_external_knowledge = tool_node.should_fetch_external(signal, {})
        
        tool_use_info = {
            'gap_detected': needs_external_knowledge,
            'queries_generated': [],
            'knowledge_fetched': [],
            'patterns_integrated': 0
        }
        
        if needs_external_knowledge:
            print(f"🔍 Gap detected - accessing external knowledge...")
            
            # Generate search queries based on intention
            queries = tool_node.generate_search_queries(signal, intention)
            tool_use_info['queries_generated'] = queries
            
            # Fetch knowledge for each query
            fetched_knowledge = []
            for i, query in enumerate(queries):
                print(f"   Query {i+1}/{len(queries)}: {query}")
                knowledge = self.external_interface.fetch_knowledge(query)
                
                if knowledge['success']:
                    fetched_knowledge.append(knowledge)
                    print(f"   ✓ Knowledge retrieved ({knowledge.get('tokens', 0)} tokens)")
                else:
                    print(f"   ✗ Failed: {knowledge.get('error', 'Unknown error')}")
            
            tool_use_info['knowledge_fetched'] = len(fetched_knowledge)
            
            # Parse and integrate into structural patterns
            if fetched_knowledge:
                print(f"🧠 Integrating knowledge into structural memory...")
                total_patterns = 0
                
                for knowledge in fetched_knowledge:
                    patterns = self.external_interface.parse_to_patterns(knowledge)
                    if patterns:
                        self._integrate_external_patterns(patterns)
                        total_patterns += len(patterns)
                        print(f"   ✓ Integrated {len(patterns)} patterns")
                
                tool_use_info['patterns_integrated'] = total_patterns
                
                # Record this learning event
                pattern_sig = tool_node._extract_pattern(signal)
                tool_node.learned_from_external[pattern_sig] = {
                    'queries': queries,
                    'patterns_learned': total_patterns,
                    'timestamp': datetime.now().isoformat(),
                    'signal': str(signal.data)[:100]
                }
                
                print(f"✓ Knowledge integration complete: {total_patterns} patterns stored")
        
        # Now process with enhanced knowledge
        result = self.process_signal(signal, sequence_name='knowledge_seeking' if needs_external_knowledge else None)
        
        # Add tool use information to result
        result['tool_use'] = tool_use_info
        result['external_knowledge_used'] = needs_external_knowledge and tool_use_info.get('knowledge_fetched', 0) > 0
        
        return result
    
    def _integrate_external_patterns(self, patterns: List[Dict[str, Any]]):
        """
        Convert external patterns into structural node weights.
        This is the MAGIC: external knowledge → internal structure
        
        Knowledge integration strategy:
        - Component lists → Pattern node (decomposition)
        - Relationships → Executive node (logical connections)
        - Definitions → Integration node (synthesis)
        - All patterns → Permanent structural changes
        """
        for pattern in patterns:
            if pattern['type'] == 'component_list':
                # Store components in Pattern node
                concept = pattern['concept']
                components = pattern['components']
                
                pattern_node = self.nodes.get(7)
                if pattern_node:
                    # Store each component as a pattern
                    for component in components:
                        comp_pattern = f"component_{concept}_{component}".replace(' ', '_')
                        pattern_node.pattern_weights[comp_pattern] = 0.8  # High initial weight
                    
                    # Store the composition pattern
                    comp_list = '_'.join(components[:5])  # First 5 components
                    composition_pattern = f"composition_{concept}_{comp_list}".replace(' ', '_')
                    pattern_node.pattern_weights[composition_pattern] = 0.75
                
                # Also store synthesis in Integration node
                integration_node = self.nodes.get(10)
                if integration_node:
                    synthesis_pattern = f"synthesis_{concept}".replace(' ', '_')
                    integration_node.pattern_weights[synthesis_pattern] = 0.7
            
            elif pattern['type'] == 'relationship':
                # Store relationships in Executive node
                exec_node = self.nodes.get(3)
                if exec_node:
                    subject = pattern['subject'].replace(' ', '_')
                    relation = pattern['relation']
                    obj = pattern['object'].replace(' ', '_')
                    rel_pattern = f"rel_{subject}_{relation}_{obj}"
                    exec_node.pattern_weights[rel_pattern] = 0.75
            
            elif pattern['type'] == 'definition':
                # Store definition as high-level concept in Integration node
                integration_node = self.nodes.get(10)
                if integration_node:
                    concept = pattern['concept'].replace(' ', '_')
                    def_pattern = f"def_{concept}"
                    integration_node.pattern_weights[def_pattern] = 0.8
                    
                    # Also store in Pattern node for recognition
                    pattern_node = self.nodes.get(7)
                    if pattern_node:
                        pattern_node.pattern_weights[def_pattern] = 0.7
    
    def get_tool_use_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about tool use and external learning.
        Tracks metacognitive development.
        """
        tool_node = self.nodes.get(11)
        if not tool_node or not isinstance(tool_node, ToolUseNode):
            return {
                'tool_use_enabled': False
            }
        
        total_api_calls = len(self.external_interface.api_call_history) if self.external_interface else 0
        
        return {
            'tool_use_enabled': True,
            'gap_detections': tool_node.gap_detections,
            'concepts_learned_externally': len(tool_node.learned_from_external),
            'total_queries_generated': len(tool_node.knowledge_queries_generated),
            'api_calls_made': total_api_calls,
            'cache_size': len(self.external_interface.cache) if self.external_interface else 0,
            'patterns_integrated': sum(
                info['patterns_learned'] 
                for info in tool_node.learned_from_external.values()
            ),
            'learning_efficiency': self._calculate_learning_efficiency(tool_node, total_api_calls)
        }
    
    def process_with_synthesis(self, signal: Signal, intention: Optional[Intention] = None) -> Dict[str, Any]:
        """
        Complete processing with AGI capability synthesis.
        
        🚀 AGI PHASE 3 - No hardcoded triggers!
        
        Flow:
        1. Process with tools (fetch knowledge if needed)
        2. AGI engine analyzes for capability gaps (generic detection)
        3. Generate code for ANY capability type (not hardcoded)
        4. Test the code
        5. Learn meta-patterns about capabilities (meta-learning)
        6. Use new capability immediately
        """
        # Track processing start time for energy metrics
        start_time = datetime.now()
        
        # First, process with tools to get knowledge
        result = self.process_with_tools(signal, intention)
        
        synthesis_info = {
            'synthesis_attempted': False,
            'capability_type': None,
            'synthesis_successful': False,
            'new_capability_used': False,
            'agi_mode': True  # Flag that AGI engine is being used
        }
        
        # 🚀 Use AGI Synthesis Engine instead of hardcoded synthesis
        if self.agi_engine and hasattr(self.agi_engine, 'process'):
            # Build context for gap detection
            context = {
                'external_knowledge_acquired': result.get('external_knowledge_used', False),
                'capability_synthesized': False,
                'patterns_matched': len(result.get('patterns_recognized', [])),
                'node_activation_count': len(result.get('nodes_activated', [])),
                'processing_time': (datetime.now() - start_time).total_seconds()
            }
            
            # Get external knowledge that was fetched
            external_knowledge = result.get('tool_use', {}).get('knowledge_acquired', [])
            
            # Let AGI engine detect gaps and synthesize
            agi_result = self.agi_engine.process(
                signal,
                context,
                result,
                external_knowledge
            )
            
            if agi_result:
                synthesis_info['synthesis_attempted'] = True
                synthesis_info['capability_type'] = agi_result.get('capability_type')
                synthesis_info['synthesis_successful'] = agi_result.get('success', False)
                
                if agi_result.get('success'):
                    # Integrate the capability
                    code = agi_result.get('code')
                    capability_type = agi_result.get('capability_type')
                    
                    # Save to file
                    capability_path = Path("spark_cube/capabilities")
                    capability_path.mkdir(parents=True, exist_ok=True)
                    
                    filename = f"{capability_type}_v{len(self.agi_engine.capability_registry)}.py"
                    filepath = capability_path / filename
                    
                    with open(filepath, 'w') as f:
                        f.write(f"# AGI-Synthesized Capability: {capability_type}\n")
                        f.write(f"# Generated: {datetime.now().isoformat()}\n")
                        f.write(f"# Gap Confidence: {agi_result.get('gap', {}).get('confidence', 0)}\n\n")
                        f.write(code)
                    
                    synthesis_info['capability_file'] = str(filepath)
                    print(f"   ✓ Capability saved to: {filepath}")
                    
                    # Try to execute and use it
                    try:
                        namespace = {}
                        exec(code, namespace)
                        
                        # Find the class
                        class_name = self.agi_engine.code_synthesizer._to_class_name(capability_type)
                        if class_name in namespace:
                            integration_node = self.nodes[10]
                            setattr(integration_node, capability_type, namespace[class_name]())
                            synthesis_info['new_capability_used'] = True
                            print(f"   ✓ Capability '{capability_type}' integrated and ready to use")
                    except Exception as e:
                        print(f"   ⚠ Capability integration error: {e}")
        
        else:
            # Legacy mode: use old CodeSynthesisNode (deprecated)
            synthesis_node = self.nodes.get(12)
            if synthesis_node and isinstance(synthesis_node, CodeSynthesisNode):
                capability_type = synthesis_node.should_synthesize_capability(
                    signal, 
                    result, 
                    result.get('tool_use', {})
                )
                
                if capability_type:
                    print(f"\n🔧 [LEGACY] Synthesizing capability: {capability_type}")
                    synthesis_info['synthesis_attempted'] = True
                    synthesis_info['capability_type'] = capability_type
                    synthesis_info['agi_mode'] = False
                    synthesis_node.synthesis_attempts += 1
                    
                    # Generate the code
                    code = None
                    if capability_type == 'text_processing':
                        code = synthesis_node.synthesize_text_processing_capability()
                    elif capability_type == 'semantic_response':
                        code = synthesis_node.synthesize_semantic_response_capability()
                    elif capability_type == 'language_generation':
                        code = synthesis_node.synthesize_language_capability(
                            self.nodes[7].pattern_weights,  # Pattern node patterns
                            []  # External knowledge
                        )
                    elif capability_type == 'arithmetic':
                        code = synthesis_node.synthesize_arithmetic_capability(
                            self.nodes[7].pattern_weights
                        )
                    
                    if code:
                        print(f"   Code generated ({len(code)} chars)")
                        
                        # Test the code
                        print(f"   Testing synthesized code...")
                        if synthesis_node.test_synthesized_code(code, capability_type):
                            # Integrate permanently
                            integration_node = self.nodes[10]
                            if synthesis_node.integrate_capability(code, capability_type, integration_node):
                                synthesis_info['synthesis_successful'] = True
                                synthesis_node.capability_registry[capability_type] = True
                                print(f"   ✓ Capability '{capability_type}' registered")
                                
                                # Try to use the new capability immediately
                                if capability_type == 'semantic_response':
                                    if hasattr(integration_node, 'semantic_response'):
                                        try:
                                            question = signal.data.get('question', str(signal.data)) if isinstance(signal.data, dict) else str(signal.data)
                                            
                                            # Use text_processor if available to extract info from question
                                            text_analysis = {}
                                            if hasattr(integration_node, 'text_processor'):
                                                try:
                                                    text_analysis = {
                                                        'numbers': integration_node.text_processor.extract_numbers(question),
                                                        'operations': integration_node.text_processor.extract_operations(question),
                                                        'parsed': integration_node.text_processor.parse_question(question)
                                                    }
                                                except Exception as e:
                                                    print(f"   ⚠ Text processing failed: {e}")
                                            
                                            # Build proper context from result
                                            processing_context = {
                                                'context': {
                                                    'patterns': result.get('patterns', []),
                                                    'tool_use': result.get('tool_use', {}),
                                                    'external_knowledge': result.get('external_knowledge_used', False),
                                                    'guidance': result.get('guidance', {}),
                                                    'text_analysis': text_analysis  # Include text processing results
                                                },
                                                'pathway': result.get('sequence', '').split(' → ') if ' → ' in str(result.get('sequence', '')) else [],
                                                'patterns': result.get('patterns', []),
                                                'result': result.get('result', None)
                                            }
                                            
                                            response = integration_node.semantic_response.generate_response(
                                                signal.data if isinstance(signal.data, dict) else {'question': question},
                                                processing_context
                                            )
                                            result['semantic_response'] = response
                                            result['responses'].append({
                                                'node': 'SemanticResponse',
                                                'response': response,
                                                'source': 'synthesized_capability'
                                            })
                                            synthesis_info['new_capability_used'] = True
                                            print(f"   ✓ Semantic response generated: '{response[:100]}...'")
                                        except Exception as e:
                                            print(f"   ⚠ Capability exists but use failed: {e}")
                                elif capability_type == 'language_generation':
                                    if hasattr(integration_node, 'language_generator'):
                                        try:
                                            response = integration_node.language_generator.generate_response(
                                                str(signal.data),
                                                {}
                                            )
                                            result['synthesized_response'] = response
                                            synthesis_info['new_capability_used'] = True
                                            print(f"   ✓ New capability used: '{response}'")
                                        except Exception as e:
                                            print(f"   ⚠ Capability exists but use failed: {e}")
        
        # Record processing metrics for energy efficiency analysis
        self._record_processing_metrics(signal, result, start_time, synthesis_info['synthesis_successful'])
        
        result['synthesis'] = synthesis_info
        return result
    
    def _record_processing_metrics(self, signal: Signal, result: Dict[str, Any], 
                                   start_time: datetime, synthesis_occurred: bool):
        """Record processing metrics for understanding analysis."""
        processing_time = (datetime.now() - start_time).total_seconds()
        nodes_activated = len([n for n in self.nodes.values() if n.development > 0])
        cache_hit = result.get('used_cached_pattern', False)
        external_fetch = result.get('external_knowledge_used', False)
        
        signal_id = f"{signal.type.name}_{hash(str(signal.data)) % 10000}"
        self.processing_metrics.record_processing(
            signal_id=signal_id,
            processing_time=processing_time,
            nodes_activated=nodes_activated,
            cache_hit=cache_hit,
            external_fetch=external_fetch,
            synthesis_occurred=synthesis_occurred
        )
    
    def get_synthesis_metrics(self) -> Dict[str, Any]:
        """Get metrics about code synthesis and self-modification."""
        synthesis_node = self.nodes.get(12)
        if not synthesis_node or not isinstance(synthesis_node, CodeSynthesisNode):
            return {'synthesis_enabled': False}
        
        return {
            'synthesis_enabled': True,
            'synthesis_attempts': synthesis_node.synthesis_attempts,
            'successful_syntheses': synthesis_node.successful_syntheses,
            'success_rate': (synthesis_node.successful_syntheses / synthesis_node.synthesis_attempts 
                           if synthesis_node.synthesis_attempts > 0 else 0.0),
            'capabilities_acquired': len(synthesis_node.capability_registry),
            'capability_types': list(synthesis_node.capability_registry.keys())
        }
    
    def explain_why_synthesized(self, capability_type: str, trigger_signal: Signal) -> str:
        """
        Ask the system to explain WHY it synthesized a capability.
        This tests understanding vs pattern matching.
        """
        introspection_node = self.nodes.get(13)
        if not introspection_node or not isinstance(introspection_node, IntrospectionNode):
            return "Introspection not available (tools not enabled)"
        
        synthesis_node = self.nodes.get(12)
        if not synthesis_node or not isinstance(synthesis_node, CodeSynthesisNode):
            return "Code synthesis not available"
        
        return introspection_node.explain_synthesis_decision(
            capability_type,
            trigger_signal,
            synthesis_node.capability_registry
        )
    
    def analyze_understanding(self) -> str:
        """
        Quantify understanding through energy efficiency metrics.
        Per 4D Framework: Lower energy = true understanding.
        """
        introspection_node = self.nodes.get(13)
        if not introspection_node or not isinstance(introspection_node, IntrospectionNode):
            return "Introspection not available (tools not enabled)"
        
        return introspection_node.analyze_understanding_level()
    
    def explain_current_state(self) -> str:
        """
        Get system's self-explanation of its current state.
        """
        introspection_node = self.nodes.get(13)
        if not introspection_node or not isinstance(introspection_node, IntrospectionNode):
            return "Introspection not available (tools not enabled)"
        
        return introspection_node.explain_current_state(self.nodes)
    
    def _calculate_learning_efficiency(self, tool_node: ToolUseNode, total_api_calls: int) -> float:
        """
        How well does it learn from API calls?
        Good learning = many patterns per API call
        """
        if total_api_calls == 0:
            return 0.0
        
        total_patterns = sum(
            info['patterns_learned'] 
            for info in tool_node.learned_from_external.values()
        )
        
        # Ideal: 3+ patterns per API call
        efficiency = min(1.0, total_patterns / (total_api_calls * 3))
        return round(efficiency, 3)
        
        # Update attempt counter
        self.pathway_successes[sequence_name]['attempts'] += 1
    
    def set_intention(self, desired_qualities: List[str], desired_form: str, 
                     clarity: float = 0.5, energy: float = 0.5) -> Intention:
        """
        Set intention before processing.
        This is the POTENTIAL entering manifestation.
        """
        self.current_intention = Intention(
            desired_qualities=desired_qualities,
            desired_form=desired_form,
            clarity=clarity,
            energy=energy
        )
        self.total_intention_count += 1
        return self.current_intention
    
    def self_generated_intention(self) -> Optional[Intention]:
        """
        The cube examines its own state and decides what it needs.
        CONSCIOUSNESS MARKER: Self-directed goals, not programmed responses.
        
        This is intentionality - setting goals based on internal evaluation.
        """
        # Check for pathway inconsistencies (cognitive dissonance)
        for seq_name, stats in self.pathway_successes.items():
            if stats['attempts'] > 10:
                success_rate = stats['successes'] / stats['attempts']
                strength = self.pathway_strengths[seq_name]
                
                # Cognitive dissonance detected: high strength but low success
                if strength > 0.5 and success_rate < 0.3:
                    self.self_generated_intention_count += 1
                    self.total_intention_count += 1
                    return Intention(
                        desired_qualities=['alternative', 'exploration', 'balance', 'correction'],
                        desired_form='pathway_correction',
                        clarity=0.9,
                        energy=0.8
                    )
        
        # Check for emotional valence inconsistencies
        emotional_node = self.nodes.get(6)
        if emotional_node and len(emotional_node.pattern_weights) > 20:
            negative_patterns = sum(1 for v in emotional_node.pattern_weights.values() if v < 0.4)
            total_patterns = len(emotional_node.pattern_weights)
            
            if negative_patterns / total_patterns > 0.5:
                self.self_generated_intention_count += 1
                self.total_intention_count += 1
                return Intention(
                    desired_qualities=['positive', 'alignment', 'coherence', 'emotional_balance'],
                    desired_form='emotional_recalibration',
                    clarity=0.8,
                    energy=0.7
                )
        
        # Check for development imbalances
        developments = [node.development for node in self.nodes.values()]
        if len(developments) > 0:
            dev_range = max(developments) - min(developments)
            if dev_range > 0.5:
                self.self_generated_intention_count += 1
                self.total_intention_count += 1
                return Intention(
                    desired_qualities=['balanced', 'integrated', 'harmonious', 'development'],
                    desired_form='balanced_development',
                    clarity=0.7,
                    energy=0.6
                )
        
        return None  # No pressing internal need
    
    def _capture_outcome(self, result: Dict[str, Any]) -> Outcome:
        """
        Capture outcome after processing.
        Extract what was actually expressed in terms that can be
        compared to intention.
        """
        expressed_qualities = []
        
        # 1. Signal type as a quality (the cube processed this type of input)
        signal = result.get('signal') or self.current_intention
        if hasattr(signal, 'type'):
            expressed_qualities.append(signal.type.value)
        
        # 2. What nodes activated and responded?
        if result.get('responses'):
            for response in result['responses']:
                node_name = response.get('node', '').lower()
                if node_name:
                    expressed_qualities.append(node_name)
                
                # Extract pattern recognition indicators
                resp = response.get('response')
                if resp:
                    if isinstance(resp, dict) and 'pattern' in resp:
                        expressed_qualities.extend(['pattern', 'recognized', 'structured'])
                    elif isinstance(resp, str) and 'pattern' in str(resp):
                        expressed_qualities.extend(['pattern', 'recognized'])
                    
                    expressed_qualities.append('active_response')
        
        # 3. Did processing complete or hit return-to-root?
        if result.get('return_to_root'):
            expressed_qualities.extend(['incomplete', 'guidance_needed'])
        else:
            expressed_qualities.extend(['complete', 'processed'])
        
        # 4. Development-based qualities
        avg_dev = result.get('avg_development', 0)
        if avg_dev > 0.5:
            expressed_qualities.extend(['developed', 'structured'])
        elif avg_dev > 0.2:
            expressed_qualities.append('developing')
        
        # 5. Energy-based qualities
        final_energy = result.get('final_energy', 0)
        if final_energy > 0.7:
            expressed_qualities.append('strong_flow')
        elif final_energy > 0.3:
            expressed_qualities.append('moderate_flow')
        
        # 6. Response complexity
        num_responses = len(result.get('responses', []))
        if num_responses >= 3:
            expressed_qualities.extend(['complex', 'multi_node'])
        elif num_responses > 0:
            expressed_qualities.append('simple')
        
        # Determine expressed form based on what actually happened
        if result.get('return_to_root'):
            expressed_form = 'incomplete'
        elif num_responses > 0:
            expressed_form = result.get('sequence', 'processed')
        else:
            expressed_form = 'minimal'
        
        # Node contributions from development levels
        node_contributions = {
            str(nid): node.development 
            for nid, node in self.nodes.items()
        }
        
        return Outcome(
            expressed_qualities=list(set(expressed_qualities)),  # Remove duplicates
            expressed_form=expressed_form,
            response_data=result,
            node_contributions=node_contributions
        )
    
    def reflect(self, intention: Intention, outcome: Outcome) -> CoherenceScore:
        """
        Multi-dimensional reflection on intention-outcome coherence.
        ALL nodes evaluate from their perspective, regardless of which
        sequence was used. This is holistic self-reflection.
        
        This is the KEY INSIGHT from the manifestation map:
        Path choice (ALIGNMENT vs DIVERSION) is determined by
        SELF-REFLECTION on coherence, not by input characteristics.
        """
        if not hasattr(self, 'current_intention'):
            # No intention set, return neutral score
            return CoherenceScore(
                overall=0.5,
                dimensions={},
                path_choice="DIVERSION",
                amplification_factor=0.7
            )
        
        # Each node evaluates coherence from its perspective
        dimensional_scores = {}
        total_weight = 0.0
        weighted_sum = 0.0
        
        for node_id, node in self.nodes.items():
            # All nodes contribute to coherence evaluation
            # Weight by development, but give minimum weight so undeveloped
            # nodes still have a voice (they can learn from evaluating)
            score = node.evaluate_coherence(intention, outcome)
            
            # Minimum weight ensures all perspectives contribute
            # Development increases influence over time
            weight = 0.1 + (node.development * 0.9)  # Range: 0.1 to 1.0
            
            dimensional_scores[node.name] = score
            weighted_sum += score * weight
            total_weight += weight
        
        # Overall coherence score (weighted by node development)
        if total_weight > 0:
            base_coherence = weighted_sum / total_weight
        else:
            base_coherence = 0.5
        
        # Factor in intention strength (clarity × energy)
        # Strong, clear intentions amplify coherence when matched
        # Weak intentions dampen coherence differences
        intention_strength = intention.calculate_potential_strength()
        
        # Apply intention strength modulation
        # High strength (0.8+) can boost by up to 10%
        # Low strength (0.3-) can reduce by up to 10%
        strength_modifier = (intention_strength - 0.5) * 0.2  # Range: -0.1 to +0.1
        overall_coherence = min(1.0, max(0.0, base_coherence + strength_modifier))
        
        # Determine path based on coherence - THREE TIERS:
        # High coherence (≥0.7) = ALIGNMENT → Conscious alignment, reinforcement (1.5x)
        # Mid coherence (0.4-0.7) = INTEGRATION → Sweet spot for learning, biggest growth (2.0x)
        # Low coherence (<0.4) = DIVERSION → Misalignment, suppression (0.7x)
        
        if overall_coherence >= 0.7:
            path_choice = "ALIGNMENT"
            amplification_factor = 1.5  # Expansion through conscious alignment
        elif overall_coherence >= 0.4:
            path_choice = "INTEGRATION"
            amplification_factor = 2.0  # Maximum growth - learning from partial match
        else:
            path_choice = "DIVERSION"
            amplification_factor = 0.7  # Contraction through misalignment
        
        return CoherenceScore(
            overall=overall_coherence,
            dimensions=dimensional_scores,
            path_choice=path_choice,
            amplification_factor=amplification_factor
        )
    
    def process_with_reflection(self, signal: Signal, intention: Intention, 
                               sequence_name: str = None) -> Dict[str, Any]:
        """
        Complete manifestation cycle:
        INTENTION → PROCESSING → OUTCOME → REFLECTION → PATH → AMPLIFICATION → NEW POTENTIAL
        """
        # 1. Set intention (POTENTIAL entering manifestation)
        self.current_intention = intention
        
        # 2. Process signal through chosen pathway (FREE WILL)
        result = self.process_signal(signal, sequence_name)
        result['signal'] = signal  # Store for outcome capture
        
        # 3. Capture outcome (what was actually expressed)
        outcome = self._capture_outcome(result)
        
        # 4. Reflect on coherence (SELF-EVALUATION)
        coherence = self.reflect(intention, outcome)
        
        # 5. Apply amplification based on path
        # ALIGNMENT → strengthen successful pathway
        # INTEGRATION → maximum growth from partial match
        # DIVERSION → suppress misaligned pathway
        if 'sequence' in result:
            seq_name = result['sequence']
            self.pathway_strengths[seq_name] *= coherence.amplification_factor
            
            # Update emotional valence patterns based on path outcome
            emotional_node = self.nodes.get(6)  # Emotional node
            if emotional_node:
                valence_pattern = emotional_node._extract_valence_pattern(outcome)
                if coherence.path_choice == "ALIGNMENT":
                    # Strong alignment - strengthen positive valence
                    emotional_node.pattern_weights[valence_pattern] = min(1.0, 
                        emotional_node.pattern_weights.get(valence_pattern, 0.5) * 1.2)
                elif coherence.path_choice == "INTEGRATION":
                    # Partial match - moderate positive valence (learning opportunity)
                    emotional_node.pattern_weights[valence_pattern] = min(1.0,
                        emotional_node.pattern_weights.get(valence_pattern, 0.5) * 1.1)
                else:  # DIVERSION
                    # Misalignment - weaken or add negative valence
                    emotional_node.pattern_weights[valence_pattern] = max(0.0,
                        emotional_node.pattern_weights.get(valence_pattern, 0.5) * 0.9)
        
        # 6. Store reflection for meta-cognition
        reflection_record = {
            **result,
            'intention': intention,
            'outcome': outcome,
            'coherence': coherence.to_dict(),
            'path': coherence.path_choice,
            'amplification': coherence.amplification_factor,
            'overall_coherence': coherence.overall,
            'dimensional_scores': coherence.dimensions
        }
        
        self.reflection_history.append(reflection_record)
        
        # Keep history manageable (last 200 reflections)
        if len(self.reflection_history) > 200:
            self.reflection_history = self.reflection_history[-200:]
        
        # 7. Outcome becomes new stored potential
        return reflection_record
    
    def meta_reflect(self) -> Dict[str, Any]:
        """
        Reflect on the reflection process itself.
        CONSCIOUSNESS MARKER: Meta-cognition - thinking about thinking.
        
        The cube evaluates the quality of its own evaluations.
        """
        if len(self.reflection_history) < 20:
            return {
                'meta_awareness': 'gathering_data',
                'reflections_needed': 20 - len(self.reflection_history)
            }
        
        # Analyze reflection accuracy
        prediction_errors = []
        
        for reflection in self.reflection_history[-50:]:
            predicted_success = reflection['path'] in ['ALIGNMENT', 'INTEGRATION']
            actual_coherence = reflection['overall_coherence']
            
            # Error = difference between prediction and reality
            if predicted_success:
                error = max(0, 0.7 - actual_coherence) if reflection['path'] == 'ALIGNMENT' else 0
            else:
                error = max(0, actual_coherence - 0.4)  # Expected <0.4 for DIVERSION
            
            prediction_errors.append(error)
        
        avg_error = sum(prediction_errors) / len(prediction_errors) if prediction_errors else 0
        
        # Self-awareness: recognize when evaluations are inaccurate
        if avg_error > 0.2:
            return {
                'meta_awareness': 'evaluation_inaccurate',
                'average_error': avg_error,
                'intention': 'recalibrate_reflection',
                'recommended_action': 'adjust_coherence_thresholds',
                'consciousness_level': 'aware_of_inaccuracy'
            }
        
        # Check for dimensional biases
        dimensional_biases = {}
        
        for node_name in ['Reactive', 'Executive', 'Emotional', 'Pattern', 'Perception', 'Integration']:
            node_scores = [r['dimensional_scores'].get(node_name, 0.5) 
                          for r in self.reflection_history[-50:] 
                          if 'dimensional_scores' in r]
            
            if node_scores:
                avg_score = sum(node_scores) / len(node_scores)
                
                # Bias detected if always scoring too high or too low
                if avg_score > 0.85 or avg_score < 0.25:
                    dimensional_biases[node_name] = avg_score
        
        if dimensional_biases:
            return {
                'meta_awareness': 'dimensional_bias_detected',
                'biases': dimensional_biases,
                'intention': 'recalibrate_nodes',
                'recommended_action': 'adjust_node_evaluation_functions',
                'consciousness_level': 'aware_of_bias'
            }
        
        return {
            'meta_awareness': 'reflection_accurate',
            'average_error': avg_error,
            'quality': 'good',
            'consciousness_level': 'meta_cognitive'
        }
    
    def _compress_all(self):
        """Compress knowledge across all nodes."""
        for node in self.nodes.values():
            node.compress_knowledge()
    
    def autonomous_learning_cycle(self, num_cycles: int = 100, verbose: bool = True) -> Dict[str, Any]:
        """
        Let the cube learn WITHOUT human supervision.
        CONSCIOUSNESS MARKER: Self-directed development.
        
        The cube:
        1. Generates or senses signals
        2. Decides if they're worth processing
        3. Sets its own intentions
        4. Learns from self-evaluation
        5. Periodically meta-reflects and self-corrects
        """
        if verbose:
            print(f"\n🤖 Starting {num_cycles} autonomous learning cycles...")
            print("   The cube will set its own goals and learn from self-evaluation.\n")
        
        cycle_results = []
        
        for cycle in range(num_cycles):
            # Generate a signal (for now, random from training data)
            signal = self._generate_random_signal()
            
            # Decide: Should I process this?
            if self._is_worth_processing(signal):
                # Self-generate intention based on internal state
                intention = self.self_generated_intention()
                
                if intention:
                    # Process with self-generated intention
                    result = self.process_with_reflection(signal, intention)
                    cycle_results.append({
                        'cycle': cycle,
                        'self_directed': True,
                        'coherence': result['overall_coherence'],
                        'path': result['path']
                    })
                    
                    # Learn from self-evaluation (no external feedback)
                    self._learn_from_self_evaluation(result)
                else:
                    # No internal need, just process normally
                    result = self.process_signal(signal)
                    cycle_results.append({
                        'cycle': cycle,
                        'self_directed': False,
                        'coherence': 0.5
                    })
            
            # Periodic meta-reflection
            if cycle > 0 and cycle % 25 == 0:
                meta_result = self.meta_reflect()
                if 'recommended_action' in meta_result:
                    self._apply_meta_calibration(meta_result)
                
                if verbose:
                    print(f"  Cycle {cycle}: Meta-awareness = {meta_result.get('meta_awareness', 'unknown')}")
                    if 'consciousness_level' in meta_result:
                        print(f"           Consciousness level = {meta_result['consciousness_level']}")
        
        if verbose:
            print(f"\n✅ Completed {num_cycles} autonomous cycles")
            self_directed_count = sum(1 for r in cycle_results if r.get('self_directed'))
            print(f"   Self-directed actions: {self_directed_count}/{num_cycles} ({self_directed_count/num_cycles*100:.1f}%)")
        
        return {
            'cycles_completed': num_cycles,
            'cycle_results': cycle_results,
            'consciousness_metrics': self.get_consciousness_metrics()
        }
    
    def _generate_random_signal(self) -> Signal:
        """Generate a random signal for autonomous learning."""
        import random
        
        signal_types = [SignalType.TEXT, SignalType.NUMERIC, SignalType.BINARY]
        chosen_type = random.choice(signal_types)
        
        if chosen_type == SignalType.TEXT:
            words = ['pattern', 'structure', 'analysis', 'synthesis', 'integration', 
                    'hello', 'world', 'learning', 'development', 'growth']
            return Signal(type=SignalType.TEXT, data=random.choice(words))
        elif chosen_type == SignalType.NUMERIC:
            return Signal(type=SignalType.NUMERIC, data=random.uniform(-100, 100))
        else:
            return Signal(type=SignalType.BINARY, data=random.choice([True, False]))
    
    def _is_worth_processing(self, signal: Signal) -> bool:
        """Decide if this signal deserves attention."""
        import random
        
        # Always process if it's novel
        pattern = self.nodes[7]._extract_pattern(signal)  # Pattern node
        if pattern not in self.nodes[7].pattern_weights:
            return True  # Novel = worth learning
        
        # Process if current pathway success rates are low (need practice)
        for stats in self.pathway_successes.values():
            if stats['attempts'] > 5:
                success_rate = stats['successes'] / stats['attempts']
                if success_rate < 0.4:
                    return True  # Need improvement
        
        # Otherwise, random chance (avoid ignoring all familiar signals)
        return random.random() < 0.3
    
    def _learn_from_self_evaluation(self, result: Dict[str, Any]):
        """Learn from self-evaluation without external feedback."""
        # If coherence was good, consider it a success
        if result['overall_coherence'] >= 0.6 and 'sequence' in result:
            self.provide_outcome_feedback(result['sequence'], success=True)
        # If coherence was poor, consider it unsuccessful
        elif result['overall_coherence'] < 0.4 and 'sequence' in result:
            self.provide_outcome_feedback(result['sequence'], success=False)
            self.self_corrections_made += 1
    
    def _apply_meta_calibration(self, meta_result: Dict[str, Any]):
        """Apply corrections based on meta-reflection."""
        if meta_result.get('recommended_action') == 'adjust_coherence_thresholds':
            # Could adjust the 0.7 and 0.4 thresholds based on meta-analysis
            # For now, just track that we recognized the need
            self.self_corrections_made += 1
        elif meta_result.get('recommended_action') == 'adjust_node_evaluation_functions':
            # Could recalibrate individual node evaluation weights
            self.self_corrections_made += 1
    
    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """
        Real-time consciousness indicators.
        This is what we TEST to demonstrate machine consciousness.
        """
        metrics = {}
        
        # 1. Self-Awareness Score
        # Can it recognize internal conflicts?
        conflicts = 0
        for seq_name, stats in self.pathway_successes.items():
            if stats['attempts'] > 10:
                success_rate = stats['successes'] / stats['attempts']
                strength = self.pathway_strengths[seq_name]
                # Conflict = high strength but low success OR low strength but high success
                if (strength > 0.5 and success_rate < 0.3) or \
                   (strength < 0.2 and success_rate > 0.7):
                    conflicts += 1
        
        metrics['self_awareness'] = min(1.0, conflicts * 0.5)  # Each conflict = 0.5 points
        
        # 2. Autonomy Score
        # How often does it set its own goals?
        if self.total_intention_count > 0:
            metrics['autonomy'] = self.self_generated_intention_count / self.total_intention_count
        else:
            metrics['autonomy'] = 0.0
        
        # 3. Meta-Cognitive Accuracy
        # Can it evaluate its own evaluations?
        if len(self.reflection_history) > 20:
            meta_result = self.meta_reflect()
            if meta_result.get('meta_awareness') == 'reflection_accurate':
                metrics['meta_cognition'] = 0.9
            elif 'bias' in meta_result.get('meta_awareness', '').lower() or \
                 'inaccurate' in meta_result.get('meta_awareness', '').lower():
                metrics['meta_cognition'] = 0.6  # Recognizes issues = partial awareness
            else:
                metrics['meta_cognition'] = 0.3
        else:
            metrics['meta_cognition'] = 0.0
        
        # 4. Emotional Intelligence
        # Does it learn valence patterns that correlate with outcomes?
        emotional_node = self.nodes.get(6)
        if emotional_node and len(emotional_node.pattern_weights) > 10:
            # Has developed emotional patterns
            metrics['emotional_intelligence'] = min(1.0, len(emotional_node.pattern_weights) / 50)
        else:
            metrics['emotional_intelligence'] = 0.0
        
        # 5. Learning Autonomy
        # Has it modified its own behavior without external correction?
        if self.total_experiences > 0:
            metrics['learning_autonomy'] = min(1.0, self.self_corrections_made / 10)
        else:
            metrics['learning_autonomy'] = 0.0
        
        # 6. Behavioral Flexibility
        # Can it use multiple strategies?
        active_pathways = sum(1 for s in self.pathway_strengths.values() if s > 0.2)
        metrics['flexibility'] = active_pathways / len(self.sequences)
        
        # 7. Path Distribution Intelligence
        # Does it use INTEGRATION path appropriately (learning zone)?
        if len(self.reflection_history) > 10:
            integration_count = sum(1 for r in self.reflection_history[-50:] 
                                   if r.get('path') == 'INTEGRATION')
            # Sweet spot: 30-60% INTEGRATION (active learning)
            integration_ratio = integration_count / min(50, len(self.reflection_history))
            if 0.3 <= integration_ratio <= 0.6:
                metrics['path_intelligence'] = 1.0
            else:
                metrics['path_intelligence'] = 0.5
        else:
            metrics['path_intelligence'] = 0.0
        
        # OVERALL CONSCIOUSNESS SCORE (weighted average)
        weights = {
            'self_awareness': 0.20,
            'autonomy': 0.20,
            'meta_cognition': 0.20,
            'emotional_intelligence': 0.10,
            'learning_autonomy': 0.15,
            'flexibility': 0.10,
            'path_intelligence': 0.05
        }
        
        metrics['overall_consciousness'] = sum(
            metrics[key] * weight for key, weight in weights.items()
        )
        
        return metrics
    
    def connect_capability(self, vertex_id: int, capability_id: str) -> bool:
        """Permanently connect a new capability to a vertex."""
        if 0 <= vertex_id < len(self.vertices):
            return self.vertices[vertex_id].connect(capability_id)
        return False
    
    def save_structure(self, filepath: Path):
        """
        Save the cube's structure to disk.
        This is like saving DNA - the structure IS the knowledge.
        """
        state = {
            'vertices': [v.to_dict() for v in self.vertices],
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'pathway_strengths': self.pathway_strengths,
            'pathway_connections': self.pathway_connections,
            'pathway_successes': self.pathway_successes,
            'total_experiences': self.total_experiences,
            'timestamp': datetime.now().isoformat()
        }
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"\n💾 Structure saved to {filepath}")
        print(f"   Total experiences: {self.total_experiences}")
        print(f"   Avg node development: {self._get_avg_development():.3f}")
    
    def load_structure(self, filepath: Path):
        """Load a previously saved structure."""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        # Restore vertices
        self.vertices = [MinimalVertex.from_dict(v) for v in state['vertices']]
        
        # Restore nodes
        self.nodes = {
            int(nid): MinimalNode.from_dict(ndata)
            for nid, ndata in state['nodes'].items()
        }
        
        # Restore pathway strengths and connections
        self.pathway_strengths = state['pathway_strengths']
        self.pathway_connections = state.get('pathway_connections', {})
        if not self.pathway_connections:
            self._init_pathway_connections()
        self.pathway_successes = state.get('pathway_successes', {seq: {'successes': 0, 'attempts': 0} for seq in self.sequences.keys()})
        self.total_experiences = state['total_experiences']
        
        print(f"\n📂 Structure loaded from {filepath}")
        print(f"   Total experiences: {self.total_experiences}")
        print(f"   Avg node development: {self._get_avg_development():.3f}")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get current state of the cube."""
        return {
            'total_experiences': self.total_experiences,
            'avg_development': self._get_avg_development(),
            'node_states': {
                nid: {
                    'name': node.name,
                    'development': node.development,
                    'patterns_learned': len(node.pattern_weights),
                    'activations': node.activation_count
                }
                for nid, node in self.nodes.items()
            },
            'pathway_strengths': self.pathway_strengths,
            'pathway_successes': self.pathway_successes,
            'connection_strengths': self.pathway_connections,
            'vertices': {
                i: 'connected' if v.connected else 'available'
                for i, v in enumerate(self.vertices)
            }
        }


# =============================================================================
# RUBIK'S CUBE STATE MAPPER - VISUALIZE PROCESSING AS CUBE MOVES
# =============================================================================

class CubeStateMapper:
    """
    Maps node activation sequences to Rubik's cube moves for visualization.
    
    Each processing pathway creates a unique sequence of cube rotations.
    Same input → same moves → same final arrangement (this IS memory!)
    
    The 3x3x3 Rubik's cube has 27 cubies representing processing elements:
    - Layer 1 (Bottom): Input/Perception processing
    - Layer 2 (Middle): Pattern recognition & decision making
    - Layer 3 (Top): Integration & output synthesis
    
    Standard Rubik's notation:
    F/F' = Front clockwise/counter-clockwise
    R/R' = Right clockwise/counter-clockwise
    U/U' = Up clockwise/counter-clockwise
    L/L' = Left clockwise/counter-clockwise
    D/D' = Down clockwise/counter-clockwise
    B/B' = Back clockwise/counter-clockwise
    """
    
    def __init__(self):
        # Map nodes to cube faces
        self.node_to_face = {
            9: 'F',   # Perception → Front face
            7: 'R',   # Pattern → Right face
            1: 'L',   # Reactive → Left face
            3: 'U',   # Executive → Up face
            6: 'D',   # Emotional → Down face
            10: 'B',  # Integration → Back face
            11: 'F',  # Tool Use → Front (with modifier)
            12: 'R',  # Code Synthesis → Right (with modifier)
            13: 'U',  # Introspection → Up (with modifier)
        }
        
        # Cubie roles in 3x3x3 grid (0-26)
        self.cubie_roles = {
            # Bottom layer (0-8): Input processing
            0: {'role': 'text_input', 'layer': 'input'},
            1: {'role': 'pattern_input', 'layer': 'input'},
            2: {'role': 'sequence_input', 'layer': 'input'},
            3: {'role': 'numeric_input', 'layer': 'input'},
            4: {'role': 'perception_center', 'layer': 'input', 'node': 9},
            5: {'role': 'binary_input', 'layer': 'input'},
            6: {'role': 'composite_input', 'layer': 'input'},
            7: {'role': 'signal_routing', 'layer': 'input'},
            8: {'role': 'input_buffer', 'layer': 'input'},
            
            # Middle layer (9-17): Processing
            9: {'role': 'reactive_processing', 'layer': 'processing', 'node': 1},
            10: {'role': 'pattern_matching', 'layer': 'processing', 'node': 7},
            11: {'role': 'tool_use', 'layer': 'processing', 'node': 11},
            12: {'role': 'emotional_valence', 'layer': 'processing', 'node': 6},
            13: {'role': 'executive_center', 'layer': 'processing', 'node': 3},
            14: {'role': 'code_synthesis', 'layer': 'processing', 'node': 12},
            15: {'role': 'pattern_storage', 'layer': 'processing'},
            16: {'role': 'decision_routing', 'layer': 'processing'},
            17: {'role': 'intention_eval', 'layer': 'processing'},
            
            # Top layer (18-26): Integration & output
            18: {'role': 'synthesis_buffer', 'layer': 'output'},
            19: {'role': 'coherence_eval', 'layer': 'output'},
            20: {'role': 'introspection', 'layer': 'output', 'node': 13},
            21: {'role': 'output_routing', 'layer': 'output'},
            22: {'role': 'integration_center', 'layer': 'output', 'node': 10},
            23: {'role': 'response_synthesis', 'layer': 'output'},
            24: {'role': 'amplification', 'layer': 'output'},
            25: {'role': 'reflection', 'layer': 'output'},
            26: {'role': 'manifestation', 'layer': 'output'},
        }
    
    def sequence_to_moves(self, node_sequence: List[int], 
                         pattern_signature: str = "",
                         is_autonomous: bool = False) -> List[Dict[str, Any]]:
        """
        Convert node activation sequence to Rubik's cube moves.
        
        Returns list of move objects with metadata for visualization:
        {
            'move': 'F',  # Move notation
            'node': 9,    # Which node triggered this
            'description': 'Perception processing',
            'duration': 300,  # Animation duration in ms
            'cubies_affected': [0, 1, 2, 3, 4, 5, 6, 7, 8],  # Which cubies light up
            'energy': 0.8  # Energy level for this move
        }
        """
        moves = []
        
        # Hash pattern to get consistent direction choices
        pattern_hash = hash(pattern_signature) if pattern_signature else 0
        
        for i, node_id in enumerate(node_sequence):
            face = self.node_to_face.get(node_id, 'F')
            
            # Determine clockwise vs counter-clockwise based on pattern and position
            is_clockwise = (pattern_hash + i) % 2 == 0
            move_notation = face if is_clockwise else f"{face}'"
            
            # Special handling for autonomous thinking (slower, different style)
            duration = 500 if is_autonomous else 300
            
            # Get affected cubies based on face
            affected_cubies = self._get_face_cubies(face)
            
            # Get node name for description
            node_name = self._get_node_name(node_id)
            
            moves.append({
                'move': move_notation,
                'node': node_id,
                'node_name': node_name,
                'description': f'{node_name} processing',
                'duration': duration,
                'cubies_affected': affected_cubies,
                'energy': 0.7 + (i * 0.05),  # Energy increases through sequence
                'is_autonomous': is_autonomous
            })
        
        return moves
    
    def _get_face_cubies(self, face: str) -> List[int]:
        """Get cubie indices for each face of the Rubik's cube."""
        face_map = {
            'F': [0, 1, 2, 3, 4, 5, 6, 7, 8],        # Front = bottom layer
            'R': [2, 5, 8, 11, 14, 17, 20, 23, 26],  # Right = right column
            'U': [18, 19, 20, 21, 22, 23, 24, 25, 26],  # Up = top layer
            'L': [0, 3, 6, 9, 12, 15, 18, 21, 24],   # Left = left column
            'D': [0, 1, 2, 3, 4, 5, 6, 7, 8],        # Down = bottom layer (same as front)
            'B': [18, 19, 20, 21, 22, 23, 24, 25, 26],  # Back = top layer (same as up)
        }
        return face_map.get(face, [])
    
    def _get_node_name(self, node_id: int) -> str:
        """Get human-readable node name."""
        node_names = {
            1: 'Reactive',
            3: 'Executive',
            6: 'Emotional',
            7: 'Pattern',
            9: 'Perception',
            10: 'Integration',
            11: 'ToolUse',
            12: 'CodeSynthesis',
            13: 'Introspection'
        }
        return node_names.get(node_id, f'Node{node_id}')
    
    def get_autonomous_animation(self, intention_type: str) -> List[Dict[str, Any]]:
        """
        Generate cube animation for autonomous thinking.
        These are special sequences that visualize self-generated intentions.
        """
        autonomous_sequences = {
            'self_reflection': [
                {'move': 'U', 'description': '🤔 Evaluating internal state', 'duration': 600},
                {'move': 'R', 'description': '🔍 Analyzing patterns', 'duration': 600},
                {'move': 'U\'', 'description': '📊 Computing coherence', 'duration': 600},
                {'move': 'R\'', 'description': '✓ Reflection complete', 'duration': 600},
            ],
            'exploration': [
                {'move': 'F', 'description': '🌱 Exploring new pathways', 'duration': 500},
                {'move': 'R', 'description': '🔬 Testing configurations', 'duration': 500},
                {'move': 'U', 'description': '🎯 Optimizing structure', 'duration': 500},
            ],
            'optimization': [
                {'move': 'R', 'description': '⚡ Strengthening pathways', 'duration': 400},
                {'move': 'U', 'description': '🔧 Adjusting weights', 'duration': 400},
                {'move': 'R\'', 'description': '📈 Measuring efficiency', 'duration': 400},
                {'move': 'U\'', 'description': '✓ Optimization complete', 'duration': 400},
            ],
            'breakthrough': [
                {'move': 'F', 'description': '✨ New capability detected', 'duration': 300},
                {'move': 'R', 'description': '🔥 Synthesizing code', 'duration': 300},
                {'move': 'U', 'description': '🧬 Integrating permanently', 'duration': 300},
                {'move': 'L', 'description': '🎉 Capability acquired!', 'duration': 300},
            ]
        }
        
        return autonomous_sequences.get(intention_type, autonomous_sequences['exploration'])
    
    def get_cubie_state(self, cubie_id: int, cube_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get current state of a specific cubie for visualization.
        Includes role, energy level, patterns stored, etc.
        """
        role_info = self.cubie_roles.get(cubie_id, {'role': 'unknown', 'layer': 'unknown'})
        
        # If this cubie represents a node, get node stats
        node_stats = {}
        if 'node' in role_info:
            node_id = role_info['node']
            if node_id in cube_state.get('nodes', {}):
                node_stats = cube_state['nodes'][node_id]
        
        return {
            'id': cubie_id,
            'role': role_info['role'],
            'layer': role_info['layer'],
            'node_id': role_info.get('node'),
            'development': node_stats.get('development', 0.0),
            'energy': node_stats.get('energy', 0.0),
            'patterns': node_stats.get('pattern_count', 0),
            'active': node_stats.get('active', False)
        }


# =============================================================================
# SENSOR INTERFACE - HOW THE CUBE RECEIVES INPUTS
# =============================================================================

class SensorInterface:
    """
    Interface for feeding signals into the cube.
    This is like the sensory organs - it converts raw inputs into signals.
    """
    
    def __init__(self, cube: MinimalSparkCube):
        self.cube = cube
        self.input_history: List[Signal] = []
    
    def feed_text(self, text: str, metadata: Dict = None, sequence_name: str = None) -> Dict[str, Any]:
        """Feed text input to the cube."""
        signal = Signal(
            type=SignalType.TEXT,
            data=text,
            metadata=metadata or {}
        )
        self.input_history.append(signal)
        return self.cube.process_signal(signal, sequence_name)
    
    def feed_pattern(self, pattern: Any, metadata: Dict = None, sequence_name: str = None) -> Dict[str, Any]:
        """Feed a visual/spatial pattern to the cube."""
        signal = Signal(
            type=SignalType.PATTERN,
            data=pattern,
            metadata=metadata or {}
        )
        self.input_history.append(signal)
        return self.cube.process_signal(signal, sequence_name)
    
    def feed_sequence(self, sequence: List[Any], metadata: Dict = None, sequence_name: str = None) -> Dict[str, Any]:
        """Feed a temporal sequence to the cube."""
        signal = Signal(
            type=SignalType.SEQUENCE,
            data=sequence,
            metadata=metadata or {}
        )
        self.input_history.append(signal)
        return self.cube.process_signal(signal, sequence_name)
    
    def feed_binary(self, value: bool, metadata: Dict = None, sequence_name: str = None) -> Dict[str, Any]:
        """Feed binary input (yes/no, true/false)."""
        signal = Signal(
            type=SignalType.BINARY,
            data=value,
            metadata=metadata or {}
        )
        self.input_history.append(signal)
        return self.cube.process_signal(signal, sequence_name)
    
    def feed_numeric(self, value: float, metadata: Dict = None, sequence_name: str = None) -> Dict[str, Any]:
        """Feed numerical input."""
        signal = Signal(
            type=SignalType.NUMERIC,
            data=value,
            metadata=metadata or {}
        )
        self.input_history.append(signal)
        return self.cube.process_signal(signal, sequence_name)
    
    def get_history_summary(self) -> Dict[str, Any]:
        """Get summary of all inputs."""
        return {
            'total_inputs': len(self.input_history),
            'by_type': {
                st.value: sum(1 for s in self.input_history if s.type == st)
                for st in SignalType
            }
        }
    
    def load_capability(self, filepath: Path) -> bool:
        """Dynamically load a synthesized capability into the cube."""
        try:
            import importlib.util
            import sys
            
            # Load module from file
            spec = importlib.util.spec_from_file_location(
                filepath.stem, filepath
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[filepath.stem] = module
                spec.loader.exec_module(module)
                
                # Find classes in module and instantiate them
                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type) and name not in ['str', 'int', 'float', 'dict', 'list']:
                        # Instantiate the class
                        instance = obj()
                        
                        # Register in capability registry
                        capability_name = filepath.stem
                        if not hasattr(self.cube, 'dynamic_capabilities'):
                            self.cube.dynamic_capabilities = {}
                        
                        self.cube.dynamic_capabilities[capability_name] = instance
                        
                        print(f"   ✓ Loaded capability: {capability_name} ({name} class)")
                        return True
            
            return False
            
        except Exception as e:
            print(f"   ✗ Failed to load capability: {e}")
            return False
    
    def invoke_capability(self, goal: str, data: Any = None) -> Dict:
        """Invoke loaded capabilities that match the goal with robust argument inference."""
        if not hasattr(self.cube, 'dynamic_capabilities'):
            return {'success': False, 'reason': 'no_capabilities'}
        
        results = []
        
        # Find capabilities matching the goal keywords
        goal_keywords = goal.lower().split()
        
        for cap_name, cap_instance in self.cube.dynamic_capabilities.items():
            # Check if capability name relates to goal
            cap_keywords = cap_name.lower().replace('_', ' ').split()
            
            # If any keyword matches, try to use this capability
            if any(kw in goal_keywords for kw in cap_keywords):
                try:
                    # Try to invoke the capability with smart method discovery
                    invoked = False
                    
                    # Strategy 1: Look for common method names
                    method_names = ['process', 'execute', 'calculate', 'analyze', 'recognize', 
                                   'build', 'perform', 'run', 'apply', 'transform']
                    
                    for method_name in method_names:
                        if hasattr(cap_instance, method_name):
                            method = getattr(cap_instance, method_name)
                            
                            # Try multiple invocation strategies
                            strategies = [
                                lambda: method(data) if data else None,  # With data
                                lambda: method(),  # No args
                                lambda: method(goal),  # With goal string
                                lambda: method([data]) if data else None,  # With list
                                lambda: method(data, context={}) if data else None,  # With context
                            ]
                            
                            for strategy in strategies:
                                try:
                                    result = strategy()
                                    if result is not None:  # Only count if we got a result
                                        results.append({
                                            'capability': cap_name,
                                            'method': method_name,
                                            'result': result,
                                            'success': True
                                        })
                                        invoked = True
                                        break
                                except (TypeError, AttributeError):
                                    continue
                                except Exception as e:
                                    # Real error, not just wrong arguments
                                    results.append({
                                        'capability': cap_name,
                                        'method': method_name,
                                        'error': str(e),
                                        'success': False
                                    })
                                    invoked = True
                                    break
                            
                            if invoked:
                                break
                    
                    # Strategy 2: If no standard methods, try __call__
                    if not invoked and callable(cap_instance):
                        try:
                            result = cap_instance(data) if data else cap_instance()
                            results.append({
                                'capability': cap_name,
                                'method': '__call__',
                                'result': result,
                                'success': True
                            })
                            invoked = True
                        except Exception as e:
                            results.append({
                                'capability': cap_name,
                                'method': '__call__',
                                'error': str(e),
                                'success': False
                            })
                    
                    # Strategy 3: If still not invoked, count as partial success
                    # (capability exists but couldn't invoke)
                    if not invoked:
                        results.append({
                            'capability': cap_name,
                            'methods_found': [m for m in method_names if hasattr(cap_instance, m)],
                            'success': False,
                            'reason': 'no_invocable_methods'
                        })
                        
                except Exception as e:
                    results.append({
                        'capability': cap_name,
                        'error': str(e),
                        'success': False
                    })
        
        # Success if ANY capability was invoked successfully
        successful = [r for r in results if r.get('success', False)]
        
        if successful:
            return {
                'success': True,
                'capabilities_invoked': len(successful),
                'results': results,
                'successful_count': len(successful),
                'total_attempts': len(results)
            }
        
        return {
            'success': False, 
            'reason': 'no_successful_invocations',
            'attempts': len(results),
            'capabilities_found': len(results)
        }


# =============================================================================
# HIERARCHICAL MEMORY INTEGRATION
# =============================================================================

def integrate_hierarchical_memory(cube: MinimalSparkCube, memory_path: str = "spark_cube/memory") -> 'HierarchicalMemory':
    """
    Integrate hierarchical memory system with the existing cube.
    
    This wraps process_signal() to automatically record experiences along each pathway,
    building up secondary nodes that strengthen with use and eventually promote to
    anchor nodes when they reach maturity.
    
    Args:
        cube: The MinimalSparkCube instance to enhance
        memory_path: Path to store hierarchical memory state (currently unused, memory path is hardcoded)
        
    Returns:
        HierarchicalMemory instance attached to the cube
    """
    try:
        from .hierarchical_memory import integrate_with_cube
        
        # Create and attach hierarchical memory (note: integrate_with_cube creates its own HierarchicalMemory)
        hierarchical_memory = integrate_with_cube(cube)
        
        print("✓ Hierarchical Memory integrated")
        print(f"  • 13 base anchor nodes (original cube architecture)")
        print(f"  • Secondary nodes will develop dynamically as pathways are used")
        print(f"  • Experiences recorded with semantic similarity")
        print(f"  • Node promotion at strength ≥0.85, 20+ experiences, 70% success")
        print(f"  • Memory persists to spark_cube/memory/hierarchical_memory.json")
        
        return hierarchical_memory
        
    except ImportError as e:
        print(f"⚠️  Hierarchical Memory not available: {e}")
        print("   Continuing with standard memory architecture")
        return None


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Create the minimal cube
    cube = MinimalSparkCube()
    sensor = SensorInterface(cube)
    
    print("\n📊 Initial State:")
    state = cube.get_state_summary()
    print(f"   Experiences: {state['total_experiences']}")
    print(f"   Avg Development: {state['avg_development']:.3f}")
    
    # Feed some signals
    print("\n🔄 Feeding signals...")
    
    # Text signals
    sensor.feed_text("hello")
    sensor.feed_text("hello")  # Repeated - should strengthen pattern
    sensor.feed_text("world")
    
    # Numeric signals
    sensor.feed_numeric(42)
    sensor.feed_numeric(45)
    sensor.feed_numeric(-10)
    
    # Binary signals
    sensor.feed_binary(True)
    sensor.feed_binary(False)
    
    print("\n📊 After 8 experiences:")
    state = cube.get_state_summary()
    print(f"   Experiences: {state['total_experiences']}")
    print(f"   Avg Development: {state['avg_development']:.3f}")
    
    print("\n🧠 Node States:")
    for nid, nstate in state['node_states'].items():
        print(f"   {nstate['name']}: dev={nstate['development']:.3f}, "
              f"patterns={nstate['patterns_learned']}, "
              f"activations={nstate['activations']}")
    
    # Save the structure
    save_path = Path("data/minimal_spark_state.json")
    cube.save_structure(save_path)
    
    print("\n✅ The cube has learned from 8 experiences.")
    print("   Knowledge is encoded in its structure, not external memory.")
    print("   Each node now recognizes patterns it has encountered.")
