"""
AGI-READY SYNTHESIS ENGINE
==========================

Phase 3: Prove AGI
- Remove all hardcoded synthesis triggers
- Generic gap detection that works for ANY capability
- Meta-pattern recognition (patterns about patterns)
- Autonomous capability discovery
- Universal code synthesis (not limited to specific classes)

This replaces keyword-based synthesis with true emergent intelligence.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import re
from pathlib import Path


@dataclass
class CapabilityGap:
    """Represents a detected gap in the system's capabilities."""
    gap_type: str  # 'missing_operation', 'inefficient_pattern', 'knowledge_gap'
    signal_data: str
    context: Dict
    evidence: List[str]  # What led to detecting this gap
    confidence: float  # 0-1 confidence score
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            'gap_type': self.gap_type,
            'signal_data': self.signal_data,
            'context': self.context,
            'evidence': self.evidence,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class CapabilityPattern:
    """Learned pattern about what capabilities exist and how to recognize them."""
    pattern_type: str  # 'operation', 'transformation', 'analysis', 'generation'
    indicators: List[str]  # Patterns that suggest this capability is needed
    abstraction_level: int  # 0=concrete, 1=domain-specific, 2=abstract, 3=meta
    examples: List[Dict]  # Example signals that triggered this pattern
    success_rate: float  # How often this pattern leads to successful synthesis
    
    def matches(self, signal_data: str, context: Dict) -> float:
        """Returns confidence score 0-1 that this pattern applies."""
        text_lower = signal_data.lower()
        
        # Count matching indicators
        matches = sum(1 for indicator in self.indicators if indicator in text_lower)
        if matches == 0:
            return 0.0
        
        # Confidence based on match ratio and success rate
        match_ratio = matches / len(self.indicators)
        confidence = (match_ratio * 0.7) + (self.success_rate * 0.3)
        
        return min(confidence, 1.0)


