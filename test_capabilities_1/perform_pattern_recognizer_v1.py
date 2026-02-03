import re
from typing import Union, Optional, List, Tuple
import operator

class ArithmeticPatternRecognizer:
    """
    A pattern recognition system for identifying and evaluating basic arithmetic operations.
    Recognizes patterns in mathematical expressions and performs calculations.
    """
    
    def __init__(self):
        """Initialize the arithmetic pattern recognizer with operation mappings."""
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '//': operator.floordiv,
            '%': operator.mod,
            '**': operator.pow
        }
        
        self.pattern = re.compile(r'(-?\d+(?:\.\d+)?)\s*([\+\-\*\/\%]{1,2}|\*\*)\s*(-?\d+(?:\.\d+)?)')
    
    def recognize_arithmetic_pattern(self, expression: str) -> Optional[Tuple[float, str, float]]:
        """
        Recognize arithmetic patterns in a given expression.
        
        Args:
            expression (str): Mathematical expression to analyze
            
        Returns:
            Optional[Tuple[float, str, float]]: Tuple of (operand1, operator, operand2) or None
        """
        try:
            expression = expression.strip()
            match = self.pattern.match(expression)
            
            if match:
                operand1 = float(match.group(1))
                operator_str = match.group(2)
                operand2 = float(match.group(3))
                return (operand1, operator_str, operand2)
            
            return None
        except (ValueError, AttributeError):
            return None
    
    def evaluate_pattern(self, pattern: Tuple[float, str, float]) -> Optional[float]:
        """
        Evaluate a recognized arithmetic pattern.
        
        Args:
            pattern (Tuple[float, str, float]): Tuple containing operands and operator
            
        Returns:
            Optional[float]: Result of the arithmetic operation or None if invalid
        """
        try:
            operand1, operator_str, operand2 = pattern
            
            if operator_str not in self.operators:
                return None
            
            if operator_str in ['/', '//'] and operand2 == 0:
                raise ZeroDivisionError("Division by zero")
            
            result = self.operators[operator_str](operand1, operand2)
            return result
        except (ZeroDivisionError, OverflowError, ValueError):
            return None
    
    def process_expression(self, expression: str) -> Optional[float]:
        """
        Complete pattern recognition and evaluation pipeline.
        
        Args:
            expression (str): Mathematical expression to process
            
        Returns:
            Optional[float]: Calculated result or None if pattern not recognized/invalid
        """
        try:
            pattern = self.recognize_arithmetic_pattern(expression)
            if pattern is None:
                return None
            
            return self.evaluate_pattern(pattern)
        except Exception:
            return None
    
    def recognize_multiple_patterns(self, expressions: List[str]) -> List[Optional[Tuple[float, str, float]]]:
        """
        Recognize arithmetic patterns in multiple expressions.
        
        Args:
            expressions (List[str]): List of mathematical expressions
            
        Returns:
            List[Optional[Tuple[float, str, float]]]: List of recognized patterns
        """
        return [self.recognize_arithmetic_pattern(expr) for expr in expressions]
    
    def batch_evaluate(self, expressions: List[str]) -> List[Optional[float]]:
        """
        Process multiple arithmetic expressions efficiently.
        
        Args:
            expressions (List[str]): List of mathematical expressions
            
        Returns:
            List[Optional[float]]: List of calculated results
        """
        return [self.process_expression(expr) for expr in expressions]
    
    def get_supported_operators(self) -> List[str]:
        """
        Get list of supported arithmetic operators.
        
        Returns:
            List[str]: List of supported operators
        """
        return list(self.operators.keys())
    
    def is_valid_pattern(self, expression: str) -> bool:
        """
        Check if an expression contains a valid arithmetic pattern.
        
        Args:
            expression (str): Expression to validate
            
        Returns:
            bool: True if valid pattern is found, False otherwise
        """
        return self.recognize_arithmetic_pattern(expression) is not None