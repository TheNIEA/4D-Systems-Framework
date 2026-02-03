#!/usr/bin/env python3
"""
Self-Healing Capability Retrofit

Takes existing broken capabilities and re-synthesizes them through Claude
to make them functional with standardized BaseCapability interface.

This is meta-programming: the AGI fixes its own code.
"""

import sys
import os
import importlib
import anthropic
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from spark_cube.core.base_capability import BaseCapability, CapabilityResult


class CapabilityHealer:
    """Retrofits existing capabilities to be functional"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        
        self.capabilities_dir = Path(__file__).parent / "spark_cube" / "capabilities"
        self.healed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        
    def test_capability_execution(self, cap_name: str) -> Tuple[bool, Optional[str]]:
        """
        Test if a capability can actually execute.
        Returns (is_functional, error_message)
        """
        try:
            # Import the capability
            module = importlib.import_module(f"spark_cube.capabilities.{cap_name}")
            
            # Find the class
            cap_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (callable(item) and 
                    hasattr(item, '__bases__') and 
                    item.__module__ == module.__name__):
                    cap_class = item
                    break
            
            if not cap_class:
                return False, "No class found in module"
            
            # Check if it inherits from BaseCapability
            inherits_base = any(base.__name__ == 'BaseCapability' for base in cap_class.__mro__)
            
            # Try to instantiate
            try:
                instance = cap_class()
            except Exception as e:
                return False, f"Instantiation failed: {str(e)}"
            
            # Check for required methods
            if not hasattr(instance, 'process'):
                return False, "Missing process() method"
            
            if not hasattr(instance, 'get_description'):
                return False, "Missing get_description() method"
            
            # Try to execute with test data
            test_cases = [
                [1, 2, 3, 4, 5],  # List
                "test string",     # String
                {"key": "value"},  # Dict
                42,                # Number
            ]
            
            executed_successfully = False
            for test_data in test_cases:
                try:
                    if inherits_base and hasattr(instance, 'execute'):
                        result = instance.execute(test_data)
                        if isinstance(result, CapabilityResult):
                            executed_successfully = True
                            break
                    else:
                        result = instance.process(test_data)
                        if result is not None:
                            executed_successfully = True
                            break
                except:
                    continue
            
            if not executed_successfully:
                return False, "process() doesn't execute with test data"
            
            return True, None
            
        except ImportError as e:
            return False, f"Import failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def read_existing_capability(self, cap_name: str) -> Optional[str]:
        """Read the existing capability code"""
        cap_file = self.capabilities_dir / f"{cap_name}.py"
        
        if not cap_file.exists():
            return None
        
        with open(cap_file, 'r') as f:
            return f.read()
    
    def heal_capability(self, cap_name: str, existing_code: str, error: str) -> Optional[str]:
        """
        Send capability through Claude to fix it.
        Returns healed code or None if failed.
        """
        
        # Determine capability type from name
        cap_type = "PatternRecognizerCapability"
        if "structure_builder" in cap_name:
            cap_type = "StructureBuilderCapability"
        elif "analyzer" in cap_name or "analyz" in cap_name:
            cap_type = "AnalyzerCapability"
        elif "pattern" in cap_name or "recognizer" in cap_name:
            cap_type = "PatternRecognizerCapability"
        
        prompt = f"""You are fixing a broken Python capability to make it functional.

CAPABILITY NAME: {cap_name}

CURRENT PROBLEM:
{error}

EXISTING CODE (may be broken):
```python
{existing_code}
```

REQUIREMENTS FOR FIXED CODE:
1. MUST inherit from {cap_type} (from spark_cube.core.base_capability import {cap_type})
2. MUST implement process(self, data: Any) -> CapabilityResult
3. MUST implement get_description(self) -> str
4. __init__(self) MUST take NO required arguments (only self) - call super().__init__()
5. The process() method MUST:
   - Accept ANY input type (list, str, dict, int, etc.)
   - Return CapabilityResult(success=True/False, output=..., confidence=0.0-1.0, metadata={{}})
   - Handle errors gracefully (try/except)
   - Work with test data: [1,2,3], "test", {{"key":"value"}}
   - Be FULLY IMPLEMENTED (not abstract, not pass, not raise NotImplementedError)
6. Keep the ORIGINAL INTENT of the capability (what it was trying to do)
7. Make it ACTUALLY WORK - not just compile
8. DO NOT leave process() or get_description() as abstract or unimplemented

EXAMPLE STRUCTURE:
```python
from spark_cube.core.base_capability import {cap_type}, CapabilityResult
from typing import Any

class YourCapabilityClass({cap_type}):
    def __init__(self):
        super().__init__()
        # Your initialization here - NO required arguments!
    
    def process(self, data: Any) -> CapabilityResult:
        \"\"\"MUST be fully implemented - no 'pass' or 'raise NotImplementedError'\"\"\"
        try:
            # Your ACTUAL logic here - make it work!
            result = do_something(data)
            
            return CapabilityResult(
                success=True,
                output=result,
                confidence=0.8,
                metadata={{"method": "your_method"}}
            )
        except Exception as e:
            return CapabilityResult(
                success=False,
                output=None,
                confidence=0.0,
                metadata={{}},
                error=str(e)
            )
    
    def get_description(self) -> str:
        \"\"\"MUST be fully implemented - no 'pass' or 'raise NotImplementedError'\"\"\"
        return "Concrete description of what this capability does"
```