class GenericGapDetector:
    """
    Detects capability gaps without hardcoded keywords.
    Uses meta-patterns learned from experience.
    """
    
    def __init__(self):
        self.capability_patterns: List[CapabilityPattern] = []
        self.detected_gaps: List[CapabilityGap] = []
        self.failure_patterns: List[Dict] = []  # Patterns of what causes failures
        
    def detect_gap(self, signal, context: Dict, processing_result: Dict) -> Optional[CapabilityGap]:
        """
        Detect if there's a capability gap in handling this signal.
        
        Gap indicators:
        1. Long processing time (inefficiency)
        2. Multiple node activations with no result
        3. External knowledge fetch without capability synthesis
        4. Repeated similar signals without improvement
        5. Pattern exists but no executable capability
        """
        
        evidence = []
        gap_type = None
        confidence = 0.0
        
        # BOOTSTRAP: If we have very few capabilities and no clear success, assume gap
        # This kickstarts the AGI from zero
        if len(self.detected_gaps) < 10 and not processing_result.get('synthesized_response'):
            evidence.append("Bootstrap mode: System has minimal capabilities, assuming gap")
            gap_type = 'knowledge_gap'
            confidence += 0.4
        
        # Indicator 1: Knowledge acquired but no capability synthesized
        if context.get('external_knowledge_acquired') and not context.get('capability_synthesized'):
            evidence.append("External knowledge acquired but no capability created")
            gap_type = 'missing_operation'
            confidence += 0.3
        
        # Indicator 2: Pattern recognized but execution failed
        if context.get('patterns_matched', 0) > 0 and not processing_result.get('success'):
            evidence.append("Patterns matched but execution failed")
            if not gap_type:
                gap_type = 'inefficient_pattern'
            confidence += 0.2
        
        # Indicator 3: Multiple attempts with no progress
        repeated_signals = self._count_similar_signals(signal, context)
        if repeated_signals > 2:
            evidence.append(f"Similar signal repeated {repeated_signals} times without improvement")
            if not gap_type:
                gap_type = 'knowledge_gap'
            confidence += 0.3
        
        # Indicator 4: High node activation count (inefficient processing)
        if context.get('node_activation_count', 0) > 5:
            evidence.append(f"High node activations ({context['node_activation_count']}) suggest inefficiency")
            if not gap_type:
                gap_type = 'inefficient_pattern'
            confidence += 0.2
        
        # Indicator 5: Check learned capability patterns
        for pattern in self.capability_patterns:
            pattern_confidence = pattern.matches(str(signal.data), context)
            if pattern_confidence > 0.6:
                evidence.append(f"Matches learned pattern '{pattern.pattern_type}' ({pattern_confidence:.0%})")
                if not gap_type:
                    gap_type = 'missing_operation'
                confidence += pattern_confidence * 0.4
        
        confidence = min(confidence, 1.0)
        
        # Lower threshold for initial capability building
        # Once we have capabilities, we can be more selective
        threshold = 0.25 if len(self.detected_gaps) < 20 else 0.4
        
        # Only return gap if confidence is high enough
        if confidence >= threshold and gap_type:
            gap = CapabilityGap(
                gap_type=gap_type,
                signal_data=str(signal.data),
                context=context.copy(),
                evidence=evidence,
                confidence=confidence,
                timestamp=datetime.now()
            )
            self.detected_gaps.append(gap)
            return gap
        
        return None
    
    def _count_similar_signals(self, signal, context: Dict) -> int:
        """Count how many similar signals have been processed recently."""
        # Look at recent gaps
        similar_count = 0
        signal_text = str(signal.data).lower()
        
        for gap in self.detected_gaps[-20:]:  # Last 20 gaps
            gap_text = gap.signal_data.lower()
            
            # Simple similarity: shared words
            signal_words = set(signal_text.split())
            gap_words = set(gap_text.split())
            
            if signal_words & gap_words:  # Intersection
                overlap = len(signal_words & gap_words) / max(len(signal_words), 1)
                if overlap > 0.3:
                    similar_count += 1
        
        return similar_count
    
    def learn_capability_pattern(self, gap: CapabilityGap, synthesis_result: Dict):
        """
        Learn a new capability pattern from successful synthesis.
        This is meta-learning: learning about what capabilities exist.
        """
        # Extract indicators from the signal that led to synthesis
        signal_words = gap.signal_data.lower().split()
        
        # Identify pattern type from context
        pattern_type = synthesis_result.get('capability_type', 'unknown')
        
        # Create or update pattern
        existing_pattern = None
        for pattern in self.capability_patterns:
            if pattern.pattern_type == pattern_type:
                existing_pattern = pattern
                break
        
        if existing_pattern:
            # Update existing pattern
            existing_pattern.indicators = list(set(existing_pattern.indicators + signal_words[:10]))
            existing_pattern.examples.append({
                'signal': gap.signal_data,
                'confidence': gap.confidence,
                'result': synthesis_result.get('success', False)
            })
            
            # Update success rate
            successes = sum(1 for ex in existing_pattern.examples if ex.get('result'))
            existing_pattern.success_rate = successes / len(existing_pattern.examples)
        else:
            # Create new pattern
            new_pattern = CapabilityPattern(
                pattern_type=pattern_type,
                indicators=signal_words[:10],  # Top 10 words as indicators
                abstraction_level=self._infer_abstraction_level(pattern_type),
                examples=[{
                    'signal': gap.signal_data,
                    'confidence': gap.confidence,
                    'result': synthesis_result.get('success', False)
                }],
                success_rate=1.0 if synthesis_result.get('success') else 0.0
            )
            self.capability_patterns.append(new_pattern)
    
    def _infer_abstraction_level(self, pattern_type: str) -> int:
        """Infer abstraction level from pattern type."""
        # Level 0: Concrete operations (add, subtract)
        concrete = ['arithmetic', 'string_operation', 'file_io']
        
        # Level 1: Domain-specific (language, image processing)
        domain = ['language_generation', 'image_processing', 'data_parsing']
        
        # Level 2: Abstract (analysis, optimization)
        abstract = ['pattern_analysis', 'optimization', 'classification']
        
        # Level 3: Meta (learning about learning)
        meta = ['meta_learning', 'self_modification', 'capability_synthesis']
        
        if any(p in pattern_type for p in concrete):
            return 0
        elif any(p in pattern_type for p in domain):
            return 1
        elif any(p in pattern_type for p in abstract):
            return 2
        elif any(p in pattern_type for p in meta):
            return 3
        else:
            return 1  # Default to domain-specific


