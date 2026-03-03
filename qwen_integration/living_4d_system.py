#!/usr/bin/env python3
"""
THE LIVING 4D SYSTEM
====================

A continuously running cognitive system that:
1. Learns autonomously in the background
2. Shows real-time growth visualization
3. Accepts questions while working
4. Demonstrates node sequencing and building
5. Self-improves over time

This is the "lights on" moment.
"""

import sys
import os
import time
import json
import threading
import queue
import random
import urllib.request
import urllib.parse
import subprocess
import re
import webbrowser
import platform
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import select

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

# Web capabilities
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# ═══════════════════════════════════════════════════════════════════════════════
# TELEMETRY SYSTEM - Track Learning Progress
# ═══════════════════════════════════════════════════════════════════════════════

class Telemetry:
    """Lightweight telemetry to track 4D system learning during real tasks."""
    
    def __init__(self, log_file: str = "telemetry.jsonl"):
        self.log_file = Path(log_file)
        self.session_start = datetime.now()
        self.metrics = {
            "queries_total": 0,
            "queries_embedded": 0,  # Answered from embedded knowledge
            "queries_llm": 0,       # Required LLM fallback
            "knowledge_stored": 0,
            "pathways_strengthened": 0,
            "retrieval_times": [],  # ms
            "llm_times": [],        # ms
            "domains_active": set(),
            "alignment_scores": [], # Track alignment quality
        }
        self._lock = threading.Lock()
    
    def log_query(self, query: str, source: str, response_time_ms: float, 
                  alignment_score: float = 0.0, domain: str = None):
        """Log a query event."""
        with self._lock:
            self.metrics["queries_total"] += 1
            if source == "embedded":
                self.metrics["queries_embedded"] += 1
                self.metrics["retrieval_times"].append(response_time_ms)
            else:
                self.metrics["queries_llm"] += 1
                self.metrics["llm_times"].append(response_time_ms)
            
            if alignment_score > 0:
                self.metrics["alignment_scores"].append(alignment_score)
            if domain:
                self.metrics["domains_active"].add(domain)
            
            self._write_event({
                "type": "query",
                "query": query[:100],
                "source": source,
                "time_ms": response_time_ms,
                "alignment": alignment_score,
                "domain": domain,
                "timestamp": datetime.now().isoformat()
            })
    
    def log_knowledge_stored(self, domain: str, key: str):
        """Log when new knowledge is embedded."""
        with self._lock:
            self.metrics["knowledge_stored"] += 1
            self._write_event({
                "type": "knowledge_stored",
                "domain": domain,
                "key": key,
                "timestamp": datetime.now().isoformat()
            })
    
    def log_pathway_strengthened(self, from_node: str, to_node: str, new_weight: float):
        """Log pathway strengthening."""
        with self._lock:
            self.metrics["pathways_strengthened"] += 1
            self._write_event({
                "type": "pathway_strengthened",
                "from": from_node,
                "to": to_node,
                "weight": new_weight,
                "timestamp": datetime.now().isoformat()
            })
    
    def _write_event(self, event: dict):
        """Append event to log file."""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        except:
            pass  # Don't break on logging failure
    
    def get_summary(self) -> dict:
        """Get current telemetry summary."""
        with self._lock:
            hit_rate = 0.0
            if self.metrics["queries_total"] > 0:
                hit_rate = self.metrics["queries_embedded"] / self.metrics["queries_total"] * 100
            
            avg_retrieval = 0.0
            if self.metrics["retrieval_times"]:
                avg_retrieval = sum(self.metrics["retrieval_times"]) / len(self.metrics["retrieval_times"])
            
            avg_llm = 0.0
            if self.metrics["llm_times"]:
                avg_llm = sum(self.metrics["llm_times"]) / len(self.metrics["llm_times"])
            
            speedup = avg_llm / avg_retrieval if avg_retrieval > 0 else 0
            
            avg_alignment = 0.0
            if self.metrics["alignment_scores"]:
                avg_alignment = sum(self.metrics["alignment_scores"]) / len(self.metrics["alignment_scores"])
            
            return {
                "session_duration": str(datetime.now() - self.session_start).split('.')[0],
                "queries_total": self.metrics["queries_total"],
                "hit_rate": f"{hit_rate:.1f}%",
                "knowledge_stored": self.metrics["knowledge_stored"],
                "pathways_strengthened": self.metrics["pathways_strengthened"],
                "avg_retrieval_ms": f"{avg_retrieval:.1f}",
                "avg_llm_ms": f"{avg_llm:.1f}",
                "speedup": f"{speedup:.0f}x" if speedup > 0 else "N/A",
                "avg_alignment": f"{avg_alignment:.3f}",
                "domains": list(self.metrics["domains_active"]),
            }
    
    def print_summary(self):
        """Print formatted telemetry summary."""
        s = self.get_summary()
        print(f"\n{'─'*50}")
        print(f"📊 TELEMETRY | {s['session_duration']}")
        print(f"{'─'*50}")
        print(f"  Queries: {s['queries_total']} (hit rate: {s['hit_rate']})")
        print(f"  Knowledge: +{s['knowledge_stored']} stored")
        print(f"  Pathways: +{s['pathways_strengthened']} strengthened")
        print(f"  Speed: {s['avg_retrieval_ms']}ms retrieval vs {s['avg_llm_ms']}ms LLM ({s['speedup']})")
        print(f"  Alignment: {s['avg_alignment']} avg")
        if s['domains']:
            print(f"  Domains: {', '.join(s['domains'])}")
        print(f"{'─'*50}\n")


# Global telemetry instance
telemetry = Telemetry()


# ═══════════════════════════════════════════════════════════════════════════════
# 4D ALIGNMENT SYSTEM - Dynamic Sequence-Based Knowledge Retrieval
# ═══════════════════════════════════════════════════════════════════════════════
# Based on 4D Framework equations:
#   Φ = ∫(Σ w_i × N_i × (S_i/S_max) × T_i) × A_path × e^(iθ_coherence) dt
#
# Where:
#   θ_coherence = phase alignment between query and knowledge
#   A_path = sequence amplification factor (pathway strength)
# ═══════════════════════════════════════════════════════════════════════════════

