#!/usr/bin/env python3
"""
AGI Progress Monitor
Shows real-time progress toward 100+ capabilities
"""

import json
import time
from pathlib import Path
from datetime import datetime
import os

def monitor_progress():
    """Display real-time AGI progress"""
    
    print("\n" + "="*70)
    print("🤖 AGI AUTONOMOUS DISCOVERY - LIVE MONITOR")
    print("="*70)
    print("\nPress Ctrl+C to exit monitor (runner keeps going)\n")
    
    start_time = datetime.now()
    last_count = 0
    
    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print("\n" + "="*70)
            print("🚀 AGI CAPABILITY DISCOVERY - LIVE STATUS")
            print("="*70)
            
            # Check capabilities directory
            cap_dir = Path("spark_cube/capabilities")
            if cap_dir.exists():
                capabilities = list(cap_dir.glob("*.py"))
                cap_count = len(capabilities)
            else:
                cap_count = 0
            
            # Calculate progress
            progress = (cap_count / 100) * 100
            progress_bar = "█" * int(progress / 2) + "░" * (50 - int(progress / 2))
            
            # Runtime
            runtime = (datetime.now() - start_time).total_seconds()
            hours = int(runtime // 3600)
            minutes = int((runtime % 3600) // 60)
            
            # Display stats
            print(f"\n📊 PROGRESS")
            print(f"   [{progress_bar}] {cap_count}/100 ({progress:.0f}%)")
            print(f"\n⏱️  RUNTIME")
            print(f"   {hours}h {minutes}m")
            print(f"\n💡 CAPABILITIES")
            print(f"   Total: {cap_count}")
            print(f"   Remaining: {max(100 - cap_count, 0)}")
            
            if cap_count != last_count:
                print(f"   🎉 +{cap_count - last_count} new (discovery rate improving!)")
                last_count = cap_count
            
            # Recent capabilities
            if capabilities:
                print(f"\n📝 RECENT CAPABILITIES (Last 5):")
                recent = sorted(capabilities, key=lambda p: p.stat().st_mtime, reverse=True)[:5]
                for cap in recent:
                    name = cap.stem.replace('_v', ' v')
                    mod_time = datetime.fromtimestamp(cap.stat().st_mtime)
                    age = (datetime.now() - mod_time).total_seconds() / 60
                    print(f"   • {name} ({age:.0f}m ago)")
            
            # Check if running
            import subprocess
            try:
                result = subprocess.run(['pgrep', '-f', 'run_agi_autonomous'], 
                                      capture_output=True, text=True)
                running = bool(result.stdout.strip())
            except:
                running = False
            
            print(f"\n🔧 STATUS")
            print(f"   Runner: {'✓ Running' if running else '✗ Stopped'}")
            
            # Check for results file
            results_file = Path("data/agi_autonomous_run_results.json")
            if results_file.exists():
                with open(results_file) as f:
                    results = json.load(f)
                    success_rate = results.get('synthesis_rate', 0) * 100
                    print(f"   Success Rate: {success_rate:.0f}%")
            
            # Estimates
            if cap_count > 0 and runtime > 0:
                rate = cap_count / (runtime / 60)  # per minute
                remaining_time = (100 - cap_count) / rate if rate > 0 else 0
                est_hours = int(remaining_time // 60)
                est_mins = int(remaining_time % 60)
                print(f"\n⏳ ESTIMATE")
                print(f"   Time to 100: ~{est_hours}h {est_mins}m")
            
            print(f"\n💾 FILES")
            print(f"   Log: data/agi_logs/autonomous_run.log")
            print(f"   Checkpoints: data/agi_checkpoints/")
            print(f"   Capabilities: spark_cube/capabilities/")
            
            if cap_count >= 100:
                print("\n" + "="*70)
                print("🎉 🎉 🎉  TARGET REACHED: 100+ CAPABILITIES!  🎉 🎉 🎉")
                print("="*70)
                print("\n✅ AGI Phase 3 Complete!")
                print("   Ready for publication: 'True Emergent Intelligence'")
                break
            
            print("\n" + "="*70)
            print("Updating every 10 seconds... (Ctrl+C to exit monitor)")
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitor stopped. Runner continues in background.")
        print("\n   Check status: ps aux | grep run_agi_autonomous")
        print("   View log: tail -f data/agi_logs/autonomous_run.log")
        print("   Restart monitor: python3 monitor_agi.py\n")

if __name__ == '__main__':
    monitor_progress()