class UniversalCodeSynthesizer:
    """
    Synthesizes ANY type of code, not limited to predefined classes.
    Uses pattern analysis + LLM to generate appropriate code structure.
    """
    
    def __init__(self, external_interface=None):
        self.external_interface = external_interface
        self.synthesis_history: List[Dict] = []
        self.code_templates: Dict[str, str] = {}
        
    def synthesize_capability(self, gap: CapabilityGap, 
                            external_knowledge: List[Dict]) -> Optional[Tuple[str, str]]:
        """
        Synthesize code to fill the capability gap.
        Returns (code, capability_type) or None if synthesis fails.
        """
        
        # Step 1: Analyze the gap to determine what kind of capability is needed
        capability_spec = self._analyze_gap(gap, external_knowledge)
        
        if not capability_spec:
            return None
        
        # Step 2: Generate code based on the specification
        code = self._generate_code(capability_spec, gap, external_knowledge)
        
        if code:
            # Record synthesis attempt
            self.synthesis_history.append({
                'gap': gap.to_dict(),
                'capability_type': capability_spec['type'],
                'code_generated': True,
                'timestamp': datetime.now().isoformat()
            })
            
            return code, capability_spec['type']
        
        return None
    
    def _analyze_gap(self, gap: CapabilityGap, 
                    external_knowledge: List[Dict]) -> Optional[Dict]:
        """
        Analyze the gap to determine what capability is needed.
        Returns a specification for the capability.
        """
        
        # Use LLM to analyze the gap
        if not (self.external_interface and self.external_interface.enabled):
            return None
        
        analysis_prompt = f"""Analyze this capability gap and determine what type of code capability is needed:

Gap Type: {gap.gap_type}
Signal: {gap.signal_data}
Evidence: {json.dumps(gap.evidence, indent=2)}
Confidence: {gap.confidence:.0%}

External Knowledge Available:
{json.dumps(external_knowledge[:3], indent=2) if external_knowledge else 'None'}

Determine:
1. What TYPE of capability is needed (be specific: 'json_parser', 'http_client', 'text_summarizer', etc.)
2. What OPERATIONS this capability should perform (list 3-5 key methods)
3. What INPUTS and OUTPUTS each operation needs
4. Any DEPENDENCIES or requirements

Respond in JSON format:
{{
    "type": "capability_name",
    "description": "brief description",
    "operations": [
        {{"name": "method_name", "inputs": ["input1"], "output": "output_type", "purpose": "what it does"}}
    ],
    "dependencies": ["any external modules needed"],
    "complexity": "simple|moderate|complex"
}}"""

        try:
            response = self.external_interface.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            spec_text = response.content[0].text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', spec_text, re.DOTALL)
            if json_match:
                spec = json.loads(json_match.group())
                return spec
            
        except Exception as e:
            print(f"   ✗ Gap analysis failed: {e}")
        
        return None
    
    def _generate_code(self, capability_spec: Dict, gap: CapabilityGap,
                      external_knowledge: List[Dict]) -> Optional[str]:
        """Generate actual Python code based on the specification."""
        
        if not (self.external_interface and self.external_interface.enabled):
            return None
        
        # Build comprehensive code generation prompt
        operations_desc = "\n".join([
            f"{i+1}. {op['name']}({', '.join(op.get('inputs', []))}) -> {op.get('output', 'Any')}"
            f"\n   Purpose: {op.get('purpose', 'No description')}"
            for i, op in enumerate(capability_spec.get('operations', []))
        ])
        
        knowledge_context = "\n".join([
            f"- {k.get('content', '')[:200]}" for k in external_knowledge[:5]
        ]) if external_knowledge else "Use general programming knowledge"
        
        generation_prompt = f"""Generate Python code for this capability:

Capability: {capability_spec['type']}
Description: {capability_spec.get('description', 'No description')}
Complexity: {capability_spec.get('complexity', 'moderate')}

Required Operations:
{operations_desc}

Dependencies: {', '.join(capability_spec.get('dependencies', ['none']))}

Context/Knowledge:
{knowledge_context}

Requirements:
- Create a Python class named '{self._to_class_name(capability_spec['type'])}'
- Implement ALL specified operations as methods
- Add helpful docstrings
- Handle errors gracefully (try/except where appropriate)
- Keep it simple and readable
- Use type hints where helpful
- No external API calls unless explicitly required
- Include __init__ method if state is needed

Return ONLY the Python class code, no markdown formatting, no explanations."""

        try:
            response = self.external_interface.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": generation_prompt}]
            )
            
            code = response.content[0].text.strip()
            
            # Clean up code
            code = code.replace('```python', '').replace('```', '').strip()
            
            return code
            
        except Exception as e:
            print(f"   ✗ Code generation failed: {e}")
        
        return None
    
    def _to_class_name(self, capability_type: str) -> str:
        """Convert capability_type to PascalCase class name."""
        # json_parser -> JsonParser
        # http_client -> HttpClient
        words = capability_type.split('_')
        return ''.join(word.capitalize() for word in words)


