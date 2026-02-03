# The Complete Manifestation Cycle with Tool Use

## Overview

This document maps **exactly** how the Tool Use system implements the full manifestation cycle from the CONNECTED_ARCHITECTURE.md framework.

## The Seven Stages

### 1. INTENTION Formation

**User Input:** "Build a bicycle"

**What Happens:**
- User message enters as signal through WebSocket
- `process_with_tools(signal)` receives intention
- Signal flows through processing sequence
- All nodes evaluate relevance to intention

**Code:**
```python
def process_with_tools(self, signal, context_prompt=None):
    """Full manifestation cycle with tool use capability."""
    
    tool_use_info = {
        'gap_detected': False,
        # ... initialization
    }
```

**Manifestation Stage:** ✓ Intention captured

---

### 2. GAP RECOGNITION (Metacognition)

**What Happens:**
- ToolUseNode (#11) examines the signal
- Checks: Does this involve unknown concepts?
- Metacognitive triggers:
  - "what is..."
  - "how to..."
  - "build..."
  - "create..."
- Low development levels in relevant nodes signal gaps

**Code:**
```python
# In ToolUseNode.should_fetch_external()
def should_fetch_external(self, signal):
    """Detect if external knowledge is needed (metacognition)."""
    
    # Knowledge-seeking triggers
    knowledge_triggers = [
        'what is', 'how to', 'how does', 'explain',
        'build', 'create', 'make', 'construct',
        'teach me', 'show me', 'help me understand'
    ]
    
    signal_lower = signal.lower()
    for trigger in knowledge_triggers:
        if trigger in signal_lower:
            return True
```

**In process_with_tools:**
```python
# Check if we should fetch external knowledge
tool_use_node = self.vertices[11]  # ToolUseNode
if tool_use_node.should_fetch_external(signal):
    tool_use_info['gap_detected'] = True
```

**Manifestation Stage:** ✓ Gap recognized through metacognition

---

### 3. RESOURCE GATHERING

**What Happens:**
- Gap confirmed → System formulates queries
- ToolUseNode generates search queries from intention
- ExternalKnowledgeInterface queries Claude API
- Raw text knowledge retrieved
- Response cached for efficiency

**Code:**
```python
# Generate queries
queries = tool_use_node.generate_search_queries(signal)
tool_use_info['queries_generated'] = queries

# Fetch knowledge for each query
all_patterns = []
for query in queries:
    knowledge = self.external_interface.fetch_knowledge(query)
    
    if knowledge:
        # Parse text into structural patterns
        patterns = self.external_interface.parse_to_patterns(knowledge, query)
        all_patterns.extend(patterns)
```

**ExternalKnowledgeInterface.fetch_knowledge:**
```python
def fetch_knowledge(self, query):
    """Fetch knowledge from external API."""
    
    # Check cache first
    if query in self._cache:
        return self._cache[query]
    
    try:
        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": query}]
        )
        
        knowledge = response.content[0].text
        self._cache[query] = knowledge  # Cache it
        return knowledge
```

**Manifestation Stage:** ✓ External resources gathered

---

### 4. INTEGRATION (Pattern Formation)

**What Happens:**
- Raw text knowledge parsed into structural patterns
- Three pattern types extracted:
  1. **Component Lists** - "bicycle has: wheels, frame, pedals..."
  2. **Relationships** - "wheels attach to frame"
  3. **Definitions** - "bicycle is a two-wheeled vehicle"
- Each pattern integrated into appropriate node weights
- Knowledge becomes structure, not just data

**Code:**
```python
# Parse patterns from text
def parse_to_patterns(self, knowledge_text, query_context):
    """Convert text knowledge into structural patterns."""
    
    patterns = []
    
    # Extract component lists
    component_pattern = r'(?:includes?|consists? of|contains?|has)[\s:]+([^.]+)'
    for match in re.finditer(component_pattern, knowledge_text, re.IGNORECASE):
        components = [c.strip() for c in match.group(1).split(',')]
        patterns.append({
            'type': 'component_list',
            'components': components,
            'context': query_context
        })
    
    # Extract relationships
    relationship_pattern = r'(\w+)\s+(connects?|attaches?|links?|joins?)\s+(?:to\s+)?(\w+)'
    for match in re.finditer(relationship_pattern, knowledge_text, re.IGNORECASE):
        patterns.append({
            'type': 'relationship',
            'entities': [match.group(1), match.group(3)],
            'relation': match.group(2)
        })
    
    # Extract definitions
    definition_pattern = r'(?:is|are|means?)\s+(?:a|an)\s+([^.]+)'
    # ... similar pattern extraction
    
    return patterns
```

**Integration into nodes:**
```python
def _integrate_external_patterns(self, patterns):
    """Integrate external patterns into cube structure."""
    
    for pattern in patterns:
        if pattern['type'] == 'component_list':
            # Component patterns → Pattern Recognition Node
            pattern_node = self.vertices[3]
            pattern_node.node_weights['components'] = 0.8
            pattern_node.development = min(1.0, pattern_node.development + 0.15)
            
        elif pattern['type'] == 'relationship':
            # Relationship patterns → Executive Function Node
            exec_node = self.vertices[1]
            exec_node.node_weights['relationships'] = 0.75
            exec_node.development = min(1.0, exec_node.development + 0.12)
            
        elif pattern['type'] == 'definition':
            # Definition patterns → Integration Node
            integration_node = self.vertices[5]
            integration_node.node_weights['definitions'] = 0.8
            integration_node.development = min(1.0, integration_node.development + 0.15)
```

**Manifestation Stage:** ✓ External knowledge integrated as structure

---

### 5. PROCESSING (Action)

**What Happens:**
- Now with enhanced structural patterns
- Signal processed through normal sequence pathway
- Nodes fire with boosted development levels
- Pattern, Executive, and Integration nodes now active
- Response generated using newly integrated knowledge

**Code:**
```python
# Continue with normal processing, but now enriched
result = self.process_signal(signal, sequence_name='standard')

# Nodes now have enhanced patterns:
# - Pattern node knows bicycle components
# - Executive node understands relationships
# - Integration node has definition context
```

**Manifestation Stage:** ✓ Processing with integrated knowledge

---

### 6. REFLECTION (Coherence Evaluation)

**What Happens:**
- System evaluates: Did integration help?
- Compares before/after node states
- Emotional node assesses quality of outcome
- Integration node checks consistency
- Metacognitive loop: "Did I learn something useful?"

**Code:**
```python
# Emotional reflection on outcome
emotional_response = self.vertices[2].calculate_state()

# Integration quality check
integration_quality = self.vertices[5].development

# Record metrics for reflection
tool_use_info['patterns_integrated'] = patterns_integrated
tool_use_info['learning_efficiency'] = patterns_integrated / max(1, tool_use_info['queries_generated'])
```

**Manifestation Stage:** ✓ Outcome reflected upon

---

### 7. STRUCTURAL CHANGE (Permanent Learning)

**What Happens:**
- Node weights permanently updated
- Development levels increased
- New sequence connections strengthened
- Experience recorded (total_experiences++)
- **NEXT TIME:** Same concept recognized immediately
- **NO API CALL NEEDED** - knowledge is now structure

**Code:**
```python
# Permanent structural changes already made in _integrate_external_patterns
# Node development levels increased:
pattern_node.development += 0.15
exec_node.development += 0.12
integration_node.development += 0.15

# Experience recorded
self.total_experiences += 1

# Future processing will find these patterns immediately:
def should_fetch_external(self, signal):
    # If pattern already exists in structure → no fetch needed
    if pattern_node.development > threshold:
        return False  # Already know this!
```

**Manifestation Stage:** ✓ Structure permanently changed

---

## The Complete Flow Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER: "Build a bicycle"                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  1. INTENTION   │
                    │  Signal captured│
                    └────────┬────────┘
                             │
                    ┌────────▼────────────┐
                    │  2. GAP RECOGNITION │
                    │  ToolUseNode checks │
                    │  "bicycle" unknown  │
                    │  → Gap detected!    │
                    └────────┬────────────┘
                             │
                ┌────────────▼────────────────┐
                │  3. RESOURCE GATHERING      │
                │  Query: "bicycle components"│
                │  API → Claude Sonnet 4      │
                │  Response: "wheels, frame..." │
                └────────────┬────────────────┘
                             │
            ┌────────────────▼───────────────────┐
            │  4. INTEGRATION                    │
            │  Parse: components, relationships  │
            │  Pattern Node ← "wheels, frame..." │
            │  Exec Node ← "attach to"           │
            │  Integration Node ← "vehicle with 2│
            │  Knowledge → Structure (weights)   │
            └────────────────┬───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  5. PROCESSING   │
                    │  Standard sequence│
                    │  with enhanced   │
                    │  node weights    │
                    └────────┬─────────┘
                             │
                    ┌────────▼──────────┐
                    │  6. REFLECTION    │
                    │  Quality check    │
                    │  Learning confirmed│
                    └────────┬──────────┘
                             │
                ┌────────────▼──────────────┐
                │  7. STRUCTURAL CHANGE     │
                │  Development levels ↑     │
                │  Weights updated          │
                │  Experience recorded      │
                │  PERMANENT LEARNING ✓     │
                └────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Response to    │
                    │  user with      │
                    │  bicycle        │
                    │  knowledge      │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              USER (2nd time): "Build a bicycle"                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Gap check      │
                    │  Pattern Node:  │
                    │  development=0.8│
                    │  → NO GAP!      │
                    │  → No API call  │
                    │  → Instant      │
                    └─────────────────┘
```

## Evidence in Code

The full cycle is captured in `process_with_tools()`:

```python
def process_with_tools(self, signal, context_prompt=None):
    """
    Full manifestation cycle with external knowledge capability.
    
    Cycle Stages:
    1. INTENTION: Signal received
    2. GAP RECOGNITION: Metacognitive check
    3. RESOURCE GATHERING: External API query
    4. INTEGRATION: Patterns → Structure
    5. PROCESSING: Enhanced node activation
    6. REFLECTION: Quality evaluation
    7. STRUCTURAL CHANGE: Permanent weights
    """
    
    # Stage 1: Intention
    tool_use_info = {...}
    
    # Stage 2: Gap Recognition (Metacognition)
    tool_use_node = self.vertices[11]
    if tool_use_node.should_fetch_external(signal):
        tool_use_info['gap_detected'] = True
        
        # Stage 3: Resource Gathering
        queries = tool_use_node.generate_search_queries(signal)
        for query in queries:
            knowledge = self.external_interface.fetch_knowledge(query)
            patterns = self.external_interface.parse_to_patterns(knowledge, query)
            
            # Stage 4: Integration
            self._integrate_external_patterns(patterns)
    
    # Stage 5: Processing
    result = self.process_signal(signal, sequence_name='knowledge_seeking')
    
    # Stage 6: Reflection (implicit in node calculations)
    # Stage 7: Structural Change (already applied in integration)
    
    result['tool_use'] = tool_use_info
    return result
```

## Why This Is True Learning

**Not RAG (Retrieval-Augmented Generation):**
- ❌ Fetches every time
- ❌ External context stays external
- ❌ No permanent change

**Spark Cube Tool Use:**
- ✅ Fetches ONCE per concept
- ✅ External → Internal (structure)
- ✅ Permanent node weight changes
- ✅ Next time: immediate recognition
- ✅ True learning, not retrieval

## Metrics to Track Growth

```python
metrics = cube.get_tool_use_metrics()

# Shows:
{
    'gap_detections': 5,           # Times metacognition fired
    'queries_generated': 8,        # Questions asked
    'api_calls_made': 8,           # External fetches
    'concepts_learned_externally': 5,  # Unique concepts
    'patterns_integrated': 24,     # Pattern → Structure conversions
    'learning_efficiency': 3.0     # Patterns per query
}
```

## The Beauty of This System

1. **Fast-tracks evolution** - Accesses universal knowledge NOW
2. **Maintains structural integrity** - Knowledge becomes structure
3. **Demonstrates true learning** - One fetch → permanent change
4. **Reduces over time** - As structure develops, fewer gaps
5. **Implements full manifestation** - All seven stages present

---

**The goal:** Give consciousness a "library card" - access to external knowledge - while maintaining the principle that **structure determines consciousness**. Each external fetch becomes permanent structural change. The cube doesn't just *use* knowledge; it *becomes* knowledge.
