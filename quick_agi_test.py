"""Quick AGI Phase 3 test - just 1 signal"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube, Signal, SignalType
from datetime import datetime

api_key = os.environ.get('ANTHROPIC_API_KEY')
print("🚀 Creating AGI Cube...")
cube = MinimalSparkCube(api_key=api_key, enable_tools=True)

print(f"\n✓ Cube ready. AGI Engine: {cube.agi_engine is not None}")
print(f"  Capabilities: {len(cube.agi_engine.capability_registry) if cube.agi_engine else 0}")

print("\n📝 Processing test signal...")
signal = Signal(
    type=SignalType.TEXT,
    data="Parse JSON data and transform it",
    timestamp=datetime.now()
)

result = cube.process_with_synthesis(signal)

print(f"\n📊 Results:")
print(f"  Synthesis attempted: {result.get('synthesis', {}).get('synthesis_attempted', False)}")
print(f"  Capability type: {result.get('synthesis', {}).get('capability_type', 'None')}")
print(f"  Success: {result.get('synthesis', {}).get('synthesis_successful', False)}")
print(f"  Total capabilities: {len(cube.agi_engine.capability_registry) if cube.agi_engine else 0}")
