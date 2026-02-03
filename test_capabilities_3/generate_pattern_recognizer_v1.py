import re
import json
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class Pattern:
    """Represents a recognized pattern with metadata."""
    pattern_type: str
    confidence: float
    data: Dict[str, Any]
    examples: List[str]


class GenerativePatternRecognizer:
    """
    A pattern recognition system for analyzing and identifying patterns
    in creative text generation to improve response quality and consistency.
    """
    
    def __init__(self, min_confidence: float = 0.7):
        """
        Initialize the pattern recognizer.
        
        Args:
            min_confidence: Minimum confidence threshold for pattern recognition
        """
        self.min_confidence = min_confidence
        self.patterns = {}
        self.training_data = []
        self._compiled_regexes = {}
        self._pattern_frequencies = Counter()
        
    def add_training_data(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add training data for pattern recognition.
        
        Args:
            text: Input text for pattern analysis
            metadata: Optional metadata about the text
        """
        try:
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Text must be a non-empty string")
                
            self.training_data.append({
                'text': text.strip(),
                'metadata': metadata or {},
                'length': len(text),
                'word_count': len(text.split())
            })
        except Exception as e:
            raise RuntimeError(f"Failed to add training data: {str(e)}")
    
    def recognize_structural_patterns(self, text: str) -> List[Pattern]:
        """
        Recognize structural patterns in text (paragraphs, lists, formatting).
        
        Args:
            text: Text to analyze
            
        Returns:
            List of recognized structural patterns
        """
        patterns = []
        
        try:
            # Paragraph structure
            paragraphs = text.split('\n\n')
            if len(paragraphs) > 1:
                avg_length = sum(len(p) for p in paragraphs) / len(paragraphs)
                patterns.append(Pattern(
                    pattern_type="multi_paragraph",
                    confidence=0.9,
                    data={"paragraph_count": len(paragraphs), "avg_length": avg_length},
                    examples=paragraphs[:3]
                ))
            
            # List patterns
            list_items = re.findall(r'^[-*•]\s+(.+)$', text, re.MULTILINE)
            if list_items:
                patterns.append(Pattern(
                    pattern_type="bulleted_list",
                    confidence=0.85,
                    data={"item_count": len(list_items)},
                    examples=list_items[:5]
                ))
            
            # Numbered lists
            numbered_items = re.findall(r'^\d+\.\s+(.+)$', text, re.MULTILINE)
            if numbered_items:
                patterns.append(Pattern(
                    pattern_type="numbered_list",
                    confidence=0.85,
                    data={"item_count": len(numbered_items)},
                    examples=numbered_items[:5]
                ))
                
            return patterns
            
        except Exception as e:
            raise RuntimeError(f"Structural pattern recognition failed: {str(e)}")
    
    def recognize_linguistic_patterns(self, text: str) -> List[Pattern]:
        """
        Recognize linguistic patterns (repetition, style, tone).
        
        Args:
            text: Text to analyze
            
        Returns:
            List of recognized linguistic patterns
        """
        patterns = []
        
        try:
            words = text.lower().split()
            word_freq = Counter(words)
            
            # Repetitive word usage
            repeated_words = {word: count for word, count in word_freq.items() 
                            if count > 2 and len(word) > 3}
            if repeated_words:
                confidence = min(0.9, len(repeated_words) / len(set(words)))
                patterns.append(Pattern(
                    pattern_type="word_repetition",
                    confidence=confidence,
                    data={"repeated_words": repeated_words},
                    examples=list(repeated_words.keys())[:5]
                ))
            
            # Question patterns
            questions = re.findall(r'[^.!?]*\?', text)
            if questions:
                patterns.append(Pattern(
                    pattern_type="interrogative",
                    confidence=0.8,
                    data={"question_count": len(questions)},
                    examples=questions[:3]
                ))
            
            # Sentence length consistency
            sentences = re.split(r'[.!?]+', text)
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if sentence_lengths:
                avg_length = sum(sentence_lengths) / len(sentence_lengths)
                variance = sum((x - avg_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
                
                if variance < 10:  # Low variance indicates consistent length
                    patterns.append(Pattern(
                        pattern_type="consistent_sentence_length",
                        confidence=0.75,
                        data={"avg_length": avg_length, "variance": variance},
                        examples=sentences[:3]
                    ))
                    
            return patterns
            
        except Exception as e:
            raise RuntimeError(f"Linguistic pattern recognition failed: {str(e)}")
    
    def recognize_creative_patterns(self, text: str) -> List[Pattern]:
        """
        Recognize creative patterns (metaphors, alliteration, rhythm).
        
        Args:
            text: Text to analyze
            
        Returns:
            List of recognized creative patterns
        """
        patterns = []
        
        try:
            # Alliteration detection
            words = text.lower().split()
            alliterative_groups = defaultdict(list)
            
            for i, word in enumerate(words):
                if word.isalpha() and len(word) > 2:
                    first_letter = word[0]
                    alliterative_groups[first_letter].append((word, i))
            
            for letter, word_list in alliterative_groups.items():
                if len(word_list) >= 3:
                    # Check if words are close to each other
                    positions = [pos for _, pos in word_list]
                    if max(positions) - min(positions) < 20:  # Within 20 words
                        patterns.append(Pattern(
                            pattern_type="alliteration",
                            confidence=0.7,
                            data={"letter": letter, "word_count": len(word_list)},
                            examples=[word for word, _ in word_list[:5]]
                        ))
            
            # Metaphor indicators
            metaphor_patterns = [
                r'\b(like|as)\s+\w+',
                r'\bis\s+(a|an)\s+\w+',
                r'\bmetaphor\b',
                r'\bsymbolizes?\b'
            ]
            
            metaphor_matches = []
            for pattern in metaphor_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                metaphor_matches.extend(matches)
            
            if metaphor_matches:
                patterns.append(Pattern(
                    pattern_type="metaphorical_language",
                    confidence=0.6,
                    data={"indicator_count": len(metaphor_matches)},
                    examples=metaphor_matches[:5]
                ))
                
            return patterns
            
        except Exception as e:
            raise RuntimeError(f"Creative pattern recognition failed: {str(e)}")
    
    def analyze_text(self, text: str) -> Dict[str, List[Pattern]]:
        """
        Perform comprehensive pattern analysis on text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary categorizing all recognized patterns
        """
        try:
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Text must be a non-empty string")
            
            results = {
                'structural': self.recognize_structural_patterns(text),
                'linguistic': self.recognize_linguistic_patterns(text),
                'creative': self.recognize_creative_patterns(text)
            }
            
            # Filter by confidence threshold
            for category in results:
                results[category] = [p for p in results[category] 
                                   if p.confidence >= self.min_confidence]
                
            # Update pattern frequencies
            for category_patterns in results.values():
                for pattern in category_patterns:
                    self._pattern_frequencies[pattern.pattern_type] += 1
                    
            return results
            
        except Exception as e:
            raise RuntimeError(f"Text analysis failed: {str(e)}")
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of recognized patterns.
        
        Returns:
            Dictionary with pattern statistics and insights
        """
        try:
            total_texts = len(self.training_data)
            if total_texts == 0:
                return {"message": "No training data available"}
            
            avg_length = sum(item['length'] for item in self.training_data) / total_texts
            avg_words = sum(item['word_count'] for item in self.training_data) / total_texts
            
            return {
                'total_analyzed_texts': total_texts,
                'average_text_length': round(avg_length, 2),
                'average_word_count': round(avg_words, 2),
                'most_common_patterns': dict(self._pattern_frequencies.most_common(10)),
                'unique_pattern_types': len(self._pattern_frequencies),
                'confidence_threshold': self.min_confidence
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate pattern summary: {str(e)}")
    
    def save_patterns(self, filepath: str) -> None:
        """
        Save recognized patterns to a JSON file.
        
        Args:
            filepath: Path to save the patterns file
        """
        try:
            data = {
                'pattern_frequencies': dict(self._pattern_frequencies),
                'training_data_count': len(self.training_data),
                'min_confidence': self.min_confidence,
                'summary': self.get_pattern_summary()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            raise RuntimeError(f"Failed to save patterns: {str(e)}")
    
    def load_patterns(self, filepath: str) -> None:
        """
        Load previously saved patterns from a JSON file.
        
        Args:
            filepath: Path to the patterns file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self._pattern_frequencies = Counter(data.get('pattern_frequencies', {}))
            self.min_confidence = data.get('min_confidence', self.min_confidence)
            
        except Exception as e:
            raise RuntimeError(f"Failed to load patterns: {str(e)}")