class AutonomousExplorer:
    """
    Explores and discovers capabilities without external prompting.
    Generates its own "curiosity signals" to expand capabilities.
    """
    
    def __init__(self):
        self.exploration_domains = [
            'data_processing', 'text_analysis', 'numerical_computation',
            'pattern_recognition', 'optimization', 'visualization',
            'communication', 'memory_management', 'meta_learning'
        ]
        self.explored_capabilities: Dict[str, int] = {}  # domain -> count
        self.exploration_queue: List[Dict] = []
        
    def generate_exploration_signal(self, current_capabilities: List[str],
                                   processing_history: List[Dict]) -> Optional[Dict]:
        """
        Generate a synthetic signal to explore a new capability area.
        This is true autonomy - acting without external input.
        """
        
        # Identify unexplored or under-explored domains
        unexplored = []
        for domain in self.exploration_domains:
            count = self.explored_capabilities.get(domain, 0)
            if count < 3:  # Explore each domain at least 3 times
                unexplored.append((domain, count))
        
        if not unexplored:
            return None
        
        # Pick the least explored domain
        target_domain = min(unexplored, key=lambda x: x[1])[0]
        
        # Generate a curiosity signal for this domain
        exploration_signal = {
            'type': 'autonomous_exploration',
            'domain': target_domain,
            'signal_data': self._generate_domain_query(target_domain),
            'timestamp': datetime.now().isoformat(),
            'motivation': 'capability_expansion'
        }
        
        self.explored_capabilities[target_domain] = self.explored_capabilities.get(target_domain, 0) + 1
        
        return exploration_signal
    
    def _generate_domain_query(self, domain: str) -> str:
        """Generate a query that would require capabilities in this domain."""
        
        queries = {
            'data_processing': "Parse and transform structured data from various formats",
            'text_analysis': "Analyze text sentiment, extract entities, summarize content",
            'numerical_computation': "Perform statistical analysis and numerical optimization",
            'pattern_recognition': "Identify patterns in sequences and classify data",
            'optimization': "Optimize processes and find efficient solutions",
            'visualization': "Create visual representations of data and processes",
            'communication': "Generate natural language and communicate effectively",
            'memory_management': "Efficiently store, retrieve, and organize information",
            'meta_learning': "Learn how to learn, improve learning strategies"
        }
        
        return queries.get(domain, f"Explore capabilities in {domain}")


