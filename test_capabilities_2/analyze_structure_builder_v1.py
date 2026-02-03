import re
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

class SentimentLabel(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

@dataclass
class SentimentResult:
    label: SentimentLabel
    confidence: float
    score: float
    text: str

class AnalyzeStructureBuilder:
    """Build strong pathways for analyzing text sentiment through structured processing."""
    
    def __init__(self):
        """Initialize the sentiment analysis structure builder."""
        self._positive_words = {
            'excellent', 'amazing', 'wonderful', 'great', 'fantastic', 'love', 
            'perfect', 'outstanding', 'brilliant', 'awesome', 'good', 'beautiful',
            'happy', 'pleased', 'satisfied', 'delighted', 'thrilled', 'joy'
        }
        self._negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'disgusting',
            'disappointing', 'poor', 'unacceptable', 'annoying', 'frustrated',
            'angry', 'sad', 'upset', 'disappointed', 'furious', 'miserable'
        }
        self._intensifiers = {
            'very': 1.5, 'extremely': 2.0, 'incredibly': 2.0, 'absolutely': 1.8,
            'really': 1.3, 'quite': 1.2, 'rather': 1.1, 'totally': 1.7
        }
        self._negations = {'not', 'no', 'never', 'none', 'nobody', 'nothing', "don't", "won't", "can't"}
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by cleaning and tokenizing.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            List of cleaned tokens
            
        Raises:
            ValueError: If text is empty or invalid
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")
        
        try:
            # Convert to lowercase and remove punctuation except apostrophes
            cleaned = re.sub(r"[^\w\s']", " ", text.lower())
            # Split and filter empty strings
            tokens = [token for token in cleaned.split() if token]
            return tokens
        except Exception as e:
            raise ValueError(f"Error preprocessing text: {str(e)}")
    
    def extract_sentiment_features(self, tokens: List[str]) -> Dict[str, Union[int, float]]:
        """
        Extract sentiment features from tokenized text.
        
        Args:
            tokens: List of preprocessed tokens
            
        Returns:
            Dictionary containing sentiment features
        """
        if not tokens:
            return {'positive_score': 0.0, 'negative_score': 0.0, 'intensity_multiplier': 1.0}
        
        try:
            positive_score = 0.0
            negative_score = 0.0
            intensity_multiplier = 1.0
            negation_active = False
            
            for i, token in enumerate(tokens):
                # Check for intensifiers
                if token in self._intensifiers:
                    if i + 1 < len(tokens):  # Apply to next word
                        intensity_multiplier = self._intensifiers[token]
                    continue
                
                # Check for negations
                if token in self._negations:
                    negation_active = True
                    continue
                
                # Calculate sentiment scores
                base_score = intensity_multiplier
                
                if token in self._positive_words:
                    score = base_score if not negation_active else -base_score
                    positive_score += max(0, score)
                    negative_score += max(0, -score)
                elif token in self._negative_words:
                    score = -base_score if not negation_active else base_score
                    positive_score += max(0, score)
                    negative_score += max(0, -score)
                
                # Reset modifiers after processing a sentiment word
                if token in self._positive_words or token in self._negative_words:
                    intensity_multiplier = 1.0
                    negation_active = False
            
            return {
                'positive_score': positive_score,
                'negative_score': negative_score,
                'total_tokens': len(tokens)
            }
        except Exception as e:
            raise RuntimeError(f"Error extracting sentiment features: {str(e)}")
    
    def calculate_sentiment_score(self, features: Dict[str, Union[int, float]]) -> Tuple[float, float]:
        """
        Calculate normalized sentiment score and confidence.
        
        Args:
            features: Dictionary of sentiment features
            
        Returns:
            Tuple of (sentiment_score, confidence)
        """
        try:
            pos_score = features.get('positive_score', 0.0)
            neg_score = features.get('negative_score', 0.0)
            total_tokens = features.get('total_tokens', 1)
            
            # Calculate net sentiment score
            net_score = pos_score - neg_score
            
            # Normalize by text length
            normalized_score = net_score / max(total_tokens, 1)
            
            # Calculate confidence based on absolute score magnitude
            total_sentiment = pos_score + neg_score
            confidence = min(total_sentiment / max(total_tokens, 1), 1.0)
            
            # Bound sentiment score between -1 and 1
            bounded_score = max(-1.0, min(1.0, normalized_score))
            
            return bounded_score, confidence
        except Exception as e:
            raise RuntimeError(f"Error calculating sentiment score: {str(e)}")
    
    def determine_sentiment_label(self, score: float, confidence: float, 
                                threshold: float = 0.1) -> SentimentLabel:
        """
        Determine sentiment label based on score and confidence.
        
        Args:
            score: Sentiment score between -1 and 1
            confidence: Confidence level
            threshold: Minimum threshold for positive/negative classification
            
        Returns:
            SentimentLabel enum value
        """
        try:
            if confidence < 0.1:  # Low confidence defaults to neutral
                return SentimentLabel.NEUTRAL
            
            if score > threshold:
                return SentimentLabel.POSITIVE
            elif score < -threshold:
                return SentimentLabel.NEGATIVE
            else:
                return SentimentLabel.NEUTRAL
        except Exception as e:
            raise RuntimeError(f"Error determining sentiment label: {str(e)}")
    
    def build_sentiment_pathway(self, text: str, threshold: float = 0.1) -> SentimentResult:
        """
        Build complete sentiment analysis pathway for input text.
        
        Args:
            text: Input text to analyze
            threshold: Classification threshold for sentiment labels
            
        Returns:
            SentimentResult object with analysis results
            
        Raises:
            ValueError: If input text is invalid
            RuntimeError: If analysis fails
        """
        try:
            # Step 1: Preprocess text
            tokens = self.preprocess_text(text)
            
            # Step 2: Extract features
            features = self.extract_sentiment_features(tokens)
            
            # Step 3: Calculate scores
            score, confidence = self.calculate_sentiment_score(features)
            
            # Step 4: Determine label
            label = self.determine_sentiment_label(score, confidence, threshold)
            
            return SentimentResult(
                label=label,
                confidence=confidence,
                score=score,
                text=text.strip()
            )
        except (ValueError, RuntimeError):
            raise
        except Exception as e:
            raise RuntimeError(f"Unexpected error in sentiment analysis: {str(e)}")
    
    def batch_analyze(self, texts: List[str], threshold: float = 0.1) -> List[Optional[SentimentResult]]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze
            threshold: Classification threshold
            
        Returns:
            List of SentimentResult objects (None for failed analyses)
        """
        if not isinstance(texts, list):
            raise ValueError("Texts must be provided as a list")
        
        results = []
        for text in texts:
            try:
                result = self.build_sentiment_pathway(text, threshold)
                results.append(result)
            except Exception:
                results.append(None)
        
        return results
    
    def get_sentiment_statistics(self, results: List[SentimentResult]) -> Dict[str, Union[int, float]]:
        """
        Calculate statistics from multiple sentiment analysis results.
        
        Args:
            results: List of SentimentResult objects
            
        Returns:
            Dictionary containing sentiment statistics
        """
        if not results:
            return {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0, 'avg_confidence': 0.0}
        
        try:
            valid_results = [r for r in results if r is not None]
            
            stats = {
                'total': len(valid_results),
                'positive': sum(1 for r in valid_results if r.label == SentimentLabel.POSITIVE),
                'negative': sum(1 for r in valid_results if r.label == SentimentLabel.NEGATIVE),
                'neutral': sum(1 for r in valid_results if r.label == SentimentLabel.NEUTRAL),
                'avg_confidence': sum(r.confidence for r in valid_results) / len(valid_results) if valid_results else 0.0,
                'avg_score': sum(r.score for r in valid_results) / len(valid_results) if valid_results else 0.0
            }
            
            return stats
        except Exception as e:
            raise RuntimeError(f"Error calculating statistics: {str(e)}")