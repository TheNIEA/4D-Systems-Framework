"""Test goal-directed exploration"""
import os
from spark_cube.core.minimal_spark import MinimalSparkCube

api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    print("Error: Set ANTHROPIC_API_KEY environment variable")
    print("  export ANTHROPIC_API_KEY='your-api-key-here'")
    exit(1)
cube = MinimalSparkCube(api_key=api_key, enable_tools=True)

print("\n" + "="*60)
print("AGI ENGINE TYPE CHECK")
print("="*60)
print(f"Type: {type(cube.agi_engine).__name__}")
print(f"Has goal_explorer: {hasattr(cube.agi_engine, 'goal_explorer')}")

if hasattr(cube.agi_engine, 'goal_explorer'):
    print("\n✅ Goal-directed exploration: ENABLED")
    
    # Test it
    explorer = cube.agi_engine.goal_explorer
    explorer.set_goal('Process natural language')
    requirements = explorer.discover_requirements('Process natural language', cube)
    
    print(f"\n✅ Discovered {len(requirements)} requirements:")
    for req in requirements:
        print(f"   • {req.name} (priority: {req.priority})")
    
    # Generate signal
    signal = explorer.generate_exploration_signal()
    if signal:
        print(f"\n✅ Generated exploration signal:")
        print(f"   Domain: {signal['domain']}")
        print(f"   Parent Goal: {signal['parent_goal']}")
        print(f"   Signal Data: {signal['signal_data']}")
else:
    print("\n❌ Using legacy domain-based exploration")

print("\n" + "="*60)
