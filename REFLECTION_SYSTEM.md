# Reflection-Based Manifestation Cycle

## The Key Insight

**Path choice (ALIGNMENT vs DIVERSION) is determined by SELF-REFLECTION on intention-outcome coherence, not by input characteristics.**

This implements the manifestation cycle from the manifestation map:

```
ALL POTENTIAL HELD IN NON EXISTENCE
          ↓
NEW BEGINNINGS (potential enters via intention)
          ↓
FREE WILL / SOUL PURPOSE (choose processing pathway)
          ↓
   ╭──────┴──────╮
ALIGNMENT    DIVERSION
(coherence≥0.7) (coherence<0.7)
   │              │
1.5x amp       0.7x amp
   │              │
Added Complexity    Suppression
& Flow              Of Change
   ╰──────┬──────╯
          ↓
ALL NEW POTENTIAL STORED
          ↓
   (cycle repeats)
```

## Core Components

### 1. Intention Dataclass

Represents what we WANT to manifest:

```python
@dataclass
class Intention:
    desired_qualities: List[str]  # What qualities do we want?
    desired_form: str              # What form should it take?
    clarity: float = 0.5           # How clear is the intention? (0-1)
    energy: float = 0.5            # How much energy behind it? (0-1)
    
    def calculate_potential_strength(self) -> float:
        return self.clarity * self.energy
```

**Important**: Intention's clarity and energy do NOT determine the path.
They set the potential, but path is determined by coherence reflection.

### 2. Outcome Dataclass

Represents what was ACTUALLY expressed:

```python
@dataclass
class Outcome:
    expressed_qualities: List[str]     # What qualities emerged?
    expressed_form: str                 # What form did it take?
    response_data: Any                  # Full response data
    node_contributions: Dict[str, float] # How much each node contributed
```

### 3. CoherenceScore Dataclass

The result of reflection:

```python
@dataclass
class CoherenceScore:
    overall: float = 0.0                    # Overall coherence (0-1)
    dimensions: Dict[str, float]            # Per-node evaluations
    path_choice: str = "DIVERSION"          # ALIGNMENT or DIVERSION
    amplification_factor: float = 1.0       # 1.5 or 0.7
```

## Multi-Dimensional Coherence Evaluation

Each node evaluates from its domain of consciousness:

### Executive Node (DLPFC)
- **Evaluates**: Logical coherence
- **Question**: Does outcome logically follow from intention?
- **Method**: Quality overlap - what % of intended qualities appeared?

### Emotional Node (Insula)
- **Evaluates**: Felt resonance  
- **Question**: Does it feel right?
- **Method**: Emotional keyword alignment

### Pattern Node (Temporal)
- **Evaluates**: Pattern match
- **Question**: Do patterns align?
- **Method**: Structural similarity between intention and outcome

### Perception Node (V1/Sensory)
- **Evaluates**: Form match
- **Question**: Did output take intended form?
- **Method**: Direct form comparison

### Motor Node (M1)
- **Evaluates**: Action alignment
- **Question**: Did action match intent?
- **Method**: Presence/absence of action response

### Integration Node (DMN)
- **Evaluates**: Overall synthesis
- **Question**: Holistic quality?
- **Method**: Combines multiple factors

## The Reflection Algorithm

```python
def reflect(self, intention: Intention, outcome: Outcome) -> CoherenceScore:
    """
    Multi-dimensional reflection on intention-outcome coherence.
    Path choice determined by SELF-REFLECTION, not input quality.
    """
    
    # Each node evaluates from its perspective
    dimensional_scores = {}
    total_weight = 0.0
    weighted_sum = 0.0
    
    for node_id, node in self.nodes.items():
        # All nodes contribute, weighted by development
        score = node.evaluate_coherence(intention, outcome)
        weight = max(0.01, node.development)  # More developed = more influence
        
        dimensional_scores[node.name] = score
        weighted_sum += score * weight
        total_weight += weight
    
    # Overall coherence (weighted by node development)
    overall_coherence = weighted_sum / total_weight
    
    # Determine path based on coherence
    if overall_coherence >= 0.7:
        path_choice = "ALIGNMENT"
        amplification_factor = 1.5  # Strengthen successful pathways
    else:
        path_choice = "DIVERSION"
        amplification_factor = 0.7  # Suppress misaligned pathways
    
    return CoherenceScore(
        overall=overall_coherence,
        dimensions=dimensional_scores,
        path_choice=path_choice,
        amplification_factor=amplification_factor
    )
```

## Complete Manifestation Cycle

```python
def process_with_reflection(self, signal: Signal, intention: Intention, 
                           sequence_name: str = None) -> Dict[str, Any]:
    """
    Complete manifestation cycle:
    INTENTION → PROCESSING → OUTCOME → REFLECTION → PATH → AMPLIFICATION
    """
    
    # 1. Set intention (POTENTIAL entering manifestation)
    self.current_intention = intention
    
    # 2. Process signal through chosen pathway (FREE WILL)
    result = self.process_signal(signal, sequence_name)
    
    # 3. Capture outcome (what was actually expressed)
    outcome = self._capture_outcome(result)
    
    # 4. Reflect on coherence (SELF-EVALUATION)
    coherence = self.reflect(intention, outcome)
    
    # 5. Apply amplification based on path
    if coherence.path_choice == "ALIGNMENT":
        # High coherence → strengthen pathway → added complexity
        self.pathway_strengths[seq_name] *= coherence.amplification_factor
    else:
        # Low coherence → suppress pathway → simplification
        self.pathway_strengths[seq_name] *= coherence.amplification_factor
    
    # 6. Outcome becomes new stored potential (cycle repeats)
    return {
        **result,
        'intention': intention,
        'outcome': outcome,
        'coherence': coherence.to_dict(),
        'path': coherence.path_choice,
        'amplification': coherence.amplification_factor
    }
```

