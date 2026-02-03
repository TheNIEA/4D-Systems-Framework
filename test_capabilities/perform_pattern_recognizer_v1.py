import re
from typing import List, Dict, Optional, Union
from dataclasses import dataclass

@dataclass
class ArithmeticPattern:
    pattern: str
    operation: str
    priority: int

class PerformPatternRecognizer:
    """
    Pattern recognition class for identifying and parsing basic arithmetic operations
    from text input and converting them to executable expressions.
    """
    
    def __init__(self):
        """Initialize the pattern recognizer with predefined arithmetic patterns."""
        self.patterns = [
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',
                'addition',
                1
            ),
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)',
                'subtraction',
                1
            ),
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',
                'multiplication',
                2
            ),
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)',
                'division',
                2
            ),
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*\*\*\s*(\d+(?:\.\d+)?)',
                'exponentiation',
                3
            ),
            ArithmeticPattern(
                r'(\d+(?:\.\d+)?)\s*%\s*(\d+(?:\.\d+)?)',
                'modulo',
                2
            )
        ]
        
        self.operation_map = {
            'addition': lambda x, y: x + y,
            'subtraction': lambda x, y: x - y,
            'multiplication': lambda x, y: x * y,
            'division': lambda x, y: x / y if y != 0 else None,
            'exponentiation': lambda x, y: x ** y,
            'modulo': lambda x, y: x % y if y != 0 else None
        }

    def recognize_patterns(self, text: str) -> List[Dict[str, Union[str, float, int]]]:
        """
        Recognize arithmetic patterns in the given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            List[Dict]: List of recognized patterns with details
            
        Raises:
            TypeError: If input is not a string
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        recognized = []
        
        try:
            for pattern in self.patterns:
                matches = re.finditer(pattern.pattern, text)
                for match in matches:
                    operand1 = self._parse_number(match.group(1))
                    operand2 = self._parse_number(match.group(2))
                    
                    if operand1 is not None and operand2 is not None:
                        recognized.append({
                            'operation': pattern.operation,
                            'operand1': operand1,
                            'operand2': operand2,
                            'expression': match.group(0),
                            'priority': pattern.priority,
                            'start_pos': match.start(),
                            'end_pos': match.end()
                        })
        except Exception as e:
            raise RuntimeError(f"Pattern recognition failed: {str(e)}")
        
        return sorted(recognized, key=lambda x: (x['start_pos'], -x['priority']))

    def evaluate_pattern(self, pattern_dict: Dict[str, Union[str, float, int]]) -> Optional[float]:
        """
        Evaluate a recognized arithmetic pattern.
        
        Args:
            pattern_dict (Dict): Pattern dictionary from recognize_patterns
            
        Returns:
            Optional[float]: Result of the arithmetic operation or None if invalid
            
        Raises:
            KeyError: If pattern dictionary is missing required keys
            TypeError: If operands are not numeric
        """
        try:
            required_keys = ['operation', 'operand1', 'operand2']
            if not all(key in pattern_dict for key in required_keys):
                raise KeyError(f"Pattern dictionary must contain keys: {required_keys}")
            
            operation = pattern_dict['operation']
            operand1 = pattern_dict['operand1']
            operand2 = pattern_dict['operand2']
            
            if not isinstance(operand1, (int, float)) or not isinstance(operand2, (int, float)):
                raise TypeError("Operands must be numeric")
            
            if operation not in self.operation_map:
                return None
            
            result = self.operation_map[operation](operand1, operand2)
            return result
            
        except ZeroDivisionError:
            return None
        except Exception as e:
            raise RuntimeError(f"Evaluation failed: {str(e)}")

    def process_text(self, text: str) -> List[Dict[str, Union[str, float, int]]]:
        """
        Process text to recognize and evaluate all arithmetic patterns.
        
        Args:
            text (str): Input text to process
            
        Returns:
            List[Dict]: List of patterns with their results
        """
        try:
            patterns = self.recognize_patterns(text)
            
            for pattern in patterns:
                result = self.evaluate_pattern(pattern)
                pattern['result'] = result
                pattern['valid'] = result is not None
                
            return patterns
            
        except Exception as e:
            raise RuntimeError(f"Text processing failed: {str(e)}")

    def extract_valid_operations(self, text: str) -> List[str]:
        """
        Extract only valid arithmetic operations that can be evaluated.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            List[str]: List of valid arithmetic expressions
        """
        try:
            patterns = self.process_text(text)
            return [p['expression'] for p in patterns if p['valid']]
        except Exception:
            return []

    def get_operation_summary(self, text: str) -> Dict[str, int]:
        """
        Get a summary count of different operation types found in text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict[str, int]: Count of each operation type
        """
        try:
            patterns = self.recognize_patterns(text)
            summary = {}
            
            for pattern in patterns:
                op_type = pattern['operation']
                summary[op_type] = summary.get(op_type, 0) + 1
                
            return summary
            
        except Exception:
            return {}

    def _parse_number(self, num_str: str) -> Optional[Union[int, float]]:
        """
        Parse a string to number, handling both integers and floats.
        
        Args:
            num_str (str): String representation of a number
            
        Returns:
            Optional[Union[int, float]]: Parsed number or None if invalid
        """
        try:
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except (ValueError, TypeError):
            return None