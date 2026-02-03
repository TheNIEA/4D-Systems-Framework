import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
import logging

class AnalyzePatternRecognizer:
    """
    A pattern recognition class for analyzing text sentiment patterns.
    
    This class identifies and analyzes sentiment patterns in text data,
    providing capabilities to recognize emotional indicators, sentiment
    strength, and pattern classification.
    """
    
    def __init__(self):
        """Initialize the pattern recognizer with default sentiment patterns."""
        self.positive_patterns = {
            r'\b(?:excellent|amazing|fantastic|wonderful|great|good|love|like)\b': 2,
            r'\b(?:nice|decent|okay|fine|pleasant)\b': 1,
            r'[!]{1,3}': 1,
            r'[:]{1}[)]{1}|[;]{1}[)]{1}': 1,
            r'\b(?:yes|yeah|absolutely|definitely)\b': 1
        }
        
        self.negative_patterns = {
            r'\b(?:terrible|awful|horrible|hate|disgusting|worst)\b': -2,
            r'\b(?:bad|poor|disappointing|annoying|sad)\b': -1,
            r'\b(?:no|not|never|nothing|none)\b': -1,
            r'[:]{1}[(]{1}|[;]{1}[(]{1}': -1,
            r'[?]{2,}': -1
        }
        
        self.neutral_patterns = {
            r'\b(?:maybe|perhaps|possibly|might|could)\b': 0,
            r'\b(?:information|data|fact|report)\b': 0
        }
        
        self.logger = logging.getLogger(__name__)
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment patterns in the given text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            Dict[str, any]: Analysis results containing sentiment score, 
                           classification, and pattern matches
            
        Raises:
            ValueError: If text is empty or None
            TypeError: If text is not a string
        """
        try:
            if not isinstance(text, str):
                raise TypeError("Text must be a string")
            if not text.strip():
                raise ValueError("Text cannot be empty")
            
            text_lower = text.lower()
            
            positive_score = self._calculate_pattern_score(text_lower, self.positive_patterns)
            negative_score = self._calculate_pattern_score(text_lower, self.negative_patterns)
            neutral_score = self._calculate_pattern_score(text_lower, self.neutral_patterns)
            
            total_score = positive_score + negative_score + neutral_score
            
            classification = self._classify_sentiment(total_score)
            confidence = self._calculate_confidence(positive_score, negative_score, neutral_score)
            
            return {
                'sentiment_score': total_score,
                'classification': classification,
                'confidence': confidence,
                'positive_score': positive_score,
                'negative_score': negative_score,
                'neutral_score': neutral_score,
                'pattern_matches': self._get_pattern_matches(text_lower)
            }
            
        except (ValueError, TypeError) as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in sentiment analysis: {e}")
            return self._default_analysis_result()
    
    def batch_analyze(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Analyze sentiment patterns for multiple texts.
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            List[Dict[str, any]]: List of analysis results
            
        Raises:
            TypeError: If texts is not a list
        """
        try:
            if not isinstance(texts, list):
                raise TypeError("Texts must be a list")
            
            results = []
            for i, text in enumerate(texts):
                try:
                    result = self.analyze_sentiment(text)
                    result['index'] = i
                    results.append(result)
                except Exception as e:
                    self.logger.warning(f"Failed to analyze text at index {i}: {e}")
                    results.append(self._default_analysis_result(index=i))
            
            return results
            
        except TypeError as e:
            self.logger.error(f"Error in batch analysis: {e}")
            raise
    
    def add_pattern(self, pattern: str, score: int, category: str = 'positive') -> None:
        """
        Add a new sentiment pattern.
        
        Args:
            pattern (str): Regular expression pattern
            score (int): Sentiment score for the pattern
            category (str): Pattern category ('positive', 'negative', 'neutral')
            
        Raises:
            ValueError: If pattern is invalid or category is unknown
            re.error: If pattern is not a valid regex
        """
        try:
            re.compile(pattern)  # Validate regex
            
            if category == 'positive':
                self.positive_patterns[pattern] = abs(score)
            elif category == 'negative':
                self.negative_patterns[pattern] = -abs(score)
            elif category == 'neutral':
                self.neutral_patterns[pattern] = 0
            else:
                raise ValueError(f"Unknown category: {category}")
                
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
    
    def get_pattern_statistics(self, texts: List[str]) -> Dict[str, any]:
        """
        Get statistics about pattern usage across multiple texts.
        
        Args:
            texts (List[str]): List of texts to analyze
            
        Returns:
            Dict[str, any]: Pattern usage statistics
        """
        try:
            if not isinstance(texts, list):
                raise TypeError("Texts must be a list")
            
            all_matches = []
            sentiment_distribution = Counter()
            
            for text in texts:
                if isinstance(text, str) and text.strip():
                    analysis = self.analyze_sentiment(text)
                    all_matches.extend(analysis['pattern_matches'])
                    sentiment_distribution[analysis['classification']] += 1
            
            pattern_frequency = Counter(match['pattern'] for match in all_matches)
            
            return {
                'total_texts': len(texts),
                'sentiment_distribution': dict(sentiment_distribution),
                'most_common_patterns': pattern_frequency.most_common(10),
                'total_pattern_matches': len(all_matches)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating pattern statistics: {e}")
            return {'error': str(e)}
    
    def _calculate_pattern_score(self, text: str, patterns: Dict[str, int]) -> int:
        """Calculate total score for a set of patterns in text."""
        score = 0
        for pattern, weight in patterns.items():
            matches = re.findall(pattern, text)
            score += len(matches) * weight
        return score
    
    def _classify_sentiment(self, score: int) -> str:
        """Classify sentiment based on total score."""
        if score > 1:
            return 'positive'
        elif score < -1:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_confidence(self, pos_score: int, neg_score: int, neu_score: int) -> float:
        """Calculate confidence level of sentiment classification."""
        total_abs_score = abs(pos_score) + abs(neg_score) + abs(neu_score)
        if total_abs_score == 0:
            return 0.0
        
        max_score = max(abs(pos_score), abs(neg_score), abs(neu_score))
        return round(max_score / total_abs_score, 3)
    
    def _get_pattern_matches(self, text: str) -> List[Dict[str, any]]:
        """Get all pattern matches found in text."""
        matches = []
        
        all_patterns = {
            **self.positive_patterns,
            **self.negative_patterns,
            **self.neutral_patterns
        }
        
        for pattern, score in all_patterns.items():
            found_matches = re.finditer(pattern, text)
            for match in found_matches:
                matches.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'position': match.span(),
                    'score': score
                })
        
        return matches
    
    def _default_analysis_result(self, index: Optional[int] = None) -> Dict[str, any]:
        """Return default analysis result for error cases."""
        result = {
            'sentiment_score': 0,
            'classification': 'neutral',
            'confidence': 0.0,
            'positive_score': 0,
            'negative_score': 0,
            'neutral_score': 0,
            'pattern_matches': [],
            'error': True
        }
        
        if index is not None:
            result['index'] = index
            
        return result