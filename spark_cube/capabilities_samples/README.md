# Capability Samples

This folder contains **sample capabilities** from the 760+ auto-generated capability files.

The full `capabilities/` folder is excluded from the repository due to size (~50MB, 760+ files). These samples demonstrate the pattern of how capabilities are synthesized.

## What These Are

Each capability file is **automatically generated** by the AGI synthesis engine (`agi_synthesis.py`) when the system detects a gap in its processing abilities.

## Sample Files

| File | Purpose | Lines |
|------|---------|-------|
| `memory_manager_v1.py` | Persistent memory storage with SQLite | 278 |
| `nlp_analyzer_v1.py` | Natural language analysis utilities | ~150 |
| `analyze_pattern_recognizer_v1.py` | Pattern recognition in analysis tasks | ~200 |
| `create_pattern_recognizer_v1.py` | Pattern recognition for creation tasks | ~180 |
| `learn_structure_builder_v1.py` | Structure building for learning tasks | ~220 |

## Capability Naming Convention

```
{verb}_{domain}_{type}_v{version}.py
```

- **verb**: analyze, create, learn, adapt, describe, etc.
- **domain**: pattern, memory, nlp, data, structure, etc.
- **type**: pattern_recognizer, structure_builder, analyzer, etc.
- **version**: v1, v2, etc. (incremented when capability is refined)

## How Capabilities Are Generated

1. System processes a signal
2. AGI engine detects a capability gap
3. Universal code synthesizer generates Python code
4. Code is tested for syntax errors
5. Broken code is auto-repaired (`.broken_backup` files are failed attempts)
6. Working capability is saved to this folder

## Generating Your Own Capabilities

```bash
# Run autonomous capability synthesis
python3 run_agi_autonomous.py --target 100 --interval 0

# This will generate ~100 capabilities in the capabilities/ folder
# Watch the synthesis: tail -f data/agi_logs/autonomous_run.log
```

## Statistics (as of v0.6.0)

- **Total capabilities**: 760+
- **Success rate**: 93%+
- **Emergent concepts**: 705+
- **Average capability size**: ~200 lines