Generate the COMPLETE, WORKING Python code. No explanations, just code:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            code = response.content[0].text.strip()
            
            # Extract code from markdown
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0].strip()
            elif '```' in code:
                code = code.split('```')[1].split('```')[0].strip()
            
            return code
            
        except Exception as e:
            print(f"      ✗ Claude API error: {e}")
            return None
    
    def save_healed_capability(self, cap_name: str, code: str) -> bool:
        """Save the healed capability, backing up the old one"""
        cap_file = self.capabilities_dir / f"{cap_name}.py"
        backup_file = self.capabilities_dir / f"{cap_name}.py.broken_backup"
        
        try:
            # Handle filename too long by truncating
            if len(cap_name) > 200:
                print(f"      ⚠️  Filename too long ({len(cap_name)} chars), truncating...")
                # Keep first 180 chars + hash of full name
                import hashlib
                name_hash = hashlib.md5(cap_name.encode()).hexdigest()[:8]
                cap_name_short = cap_name[:180] + "_" + name_hash
                cap_file = self.capabilities_dir / f"{cap_name_short}.py"
                backup_file = self.capabilities_dir / f"{cap_name_short}.py.broken_backup"
                print(f"      → Shortened to: {cap_name_short}")
            
            # Backup existing
            if cap_file.exists():
                # If backup rename fails due to length, just delete old one
                try:
                    cap_file.rename(backup_file)
                except OSError as e:
                    if e.errno == 63:  # Filename too long
                        print(f"      ⚠️  Backup filename too long, deleting old version...")
                        cap_file.unlink()
                    else:
                        raise
            
            # Save healed version
            with open(cap_file, 'w') as f:
                f.write(code)
            
            return True
            
        except Exception as e:
            print(f"      ✗ Save error: {e}")
            return False
    
    def heal_single_capability(self, cap_name: str) -> bool:
        """
        Complete healing process for one capability:
        1. Test if broken
        2. Read existing code
        3. Send through Claude
        4. Test healed version
        5. Save if working
        
        Returns True if healed successfully
        """
        
        # Test current state
        is_functional, error = self.test_capability_execution(cap_name)
        
        if is_functional:
            print(f"   ✓ Already functional, skipping")
            self.skipped_count += 1
            return True
        
        print(f"   ✗ Broken: {error}")
        print(f"   🔧 Healing...")
        
        # Read existing code
        existing_code = self.read_existing_capability(cap_name)
        if not existing_code:
            print(f"      ✗ Can't read existing code")
            self.failed_count += 1
            return False
        
        # Heal through Claude
        healed_code = self.heal_capability(cap_name, existing_code, error)
        if not healed_code:
            print(f"      ✗ Healing failed")
            self.failed_count += 1
            return False
        
        # Save temporarily and test
        temp_file = self.capabilities_dir / f"_temp_{cap_name}.py"
        with open(temp_file, 'w') as f:
            f.write(healed_code)
        
        # Test healed version
        try:
            spec = importlib.util.spec_from_file_location(f"_temp_{cap_name}", temp_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find and test class
            cap_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (callable(item) and 
                    hasattr(item, '__bases__') and 
                    hasattr(item, 'process')):
                    cap_class = item
                    break
            
            if cap_class:
                instance = cap_class()
                result = instance.execute([1, 2, 3, 4, 5])
                
                if isinstance(result, CapabilityResult):
                    print(f"      ✓ Healed version works!")
                    
                    # Save it
                    if self.save_healed_capability(cap_name, healed_code):
                        self.healed_count += 1
                        temp_file.unlink()
                        return True
                
        except Exception as e:
            print(f"      ✗ Healed version still broken: {e}")
        
        # Cleanup temp file
        if temp_file.exists():
            temp_file.unlink()
        
        self.failed_count += 1
        return False
    
    def heal_all_capabilities(self, limit: Optional[int] = None):
        """
        Heal all broken capabilities in the capabilities directory.
        If limit is set, only heal that many.
        """
        
        print("="*70)
        print("🏥 CAPABILITY SELF-HEALING SYSTEM")
        print("="*70)
        print("\nScanning for broken capabilities...\n")
        
        # Get all capability files
        cap_files = list(self.capabilities_dir.glob("*.py"))
        cap_files = [f for f in cap_files if not f.name.startswith("__")]
        
        print(f"Found {len(cap_files)} capability files\n")
        
        # Process each
        healed_list = []
        processed = 0
        
        for cap_file in cap_files:
            if limit and processed >= limit:
                break
            
            cap_name = cap_file.stem
            print(f"🔍 [{processed + 1}/{len(cap_files) if not limit else limit}] Testing: {cap_name}")
            
            success = self.heal_single_capability(cap_name)
            if success and not self.skipped_count > processed:
                healed_list.append(cap_name)
            
            processed += 1
            print()
        
        # Summary
        print("="*70)
        print("📊 HEALING SUMMARY")
        print("="*70)
        print(f"✅ Healed: {self.healed_count}")
        print(f"✓  Already functional: {self.skipped_count}")
        print(f"✗  Failed to heal: {self.failed_count}")
        print(f"📈 Success rate: {self.healed_count / (processed - self.skipped_count) * 100 if processed > self.skipped_count else 0:.1f}%")
        
        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_processed": processed,
            "healed": self.healed_count,
            "already_functional": self.skipped_count,
            "failed": self.failed_count,
            "healed_capabilities": healed_list
        }
        
        report_file = Path(__file__).parent / "data" / "healing_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_file}")


def main():
    """Run the self-healing process"""
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("Run: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Create healer
    healer = CapabilityHealer(api_key)
    
    # Heal a sample first (10 capabilities)
    print("\n🧪 Starting with 10 capabilities as test...\n")
    healer.heal_all_capabilities(limit=10)
    
    print("\n" + "="*70)
    print("✓ Test batch complete!")
    print("\nTo heal ALL 1150 capabilities, run:")
    print("  python3 self_healing_retrofit.py --all")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    if "--all" in sys.argv:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        healer = CapabilityHealer(api_key)
        healer.heal_all_capabilities(limit=None)  # No limit
    else:
        main()