class AGISynthesisEngine:
    """
    Main AGI synthesis engine that orchestrates all components.
    This replaces the hardcoded synthesis in CodeSynthesisNode.
    """
    
    def __init__(self, external_interface=None):
        self.gap_detector = GenericGapDetector()
        self.code_synthesizer = UniversalCodeSynthesizer(external_interface)
        self.explorer = AutonomousExplorer()
        
        self.total_synthesis_attempts = 0
        self.successful_syntheses = 0
        self.capability_registry: Dict[str, Dict] = {}
        
    def process(self, signal, context: Dict, processing_result: Dict,
               external_knowledge: List[Dict]) -> Optional[Dict]:
        """
        Main AGI synthesis loop.
        Returns synthesis result or None.
        """
        
        # Step 1: Detect capability gap
        gap = self.gap_detector.detect_gap(signal, context, processing_result)
        
        if not gap:
            return None
        
        # 🔥 FIX 2: Check if similar capability already exists
        existing_capability = self._find_similar_capability(gap.gap_type)
        if existing_capability:
            print(f"\n♻️  Reusing Existing Capability: {existing_capability}")
            print(f"   Gap type: {gap.gap_type}")
            print(f"   Similar to: {existing_capability}")
            return {
                'success': True,
                'capability_type': existing_capability,
                'code': self.capability_registry[existing_capability]['code'],
                'gap': gap.to_dict(),
                'reused': True
            }
        
        print(f"\n🔍 Capability Gap Detected:")
        print(f"   Type: {gap.gap_type}")
        print(f"   Confidence: {gap.confidence:.0%}")
        print(f"   Evidence:")
        for evidence in gap.evidence:
            print(f"   - {evidence}")
        
        # Step 2: Synthesize capability to fill gap
        self.total_synthesis_attempts += 1
        
        synthesis_result = self.code_synthesizer.synthesize_capability(gap, external_knowledge)
        
        if not synthesis_result:
            return None
        
        code, capability_type = synthesis_result
        
        print(f"\n💡 Synthesizing Capability: {capability_type}")
        
        # Step 3: Test the synthesized code
        if not self._test_capability(code, capability_type):
            return {'success': False, 'capability_type': capability_type}
        
        # Step 4: Learn from successful synthesis
        self.successful_syntheses += 1
        result = {
            'success': True,
            'capability_type': capability_type,
            'code': code,
            'gap': gap.to_dict()
        }
        
        self.gap_detector.learn_capability_pattern(gap, result)
        self.capability_registry[capability_type] = {
            'code': code,
            'synthesized_at': datetime.now().isoformat(),
            'gap_confidence': gap.confidence,
            'success': True
        }
        
        print(f"   ✓ Capability '{capability_type}' synthesized and integrated")
        print(f"   Total capabilities: {len(self.capability_registry)}")
        print(f"   Success rate: {self.successful_syntheses}/{self.total_synthesis_attempts} ({self.successful_syntheses/max(self.total_synthesis_attempts,1)*100:.0f}%)")
        
        return result
    
    def _find_similar_capability(self, gap_type: str) -> Optional[str]:
        """Check if similar capability already exists in registry."""
        gap_keywords = set(gap_type.lower().replace('_', ' ').split())
        
        # Check for exact match first
        if gap_type in self.capability_registry:
            return gap_type
        
        # Check for semantic similarity
        best_match = None
        best_score = 0
        
        for existing_cap in self.capability_registry.keys():
            cap_keywords = set(existing_cap.lower().replace('_', ' ').split())
            
            # Calculate keyword overlap
            overlap = len(gap_keywords & cap_keywords)
            total = len(gap_keywords | cap_keywords)
            
            if total > 0:
                similarity = overlap / total
                
                # If >70% similar, consider it a match
                if similarity > 0.7 and similarity > best_score:
                    best_score = similarity
                    best_match = existing_cap
        
        return best_match
    
    def _test_capability(self, code: str, capability_type: str) -> bool:
        """Test synthesized code before integration."""
        try:
            # Basic syntax check
            compile(code, '<synthesized>', 'exec')
            
            # Try to execute and instantiate
            namespace = {}
            exec(code, namespace)
            
            # Find the class
            class_name = self.code_synthesizer._to_class_name(capability_type)
            if class_name not in namespace:
                print(f"   ✗ Class {class_name} not found in synthesized code")
                return False
            
            # Try to instantiate
            instance = namespace[class_name]()
            
            print(f"   ✓ Code compiles and executes successfully")
            return True
            
        except Exception as e:
            print(f"   ✗ Capability test failed: {e}")
            return False
    
    def explore_autonomously(self, current_capabilities: List[str],
                           processing_history: List[Dict]) -> Optional[Dict]:
        """Generate an autonomous exploration signal."""
        return self.explorer.generate_exploration_signal(
            current_capabilities, processing_history
        )