class AlignmentScorer:
    """
    Computes θ_coherence (alignment score) between query and knowledge.
    
    Unlike exact matching, alignment considers:
    1. Semantic overlap (synonyms, related concepts)
    2. Structural similarity (word order, phrase patterns)
    3. Domain coherence (same conceptual space)
    """
    
    # Semantic clusters - words that "align" conceptually
    SEMANTIC_CLUSTERS = {
        'python': {'programming', 'code', 'coding', 'script', 'function', 'class', 'module', 'pip'},
        'programming': {'code', 'coding', 'software', 'development', 'function', 'algorithm'},
        'list': {'array', 'collection', 'sequence', 'items', 'elements'},
        'function': {'method', 'procedure', 'routine', 'def', 'callable'},
        'variable': {'var', 'value', 'data', 'name', 'identifier'},
        'loop': {'iterate', 'iteration', 'for', 'while', 'repeat'},
        'condition': {'if', 'else', 'conditional', 'branch', 'check'},
        'class': {'object', 'type', 'instance', 'oop', 'inheritance'},
        'error': {'exception', 'bug', 'issue', 'problem', 'fail'},
        'file': {'read', 'write', 'open', 'save', 'path', 'io'},
        'string': {'text', 'str', 'character', 'chars'},
        'number': {'int', 'float', 'integer', 'decimal', 'numeric'},
        'dictionary': {'dict', 'map', 'hash', 'key', 'value', 'mapping'},
        'memory': {'remember', 'recall', 'store', 'knowledge', 'learned'},
        'search': {'find', 'look', 'query', 'locate', 'fetch'},
        'sort': {'order', 'arrange', 'organize', 'rank'},
        'api': {'endpoint', 'request', 'response', 'rest', 'http'},
        'database': {'db', 'sql', 'query', 'table', 'record'},
        'web': {'http', 'url', 'browser', 'internet', 'online'},
        'security': {'secure', 'authentication', 'auth', 'encryption', 'protect', 'vulnerability'},
        'devops': {'deploy', 'deployment', 'ci', 'cd', 'pipeline', 'infrastructure'},
        'algorithms': {'algorithm', 'sort', 'search', 'optimize', 'recursive', 'dynamic'},
    }
    
    STOP_WORDS = {
        'i', 'me', 'my', 'you', 'your', 'the', 'a', 'an', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'to',
        'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through',
        'tell', 'show', 'give', 'get', 'make', 'know', 'think', 'want', 'need',
        'dont', "don't", 'what', 'how', 'why', 'when', 'where', 'who', 'which',
        'about', 'just', 'like', 'this', 'that', 'these', 'those', 'it', 'its'
    }
    
    @classmethod
    def extract_concepts(cls, text: str) -> set:
        """Extract meaningful concepts from text"""
        if isinstance(text, dict):
            # If it's a knowledge dict, combine all text fields
            text = ' '.join(str(v) for v in text.values() if isinstance(v, str))
        
        words = set(str(text).lower().split())
        # Strip punctuation from each word
        words = {w.strip('?!.,;:\'"()[]{}') for w in words}
        # Remove stop words
        meaningful = words - cls.STOP_WORDS
        # Remove short words and empty strings
        meaningful = {w for w in meaningful if len(w) > 2}
        return meaningful
    
    @classmethod
    def expand_concepts(cls, concepts: set) -> set:
        """Expand concepts with semantic relatives"""
        expanded = set(concepts)
        for concept in concepts:
            for cluster_key, cluster_words in cls.SEMANTIC_CLUSTERS.items():
                if concept in cluster_words or concept == cluster_key:
                    expanded.update(cluster_words)
                    expanded.add(cluster_key)
        return expanded
    
    @classmethod
    def compute_alignment(cls, query: str, knowledge: Any, pathway_strength: float = 1.0) -> float:
        """
        Compute θ_coherence between query and knowledge.
        
        Returns alignment score 0.0 to 1.0 (phase coherence).
        Higher pathway_strength amplifies weak alignments (A_path effect).
        """
        # Extract concepts from query
        query_concepts = cls.extract_concepts(query)
        query_expanded = cls.expand_concepts(query_concepts)
        
        # Extract concepts from knowledge
        if isinstance(knowledge, dict):
            # Combine all text fields for matching
            knowledge_text = ""
            if 'response' in knowledge:
                knowledge_text += str(knowledge['response']) + " "
            if 'keywords' in knowledge:
                knowledge_text += ' '.join(knowledge['keywords']) + " "
            if 'query' in knowledge:
                knowledge_text += str(knowledge['query']) + " "
            knowledge_concepts = cls.extract_concepts(knowledge_text)
        else:
            knowledge_concepts = cls.extract_concepts(str(knowledge))
        
        knowledge_expanded = cls.expand_concepts(knowledge_concepts)
        
        if not query_concepts or not knowledge_concepts:
            return 0.0
        
        # === COMPUTE ALIGNMENT SCORE ===
        
        # Direct overlap (strongest signal)
        direct_overlap = len(query_concepts & knowledge_concepts)
        
        # Semantic overlap (expanded concepts)
        semantic_overlap = len(query_expanded & knowledge_expanded)
        
        # Normalize scores
        max_possible = max(len(query_concepts), len(knowledge_concepts))
        
        # Base alignment score
        direct_score = direct_overlap / max_possible if max_possible > 0 else 0
        semantic_score = (semantic_overlap - direct_overlap) / (len(query_expanded) + 1) * 0.5
        
        base_alignment = min(1.0, direct_score + semantic_score)
        
        # === PATHWAY AMPLIFICATION (A_path) ===
        # Stronger pathways can surface weaker alignments
        # This is the key 4D insight: developed pathways "boost" the signal
        if pathway_strength > 1.0:
            # Amplification factor - logarithmic to prevent runaway
            amplification = 1 + (0.2 * min(pathway_strength - 1.0, 5.0))
            # Boost weak signals but don't exceed 1.0
            amplified_alignment = min(1.0, base_alignment * amplification)
        else:
            amplified_alignment = base_alignment
        
        return amplified_alignment
    
    @classmethod
    def compute_batch_alignment(cls, query: str, knowledge_items: Dict, pathway_strength: float = 1.0) -> List[Tuple[str, Any, float]]:
        """
        Compute alignment for multiple knowledge items.
        Returns sorted list of (key, knowledge, score) tuples.
        """
        results = []
        for key, knowledge in knowledge_items.items():
            score = cls.compute_alignment(query, knowledge, pathway_strength)
            if score > 0.1:  # Minimum threshold
                results.append((key, knowledge, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[2], reverse=True)
        return results


class SequenceSelector:
    """
    Selects optimal processing sequence based on query type.
    
    Different sequences produce different outcomes (core 4D principle):
    - Standard: Reactive processing (0.7x)
    - Deep Understanding: Intentional processing (1.5x)
    - Emotional Learning: Integrated transformation (2.0x)
    """
    
    # Processing sequences (node traversal order)
    SEQUENCES = {
        'standard': ['input', 'pattern', 'memory', 'reasoning', 'synthesis', 'output'],
        'deep_retrieval': ['input', 'memory', 'pattern', 'reasoning', 'synthesis', 'output'],
        'creative': ['input', 'pattern', 'synthesis', 'reasoning', 'memory', 'output'],
        'action': ['input', 'pattern', 'action', 'output'],
        'learning': ['input', 'pattern', 'memory', 'learning', 'synthesis', 'output'],
    }
    
    QUERY_PATTERNS = {
        'recall': ['what is', 'what are', 'define', 'explain', 'tell me about', 'remember'],
        'creative': ['create', 'generate', 'make', 'design', 'build', 'new'],
        'action': ['open', 'run', 'execute', 'start', 'stop', 'do', 'show'],
        'learning': ['learn', 'teach', 'remember', 'store', 'save'],
    }
    
    @classmethod
    def select_sequence(cls, query: str, pathway_weights: Dict = None) -> Tuple[str, List[str]]:
        """
        Select optimal sequence for query.
        Returns (sequence_name, sequence_nodes).
        """
        query_lower = query.lower()
        
        # Check query patterns
        for seq_type, patterns in cls.QUERY_PATTERNS.items():
            if any(p in query_lower for p in patterns):
                if seq_type == 'recall':
                    return 'deep_retrieval', cls.SEQUENCES['deep_retrieval']
                elif seq_type in cls.SEQUENCES:
                    return seq_type, cls.SEQUENCES[seq_type]
        
        # Default to standard if no pattern matched
        return 'standard', cls.SEQUENCES['standard']


# ANSI Colors
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    # Background colors
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    BG_RED = '\033[41m'


@dataclass
class CognitiveNode:
    """A node in the 4D cognitive network - with TRUE learning"""
    id: str
    name: str
    purpose: str
    activation_count: int = 0
    knowledge_items: int = 0
    connections: List[str] = field(default_factory=list)
    last_activated: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    # TRUE ARCHITECTURAL LEARNING
    capability: float = 1.0  # Node's learned capability (1.0 = baseline)
    embedded_knowledge: Dict = field(default_factory=dict)  # Knowledge INSIDE the node
    success_rate: float = 0.5  # How often this node contributes to good outcomes
    processing_speed: float = 1.0  # Gets faster with use
    specializations: List[str] = field(default_factory=list)  # Domains this node is strong in
    
    def activate(self, success: bool = True):
        """Activate node and update capability based on outcome"""
        self.activation_count += 1
        self.last_activated = datetime.now()
        
        # TRUE LEARNING: capability changes based on success
        if success:
            # Strengthen - logarithmic growth prevents runaway
            self.capability = min(10.0, self.capability + 0.01 * (1 / self.capability))
            self.success_rate = self.success_rate * 0.95 + 0.05  # Moving average toward 1
            self.processing_speed = min(5.0, self.processing_speed + 0.005)
        else:
            # Weaken slightly on failure
            self.capability = max(0.1, self.capability - 0.005)
            self.success_rate = self.success_rate * 0.95  # Moving average toward 0
    
    def add_embedded_knowledge(self, key: str, knowledge: Any):
        """Store knowledge INSIDE the node - not external"""
        self.embedded_knowledge[key] = knowledge
        self.knowledge_items = len(self.embedded_knowledge)
    
    def retrieve_relevant(self, query: str, pathway_strength: float = 1.0, threshold: float = 0.15) -> List[Tuple[Any, float]]:
        """
        Retrieve knowledge using 4D ALIGNMENT scoring.
        
        Unlike keyword matching, this computes θ_coherence (phase alignment)
        and uses A_path (pathway amplification) to surface weak-but-relevant matches.
        
        Args:
            query: The query string (or keywords as string)
            pathway_strength: The strength of pathway leading to this node (A_path)
            threshold: Minimum alignment score to include (default 0.15)
        
        Returns:
            List of (knowledge, alignment_score) tuples, sorted by score
        """
        if not self.embedded_knowledge:
            return []
        
        results = []
        for key, knowledge in self.embedded_knowledge.items():
            # Compute alignment score with pathway amplification
            score = AlignmentScorer.compute_alignment(query, knowledge, pathway_strength)
            
            # Node capability affects retrieval quality
            # Higher capability = lower threshold (can surface weaker matches)
            effective_threshold = threshold / (self.capability ** 0.5)
            
            if score >= effective_threshold:
                results.append((knowledge, score))
        
        # Sort by alignment score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def retrieve_best(self, query: str, pathway_strength: float = 1.0) -> Optional[Tuple[Any, float]]:
        """Retrieve the single best-aligned knowledge item"""
        results = self.retrieve_relevant(query, pathway_strength)
        return results[0] if results else None
    
    def get_strength(self) -> float:
        """Overall node strength - combines all factors"""
        return self.capability * self.success_rate * self.processing_speed


@dataclass
class LearningEvent:
    """A learning event in the system"""
    timestamp: datetime
    event_type: str  # 'knowledge_added', 'node_created', 'connection_formed', 'pattern_discovered'
    description: str
    node_involved: Optional[str] = None
    knowledge_gained: Optional[str] = None


class Living4DSystem:
    """
    The Living System - Always learning, always growing.
    
    Architecture:
    - Core cognitive nodes (expandable)
    - Autonomous learning thread
    - Interactive query interface
    - Real-time growth visualization
    """
    
    def __init__(self):
        # Core nodes - the initial cognitive architecture
        self.nodes: Dict[str, CognitiveNode] = {}
        self._initialize_core_nodes()
        
        # Knowledge storage - NOW DISTRIBUTED ACROSS NODES
        self.knowledge_base: Dict[str, Dict] = {}  # Legacy - will migrate to nodes
        self.knowledge_file = Path(__file__).parent / "living_knowledge.json"
        self.architecture_file = Path(__file__).parent / "architecture_state.json"
        self._load_knowledge()
        
        # PATHWAY WEIGHTS - The TRUE learning happens here
        # pathway_weights[(from_node, to_node)] = strength (0.0 to 10.0)
        self.pathway_weights: Dict[Tuple[str, str], float] = {}
        self._initialize_pathway_weights()
        self._load_architecture()
        
        # Learning state
        self.learning_events: List[LearningEvent] = []
        self.is_alive = False
        self.learning_thread: Optional[threading.Thread] = None
        self.question_queue = queue.Queue()
        self.answer_queue = queue.Queue()
        
        # Growth metrics
        self.session_start = datetime.now()
        self.total_queries_processed = 0
        self.total_knowledge_items = len(self.knowledge_base)
        self.nodes_created_this_session = 0
        self.patterns_discovered = 0
        
        # Learning curriculum - what the system explores autonomously
        self.learning_curriculum = [
            # Python fundamentals
            {"domain": "python", "topic": "list comprehensions", "complexity": 1},
            {"domain": "python", "topic": "dictionary methods", "complexity": 1},
            {"domain": "python", "topic": "string formatting", "complexity": 1},
            {"domain": "python", "topic": "file handling", "complexity": 2},
            {"domain": "python", "topic": "exception handling", "complexity": 2},
            {"domain": "python", "topic": "decorators", "complexity": 3},
            {"domain": "python", "topic": "generators", "complexity": 3},
            {"domain": "python", "topic": "context managers", "complexity": 3},
            {"domain": "python", "topic": "metaclasses", "complexity": 4},
            {"domain": "python", "topic": "async await", "complexity": 4},
            # Algorithms
            {"domain": "algorithms", "topic": "sorting algorithms", "complexity": 2},
            {"domain": "algorithms", "topic": "binary search", "complexity": 2},
            {"domain": "algorithms", "topic": "graph traversal", "complexity": 3},
            {"domain": "algorithms", "topic": "dynamic programming", "complexity": 4},
            {"domain": "algorithms", "topic": "recursion patterns", "complexity": 3},
            # Architecture
            {"domain": "architecture", "topic": "design patterns", "complexity": 3},
            {"domain": "architecture", "topic": "SOLID principles", "complexity": 3},
            {"domain": "architecture", "topic": "microservices", "complexity": 4},
            {"domain": "architecture", "topic": "event driven", "complexity": 4},
            # Data
            {"domain": "data", "topic": "SQL queries", "complexity": 2},
            {"domain": "data", "topic": "JSON handling", "complexity": 1},
            {"domain": "data", "topic": "data validation", "complexity": 2},
            {"domain": "data", "topic": "API design", "complexity": 3},
        ]
        self.curriculum_index = 0
        
        # Node sequences - how information flows
        self.active_sequence: List[str] = []
        self.sequence_history: List[List[str]] = []
        
        # Learning control
        self.learning_paused = False
        
    def _initialize_core_nodes(self):
        """Initialize the core cognitive nodes"""
        core_nodes = [
            CognitiveNode("input", "Input Processing", "Receives and parses incoming queries"),
            CognitiveNode("pattern", "Pattern Recognition", "Identifies patterns in queries"),
            CognitiveNode("memory", "Memory Retrieval", "Searches knowledge base for relevant info"),
            CognitiveNode("reasoning", "Reasoning Engine", "Applies logic and inference"),
            CognitiveNode("synthesis", "Knowledge Synthesis", "Combines information to form responses"),
            CognitiveNode("output", "Output Generation", "Formats and delivers responses"),
            CognitiveNode("learning", "Learning Module", "Acquires new knowledge from interactions"),
            CognitiveNode("meta", "Meta-Cognition", "Monitors and optimizes own processing"),
            CognitiveNode("web", "Web Access", "Fetches information from the internet"),
            CognitiveNode("api", "API Integration", "Calls external APIs and services"),
            CognitiveNode("action", "System Action", "Executes actions on the computer"),
        ]
        
        for node in core_nodes:
            self.nodes[node.id] = node
            
        # Establish initial connections
        self.nodes["input"].connections = ["pattern", "memory", "web", "action"]
        self.nodes["pattern"].connections = ["reasoning", "memory", "web", "action"]
        self.nodes["memory"].connections = ["reasoning", "synthesis"]
        self.nodes["reasoning"].connections = ["synthesis", "web", "action"]
        self.nodes["synthesis"].connections = ["output", "learning"]
        self.nodes["output"].connections = ["meta"]
        self.nodes["learning"].connections = ["memory", "meta"]
        self.nodes["meta"].connections = ["input", "learning"]
        self.nodes["web"].connections = ["memory", "synthesis", "api"]
        self.nodes["api"].connections = ["web", "synthesis"]
        self.nodes["action"].connections = ["output", "meta"]
    
    def _initialize_pathway_weights(self):
        """Initialize pathway weights between all connected nodes"""
        for node_id, node in self.nodes.items():
            for connected_id in node.connections:
                # Initial weight = 1.0 (neutral)
                self.pathway_weights[(node_id, connected_id)] = 1.0
    
    def _load_architecture(self):
        """Load learned architecture state - this IS the learning!"""
        if self.architecture_file.exists():
            try:
                state = json.loads(self.architecture_file.read_text())
                
                # Restore pathway weights
                for key_str, weight in state.get("pathway_weights", {}).items():
                    from_node, to_node = key_str.split("->")
                    self.pathway_weights[(from_node, to_node)] = weight
                
                # Restore node capabilities
                for node_id, node_state in state.get("nodes", {}).items():
                    if node_id in self.nodes:
                        self.nodes[node_id].capability = node_state.get("capability", 1.0)
                        self.nodes[node_id].success_rate = node_state.get("success_rate", 0.5)
                        self.nodes[node_id].processing_speed = node_state.get("processing_speed", 1.0)
                        self.nodes[node_id].specializations = node_state.get("specializations", [])
                        self.nodes[node_id].activation_count = node_state.get("activation_count", 0)
                        # Restore embedded knowledge
                        for key, knowledge in node_state.get("embedded_knowledge", {}).items():
                            self.nodes[node_id].embedded_knowledge[key] = knowledge
                        self.nodes[node_id].knowledge_items = len(self.nodes[node_id].embedded_knowledge)
                
                print(f"{C.GREEN}✓ Restored learned architecture{C.RESET}")
            except Exception as e:
                print(f"{C.YELLOW}Starting fresh architecture: {e}{C.RESET}")
    
    def _save_architecture(self):
        """Save learned architecture state - PERSISTS THE LEARNING!"""
        state = {
            "saved_at": datetime.now().isoformat(),
            "pathway_weights": {
                f"{from_node}->{to_node}": weight 
                for (from_node, to_node), weight in self.pathway_weights.items()
            },
            "nodes": {
                node_id: {
                    "capability": node.capability,
                    "success_rate": node.success_rate,
                    "processing_speed": node.processing_speed,
                    "specializations": node.specializations,
                    "activation_count": node.activation_count,
                    "embedded_knowledge": node.embedded_knowledge,
                    "knowledge_items": node.knowledge_items
                }
                for node_id, node in self.nodes.items()
            }
        }
        self.architecture_file.write_text(json.dumps(state, indent=2, default=str))
    
    def strengthen_pathway(self, from_node: str, to_node: str, amount: float = 0.1):
        """Strengthen a pathway between nodes - THIS IS LEARNING!"""
        key = (from_node, to_node)
        if key in self.pathway_weights:
            old_weight = self.pathway_weights[key]
            # Logarithmic strengthening - prevents runaway
            new_weight = min(10.0, old_weight + amount * (1.0 / old_weight))
            self.pathway_weights[key] = new_weight
            
            # Also create reverse pathway if it doesn't exist (bidirectional learning)
            reverse_key = (to_node, from_node)
            if reverse_key not in self.pathway_weights:
                self.pathway_weights[reverse_key] = 1.0
            
            # Log pathway strengthening
            telemetry.log_pathway_strengthened(from_node, to_node, new_weight)
            
            return new_weight - old_weight
        return 0
    
    def weaken_pathway(self, from_node: str, to_node: str, amount: float = 0.05):
        """Weaken unused or failed pathways"""
        key = (from_node, to_node)
        if key in self.pathway_weights:
            self.pathway_weights[key] = max(0.1, self.pathway_weights[key] - amount)
    
    def get_strongest_path(self, from_node: str, to_nodes: List[str]) -> str:
        """Choose next node based on pathway strengths - learned routing!"""
        if not to_nodes:
            return None
        
        # Weight probabilities by pathway strength
        weights = []
        for to_node in to_nodes:
            key = (from_node, to_node)
            weight = self.pathway_weights.get(key, 1.0)
            # Also factor in target node's capability
            if to_node in self.nodes:
                weight *= self.nodes[to_node].capability
            weights.append(weight)
        
        # Probabilistic selection weighted by strength
        total = sum(weights)
        if total == 0:
            return random.choice(to_nodes)
        
        r = random.random() * total
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if r <= cumulative:
                return to_nodes[i]
        
        return to_nodes[-1]
    
    def _load_knowledge(self):
        """Load existing knowledge"""
        if self.knowledge_file.exists():
            try:
                self.knowledge_base = json.loads(self.knowledge_file.read_text())
            except:
                self.knowledge_base = {}
    
    def _save_knowledge(self):
        """Save knowledge to disk"""
        self.knowledge_file.write_text(json.dumps(self.knowledge_base, indent=2, default=str))
    
    def _log_event(self, event_type: str, description: str, node: str = None, knowledge: str = None):
        """Log a learning event"""
        event = LearningEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            description=description,
            node_involved=node,
            knowledge_gained=knowledge
        )
        self.learning_events.append(event)
    
    def activate_node(self, node_id: str, success: bool = True) -> Optional[CognitiveNode]:
        """Activate a cognitive node and strengthen pathways"""
        if node_id in self.nodes:
            # Track pathway for strengthening
            if self.active_sequence:
                prev_node = self.active_sequence[-1]
                if success:
                    self.strengthen_pathway(prev_node, node_id)
                else:
                    self.weaken_pathway(prev_node, node_id)
            
            self.nodes[node_id].activate(success)
            self.active_sequence.append(node_id)
            return self.nodes[node_id]
        return None
    
    def create_new_node(self, name: str, purpose: str, connections: List[str] = None) -> CognitiveNode:
        """Dynamically create a new cognitive node"""
        node_id = f"node_{len(self.nodes)}_{name.lower().replace(' ', '_')}"
        
        new_node = CognitiveNode(
            id=node_id,
            name=name,
            purpose=purpose,
            connections=connections or []
        )
        
        self.nodes[node_id] = new_node
        self.nodes_created_this_session += 1
        
        self._log_event(
            'node_created',
            f"Created new node: {name}",
            node_id,
            purpose
        )
        
        return new_node
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query through the cognitive network"""
        start_time = time.time()
        self.active_sequence = []
        
        # Stage 1: Input Processing
        self.activate_node("input")
        query_lower = query.lower()
        
        # Stage 2: Pattern Recognition  
        self.activate_node("pattern")
        domain = self._detect_domain(query_lower)
        needs_web = self._needs_web_access(query_lower)
        
        # Check for system action intent FIRST
        action_intent = self._detect_action_intent(query)
        if action_intent:
            self.activate_node("action")
            result = self.execute_system_action(action_intent["action"], action_intent.get("params", {}))
            
            elapsed = (time.time() - start_time) * 1000
            self.total_queries_processed += 1
            
            if result["success"]:
                response = f"✓ Action executed: {action_intent['action']}\n"
                for k, v in result.items():
                    if k not in ['success', 'action']:
                        response += f"  • {k}: {v}\n"
            else:
                response = f"✗ Action failed: {result.get('error', 'unknown error')}"
            
            self._log_event('action_executed', f"Executed: {action_intent['action']}", "action")
            
            self.activate_node("output")
            self.activate_node("meta")
            
            return {
                "response": response,
                "source": "system_action",
                "time_ms": elapsed,
                "sequence": self.active_sequence.copy(),
                "learned": False,
                "used_web": False,
                "action_result": result
            }
        
        # Stage 3: Memory Retrieval
        self.activate_node("memory")
        cached = self._check_knowledge(query_lower)
        
        if cached and not needs_web:
            # Fast path - knowledge exists
            self.activate_node("synthesis")
            self.activate_node("output")
            
            elapsed = (time.time() - start_time) * 1000
            self.total_queries_processed += 1
            
            # Log successful embedded retrieval
            domain = self._detect_domain(query_lower)
            telemetry.log_query(query, "embedded", elapsed, domain=domain)
            
            return {
                "response": cached["content"],
                "source": "crystallized_memory",
                "time_ms": elapsed,
                "sequence": self.active_sequence.copy(),
                "learned": False,
                "used_web": False
            }
        
        # Check if this needs web access
        if needs_web:
            web_result = self._handle_web_query(query, query_lower)
            if web_result:
                self.activate_node("synthesis")
                self.activate_node("learning")
                self._store_knowledge(query, web_result, "web")
                self.activate_node("output")
                
                elapsed = (time.time() - start_time) * 1000
                self.total_queries_processed += 1
                self.total_knowledge_items += 1
                
                return {
                    "response": web_result,
                    "source": "web_fetch",
                    "time_ms": elapsed,
                    "sequence": self.active_sequence.copy(),
                    "learned": True,
                    "used_web": True
                }
        
        # Stage 4: Reasoning (need to generate new knowledge)
        self.activate_node("reasoning")
        
        # Stage 5: Knowledge Synthesis via Qwen
        self.activate_node("synthesis")
        response = self._generate_knowledge(query, domain)
        
        # Stage 6: Learning
        self.activate_node("learning")
        self._store_knowledge(query, response, domain)
        
        # Stage 7: Output
        self.activate_node("output")
        
        # Stage 8: Meta-cognition
        self.activate_node("meta")
        
        elapsed = (time.time() - start_time) * 1000
        self.total_queries_processed += 1
        self.total_knowledge_items += 1
        
        # Log LLM generation
        telemetry.log_query(query, "llm", elapsed, domain=domain)
        
        self._log_event(
            'knowledge_added',
            f"Learned about: {query[:50]}...",
            "learning",
            query
        )
        
        return {
            "response": response,
            "source": "newly_synthesized",
            "time_ms": elapsed,
            "sequence": self.active_sequence.copy(),
            "learned": True,
            "used_web": False
        }
    
    def _needs_web_access(self, query: str) -> bool:
        """Detect if query needs web access"""
        web_keywords = [
            'search', 'find online', 'look up', 'google', 'website',
            'fetch', 'url', 'http', 'www.', 'latest', 'current',
            'news', 'today', 'recent', 'download', 'api call',
            'web search', 'browse', 'internet'
        ]
        return any(kw in query for kw in web_keywords)
    
    def _handle_web_query(self, query: str, query_lower: str) -> Optional[str]:
        """Handle a web-related query"""
        # Direct URL fetch
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, query)
        
        if urls:
            result = self.fetch_webpage(urls[0])
            if result["success"]:
                return f"**Fetched: {result['title']}**\n\n{result['content'][:2000]}"
        
        # Web search
        if any(kw in query_lower for kw in ['search', 'find', 'look up', 'google']):
            # Extract search terms
            search_query = query_lower
            for remove in ['search for', 'search', 'find', 'look up', 'google']:
                search_query = search_query.replace(remove, '').strip()
            
            if search_query:
                result = self.search_web(search_query)
                if result["success"] and result["results"]:
                    response = f"**Web Search Results for: {search_query}**\n\n"
                    for i, r in enumerate(result["results"], 1):
                        response += f"{i}. **{r['title']}**\n"
                        if r['snippet']:
                            response += f"   {r['snippet'][:150]}...\n"
                        if r['url']:
                            response += f"   URL: {r['url']}\n"
                        response += "\n"
                    return response
        
        return None
    
    def _detect_domain(self, query: str) -> str:
        """Detect the domain of a query"""
        domain_keywords = {
            "python": ["python", "def", "class", "import", "list", "dict", "string", "file"],
            "algorithms": ["sort", "search", "algorithm", "complexity", "recursion", "graph"],
            "architecture": ["design", "pattern", "solid", "microservice", "architecture"],
            "data": ["sql", "database", "json", "api", "data", "query"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(kw in query for kw in keywords):
                return domain
        return "general"
    
    def _check_knowledge(self, query: str) -> Optional[Dict]:
        """
        Check for knowledge using 4D ALIGNMENT-BASED retrieval.
        
        Key differences from exact matching:
        1. Uses θ_coherence (alignment score) instead of exact match
        2. Pathway strength provides A_path amplification
        3. Multiple sequence paths are tried based on query type
        4. Node capability affects retrieval threshold
        """
        query_lower = query.lower()
        
        # Skip retrieval for novelty queries
        novelty_indicators = ['something', 'anything', 'random', 'new idea', 'different', 'another', 'else']
        if any(indicator in query_lower for indicator in novelty_indicators):
            return None
        
        # === SELECT OPTIMAL SEQUENCE ===
        sequence_name, sequence = SequenceSelector.select_sequence(query)
        
        best_result = None
        best_score = 0.0
        
        # === TRY MULTIPLE RETRIEVAL PATHS ===
        # 4D Principle: Different sequences produce different outcomes
        
        # Path 1: Memory-first retrieval (for recall queries)
        memory_pathway_strength = self.pathway_weights.get(("input", "memory"), 1.0)
        memory_node = self.nodes["memory"]
        memory_results = memory_node.retrieve_relevant(query, memory_pathway_strength)
        
        if memory_results:
            knowledge, score = memory_results[0]
            if score > best_score:
                best_result = knowledge
                best_score = score
                # Strengthen the successful pathway
                self.strengthen_pathway("input", "memory", 0.03)
                memory_node.activate(success=True)
        
        # Path 2: Domain-specialized node retrieval
        domain = self._detect_domain(query_lower)
        domain_node_map = {
            "python": "reasoning",
            "programming": "reasoning",
            "algorithms": "reasoning",
            "architecture": "synthesis",
            "web": "web",
            "data": "memory"
        }
        
        target_node_id = domain_node_map.get(domain, "reasoning")
        if target_node_id in self.nodes:
            target_node = self.nodes[target_node_id]
            pathway_strength = self.pathway_weights.get(("input", target_node_id), 1.0)
            
            domain_results = target_node.retrieve_relevant(query, pathway_strength)
            if domain_results:
                knowledge, score = domain_results[0]
                if score > best_score:
                    best_result = knowledge
                    best_score = score
                    self.strengthen_pathway("input", target_node_id, 0.03)
                    target_node.activate(success=True)
        
        # Path 3: Pattern-based retrieval (if pattern node is specialized)
        if "pattern" in self.nodes:
            pattern_node = self.nodes["pattern"]
            if pattern_node.capability > 1.5 or domain in pattern_node.specializations:
                pathway_strength = self.pathway_weights.get(("input", "pattern"), 1.0)
                pattern_results = pattern_node.retrieve_relevant(query, pathway_strength)
                if pattern_results:
                    knowledge, score = pattern_results[0]
                    if score > best_score:
                        best_result = knowledge
                        best_score = score
                        self.strengthen_pathway("input", "pattern", 0.03)
                        pattern_node.activate(success=True)
        
        # If we found aligned knowledge, return it
        if best_result and best_score >= 0.15:
            return best_result
        
        # === FALLBACK: Legacy knowledge base with ALIGNMENT scoring ===
        # Even the fallback now uses alignment instead of exact match
        if self.knowledge_base:
            aligned_results = AlignmentScorer.compute_batch_alignment(
                query, 
                self.knowledge_base,
                pathway_strength=1.0  # Legacy has no pathway boost
            )
            
            if aligned_results:
                key, knowledge, score = aligned_results[0]
                if score >= 0.2:  # Higher threshold for legacy (no node capability boost)
                    return knowledge
        
        return None
    
    def _generate_knowledge(self, query: str, domain: str) -> str:
        """Generate new knowledge using Qwen"""
        if not HAS_OLLAMA:
            return f"[Simulated response for: {query}]"
        
        try:
            response = ollama.chat(
                model='qwen3:4b',
                messages=[
                    {"role": "system", "content": f"You are a {domain} expert. Give concise, practical answers. /no_think"},
                    {"role": "user", "content": query}
                ]
            )
            return response.message.content
        except Exception as e:
            return f"[Error generating: {e}]"
    
    def _store_knowledge(self, query: str, response: str, domain: str):
        """Store newly acquired knowledge - BOTH in nodes AND backup file"""
        query_hash = hash(query.lower()) % 10000000
        key = f"q_{query_hash}"
        
        knowledge_item = {
            "query": query,
            "content": response,
            "domain": domain,
            "keywords": query.lower().split(),
            "created": datetime.now().isoformat(),
            "access_count": 1
        }
        
        # LEGACY: Store in external file (backup)
        self.knowledge_base[key] = knowledge_item
        self._save_knowledge()
        
        # TRUE ARCHITECTURAL LEARNING: Store IN the relevant nodes
        # Memory node gets everything
        self.nodes["memory"].add_embedded_knowledge(key, knowledge_item)
        
        # Log knowledge storage
        telemetry.log_knowledge_stored(domain, key)
        
        # Domain-specific nodes get specialized knowledge
        domain_node_map = {
            "programming": "reasoning",
            "python": "reasoning", 
            "algorithms": "reasoning",
            "architecture": "synthesis",
            "data": "memory",
            "web": "web",
            "api": "api",
            "system": "action",
            "general": "synthesis"
        }
        
        target_node = domain_node_map.get(domain, "synthesis")
        if target_node in self.nodes:
            self.nodes[target_node].add_embedded_knowledge(key, knowledge_item)
            # Node becomes specialized in this domain
            if domain not in self.nodes[target_node].specializations:
                self.nodes[target_node].specializations.append(domain)
        
        # SAVE THE ARCHITECTURE - this persists the learning!
        self._save_architecture()
    
    # ═══════════════════════════════════════════════════════════════
    # INTERNET CAPABILITIES
    # ═══════════════════════════════════════════════════════════════
    
    def fetch_webpage(self, url: str) -> Dict[str, Any]:
        """Fetch and parse a webpage"""
        self.activate_node("web")
        
        try:
            if HAS_REQUESTS:
                headers = {'User-Agent': 'Mozilla/5.0 (4D-System/1.0)'}
                response = requests.get(url, headers=headers, timeout=10)
                html = response.text
                status = response.status_code
            else:
                # Fallback to urllib
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (4D-System/1.0)'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8')
                    status = response.status
            
            # Parse if BeautifulSoup available
            if HAS_BS4:
                soup = BeautifulSoup(html, 'html.parser')
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator='\n', strip=True)
                title = soup.title.string if soup.title else "No title"
            else:
                # Basic text extraction
                text = re.sub(r'<[^>]+>', '', html)
                title_match = re.search(r'<title>([^<]+)</title>', html, re.I)
                title = title_match.group(1) if title_match else "No title"
            
            self._log_event('knowledge_added', f"Fetched webpage: {url[:50]}", "web", url)
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "content": text[:5000],  # Limit content
                "status": status
            }
            
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def search_web(self, query: str) -> Dict[str, Any]:
        """Search the web using DuckDuckGo (no API key needed)"""
        self.activate_node("web")
        
        try:
            # Use DuckDuckGo HTML search (no API key required)
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            headers = {'User-Agent': 'Mozilla/5.0 (4D-System/1.0)'}
            
            if HAS_REQUESTS:
                response = requests.get(url, headers=headers, timeout=10)
                html = response.text
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8')
            
            # Extract results
            results = []
            
            if HAS_BS4:
                soup = BeautifulSoup(html, 'html.parser')
                for result in soup.select('.result')[:5]:
                    title_elem = result.select_one('.result__title')
                    snippet_elem = result.select_one('.result__snippet')
                    link_elem = result.select_one('.result__url')
                    
                    if title_elem:
                        results.append({
                            "title": title_elem.get_text(strip=True),
                            "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                            "url": link_elem.get_text(strip=True) if link_elem else ""
                        })
            else:
                # Basic regex extraction
                pattern = r'class="result__title"[^>]*>([^<]+)'
                matches = re.findall(pattern, html)[:5]
                results = [{"title": m, "snippet": "", "url": ""} for m in matches]
            
            self._log_event('knowledge_added', f"Web search: {query[:30]}", "web", query)
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e)
            }
    
    def call_api(self, url: str, method: str = "GET", data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Call an external API"""
        self.activate_node("api")
        
        try:
            default_headers = {'User-Agent': 'Mozilla/5.0 (4D-System/1.0)', 'Accept': 'application/json'}
            if headers:
                default_headers.update(headers)
            
            if HAS_REQUESTS:
                if method.upper() == "GET":
                    response = requests.get(url, headers=default_headers, timeout=10)
                elif method.upper() == "POST":
                    response = requests.post(url, json=data, headers=default_headers, timeout=10)
                else:
                    response = requests.request(method, url, json=data, headers=default_headers, timeout=10)
                
                try:
                    json_response = response.json()
                except:
                    json_response = {"text": response.text[:1000]}
                
                return {
                    "success": True,
                    "status": response.status_code,
                    "data": json_response
                }
            else:
                # Fallback
                req = urllib.request.Request(url, headers=default_headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    return {
                        "success": True,
                        "status": response.status,
                        "data": json.loads(response.read().decode('utf-8'))
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_internet(self) -> bool:
        """Check if internet is available"""
        try:
            urllib.request.urlopen('https://www.google.com', timeout=3)
            return True
        except:
            try:
                urllib.request.urlopen('https://www.cloudflare.com', timeout=3)
                return True
            except:
                return False
    
    # ═══════════════════════════════════════════════════════════════
    # SYSTEM ACTION CAPABILITIES
    # ═══════════════════════════════════════════════════════════════
    
    def execute_system_action(self, action: str, params: Dict = None) -> Dict[str, Any]:
        """Execute a system action on the computer"""
        self.activate_node("action")
        params = params or {}
        
        import platform
        system = platform.system()
        
        try:
            if action == "brightness":
                return self._set_brightness(params.get("level", 100), system)
            elif action == "volume":
                return self._set_volume(params.get("level", 50), system)
            elif action == "mute":
                return self._toggle_mute(system)
            elif action == "open_app":
                return self._open_application(params.get("app", ""), system)
            elif action == "open_url":
                return self._open_url(params.get("url", ""))
            elif action == "say":
                return self._text_to_speech(params.get("text", ""), system)
            elif action == "notification":
                return self._send_notification(params.get("title", "4D System"), params.get("message", ""), system)
            elif action == "clipboard":
                return self._manage_clipboard(params.get("operation", "get"), params.get("text", ""), system)
            elif action == "screenshot":
                return self._take_screenshot(params.get("path", ""), system)
            elif action == "dark_mode":
                return self._toggle_dark_mode(params.get("enable", True), system)
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _set_brightness(self, level: int, system: str) -> Dict:
        """Set screen brightness"""
        level = max(0, min(100, level))
        
        if system == "Darwin":  # macOS
            # Use brightness command if available, otherwise AppleScript
            try:
                # Try using brightness CLI tool
                result = subprocess.run(["brightness", str(level / 100)], capture_output=True, timeout=5)
                if result.returncode == 0:
                    return {"success": True, "action": "brightness", "level": level, "method": "brightness_cli"}
            except:
                pass
            
            # Fallback: Use AppleScript with System Events (works on most Macs)
            script = f'''
            tell application "System Preferences"
                reveal anchor "displaysDisplayTab" of pane id "com.apple.preference.displays"
            end tell
            delay 0.5
            tell application "System Events"
                tell process "System Preferences"
                    set value of slider 1 of group 1 of tab group 1 of window 1 to {level / 100}
                end tell
            end tell
            tell application "System Preferences" to quit
            '''
            try:
                subprocess.run(["osascript", "-e", script], capture_output=True, timeout=10)
                return {"success": True, "action": "brightness", "level": level, "method": "applescript", 
                        "note": "If this didn't work, try: brew install brightness"}
            except:
                return {"success": False, "error": "Could not set brightness. Install 'brightness' CLI: brew install brightness"}
        
        elif system == "Linux":
            # Try xrandr
            try:
                result = subprocess.run(["xrandr", "--output", "eDP-1", "--brightness", str(level / 100)], 
                                       capture_output=True, timeout=5)
                return {"success": True, "action": "brightness", "level": level}
            except:
                return {"success": False, "error": "xrandr not available"}
        
        return {"success": False, "error": f"Brightness control not supported on {system}"}
    
    def _set_volume(self, level: int, system: str) -> Dict:
        """Set system volume"""
        level = max(0, min(100, level))
        
        if system == "Darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"], capture_output=True)
            return {"success": True, "action": "volume", "level": level}
        elif system == "Linux":
            subprocess.run(["amixer", "set", "Master", f"{level}%"], capture_output=True)
            return {"success": True, "action": "volume", "level": level}
        
        return {"success": False, "error": f"Volume control not supported on {system}"}
    
    def _toggle_mute(self, system: str) -> Dict:
        """Toggle mute"""
        if system == "Darwin":
            # Get current mute state and toggle
            subprocess.run(["osascript", "-e", "set volume with output muted"], capture_output=True)
            return {"success": True, "action": "mute", "state": "toggled"}
        return {"success": False, "error": f"Mute not supported on {system}"}
    
    def _open_application(self, app: str, system: str) -> Dict:
        """Open an application"""
        if system == "Darwin":
            result = subprocess.run(["open", "-a", app], capture_output=True)
            return {"success": result.returncode == 0, "action": "open_app", "app": app}
        elif system == "Linux":
            subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"success": True, "action": "open_app", "app": app}
        return {"success": False, "error": f"Cannot open apps on {system}"}
    
    def _open_url(self, url: str) -> Dict:
        """Open a URL in default browser"""
        import webbrowser
        webbrowser.open(url)
        return {"success": True, "action": "open_url", "url": url}
    
    def _text_to_speech(self, text: str, system: str) -> Dict:
        """Speak text aloud"""
        if system == "Darwin":
            subprocess.run(["say", text], capture_output=True)
            return {"success": True, "action": "say", "text": text[:50]}
        elif system == "Linux":
            subprocess.run(["espeak", text], capture_output=True)
            return {"success": True, "action": "say", "text": text[:50]}
        return {"success": False, "error": f"TTS not supported on {system}"}
    
    def _send_notification(self, title: str, message: str, system: str) -> Dict:
        """Send a system notification"""
        if system == "Darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], capture_output=True)
            return {"success": True, "action": "notification", "title": title}
        return {"success": False, "error": f"Notifications not supported on {system}"}
    
    def _manage_clipboard(self, operation: str, text: str, system: str) -> Dict:
        """Get or set clipboard"""
        if system == "Darwin":
            if operation == "set":
                process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
                process.communicate(text.encode())
                return {"success": True, "action": "clipboard_set"}
            else:
                result = subprocess.run(["pbpaste"], capture_output=True, text=True)
                return {"success": True, "action": "clipboard_get", "content": result.stdout[:500]}
        return {"success": False, "error": f"Clipboard not supported on {system}"}
    
    def _take_screenshot(self, path: str, system: str) -> Dict:
        """Take a screenshot"""
        if not path:
            path = f"/tmp/screenshot_{int(time.time())}.png"
        
        if system == "Darwin":
            subprocess.run(["screencapture", path], capture_output=True)
            return {"success": True, "action": "screenshot", "path": path}
        elif system == "Linux":
            subprocess.run(["scrot", path], capture_output=True)
            return {"success": True, "action": "screenshot", "path": path}
        return {"success": False, "error": f"Screenshot not supported on {system}"}
    
    def _toggle_dark_mode(self, enable: bool, system: str) -> Dict:
        """Toggle dark mode"""
        if system == "Darwin":
            mode = "true" if enable else "false"
            script = f'tell app "System Events" to tell appearance preferences to set dark mode to {mode}'
            subprocess.run(["osascript", "-e", script], capture_output=True)
            return {"success": True, "action": "dark_mode", "enabled": enable}
        return {"success": False, "error": f"Dark mode not supported on {system}"}
    
    def _detect_action_intent(self, query: str) -> Optional[Dict]:
        """Detect if query is requesting a system action"""
        query_lower = query.lower()
        
        # Brightness patterns
        if any(w in query_lower for w in ['brightness', 'screen bright', 'display bright']):
            level = 100 if any(w in query_lower for w in ['max', 'full', 'all the way', 'highest', '100']) else \
                    0 if any(w in query_lower for w in ['min', 'lowest', 'off', '0']) else \
                    50 if 'half' in query_lower else None
            if level is not None:
                return {"action": "brightness", "params": {"level": level}}
            # Try to extract number
            nums = re.findall(r'\d+', query)
            if nums:
                return {"action": "brightness", "params": {"level": int(nums[0])}}
        
        # Volume patterns
        if any(w in query_lower for w in ['volume', 'sound level']):
            level = 100 if any(w in query_lower for w in ['max', 'full', 'highest']) else \
                    0 if any(w in query_lower for w in ['min', 'lowest', 'off', 'mute']) else \
                    50 if 'half' in query_lower else None
            if level is not None:
                return {"action": "volume", "params": {"level": level}}
            nums = re.findall(r'\d+', query)
            if nums:
                return {"action": "volume", "params": {"level": int(nums[0])}}
        
        # Mute
        if 'mute' in query_lower:
            return {"action": "mute", "params": {}}
        
        # Open application
        if any(w in query_lower for w in ['open', 'launch', 'start']):
            apps = ['safari', 'chrome', 'firefox', 'terminal', 'finder', 'notes', 'calendar', 
                    'mail', 'messages', 'music', 'spotify', 'slack', 'discord', 'vscode', 
                    'code', 'xcode', 'photoshop', 'figma']
            for app in apps:
                if app in query_lower:
                    return {"action": "open_app", "params": {"app": app.capitalize() if app != 'vscode' else 'Visual Studio Code'}}
        
        # Say/speak
        if any(w in query_lower for w in ['say ', 'speak ']):
            # Extract what to say
            for prefix in ['say ', 'speak ']:
                if prefix in query_lower:
                    text = query_lower.split(prefix, 1)[1]
                    if text:  # Only if there's something to say
                        return {"action": "say", "params": {"text": text}}
        
        # Dark mode
        if 'dark mode' in query_lower:
            enable = 'off' not in query_lower and 'disable' not in query_lower
            return {"action": "dark_mode", "params": {"enable": enable}}
        
        # Screenshot
        if 'screenshot' in query_lower or 'screen shot' in query_lower:
            return {"action": "screenshot", "params": {}}
        
        # Notification
        if 'notification' in query_lower or 'notify' in query_lower:
            return {"action": "notification", "params": {"title": "4D System", "message": "Test notification"}}
        
        return None
    
    def _autonomous_learning_loop(self):
        """Background thread for autonomous learning - ALWAYS LEARNING"""
        learning_interval = 0  # Track time since last auto-learn
        
        while self.is_alive:
            # Check for user questions first (priority)
            try:
                question = self.question_queue.get_nowait()
                result = self.process_query(question)
                self.answer_queue.put(result)
                continue
            except queue.Empty:
                pass
            
            # Skip learning if paused
            if self.learning_paused:
                time.sleep(1)
                continue
            
            # AUTONOMOUS LEARNING - happens continuously
            learning_interval += 1
            
            # Learn something new every ~3 seconds
            if learning_interval >= 3:
                learning_interval = 0
                
                # Pick what to learn
                if self.curriculum_index < len(self.learning_curriculum):
                    # Learn from curriculum
                    item = self.learning_curriculum[self.curriculum_index]
                    query = f"Explain {item['topic']} in {item['domain']} with a code example"
                    
                    # Check if we already know this
                    if not self._check_knowledge(query.lower()):
                        # Show learning activity
                        self._show_learning_activity(f"Learning: {item['topic']} ({item['domain']})")
                        
                        # Learn it (silently)
                        old_stdout = sys.stdout
                        sys.stdout = open(os.devnull, 'w')
                        try:
                            self.process_query(query)
                        finally:
                            sys.stdout.close()
                            sys.stdout = old_stdout
                        
                        self._show_learning_complete(item['topic'])
                    
                    self.curriculum_index += 1
                    
                else:
                    # Finished curriculum - explore connections and deepen knowledge
                    self._autonomous_exploration()
            
            # Small sleep to not overwhelm CPU
            time.sleep(1)
    
    def _show_learning_activity(self, message: str):
        """Show that learning is happening (non-blocking)"""
        # Print above the prompt
        print(f"\r{C.DIM}🧠 {message}...{C.RESET}", end='', flush=True)
    
    def _show_learning_complete(self, topic: str):
        """Show learning completed"""
        print(f"\r{C.GREEN}✓ Learned: {topic}{C.RESET}                              ")
        # Reprint prompt
        elapsed = (datetime.now() - self.session_start).total_seconds()
        print(f"{C.GREEN}●{C.RESET} {C.CYAN}4D [{self.total_knowledge_items} items | {elapsed:.0f}s]{C.RESET}> ", end='', flush=True)
    
    def _autonomous_exploration(self):
        """Explore and learn on its own - find connections, deepen knowledge"""
        exploration_types = [
            self._explore_connections,
            self._deepen_random_topic,
            self._learn_related_concept,
            self._practice_coding_problem,
        ]
        
        # Pick a random exploration type
        explorer = random.choice(exploration_types)
        explorer()
    
    def _deepen_random_topic(self):
        """Pick a known topic and learn more about it"""
        if not self.knowledge_base:
            return
        
        # Pick a random known topic
        key = random.choice(list(self.knowledge_base.keys()))
        item = self.knowledge_base[key]
        
        domain = item.get('domain', 'programming')
        deepening_queries = [
            f"What are advanced techniques for {domain}?",
            f"Common mistakes when working with {domain}",
            f"Best practices for {domain} in production",
            f"How to optimize {domain} performance",
        ]
        
        query = random.choice(deepening_queries)
        
        if not self._check_knowledge(query.lower()):
            self._show_learning_activity(f"Deepening: {domain}")
            
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                self.process_query(query)
            finally:
                sys.stdout.close()
                sys.stdout = old_stdout
            
            self._show_learning_complete(f"{domain} (advanced)")
    
    def _learn_related_concept(self):
        """Learn something related to existing knowledge"""
        related_concepts = [
            ("python", ["typing", "asyncio", "dataclasses", "protocols", "slots"]),
            ("algorithms", ["time complexity", "space complexity", "amortized analysis"]),
            ("architecture", ["dependency injection", "event sourcing", "CQRS"]),
            ("data", ["indexing", "normalization", "caching strategies"]),
        ]
        
        domain, concepts = random.choice(related_concepts)
        concept = random.choice(concepts)
        
        query = f"Explain {concept} in {domain} with examples"
        
        if not self._check_knowledge(query.lower()):
            self._show_learning_activity(f"Exploring: {concept}")
            
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                self.process_query(query)
            finally:
                sys.stdout.close()
                sys.stdout = old_stdout
            
            self._show_learning_complete(concept)
    
    def _practice_coding_problem(self):
        """Learn by practicing a coding problem"""
        problems = [
            "Implement a LRU cache in Python",
            "Write a function to detect cycles in a linked list",
            "Implement binary search with edge cases",
            "Write a decorator that memoizes function results",
            "Implement a rate limiter class",
            "Write a function to merge overlapping intervals",
            "Implement a trie data structure",
            "Write a thread-safe singleton pattern",
        ]
        
        problem = random.choice(problems)
        
        if not self._check_knowledge(problem.lower()):
            self._show_learning_activity(f"Practicing: {problem[:30]}...")
            
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')
            try:
                self.process_query(problem)
            finally:
                sys.stdout.close()
                sys.stdout = old_stdout
            
            self._show_learning_complete(problem[:40])
    
    def _explore_connections(self):
        """Explore connections between learned topics"""
        if len(self.knowledge_base) < 5:
            return
        
        # Pick two random knowledge items
        keys = list(self.knowledge_base.keys())
        if len(keys) >= 2:
            k1, k2 = random.sample(keys, 2)
            item1 = self.knowledge_base[k1]
            item2 = self.knowledge_base[k2]
            
            # Try to find connections
            if item1.get("domain") != item2.get("domain"):
                d1 = item1.get('domain', 'topic1')
                d2 = item2.get('domain', 'topic2')
                connection_query = f"How does {d1} relate to {d2} in software engineering?"
                
                if not self._check_knowledge(connection_query.lower()):
                    self._show_learning_activity(f"Connecting: {d1} ↔ {d2}")
                    
                    old_stdout = sys.stdout
                    sys.stdout = open(os.devnull, 'w')
                    try:
                        self.process_query(connection_query)
                    finally:
                        sys.stdout.close()
                        sys.stdout = old_stdout
                    
                    self.patterns_discovered += 1
                    self._show_learning_complete(f"Connection: {d1} ↔ {d2}")
                    
                    self._log_event(
                        'pattern_discovered',
                        f"Found connection: {d1} ↔ {d2}",
                        "meta"
                    )
    
    def start(self):
        """Start the living system - TURN THE LIGHTS ON"""
        self.is_alive = True
        self.session_start = datetime.now()
        
        # Start autonomous learning thread
        self.learning_thread = threading.Thread(target=self._autonomous_learning_loop, daemon=True)
        self.learning_thread.start()
        
        self._display_startup()
        self._interactive_loop()
    
    def _display_startup(self):
        """Display the startup sequence"""
        # Check internet connectivity
        internet_status = self.check_internet()
        internet_indicator = f"{C.GREEN}● ONLINE{C.RESET}" if internet_status else f"{C.RED}● OFFLINE{C.RESET}"
        
        print(f"""
{C.RED}{C.BOLD}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ████  █████      ██      ██ ██    ██ ██ ██    ██  ██████                     ║
║   ██  █ ██  ██     ██      ██ ██    ██ ██ ███   ██ ██                          ║
║   ████  ██  ██     ██      ██ ██    ██ ██ ██ █  ██ ██  ███                     ║
║   ██  █ ██  ██     ██      ██  ██  ██  ██ ██  █ ██ ██   ██                     ║
║   ████  █████      ███████ ██   ████   ██ ██   ███  ██████                     ║
║                                                                               ║
║                     THE LIVING 4D COGNITIVE SYSTEM                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{C.RESET}
{C.GREEN}System Status:{C.RESET}
  • Cognitive nodes: {len(self.nodes)} active
  • Knowledge items: {self.total_knowledge_items}
  • Learning curriculum: {len(self.learning_curriculum)} topics
  • Internet: {internet_indicator}
  • Status: {C.GREEN}ALIVE & LEARNING{C.RESET}

{C.YELLOW}╔════════════════════════════════════════════════════════════════════╗
║  🧠 AUTONOMOUS LEARNING ACTIVE                                     ║
║                                                                    ║
║  The system is now learning continuously in the background.        ║
║  Watch as it acquires new knowledge automatically.                 ║
║  You can ask questions anytime - they take priority.               ║
╚════════════════════════════════════════════════════════════════════╝{C.RESET}

{C.DIM}Commands:
  /status    - Show current growth status
  /nodes     - Show cognitive node network
  /sequence  - Show last processing sequence
  /events    - Show recent learning events  
  /growth    - Show growth visualization
  /web       - Test internet connectivity
  /search X  - Search the web for X
  /fetch URL - Fetch a webpage
  /pause     - Pause autonomous learning
  /resume    - Resume autonomous learning
  /stop      - Shut down the system{C.RESET}

{C.CYAN}Learning will begin in 3 seconds...{C.RESET}
""")
    
    def _interactive_loop(self):
        """Main interactive loop"""
        while self.is_alive:
            try:
                # Show that system is alive
                elapsed = (datetime.now() - self.session_start).total_seconds()
                
                # Prompt with live indicator
                prompt = f"{C.GREEN}●{C.RESET} {C.CYAN}4D [{self.total_knowledge_items} items | {elapsed:.0f}s]{C.RESET}> "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == '/stop':
                    self.stop()
                    break
                
                elif user_input.lower() == '/status':
                    self._show_status()
                    continue
                
                elif user_input.lower() == '/nodes':
                    self._show_nodes()
                    continue
                
                elif user_input.lower() == '/sequence':
                    self._show_sequence()
                    continue
                
                elif user_input.lower() == '/events':
                    self._show_events()
                    continue
                
                elif user_input.lower() == '/growth':
                    self._show_growth()
                    continue
                
                elif user_input.lower() == '/pathways':
                    self._show_pathways()
                    continue
                
                elif user_input.lower() == '/web':
                    self._test_internet()
                    continue
                
                elif user_input.lower().startswith('/search '):
                    search_term = user_input[8:].strip()
                    if search_term:
                        print(f"\n{C.CYAN}Searching the web for: {search_term}{C.RESET}")
                        result = self.search_web(search_term)
                        self._display_web_results(result)
                    continue
                
                elif user_input.lower().startswith('/fetch '):
                    url = user_input[7:].strip()
                    if url:
                        print(f"\n{C.CYAN}Fetching: {url}{C.RESET}")
                        result = self.fetch_webpage(url)
                        self._display_fetch_result(result)
                    continue
                
                elif user_input.lower() == '/pause':
                    self.learning_paused = True
                    print(f"\n{C.YELLOW}⏸  Autonomous learning PAUSED{C.RESET}")
                    print(f"{C.DIM}   Use /resume to continue learning{C.RESET}")
                    continue
                
                elif user_input.lower() == '/resume':
                    self.learning_paused = False
                    print(f"\n{C.GREEN}▶  Autonomous learning RESUMED{C.RESET}")
                    continue
                
                elif user_input.lower() == '/help':
                    print(f"""
{C.CYAN}┌─────────────────────────────────────────────────────────────────┐
│ 4D LIVING SYSTEM COMMANDS                                       │
├─────────────────────────────────────────────────────────────────┤{C.RESET}
│ {C.GREEN}/status{C.RESET}   - Show system status and statistics
│ {C.GREEN}/nodes{C.RESET}    - Show cognitive node capabilities (TRUE learning!)
│ {C.GREEN}/pathways{C.RESET} - Show pathway strengths (the learned architecture)
│ {C.GREEN}/sequence{C.RESET} - Show current processing sequence
│ {C.GREEN}/events{C.RESET}   - Show recent learning events
│ {C.GREEN}/growth{C.RESET}   - Show growth visualization
│ {C.GREEN}/web{C.RESET}      - Test internet connectivity
│ {C.GREEN}/search{C.RESET}   - Search the web (e.g., /search quantum physics)
│ {C.GREEN}/fetch{C.RESET}    - Fetch a webpage (e.g., /fetch https://...)
│ {C.GREEN}/pause{C.RESET}    - Pause autonomous learning
│ {C.GREEN}/resume{C.RESET}   - Resume autonomous learning
│ {C.GREEN}/stop{C.RESET}     - Shutdown the system
{C.CYAN}└─────────────────────────────────────────────────────────────────┘{C.RESET}
""")
                    continue
                
                # Process as question
                print(f"\n{C.DIM}Processing through cognitive network...{C.RESET}")
                
                # Queue the question for the learning thread
                self.question_queue.put(user_input)
                
                # Wait for answer
                try:
                    result = self.answer_queue.get(timeout=30)
                    self._display_result(result)
                except queue.Empty:
                    print(f"{C.RED}Timeout waiting for response{C.RESET}")
                
            except KeyboardInterrupt:
                print(f"\n{C.YELLOW}Use /stop to shutdown gracefully{C.RESET}")
                continue
            except EOFError:
                self.stop()
                break
    
    def _display_result(self, result: Dict):
        """Display a query result with cognitive trace"""
        print(f"""
{C.CYAN}┌─────────────────────────────────────────────────────────────────┐
│ COGNITIVE PROCESSING COMPLETE                                   │
├─────────────────────────────────────────────────────────────────┤{C.RESET}
│ Source: {result['source']:20} Time: {result['time_ms']:.1f}ms
│ Learned: {str(result['learned']):5}               Nodes activated: {len(result['sequence'])}
{C.CYAN}├─────────────────────────────────────────────────────────────────┤
│ NODE SEQUENCE:{C.RESET}
│   {' → '.join(result['sequence'])}
{C.CYAN}├─────────────────────────────────────────────────────────────────┤
│ RESPONSE:{C.RESET}
""")
        
        # Display response with wrapping
        response = result['response'][:500]
        for line in response.split('\n'):
            print(f"│   {line}")
        
        print(f"{C.CYAN}└─────────────────────────────────────────────────────────────────┘{C.RESET}\n")
    
    def _show_status(self):
        """Show current system status"""
        elapsed = datetime.now() - self.session_start
        
        print(f"""
{C.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║  SYSTEM STATUS                                                    ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}

  {C.BOLD}Runtime:{C.RESET}         {elapsed}
  {C.BOLD}Status:{C.RESET}          {C.GREEN}ALIVE{C.RESET}
  
  {C.BOLD}Growth Metrics:{C.RESET}
    Knowledge items:      {self.total_knowledge_items}
    Queries processed:    {self.total_queries_processed}
    New nodes created:    {self.nodes_created_this_session}
    Patterns discovered:  {self.patterns_discovered}
    Learning events:      {len(self.learning_events)}
  
  {C.BOLD}Learning Progress:{C.RESET}
    Curriculum progress:  {self.curriculum_index}/{len(self.learning_curriculum)} topics
    Progress bar:         [{'█' * (self.curriculum_index * 20 // max(len(self.learning_curriculum), 1))}{' ' * (20 - self.curriculum_index * 20 // max(len(self.learning_curriculum), 1))}]

{C.CYAN}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}
""")
    
    def _show_nodes(self):
        """Show the cognitive node network with TRUE capability levels"""
        print(f"""
{C.MAGENTA}╔═══════════════════════════════════════════════════════════════════╗
║  COGNITIVE NODE NETWORK - LEARNED CAPABILITIES                    ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
""")
        
        for node_id, node in self.nodes.items():
            # Calculate capability bar (capability ranges 0.1 to 10.0)
            cap_bar_len = int(node.capability * 2)  # Max 20 chars at capability 10
            cap_bar = '█' * min(cap_bar_len, 20)
            
            # Color based on capability
            if node.capability >= 3.0:
                cap_color = C.GREEN
            elif node.capability >= 1.5:
                cap_color = C.CYAN
            else:
                cap_color = C.DIM
            
            status = f"{C.GREEN}●{C.RESET}" if node.last_activated and (datetime.now() - node.last_activated).seconds < 60 else f"{C.DIM}○{C.RESET}"
            
            print(f"  {status} {node.name:25} {cap_color}{cap_bar:20}{C.RESET} cap={node.capability:.2f}")
            print(f"     {C.DIM}├─ {node.purpose}{C.RESET}")
            print(f"     {C.DIM}├─ Knowledge: {node.knowledge_items} items | Success: {node.success_rate:.0%} | Speed: {node.processing_speed:.2f}x{C.RESET}")
            if node.specializations:
                print(f"     {C.DIM}├─ Specializations: {', '.join(node.specializations)}{C.RESET}")
            if node.connections:
                print(f"     {C.DIM}└─ Connects to: {', '.join(node.connections)}{C.RESET}")
            print()
        
        print(f"{C.MAGENTA}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")
    
    def _show_pathways(self):
        """Show pathway strengths - the TRUE learned architecture"""
        print(f"""
{C.YELLOW}╔═══════════════════════════════════════════════════════════════════╗
║  PATHWAY STRENGTHS - THE LEARNED ARCHITECTURE                     ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
""")
        
        # Sort pathways by strength
        sorted_pathways = sorted(self.pathway_weights.items(), key=lambda x: x[1], reverse=True)
        
        # Show strongest pathways
        print(f"  {C.GREEN}STRONGEST PATHWAYS (most developed):{C.RESET}")
        for (from_node, to_node), weight in sorted_pathways[:10]:
            bar_len = int(weight * 2)
            bar = '═' * min(bar_len, 15)
            color = C.GREEN if weight > 2.0 else C.CYAN if weight > 1.0 else C.DIM
            print(f"    {from_node:12} {color}{bar}▶{C.RESET} {to_node:12} ({weight:.2f})")
        
        print(f"\n  {C.RED}WEAKEST PATHWAYS (need development):{C.RESET}")
        for (from_node, to_node), weight in sorted_pathways[-5:]:
            bar_len = int(weight * 2)
            bar = '─' * max(bar_len, 1)
            print(f"    {from_node:12} {C.DIM}{bar}▸{C.RESET} {to_node:12} ({weight:.2f})")
        
        print(f"""
{C.YELLOW}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}
""")
    
    def _test_internet(self):
        """Test internet connectivity"""
        print(f"\n{C.CYAN}Testing internet connectivity...{C.RESET}")
        
        if self.check_internet():
            print(f"{C.GREEN}✓ Internet is available{C.RESET}")
            
            # Test web search
            print(f"{C.DIM}Testing DuckDuckGo search...{C.RESET}")
            result = self.search_web("python programming")
            if result["success"]:
                print(f"{C.GREEN}✓ Web search working ({result['count']} results){C.RESET}")
            else:
                print(f"{C.YELLOW}⚠ Web search failed: {result.get('error', 'unknown')}{C.RESET}")
            
            # Show capabilities
            print(f"\n{C.BOLD}Web Capabilities:{C.RESET}")
            print(f"  • requests library: {'✓' if HAS_REQUESTS else '✗'}")
            print(f"  • BeautifulSoup: {'✓' if HAS_BS4 else '✗'}")
        else:
            print(f"{C.RED}✗ No internet connection{C.RESET}")
        print()
    
    def _display_web_results(self, result: Dict):
        """Display web search results"""
        if result["success"]:
            print(f"""
{C.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║  WEB SEARCH RESULTS                                               ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
  Query: {result['query']}
  Results: {result['count']}
""")
            for i, r in enumerate(result["results"], 1):
                print(f"  {i}. {C.BOLD}{r['title']}{C.RESET}")
                if r['snippet']:
                    print(f"     {C.DIM}{r['snippet'][:100]}...{C.RESET}")
                if r['url']:
                    print(f"     {C.BLUE}{r['url']}{C.RESET}")
                print()
            
            print(f"{C.CYAN}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")
        else:
            print(f"{C.RED}Search failed: {result.get('error', 'unknown')}{C.RESET}")
    
    def _display_fetch_result(self, result: Dict):
        """Display webpage fetch result"""
        if result["success"]:
            print(f"""
{C.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║  WEBPAGE FETCHED                                                  ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
  URL: {result['url']}
  Title: {result['title']}
  Status: {result['status']}
{C.GREEN}├───────────────────────────────────────────────────────────────────┤{C.RESET}
""")
            # Show content preview
            content = result['content'][:1500]
            for line in content.split('\n')[:30]:
                if line.strip():
                    print(f"  {line[:70]}")
            
            print(f"\n{C.DIM}  ... (content truncated){C.RESET}")
            print(f"{C.GREEN}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")
        else:
            print(f"{C.RED}Fetch failed: {result.get('error', 'unknown')}{C.RESET}")
    
    def _show_sequence(self):
        """Show the last processing sequence"""
        print(f"""
{C.YELLOW}╔═══════════════════════════════════════════════════════════════════╗
║  LAST PROCESSING SEQUENCE                                         ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
""")
        
        if self.active_sequence:
            for i, node_id in enumerate(self.active_sequence):
                node = self.nodes.get(node_id)
                if node:
                    arrow = "→" if i < len(self.active_sequence) - 1 else "◆"
                    print(f"  {i+1}. {C.CYAN}[{node.name}]{C.RESET}")
                    print(f"     {C.DIM}{node.purpose}{C.RESET}")
                    if i < len(self.active_sequence) - 1:
                        print(f"        ↓")
        else:
            print(f"  {C.DIM}No sequence recorded yet{C.RESET}")
        
        print(f"{C.YELLOW}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")
    
    def _show_events(self):
        """Show recent learning events"""
        print(f"""
{C.GREEN}╔═══════════════════════════════════════════════════════════════════╗
║  RECENT LEARNING EVENTS                                           ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}
""")
        
        recent = self.learning_events[-10:]
        for event in recent:
            icon = {
                'knowledge_added': '📚',
                'node_created': '🔧',
                'connection_formed': '🔗',
                'pattern_discovered': '💡'
            }.get(event.event_type, '•')
            
            time_str = event.timestamp.strftime("%H:%M:%S")
            print(f"  {C.DIM}{time_str}{C.RESET} {icon} {event.description[:50]}")
        
        if not recent:
            print(f"  {C.DIM}No events yet - learning in progress...{C.RESET}")
        
        print(f"{C.GREEN}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")
    
    def _show_growth(self):
        """Show growth visualization"""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        
        # Calculate growth rate
        if elapsed > 0:
            knowledge_rate = self.total_knowledge_items / elapsed * 60  # per minute
            query_rate = self.total_queries_processed / elapsed * 60
        else:
            knowledge_rate = query_rate = 0
        
        print(f"""
{C.MAGENTA}╔═══════════════════════════════════════════════════════════════════╗
║  GROWTH VISUALIZATION                                             ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}

  {C.BOLD}Knowledge Growth:{C.RESET}
  
  Items: {self.total_knowledge_items}
  ┌────────────────────────────────────────────────────┐
  │{'█' * min(self.total_knowledge_items, 50)}{' ' * max(0, 50 - self.total_knowledge_items)}│
  └────────────────────────────────────────────────────┘
  Rate: {knowledge_rate:.1f} items/minute
  
  {C.BOLD}Node Activity:{C.RESET}
""")
        
        # Show node activity bars
        for node_id, node in sorted(self.nodes.items(), key=lambda x: -x[1].activation_count)[:5]:
            bar_len = min(node.activation_count, 30)
            print(f"  {node.name:20} [{C.CYAN}{'█' * bar_len}{' ' * (30 - bar_len)}{C.RESET}] {node.activation_count}")
        
        print(f"""
  {C.BOLD}Learning Progress:{C.RESET}
  
  Curriculum: {self.curriculum_index}/{len(self.learning_curriculum)}
  ┌────────────────────────────────────────────────────┐
  │{C.GREEN}{'█' * (self.curriculum_index * 50 // max(len(self.learning_curriculum), 1))}{C.RESET}{' ' * (50 - self.curriculum_index * 50 // max(len(self.learning_curriculum), 1))}│
  └────────────────────────────────────────────────────┘

{C.MAGENTA}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}
""")
    
    def stop(self):
        """Shutdown the system gracefully"""
        print(f"\n{C.YELLOW}Shutting down living system...{C.RESET}")
        
        self.is_alive = False
        
        # Save final state
        self._save_knowledge()
        
        elapsed = datetime.now() - self.session_start
        
        print(f"""
{C.RED}╔═══════════════════════════════════════════════════════════════════╗
║  SESSION SUMMARY                                                  ║
╠═══════════════════════════════════════════════════════════════════╣{C.RESET}

  Session duration:       {elapsed}
  Knowledge items:        {self.total_knowledge_items}
  Queries processed:      {self.total_queries_processed}
  New nodes created:      {self.nodes_created_this_session}
  Patterns discovered:    {self.patterns_discovered}
  Learning events:        {len(self.learning_events)}
  
  {C.GREEN}All knowledge has been persisted to disk.{C.RESET}
  {C.GREEN}The system will remember everything when restarted.{C.RESET}

{C.RED}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}
""")


def main():
    """Main entry point"""
    print(f"{C.BOLD}Initializing Living 4D System...{C.RESET}")
    
    system = Living4DSystem()
    system.start()


if __name__ == '__main__':
    main()