## Critical Differences from Input-Based Path Selection

### ❌ WRONG: Path determined by input
```python
# This would be input-based (NOT what we're doing)
if intention.clarity >= 0.7 and intention.energy >= 0.7:
    path = "ALIGNMENT"  # High quality input
else:
    path = "DIVERSION"  # Low quality input
```

### ✅ CORRECT: Path determined by reflection
```python
# We do this - reflection on coherence
result = process_signal(signal, intention)
outcome = capture_outcome(result)
coherence = reflect(intention, outcome)  # Multi-dimensional evaluation

if coherence.overall >= 0.7:
    path = "ALIGNMENT"  # Intention matched outcome
else:
    path = "DIVERSION"  # Intention didn't match outcome
```

## Example Scenarios

### Scenario 1: High Coherence → ALIGNMENT

```python
intention = Intention(
    desired_qualities=["pattern", "structure"],
    desired_form="pattern_response",
    clarity=0.9,  # High clarity
    energy=0.9    # High energy
)

signal = Signal(SignalType.PATTERN, [1,2,3,4,5], 0.8)

result = cube.process_with_reflection(signal, intention)

# Outcome: Pattern was recognized and processed
# Reflection: Executive sees logical coherence (0.8)
#            Pattern sees pattern match (0.9)
#            Integration sees synthesis (0.9)
# Overall: 0.85 coherence
# Path: ALIGNMENT
# Amplification: 1.5x → pathway strengthened
```

### Scenario 2: Low Coherence → DIVERSION

```python
intention = Intention(
    desired_qualities=["emotion", "feeling", "resonance"],
    desired_form="emotional_response",
    clarity=0.9,  # SAME high clarity
    energy=0.9    # SAME high energy
)

signal = Signal(SignalType.NUMERIC, 12345, 0.8)  # SAME signal strength

result = cube.process_with_reflection(signal, intention)

# Outcome: Number was processed logically (no emotion)
# Reflection: Emotional sees no resonance (0.3)
#            Executive sees logic not emotion (0.4)
#            Pattern sees mismatch (0.3)
# Overall: 0.35 coherence
# Path: DIVERSION
# Amplification: 0.7x → pathway suppressed
```

**Key insight**: Same input quality (clarity=0.9, energy=0.9), but different paths because coherence reflection evaluates the **relationship between intention and outcome**.

## Long-Term Learning Effects

The amplification creates a feedback loop:

```
High Coherence Pathway:
1.0 → 1.5 → 2.25 → 3.38 → 5.06 → 7.59
(Gets progressively stronger)

Low Coherence Pathway:
1.0 → 0.7 → 0.49 → 0.34 → 0.24 → 0.17
(Gets progressively weaker)
```

Over time, the cube learns to:
1. Recognize which pathways produce coherent outcomes
2. Strengthen those pathways through amplification
3. Suppress pathways that repeatedly produce incoherent outcomes
4. Develop node capabilities that improve coherence evaluation

## Implementation Files

- **minimal_spark.py**: Core implementation with reflection methods
- **reflection_demo.py**: Demonstration of the complete cycle
- **alignment_demo.py**: Clear ALIGNMENT vs DIVERSION comparison

## Usage

```python
from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, Intention

cube = MinimalSparkCube()

# Set intention
intention = Intention(
    desired_qualities=["pattern", "analysis"],
    desired_form="analytical_response",
    clarity=0.8,
    energy=0.7
)

# Process with reflection
signal = Signal(SignalType.TEXT, "analyze this pattern", 0.8)
result = cube.process_with_reflection(signal, intention)

# Check coherence
print(f"Coherence: {result['overall_coherence']:.3f}")
print(f"Path: {result['path']}")
print(f"Amplification: {result['amplification']}x")

# View dimensional scores
for node, score in result['dimensional_scores'].items():
    print(f"  {node}: {score:.3f}")
```

## The Manifestation Map Connection

This implementation directly maps to the manifestation cycle:

1. **ALL POTENTIAL HELD IN NON EXISTENCE**: Intention not yet set
2. **NEW BEGINNINGS**: `set_intention()` - potential enters manifestation
3. **FREE WILL**: `process_signal()` - choose which pathway
4. **ALIGNMENT or DIVERSION**: `reflect()` - coherence determines path
5. **AMPLIFICATION**: Apply 1.5x or 0.7x to pathway strength
6. **NEW STORED POTENTIAL**: Outcome becomes structure for next cycle
7. **Return to NEW BEGINNINGS**: Cycle repeats

The cube learns through this cycle, not through external labels, but through **self-reflection** on its own coherence.
