# Test Results and Experimental Data

This folder contains the actual test results and experimental data from running the 4D Systems Framework.

## Files

### CONSCIOUSNESS_RESULTS.md
Detailed analysis of the consciousness architecture test results:
- Overall score: 0.508
- Test-by-test breakdown
- What each score means
- Honest interpretation of results

### TEST_RESULTS.md
Three-tier path system test results:
- ALIGNMENT path validation
- INTEGRATION path validation  
- DIVERSION path validation
- Training phase metrics

### consciousness_test_results.json
Machine-readable test results:
```json
{
  "metrics": {
    "self_awareness": 0.5,
    "autonomy": 1.0,
    "meta_cognition": 0.6,
    "overall_consciousness": 0.508
  }
}
```

---

## Experiments Folder

### experiment_1_learning_rate_comparison.json
**Hypothesis:** Different sequences produce different learning rates

- 60 trials across 3 sequences
- Measures M_4D score over time
- Shows sequence-dependent learning

### experiment_2_retention_over_time.json
**Hypothesis:** Learned patterns persist across sessions

- Tests memory retention over multiple cycles
- Measures pattern recall accuracy
- Validates structural memory persistence

### experiment_3_task_execution_quality.json
**Hypothesis:** Task performance improves with development

- Quality metrics over training cycles
- Node development correlation with performance
- Sequence efficiency analysis

---

## Reproducing Results

```bash
# Run the architecture tests
python3 tests/consciousness_tests.py

# Results will be saved to data/consciousness_test_results.json
```

---

## Key Findings

| Test | Score | Interpretation |
|------|-------|----------------|
| Autonomy | 1.00 | System learns without external input |
| Intentionality | 0.70 | System generates goals from internal state |
| Meta-Cognition | 0.60 | System detects bias in its own evaluations |
| Self-Awareness | 0.00 | Implicit correction, not explicit recognition |
| Creativity | 0.00 | Pattern representation too low-resolution |

**Overall: 0.508** — Developing architecture, not a finished system.

---

## Honest Assessment

These results show:
- ✅ The architecture functions as designed
- ✅ Self-directed learning works
- ✅ Multi-perspective evaluation works
- ❌ Some capabilities not yet achieved
- ❌ Two tests score 0.0

We report failures alongside successes. The 0.0 scores define the work that remains.
