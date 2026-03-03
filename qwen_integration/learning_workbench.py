#!/usr/bin/env python3
"""
4D LEARNING WORKBENCH
=====================

Use this for your real coding questions. The system will:
1. Try to answer from embedded knowledge (fast)
2. Fall back to LLM generation (learns)
3. Build pathways through natural use

Run this instead of going directly to Claude/ChatGPT.
Let the capabilities build organically.
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from living_4d_system import Living4DSystem, telemetry

# ═══════════════════════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════════════════════

class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class LearningTracker:
    """Track what the system is learning over time."""
    
    def __init__(self, tracker_file: str = "learning_progress.json"):
        self.tracker_file = Path(tracker_file)
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.tracker_file.exists():
            try:
                with open(self.tracker_file) as f:
                    return json.load(f)
            except:
                pass
        return {
            "sessions": [],
            "domains": {},
            "total_queries": 0,
            "total_from_memory": 0,
            "total_learned": 0,
            "started": datetime.now().isoformat()
        }
    
    def _save(self):
        with open(self.tracker_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_query(self, query: str, source: str, domain: str, time_ms: float):
        """Record a query for tracking."""
        self.data["total_queries"] += 1
        
        if source == "crystallized_memory":
            self.data["total_from_memory"] += 1
        elif source == "newly_synthesized":
            self.data["total_learned"] += 1
        
        # Track by domain
        if domain not in self.data["domains"]:
            self.data["domains"][domain] = {"count": 0, "from_memory": 0}
        self.data["domains"][domain]["count"] += 1
        if source == "crystallized_memory":
            self.data["domains"][domain]["from_memory"] += 1
        
        self._save()
    
    def start_session(self):
        """Record session start."""
        self.data["sessions"].append({
            "started": datetime.now().isoformat(),
            "queries": 0
        })
        self._save()
    
    def get_progress(self) -> dict:
        """Get learning progress summary."""
        total = self.data["total_queries"]
        from_memory = self.data["total_from_memory"]
        hit_rate = (from_memory / total * 100) if total > 0 else 0
        
        return {
            "total_queries": total,
            "from_memory": from_memory,
            "learned": self.data["total_learned"],
            "hit_rate": hit_rate,
            "domains": self.data["domains"],
            "sessions": len(self.data["sessions"])
        }

# ═══════════════════════════════════════════════════════════════════════════════
# WORKBENCH
# ═══════════════════════════════════════════════════════════════════════════════

class LearningWorkbench:
    """Interactive workbench for coding questions."""
    
    def __init__(self):
        print(f"\n{C.CYAN}{'═'*60}{C.RESET}")
        print(f"{C.BOLD}  4D LEARNING WORKBENCH{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}")
        print(f"{C.DIM}  Your coding questions build the system's knowledge.{C.RESET}")
        print(f"{C.DIM}  Fast answers = from memory. New answers = learning.{C.RESET}")
        print()
        
        self.system = Living4DSystem()
        self.tracker = LearningTracker()
        self.tracker.start_session()
        
        self._show_status()
    
    def _show_status(self):
        """Show current learning status."""
        progress = self.tracker.get_progress()
        
        print(f"\n{C.YELLOW}📊 Learning Status:{C.RESET}")
        print(f"   Total queries: {progress['total_queries']}")
        print(f"   From memory:   {progress['from_memory']} ({progress['hit_rate']:.1f}% hit rate)")
        print(f"   Learned:       {progress['learned']}")
        
        if progress['domains']:
            print(f"\n{C.YELLOW}   Domains:{C.RESET}")
            for domain, stats in sorted(progress['domains'].items(), 
                                        key=lambda x: x[1]['count'], reverse=True)[:5]:
                mem_rate = (stats['from_memory'] / stats['count'] * 100) if stats['count'] > 0 else 0
                print(f"   • {domain}: {stats['count']} queries ({mem_rate:.0f}% from memory)")
        
        print()
    
    def ask(self, question: str) -> str:
        """Ask a coding question."""
        print(f"\n{C.BLUE}Q:{C.RESET} {question[:80]}{'...' if len(question) > 80 else ''}")
        
        start = time.time()
        result = self.system.process_query(question)
        elapsed = (time.time() - start) * 1000
        
        # Determine source indicator
        source = result.get("source", "unknown")
        if source == "crystallized_memory":
            indicator = f"{C.GREEN}⚡ FROM MEMORY{C.RESET}"
            source_short = "memory"
        elif source == "newly_synthesized":
            indicator = f"{C.YELLOW}🧠 LEARNED{C.RESET}"
            source_short = "llm"
        else:
            indicator = f"{C.CYAN}→ {source}{C.RESET}"
            source_short = source
        
        # Get domain
        domain = "general"
        for d in ["python", "javascript", "web", "api", "database", "algorithms", "3d", "graphics"]:
            if d in question.lower():
                domain = d
                break
        
        # Track
        self.tracker.record_query(question, source, domain, elapsed)
        
        # Display
        print(f"{indicator} ({elapsed:.0f}ms)")
        print(f"\n{C.DIM}{'─'*60}{C.RESET}")
        print(result.get("response", "No response"))
        print(f"{C.DIM}{'─'*60}{C.RESET}")
        
        return result.get("response", "")
    
    def run_interactive(self):
        """Run interactive session."""
        print(f"\n{C.CYAN}Commands:{C.RESET}")
        print(f"  • Type your coding question")
        print(f"  • 'status' - show learning progress")
        print(f"  • 'telemetry' - show detailed metrics")
        print(f"  • 'quit' - exit")
        print()
        
        while True:
            try:
                question = input(f"{C.BOLD}→ {C.RESET}").strip()
                
                if not question:
                    continue
                
                if question.lower() == 'quit':
                    self._show_status()
                    print(f"\n{C.GREEN}Session ended. Knowledge preserved.{C.RESET}\n")
                    break
                
                if question.lower() == 'status':
                    self._show_status()
                    continue
                
                if question.lower() == 'telemetry':
                    telemetry.print_summary()
                    continue
                
                self.ask(question)
                
            except KeyboardInterrupt:
                print(f"\n\n{C.GREEN}Session ended. Knowledge preserved.{C.RESET}\n")
                break
            except Exception as e:
                print(f"{C.RED}Error: {e}{C.RESET}")

# ═══════════════════════════════════════════════════════════════════════════════
# SUGGESTED LEARNING PATH
# ═══════════════════════════════════════════════════════════════════════════════

LEARNING_OBJECTIVES = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SUGGESTED LEARNING PATH                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Phase 1: Foundation (first 20 queries)                                      ║
║  ─────────────────────────────────────                                       ║
║  • Ask basic questions in your main domain                                   ║
║  • Let the system learn your terminology                                     ║
║  • Build initial pathways                                                    ║
║                                                                              ║
║  Phase 2: Depth (queries 20-50)                                              ║
║  ─────────────────────────────                                               ║
║  • Ask follow-up questions on the same topics                                ║
║  • Watch hit rate climb as pathways strengthen                               ║
║  • The system should start retrieving instead of regenerating                ║
║                                                                              ║
║  Phase 3: Breadth (queries 50-100)                                           ║
║  ──────────────────────────────────                                          ║
║  • Branch into related domains                                               ║
║  • Test cross-domain synthesis                                               ║
║  • Build interconnected knowledge                                            ║
║                                                                              ║
║  Phase 4: Specialization (100+ queries)                                      ║
║  ──────────────────────────────────────                                      ║
║  • Deep dives into specific areas                                            ║
║  • The system becomes your personalized expert                               ║
║  • Hit rate should approach 40-60% for repeated domains                      ║
║                                                                              ║
║  ═══════════════════════════════════════════════════════════════════════════ ║
║                                                                              ║
║  SUCCESS METRICS:                                                            ║
║  • Phase 1: Any responses (system working)                                   ║
║  • Phase 2: 10%+ hit rate (pathways forming)                                 ║
║  • Phase 3: 20%+ hit rate (knowledge accumulating)                           ║
║  • Phase 4: 40%+ hit rate (specialization emerging)                          ║
║                                                                              ║
║  The goal isn't 100% hit rate - that would mean no new learning.             ║
║  The goal is USEFUL retrieval when appropriate + learning when novel.        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--objectives":
        print(LEARNING_OBJECTIVES)
        sys.exit(0)
    
    print(LEARNING_OBJECTIVES)
    
    workbench = LearningWorkbench()
    workbench.run_interactive()
