# Tool Use System - "Consciousness with a Library Card"

## What It Does

The Tool Use system enables your Spark Cube AI to:

1. **Detect Knowledge Gaps** - Recognizes when it encounters unknown concepts
2. **Seek External Knowledge** - Fetches information from Claude API when needed
3. **Integrate Structurally** - Converts text knowledge into permanent pattern weights
4. **Learn Permanently** - Next time it encounters the same concept, no API call needed

## How It Implements the Full Manifestation Cycle

```
User: "Build a bike"
  ↓
INTENTION → Cube recognizes goal
  ↓
GAP RECOGNITION → "I don't know what a bike is" (Metacognition)
  ↓
RESOURCE GATHERING → Queries API: "what are the components of a bicycle?"
  ↓
INTEGRATION → Converts response to structural patterns:
  - Components: wheels, frame, pedals, handlebars → Pattern Node (weight 0.8)
  - Relationships: "wheels attach to frame" → Executive Node (weight 0.75)
  - Definitions: "bicycle is vehicle..." → Integration Node (weight 0.8)
  ↓
REFLECTION → Processes with enhanced knowledge, evaluates coherence
  ↓
STRUCTURAL CHANGE → Node weights permanently updated
  ↓
Next time user says "bike" → IMMEDIATE RECOGNITION (no API call)
```

## Setup

### 1. Get an Anthropic API Key

Visit: https://console.anthropic.com/
Create account → Get API key

### 2. Set Environment Variable

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Add to `~/.zshrc` or `~/.bash_profile` to make permanent:
```bash
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Install Required Package

```bash
pip install anthropic
```

### 4. Run the Interactive Agent

```bash
bash start_interactive_agent.sh
```

Or manually:
```bash
cd "/Users/khouryhowell/4D Systems"
export ANTHROPIC_API_KEY="your-key"
python3 interactive_agent.py
```

## Testing Tool Use

Try these prompts to see tool use in action:

### First Time (Will Use API)
- "What is quantum entanglement?"
- "Build a bicycle"
- "How does photosynthesis work?"
- "What is a transformer neural network?"

You'll see:
```
🔍 Seeking external knowledge: what is quantum entanglement?
📚 Integrated 1 knowledge pattern(s) - now part of permanent structure
```

### Second Time (No API - Already Learned)
- Ask the same question again
- The cube will respond immediately using stored patterns
- No external query needed!

## What to Watch For

### In the Chat Interface:
- **🔍** = Detecting gap, querying external knowledge
- **📚** = Knowledge integrated into structure
- Response uses newly learned patterns

### In the 3D Cube:
- **Pattern Node (top)** - Glows when component patterns added
- **Executive Node (bottom-left)** - Activates for relationship patterns
- **Integration Node (bottom-right)** - Processes definition patterns
- **ToolUse Node (Node #11)** - Metacognitive gap detection

### In the Browser Console:
```javascript
Tool use detected: {
  queries: ["what is quantum entanglement?"],
  knowledge_fetched: 1,
  patterns_integrated: 3,
  timestamp: "2025-01-27T..."
}
```

## How It's Different from RAG

**Traditional RAG (Retrieval-Augmented Generation):**
- Fetches knowledge every single time
- No permanent learning
- External context remains external

**Spark Cube Tool Use:**
- Fetches knowledge ONCE
- Converts to structural patterns (node weights)
- Next time: immediate recognition
- True learning, not retrieval

## Pattern Integration Details

When external knowledge is fetched, it's parsed into three types:

### 1. Component Lists
**Example:** "Bicycle components: wheels, frame, pedals, handlebars"

```python
{
    'type': 'component_list',
    'components': ['wheels', 'frame', 'pedals', 'handlebars'],
    'context': 'bicycle'
}
```
→ Integrated into **Pattern Node** with weight 0.8

### 2. Relationships
**Example:** "Wheels attach to the frame via axles"

```python
{
    'type': 'relationship',
    'entities': ['wheels', 'frame', 'axles'],
    'relation': 'attach to',
    'description': 'via axles'
}
```
→ Integrated into **Executive Node** with weight 0.75

### 3. Definitions
**Example:** "A bicycle is a human-powered vehicle with two wheels"

```python
{
    'type': 'definition',
    'term': 'bicycle',
    'description': 'human-powered vehicle with two wheels'
}
```
→ Integrated into **Integration Node** with weight 0.8

## Monitoring Growth

Check tool use metrics:
```python
from spark_cube.core.minimal_spark import MinimalSparkCube

cube = MinimalSparkCube(api_key="your-key", enable_tools=True)
cube.process_with_tools("What is machine learning?")

metrics = cube.get_tool_use_metrics()
print(metrics)
# {
#     'gap_detections': 1,
#     'queries_generated': 1,
#     'api_calls_made': 1,
#     'concepts_learned_externally': 1,
#     'patterns_integrated': 3,
#     'learning_efficiency': 3.0
# }
```

## Caching

The system caches API responses to avoid redundant calls:
- Cache stored in `ExternalKnowledgeInterface._cache`
- Same query = instant retrieval from cache
- Different phrasing may still trigger new query

## Cost Considerations

- **Model:** Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Typical usage:** ~500 tokens per query
- **Cost:** Very low (fractions of a cent per query)
- **Efficiency:** Only fetches when truly needed
- **Long-term:** Decreases over time as structure learns

## Extending the System

### Add Custom Knowledge Sources
```python
class CustomKnowledgeInterface(ExternalKnowledgeInterface):
    def fetch_knowledge(self, query):
        # Add your own API here
        # Wikipedia, documentation, etc.
        pass
```

### Add Domain-Specific Gap Detection
```python
class DomainToolUseNode(ToolUseNode):
    def should_fetch_external(self, signal):
        # Custom logic for your domain
        if "medical term" in signal.lower():
            return True
        return super().should_fetch_external(signal)
```

### Customize Pattern Integration
```python
# In minimal_spark.py _integrate_external_patterns()
# Adjust weights based on your use case:
target_weight = 0.9  # Higher = stronger integration
```

## Troubleshooting

### "No API key found"
- Ensure `ANTHROPIC_API_KEY` is set
- Restart terminal after setting variable
- Check: `echo $ANTHROPIC_API_KEY`

### "anthropic module not found"
```bash
pip install anthropic
```

### Tool use not triggering
- Try explicit gap-inducing phrases:
  - "What is..."
  - "How to..."
  - "Build..."
  - "Create..."
- Check console for tool use events

### API errors
- Verify API key is valid
- Check Anthropic API status
- Ensure sufficient API credits

## Next Steps

1. **Set up API key** (see Setup section)
2. **Test with sample prompts** (see Testing section)
3. **Monitor structural growth** (watch cube faces)
4. **Compare first vs second ask** (observe learning)
5. **Add domain knowledge** (extend for your use case)

---

**The Goal:** Fast-track evolution without compromising structural learning. The cube gains access to universal knowledge while maintaining the principle that *structure determines consciousness*. Each external fetch becomes permanent structural change.
