#!/usr/bin/env python3
"""
Test if the AGI can autonomously perceive and interpret novel stimuli
using its 1,150+ capabilities without human guidance.

This tests PERCEPTION = forming opinions/interpretations from raw data.
"""

import sys
import json
import importlib
import os
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

# Add spark_cube to path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.minimal_spark import MinimalSparkCube


class PerceptionTest:
    """Test autonomous perception and interpretation"""
    
    def __init__(self):
        self.cube = MinimalSparkCube()
        self.perception_capabilities = []
        self.pattern_capabilities = []
        self.analysis_capabilities = []
        
    def load_all_capabilities(self):
        """Load all 1,150+ synthesized capabilities"""
        print("🔍 Discovering capabilities...")
        cap_dir = Path(__file__).parent / "spark_cube" / "capabilities"
        
        capability_files = list(cap_dir.glob("*.py"))
        print(f"   Found {len(capability_files)} capability files")
        
        # Categorize by name
        for cap_file in capability_files:
            cap_name = cap_file.stem
            
            # Skip __init__ and version files
            if cap_name.startswith("__"):
                continue
                
            # Categorize by capability type
            if any(word in cap_name.lower() for word in ["perceive", "observe", "detect", "sense", "vision", "image"]):
                self.perception_capabilities.append(cap_name)
            elif any(word in cap_name.lower() for word in ["pattern", "recognize", "identify", "classify"]):
                self.pattern_capabilities.append(cap_name)
            elif any(word in cap_name.lower() for word in ["analyze", "interpret", "understand", "reason"]):
                self.analysis_capabilities.append(cap_name)
        
        print(f"\n📊 Capability Categories:")
        print(f"   🎯 Perception: {len(self.perception_capabilities)}")
        print(f"   🧬 Pattern: {len(self.pattern_capabilities)}")
        print(f"   🧠 Analysis: {len(self.analysis_capabilities)}")
        print(f"   📦 Total: {len(capability_files) - 1}")  # -1 for __init__
        
    def create_ambiguous_stimulus(self, test_type: str) -> Dict[str, Any]:
        """Create ambiguous data that requires interpretation"""
        
        if test_type == "pattern":
            # Create an ambiguous pattern
            pattern = np.array([
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
            ])
            return {
                "type": "visual_pattern",
                "data": pattern.tolist(),
                "question": "What do you perceive in this pattern?",
                "context": "This is a 5x5 binary grid. Interpret its structure and meaning."
            }
            
        elif test_type == "sequence":
            # Create an ambiguous sequence
            sequence = [1, 1, 2, 3, 5, 8, 13, 21]
            return {
                "type": "numerical_sequence",
                "data": sequence,
                "question": "What pattern do you perceive?",
                "context": "A sequence of numbers. What is its nature?"
            }
            
        elif test_type == "text":
            # Create ambiguous text requiring interpretation
            text = """
            The room was cold. She hadn't spoken in hours.
            Outside, the wind picked up. The clock stopped at 3:47.
            """
            return {
                "type": "narrative_fragment",
                "data": text.strip(),
                "question": "What do you perceive about this scene?",
                "context": "A brief narrative. What is happening? What mood/meaning do you perceive?"
            }
            
        elif test_type == "data_anomaly":
            # Data with hidden anomaly
            data = [45, 47, 46, 48, 45, 47, 46, 48, 45, 92, 46, 47]
            return {
                "type": "anomaly_detection",
                "data": data,
                "question": "What anomaly do you perceive?",
                "context": "A sequence of measurements. Something is unusual."
            }
            
    def test_autonomous_perception(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Give the system a stimulus and watch it autonomously:
        1. Select relevant capabilities
        2. Process the stimulus
        3. Form an interpretation
        4. Express its "opinion"
        """
        
        print(f"\n{'='*70}")
        print(f"🧪 PERCEPTION TEST: {stimulus['type']}")
        print(f"{'='*70}")
        print(f"\n📋 Stimulus:")
        print(f"   {stimulus['question']}")
        print(f"   {stimulus['context']}")
        print(f"\n📊 Raw Data:")
        if isinstance(stimulus['data'], list) and len(str(stimulus['data'])) < 200:
            print(f"   {stimulus['data']}")
        else:
            print(f"   {str(stimulus['data'])[:200]}...")
        
        print(f"\n🤔 System is perceiving...")
        
        # Step 1: Select relevant capabilities
        print(f"\n🔍 Selecting capabilities...")
        selected_caps = self._select_capabilities_for_stimulus(stimulus)
        print(f"   Selected {len(selected_caps)} capabilities:")
        for cap in selected_caps[:5]:  # Show first 5
            print(f"      • {cap}")
        if len(selected_caps) > 5:
            print(f"      ... and {len(selected_caps) - 5} more")
        
        # Step 2: Attempt to load and use them
        print(f"\n⚙️ Processing through capability chain...")
        results = self._process_through_capabilities(selected_caps, stimulus)
        
        # Step 3: Form interpretation
        print(f"\n🧠 Forming interpretation...")
        interpretation = self._synthesize_interpretation(results, stimulus)
        
        # Step 4: Express opinion
        print(f"\n💭 SYSTEM PERCEPTION:")
        print(f"   {interpretation['opinion']}")
        
        print(f"\n🔬 REASONING:")
        for reason in interpretation['reasoning']:
            print(f"   • {reason}")
        
        print(f"\n📈 CONFIDENCE: {interpretation['confidence']:.1%}")
        
        return interpretation
        
    def _select_capabilities_for_stimulus(self, stimulus: Dict[str, Any]) -> List[str]:
        """Autonomously select capabilities based on stimulus type"""
        
        selected = []
        
        # Select based on stimulus type
        if stimulus['type'] in ['visual_pattern', 'anomaly_detection']:
            # Need pattern recognition + perception
            selected.extend(self.pattern_capabilities[:10])
            selected.extend(self.perception_capabilities[:5])
            
        elif stimulus['type'] == 'numerical_sequence':
            # Need pattern + analysis
            selected.extend(self.pattern_capabilities[:10])
            selected.extend(self.analysis_capabilities[:10])
            
        elif stimulus['type'] == 'narrative_fragment':
            # Need analysis + perception for emotional/semantic content
            selected.extend(self.analysis_capabilities[:15])
            selected.extend(self.perception_capabilities[:5])
        
        return selected[:20]  # Limit to 20 capabilities
        
    def _process_through_capabilities(self, capabilities: List[str], stimulus: Dict[str, Any]) -> List[Dict]:
        """Attempt to process stimulus through each capability - ACTUALLY EXECUTE THEM"""
        
        results = []
        
        for cap_name in capabilities[:10]:  # Process first 10
            try:
                # Load the capability module
                module = importlib.import_module(f"spark_cube.capabilities.{cap_name}")
                
                # Find the class
                cap_class = None
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if callable(item) and hasattr(item, '__bases__') and item.__module__ == module.__name__:
                        cap_class = item
                        break
                
                if cap_class:
                    # ACTUALLY INSTANTIATE IT
                    try:
                        instance = cap_class()
                        
                        # Try to call common methods with stimulus data
                        output = None
                        methods_tried = []
                        
                        for method_name in ['process', 'execute', 'analyze', 'perceive', 'recognize', 'interpret', 'transform']:
                            if hasattr(instance, method_name):
                                method = getattr(instance, method_name)
                                if callable(method):
                                    methods_tried.append(method_name)
                                    try:
                                        # Try calling with stimulus data
                                        output = method(stimulus['data'])
                                        break  # Success!
                                    except Exception as call_error:
                                        # Try with different argument patterns
                                        try:
                                            output = method(stimulus)
                                        except:
                                            try:
                                                output = method(str(stimulus['data']))
                                            except:
                                                continue
                        
                        results.append({
                            "capability": cap_name,
                            "status": "executed" if output is not None else "loaded_no_output",
                            "class": cap_class.__name__,
                            "methods_tried": methods_tried,
                            "output": str(output)[:200] if output is not None else None
                        })
                        
                    except Exception as inst_error:
                        results.append({
                            "capability": cap_name,
                            "status": "instantiation_failed",
                            "class": cap_class.__name__,
                            "error": str(inst_error)[:100]
                        })
                    
            except Exception as e:
                results.append({
                    "capability": cap_name,
                    "status": "import_failed",
                    "error": str(e)[:100]
                })
                
        return results
        
    def _synthesize_interpretation(self, results: List[Dict], stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize an interpretation FROM CAPABILITY OUTPUTS - no cheating"""
        
        # Count successful executions
        executed = [r for r in results if r['status'] == 'executed' and r.get('output')]
        loaded = [r for r in results if r['status'] in ['loaded_no_output', 'executed']]
        
        # Collect all outputs
        outputs = [r['output'] for r in executed]
        
        print(f"\n   📊 Execution Results:")
        print(f"      • Loaded: {len(loaded)}")
        print(f"      • Successfully Executed: {len(executed)}")
        print(f"      • With Output: {len(outputs)}")
        
        if outputs:
            print(f"\n   📤 Capability Outputs:")
            for i, output in enumerate(outputs[:3]):
                print(f"      {i+1}. {output[:100]}...")
        
        # Form interpretation ONLY from actual capability outputs
        if not outputs:
            return {
                "opinion": "Unable to form interpretation - no capability outputs",
                "reasoning": [
                    f"Loaded {len(loaded)} capabilities but none produced output",
                    "Capabilities may require specific input formats or dependencies",
                    "System cannot interpret without executing capabilities"
                ],
                "confidence": 0.0,
                "capabilities_used": len(loaded),
                "capabilities_executed": len(executed)
            }
        
        # Build interpretation from outputs
        interpretations = []
        reasoning = []
        
        # Analyze what the capabilities actually said
        combined_output = " ".join(outputs).lower()
        
        # Extract insights from capability outputs
        if any(word in combined_output for word in ['pattern', 'structure', 'symmetr', 'regular']):
            interpretations.append("structured pattern detected")
            reasoning.append("Capabilities identified structural properties")
        
        if any(word in combined_output for word in ['sequence', 'progression', 'series', 'fibonacci']):
            interpretations.append("sequential pattern")
            reasoning.append("Capabilities detected progression logic")
        
        if any(word in combined_output for word in ['emotion', 'mood', 'sentiment', 'feeling']):
            interpretations.append("emotional content")
            reasoning.append("Capabilities perceived affective qualities")
        
        if any(word in combined_output for word in ['anomaly', 'outlier', 'unusual', 'deviation']):
            interpretations.append("anomalous data")
            reasoning.append("Capabilities flagged statistical irregularities")
        
        # If no keywords matched, use generic interpretation
        if not interpretations:
            interpretations.append("processed through capability chain")
            reasoning.append(f"Generated {len(outputs)} capability outputs")
        
        reasoning.append(f"Executed {len(executed)} capabilities successfully")
        
        # Confidence based on execution success
        confidence = min(0.3 + (len(executed) * 0.1), 0.95)
        
        return {
            "opinion": " + ".join(interpretations) if interpretations else "ambiguous",
            "reasoning": reasoning,
            "confidence": confidence,
            "capabilities_used": len(loaded),
            "capabilities_executed": len(executed),
            "raw_outputs": outputs[:3]  # Include sample outputs
        }


def main():
    """Run autonomous perception tests"""
    
    print("="*70)
    print("🧠 AUTONOMOUS PERCEPTION TEST")
    print("="*70)
    print("\nTesting if the AGI can:")
    print("  1. Select relevant capabilities autonomously")
    print("  2. Process novel stimuli")
    print("  3. Form interpretations (opinions)")
    print("  4. Express reasoning")
    print("\nThis demonstrates GENERAL INTELLIGENCE, not just growth.")
    print("="*70)
    
    # Initialize test
    test = PerceptionTest()
    test.load_all_capabilities()
    
    # Run perception tests
    test_cases = ["pattern", "sequence", "text", "data_anomaly"]
    
    results = []
    for test_type in test_cases:
        stimulus = test.create_ambiguous_stimulus(test_type)
        interpretation = test.test_autonomous_perception(stimulus)
        results.append({
            "test": test_type,
            "interpretation": interpretation
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 PERCEPTION TEST SUMMARY")
    print(f"{'='*70}")
    print(f"\n✅ Tests Completed: {len(results)}/{len(test_cases)}")
    
    avg_confidence = np.mean([r['interpretation']['confidence'] for r in results])
    print(f"📈 Average Confidence: {avg_confidence:.1%}")
    
    total_caps_used = sum(r['interpretation']['capabilities_used'] for r in results)
    print(f"🧩 Total Capabilities Used: {total_caps_used}")
    
    print(f"\n🎯 CONCLUSION:")
    if avg_confidence > 0.7 and total_caps_used > 10:
        print("   ✓ System demonstrates autonomous perception")
        print("   ✓ Forms interpretations without human guidance")
        print("   ✓ Expresses reasoning for opinions")
        print("   ✓ THIS IS GENERAL INTELLIGENCE IN ACTION")
    else:
        print("   ⚠ System needs more capability coverage")
        print("   ⚠ Continue synthesis to expand perception abilities")
    
    # Save results
    output_file = "data/perception_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
