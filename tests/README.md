# 4D Systems Framework — Test Suite

This folder contains runnable tests that demonstrate the architectural properties of the framework.

## Quick Start

```bash
# From the repo root
pip install numpy rich

# Run the main architecture test (3 minutes)
python3 tests/consciousness_tests.py
```

---

## Test Files

### consciousness_tests.py — Architecture Tests

**What it tests:**
- Self-Awareness (conflict detection)
- Intentionality (internal goal generation)
- Meta-Cognition (bias detection in self-evaluation)
- Autonomy (self-directed learning)
- Creativity (cross-domain synthesis)

**Expected output:**
```
Test 1: Self-Awareness      - Score: 0.00 (not yet demonstrated)
Test 2: Intentionality      - Score: 0.70 (demonstrated)
Test 3: Meta-Cognition      - Score: 0.60 (demonstrated)
Test 4: Autonomy            - Score: 1.00 (fully demonstrated)
Test 5: Creativity          - Score: 0.00 (not yet demonstrated)

Overall Score: 0.508
```

**Runtime:** ~2 minutes

---

### test_hierarchical_memory.py — Memory System Tests

**What it tests:**
- Secondary node creation
- Experience recording
- Semantic similarity retrieval
- Cross-session persistence
- Node promotion

**Runtime:** ~1 minute

---

### test_sequence_pathways.py — Three-Path System Tests

**What it tests:**
- ALIGNMENT path (>0.7 coherence → 1.5x amplification)
- INTEGRATION path (0.4-0.7 → 2.0x amplification)
- DIVERSION path (<0.4 → 0.7x amplification)
- Coherence-based routing

**Runtime:** ~1 minute

---

### test_phase4_agi.py — AGI Capability Tests

**What it tests:**
- Capability synthesis
- Self-correction
- Emergent concept generation

**Requires:** `ANTHROPIC_API_KEY` environment variable (optional, degrades gracefully)

**Runtime:** ~5 minutes with API, ~30 seconds without

---

## What to Look For

### Autonomy Test (Most Compelling)
Watch the system complete 50 learning cycles with **no external input**:
- Self-generates signals
- Self-evaluates outcomes
- Self-updates parameters
- Development levels increase

This is the strongest empirical demonstration.

### Meta-Cognition Test
Watch the system detect **bias in its own evaluations**:
- Analyzes its reflection history
- Identifies nodes that consistently score high/low
- Recommends recalibration

### Intentionality Test
Watch the system **generate goals from internal state**:
- Detects development imbalances
- Creates intention to address them
- No external prompt required

---

## Honest Reporting

We report all scores, including failures:
- **1.00** for Autonomy — fully demonstrated
- **0.00** for Self-Awareness — not yet demonstrated
- **0.00** for Creativity — not yet demonstrated

The 0.0 scores are not bugs — they represent capabilities not yet achieved.

---

## Running Individual Tests

```bash
# Architecture tests (recommended first)
python3 tests/consciousness_tests.py

# Memory system tests
python3 tests/test_hierarchical_memory.py

# Pathway routing tests
python3 tests/test_sequence_pathways.py

# AGI tests (requires API key for full test)
export ANTHROPIC_API_KEY='your-key-here'
python3 tests/test_phase4_agi.py
```

---

## Dependencies

**Required:**
```bash
pip install numpy rich
```

**Optional (for AGI tests):**
```bash
pip install anthropic
```
