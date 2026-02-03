"""
Base Capability Interface - Standardized contract for all capabilities

All synthesized capabilities must inherit from BaseCapability to ensure:
1. Consistent .process() interface
2. Execution validation
3. Type safety
4. Self-documentation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import json


@dataclass
class CapabilityResult:
    """Standardized result from capability execution"""
    success: bool
    output: Any
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "success": self.success,
            "output": self.output if isinstance(self.output, (str, int, float, list, dict)) else str(self.output),
            "confidence": self.confidence,
            "metadata": self.metadata,
            "error": self.error
        }


class BaseCapability(ABC):
    """
    Abstract base class for all capabilities.
    
    Every capability MUST implement:
    - process(data): Takes input, returns CapabilityResult
    - get_description(): Returns what this capability does
    
    Optional to override:
    - validate_input(data): Check if input is valid
    - get_input_types(): List of accepted input types
    """
    
    def __init__(self):
        """Initialize capability"""
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        
    @abstractmethod
    def process(self, data: Any) -> CapabilityResult:
        """
        Core processing method - MUST be implemented.
        
        Args:
            data: Input data (can be any type - str, list, dict, np.array, etc.)
            
        Returns:
            CapabilityResult with success status, output, and confidence
            
        Raises:
            Should NOT raise - catch exceptions and return CapabilityResult with success=False
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Return human-readable description of what this capability does.
        
        Example: "Detects patterns in numerical sequences"
        """
        pass
    
    def validate_input(self, data: Any) -> bool:
        """
        Validate input before processing. Override if needed.
        
        Args:
            data: Input to validate
            
        Returns:
            True if valid, False otherwise
        """
        return data is not None
    
    def get_input_types(self) -> List[str]:
        """
        List of accepted input types. Override if needed.
        
        Returns:
            List like ["str", "list", "dict"]
        """
        return ["any"]
    
    def execute(self, data: Any) -> CapabilityResult:
        """
        Wrapper around process() that adds tracking and validation.
        Use this instead of calling process() directly.
        """
        self.execution_count += 1
        
        # Validate input
        if not self.validate_input(data):
            self.failure_count += 1
            return CapabilityResult(
                success=False,
                output=None,
                confidence=0.0,
                metadata={"error_type": "validation_failed"},
                error=f"Input validation failed. Expected types: {self.get_input_types()}"
            )
        
        # Execute
        try:
            result = self.process(data)
            
            if result.success:
                self.success_count += 1
            else:
                self.failure_count += 1
                
            return result
            
        except Exception as e:
            self.failure_count += 1
            return CapabilityResult(
                success=False,
                output=None,
                confidence=0.0,
                metadata={"error_type": "exception", "exception_class": type(e).__name__},
                error=f"Execution failed: {str(e)}"
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            "executions": self.execution_count,
            "successes": self.success_count,
            "failures": self.failure_count,
            "success_rate": self.success_count / self.execution_count if self.execution_count > 0 else 0.0
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(executions={self.execution_count}, success_rate={self.get_stats()['success_rate']:.1%})"


class PatternRecognizerCapability(BaseCapability):
    """
    Base class for pattern recognition capabilities.
    Provides common utilities for detecting patterns.
    """
    
    def detect_sequence_pattern(self, data: List) -> Optional[str]:
        """Detect common sequence patterns (Fibonacci, arithmetic, geometric, etc.)"""
        if not isinstance(data, list) or len(data) < 3:
            return None
        
        # Check Fibonacci
        is_fib = True
        for i in range(2, len(data)):
            if data[i] != data[i-1] + data[i-2]:
                is_fib = False
                break
        if is_fib:
            return "fibonacci"
        
        # Check arithmetic progression
        if len(data) >= 2:
            diff = data[1] - data[0]
            is_arithmetic = all(data[i] - data[i-1] == diff for i in range(1, len(data)))
            if is_arithmetic:
                return f"arithmetic(+{diff})"
        
        # Check geometric progression
        if len(data) >= 2 and data[0] != 0:
            ratio = data[1] / data[0]
            is_geometric = all(abs(data[i] / data[i-1] - ratio) < 0.001 for i in range(1, len(data)) if data[i-1] != 0)
            if is_geometric:
                return f"geometric(*{ratio:.2f})"
        
        return None


class AnalyzerCapability(BaseCapability):
    """
    Base class for analysis capabilities.
    Provides common analysis utilities.
    """
    
    def analyze_statistics(self, data: List) -> Dict[str, float]:
        """Common statistical analysis"""
        import numpy as np
        arr = np.array(data)
        return {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "median": float(np.median(arr))
        }
    
    def detect_anomalies(self, data: List, threshold: float = 2.0) -> List[int]:
        """Detect statistical anomalies (values > threshold std devs from mean)"""
        import numpy as np
        arr = np.array(data)
        mean = np.mean(arr)
        std = np.std(arr)
        
        anomalies = []
        for i, val in enumerate(arr):
            if abs(val - mean) > threshold * std:
                anomalies.append(i)
        return anomalies


class StructureBuilderCapability(BaseCapability):
    """
    Base class for structure building capabilities.
    Provides common structure manipulation utilities.
    """
    
    def build_hierarchy(self, data: List) -> Dict:
        """Build hierarchical structure from flat data"""
        # Default implementation - can be overridden
        return {
            "root": {
                "children": data,
                "count": len(data)
            }
        }
