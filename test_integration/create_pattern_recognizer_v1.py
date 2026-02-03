import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class GreetingPatternRecognizer:
    """
    A pattern recognition system for identifying and categorizing greeting patterns.
    
    This class provides functionality to recognize various greeting patterns,
    classify their types, and generate appropriate responses.
    """
    
    def __init__(self):
        """Initialize the greeting pattern recognizer with predefined patterns."""
        self.greeting_patterns = {
            'formal': [
                r'\b(good morning|good afternoon|good evening)\b',
                r'\b(hello|greetings)\b',
                r'\bhow do you do\b'
            ],
            'casual': [
                r'\b(hi|hey|sup|yo)\b',
                r'\bwhat\'s up\b',
                r'\bhowdy\b'
            ],
            'time_based': [
                r'\b(morning|afternoon|evening)\b',
                r'\bgood (morning|afternoon|evening|night)\b'
            ],
            'question': [
                r'\bhow are you\b',
                r'\bhow\'s it going\b',
                r'\bhow have you been\b'
            ]
        }
        
        self.response_templates = {
            'formal': [
                "Good {time_of_day}! How may I assist you?",
                "Hello! It's a pleasure to meet you.",
                "Greetings! How are you doing today?"
            ],
            'casual': [
                "Hey there! What's up?",
                "Hi! How's it going?",
                "Hey! Nice to see you!"
            ],
            'time_based': [
                "Good {time_of_day}! Hope you're having a great day!",
                "Hello! Lovely {time_of_day}, isn't it?"
            ],
            'question': [
                "I'm doing well, thank you! How about you?",
                "Great, thanks for asking! How are things with you?",
                "I'm fine, thank you! What brings you here today?"
            ]
        }
        
        self._compile_patterns()
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for better performance."""
        try:
            self.compiled_patterns = {}
            for category, patterns in self.greeting_patterns.items():
                self.compiled_patterns[category] = [
                    re.compile(pattern, re.IGNORECASE) for pattern in patterns
                ]
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    
    def recognize_greeting(self, text: str) -> Dict[str, any]:
        """
        Recognize greeting patterns in the input text.
        
        Args:
            text (str): The input text to analyze
            
        Returns:
            Dict: Recognition results containing pattern type, confidence, and matches
            
        Raises:
            TypeError: If input is not a string
            ValueError: If input text is empty
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        if not text.strip():
            raise ValueError("Input text cannot be empty")
        
        try:
            results = {
                'recognized': False,
                'patterns': [],
                'primary_type': None,
                'confidence': 0.0,
                'matches': []
            }
            
            pattern_scores = {}
            all_matches = []
            
            for category, compiled_patterns in self.compiled_patterns.items():
                category_matches = []
                for pattern in compiled_patterns:
                    matches = pattern.findall(text.lower())
                    if matches:
                        category_matches.extend(matches)
                        all_matches.extend([(match, category) for match in matches])
                
                if category_matches:
                    pattern_scores[category] = len(category_matches)
            
            if pattern_scores:
                results['recognized'] = True
                results['patterns'] = list(pattern_scores.keys())
                results['primary_type'] = max(pattern_scores, key=pattern_scores.get)
                results['confidence'] = min(sum(pattern_scores.values()) / len(text.split()) * 2, 1.0)
                results['matches'] = all_matches
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Error during pattern recognition: {e}")
    
    def generate_response(self, recognition_result: Dict[str, any]) -> Optional[str]:
        """
        Generate an appropriate response based on recognition results.
        
        Args:
            recognition_result (Dict): Results from recognize_greeting method
            
        Returns:
            Optional[str]: Generated response or None if no pattern recognized
            
        Raises:
            TypeError: If input is not a dictionary
        """
        if not isinstance(recognition_result, dict):
            raise TypeError("Recognition result must be a dictionary")
        
        try:
            if not recognition_result.get('recognized', False):
                return None
            
            primary_type = recognition_result.get('primary_type')
            if not primary_type or primary_type not in self.response_templates:
                return "Hello! How can I help you today?"
            
            templates = self.response_templates[primary_type]
            template = templates[hash(str(recognition_result.get('matches', []))) % len(templates)]
            
            # Format with current time of day
            current_hour = datetime.now().hour
            if current_hour < 12:
                time_of_day = "morning"
            elif current_hour < 17:
                time_of_day = "afternoon"
            else:
                time_of_day = "evening"
            
            return template.format(time_of_day=time_of_day)
            
        except Exception as e:
            return "Hello! How can I help you today?"
    
    def analyze_greeting_patterns(self, text_list: List[str]) -> Dict[str, any]:
        """
        Analyze greeting patterns across multiple text samples.
        
        Args:
            text_list (List[str]): List of text samples to analyze
            
        Returns:
            Dict: Analysis results with pattern statistics
            
        Raises:
            TypeError: If input is not a list
            ValueError: If list is empty
        """
        if not isinstance(text_list, list):
            raise TypeError("Input must be a list of strings")
        
        if not text_list:
            raise ValueError("Input list cannot be empty")
        
        try:
            analysis = {
                'total_samples': len(text_list),
                'recognized_greetings': 0,
                'pattern_frequency': {},
                'average_confidence': 0.0,
                'most_common_pattern': None
            }
            
            total_confidence = 0.0
            pattern_counts = {}
            
            for text in text_list:
                if isinstance(text, str) and text.strip():
                    result = self.recognize_greeting(text)
                    if result['recognized']:
                        analysis['recognized_greetings'] += 1
                        total_confidence += result['confidence']
                        
                        primary_type = result['primary_type']
                        pattern_counts[primary_type] = pattern_counts.get(primary_type, 0) + 1
            
            if analysis['recognized_greetings'] > 0:
                analysis['average_confidence'] = total_confidence / analysis['recognized_greetings']
                analysis['pattern_frequency'] = {
                    pattern: count / analysis['recognized_greetings'] 
                    for pattern, count in pattern_counts.items()
                }
                analysis['most_common_pattern'] = max(pattern_counts, key=pattern_counts.get)
            
            return analysis
            
        except Exception as e:
            raise RuntimeError(f"Error during pattern analysis: {e}")
    
    def add_custom_pattern(self, category: str, pattern: str) -> bool:
        """
        Add a custom greeting pattern to an existing or new category.
        
        Args:
            category (str): Pattern category name
            pattern (str): Regex pattern string
            
        Returns:
            bool: True if pattern was added successfully
            
        Raises:
            TypeError: If inputs are not strings
            ValueError: If pattern is invalid regex
        """
        if not isinstance(category, str) or not isinstance(pattern, str):
            raise TypeError("Category and pattern must be strings")
        
        if not category.strip() or not pattern.strip():
            raise ValueError("Category and pattern cannot be empty")
        
        try:
            # Validate regex pattern
            re.compile(pattern, re.IGNORECASE)
            
            if category not in self.greeting_patterns:
                self.greeting_patterns[category] = []
                self.response_templates[category] = ["Hello! How can I help you?"]
            
            self.greeting_patterns[category].append(pattern)
            self._compile_patterns()
            
            return True
            
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        except Exception as e:
            raise RuntimeError(f"Error adding custom pattern: {e}")