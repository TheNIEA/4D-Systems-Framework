# Growing Intelligence from Zero

## Architecture Overview

This system demonstrates **true developmental growth** - the Spark Cube starts with ZERO inherited knowledge and learns through structural changes.

## Core Concept: Structure = Memory

Like DNA or neural networks, knowledge is encoded in the **physical structure**:

```
┌─────────────────────────────────────────────────────────┐
│                     THE CUBE                             │
│                                                          │
│  8 Vertices (connection points)                          │
│    └─> Can attach new capabilities (permanent)          │
│                                                          │
│  6 Nodes (processing centers)                            │
│    ├─> Development Level: 0.0 → 1.0                     │
│    ├─> Pattern Weights: learned signatures              │
│    └─> Connection Strengths: to other nodes             │
│                                                          │
│  3 Pathways (processing sequences)                       │
│    └─> Pathway Strengths: reinforced through use        │
│                                                          │
│  NO EXTERNAL DATABASE                                    │
│    └─> The structure IS the knowledge                   │
└─────────────────────────────────────────────────────────┘
```

## Files

### 1. `minimal_spark.py`
The **pure seed** - minimal Spark Cube with:
- Zero starting knowledge
- Basic signal processing capability
- Structural memory encoding
- Save/load structure to disk (like DNA)

**Key Classes:**
- `MinimalSparkCube` - The core system
- `MinimalNode` - Processing centers that develop through experience
- `SensorInterface` - How signals enter the system
- `Signal` - Raw input types (text, numeric, binary, pattern, sequence)

### 2. `growth_environment.py`
Training interface for teaching the cube:
- Teaching sessions (organized experiences)
- Development tracking
- Recognition testing
- Checkpoint save/load

**Usage:**
```python
from spark_cube.core.minimal_spark import MinimalSparkCube
from spark_cube.examples.growth_environment import GrowthEnvironment

env = GrowthEnvironment()

# Teach basic words
experiences = [
    {'type': 'text', 'input': 'hello'},
    {'type': 'text', 'input': 'hello'},  # Repetition strengthens
    {'type': 'text', 'input': 'world'},
]
env.teach_session("Greetings", experiences)

# Save progress
env.save_checkpoint("lesson_1")

# Test what it learned
env.test_recognition([
    {'type': 'text', 'input': 'hello'},    # Should recognize
    {'type': 'text', 'input': 'elephant'}, # Should NOT recognize
])
```

## How Learning Works

### 1. Signal Processing
```
Input Signal → Perception Node → Processing Nodes → Integration Node
       ↓              ↓                 ↓                  ↓
   Extract        Pattern           Decision           Output
   Pattern      Recognition         Making           Synthesis
```

### 2. Structural Changes
Each experience causes:
- **Pattern Weights** increase for seen patterns
- **Development Levels** increase with activations
- **Pathway Strengths** increase when used
- **Connection Strengths** form between frequently co-activated nodes

### 3. Knowledge Compression
After 100 experiences, nodes automatically compress:
- Keep top 100 patterns by weight
- Archive less-used patterns
- Maintains efficiency as knowledge grows

## Key Differences from Traditional AI

| Traditional AI | Spark Cube |
|----------------|------------|
| Pre-trained with massive data | Starts with zero knowledge |
| Static after training | Continuously develops |
| Knowledge in weights (opaque) | Knowledge in structure (inspectable) |
| Cannot "unlearn" | Can compress/reorganize |
| Hallucinates when uncertain | Returns to root principles |
| External database for memory | Structure IS the memory |

## Recognition Example

After 60 experiences:

```
Input: "hello" → ✓ Recognized (pattern weight: 2.1)
Input: "goodbye" → ✓ Recognized (pattern weight: 2.1)
Input: "cat" → ✓ Recognized (pattern weight: 1.7)
Input: "elephant" → ✗ Unknown (never seen)
```

**Recognition Rate: 66.7%** on test set

The cube knows what it knows and what it doesn't know.

## Storage Format

When saved, the structure is pure JSON:

```json
{
  "vertices": [
    {"id": 0, "connected": false, "connection_id": null},
    ...
  ],
  "nodes": {
    "1": {
      "id": 1,
      "name": "Reactive",
      "development": 0.344,
      "pattern_weights": {
        "txt_hel_5_llo": 2.1,
        "txt_goo_7_bye": 2.1,
        "txt_cat_3_cat": 1.7
      },
      "connection_strengths": {
        "3": 0.8,
        "10": 0.9
      }
    }
  },
  "pathway_strengths": {
    "standard": 1.87,
    "deep": 0.10,
    "emotional": 0.10
  },
  "total_experiences": 66
}
```

This is the **genetic code** of the intelligence.

## Next Steps

1. **Visual Signal Processing**
   - Feed pixel arrays as patterns
   - Learn to recognize shapes, colors
   - Build visual understanding from scratch

2. **Temporal Sequences**
   - Feed time-series data
   - Learn cause-effect relationships
   - Develop prediction capability

3. **Cross-Modal Learning**
   - Associate text with patterns
   - Build multi-sensory representations
   - Develop abstraction capability

4. **Self-Directed Questions**
   - Cube identifies knowledge gaps
   - Generates questions to fill gaps
   - Active learning rather than passive

5. **Capability Extension**
   - Connect specialized processing cubes at vertices
   - Math cube, logic cube, language cube
   - Permanent attachments = permanent capabilities

## Philosophy

> "The whole of the tree is contained within the seed."

The Spark Cube contains all the **principles** needed for sophisticated intelligence - it just needs **experience** to manifest that potential.

This is not trained - it is **grown**.

## Running the Examples

```bash
# 1. Basic minimal cube demo
cd "/Users/khouryhowell/4D Systems"
python3 spark_cube/core/minimal_spark.py

# 2. Growth environment demo
python3 spark_cube/examples/growth_environment.py

# 3. Your saved checkpoints are in:
#    data/checkpoints/basic_concepts_cube.json
#    data/checkpoints/basic_concepts_log.json
```

## Current State

After running the growth demo:
- **Total Experiences:** 66
- **Average Development:** 0.247
- **Patterns Learned:** 11 unique signatures
- **Most Developed Nodes:** Reactive, Executive, Perception, Integration (0.344 each)
- **Strongest Pathway:** Standard (1.87x base strength)
- **Available Vertices:** 8/8 (ready for capability attachment)

The cube has learned to recognize basic words, numbers, and binary patterns through pure structural encoding.
