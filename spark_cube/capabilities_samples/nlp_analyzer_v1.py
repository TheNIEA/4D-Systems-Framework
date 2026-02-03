# AGI-Synthesized Capability: nlp_analyzer
# Generated: 2026-01-15T10:53:50.490438
# Gap Confidence: 0.4

import re
from collections import Counter
from typing import Dict, List, Optional, Tuple, Any
import math

class NlpAnalyzer:
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 
            'brilliant', 'outstanding', 'superb', 'perfect', 'love', 'like', 'enjoy',
            'happy', 'pleased', 'satisfied', 'delighted', 'thrilled', 'excited'
        }
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
            'angry', 'sad', 'disappointed', 'frustrated', 'annoyed', 'upset', 'furious',
            'worst', 'poor', 'stupid', 'useless', 'pathetic', 'ridiculous'
        }
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Determines the emotional tone of text (positive, negative, neutral) with confidence score.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence score
        """
        try:
            if not text or not text.strip():
                return {'label': 'neutral', 'score': 0.0}
                
            words = re.findall(r'\b\w+\b', text.lower())
            total_words = len(words)
            
            if total_words == 0:
                return {'label': 'neutral', 'score': 0.0}
            
            positive_count = sum(1 for word in words if word in self.positive_words)
            negative_count = sum(1 for word in words if word in self.negative_words)
            
            sentiment_score = (positive_count - negative_count) / total_words
            
            if sentiment_score > 0.1:
                label = 'positive'
            elif sentiment_score < -0.1:
                label = 'negative'
            else:
                label = 'neutral'
                
            confidence = min(abs(sentiment_score) * 10, 1.0)
            
            return {'label': label, 'score': round(confidence, 3)}
            
        except Exception as e:
            return {'label': 'neutral', 'score': 0.0, 'error': str(e)}

    def extract_entities(self, text: str, entity_types: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        Identifies and extracts named entities like people, organizations, locations, dates from text.
        
        Args:
            text: Input text to analyze
            entity_types: Optional list of entity types to extract
            
        Returns:
            List of dictionaries containing entity text and type
        """
        try:
            if not text or not text.strip():
                return []
                
            entities = []
            
            # Extract capitalized words (potential names/organizations)
            name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
            names = re.findall(name_pattern, text)
            
            for name in names:
                if len(name.split()) > 1:
                    entities.append({'text': name, 'type': 'PERSON'})
                else:
                    entities.append({'text': name, 'type': 'ORG'})
            
            # Extract dates
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
            ]
            
            for pattern in date_patterns:
                dates = re.findall(pattern, text, re.IGNORECASE)
                for date in dates:
                    entities.append({'text': date, 'type': 'DATE'})
            
            # Extract email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            for email in emails:
                entities.append({'text': email, 'type': 'EMAIL'})
            
            # Extract phone numbers
            phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
            phones = re.findall(phone_pattern, text)
            for phone in phones:
                entities.append({'text': phone, 'type': 'PHONE'})
            
            # Filter by entity types if specified
            if entity_types:
                entities = [e for e in entities if e['type'] in entity_types]
            
            return entities
            
        except Exception as e:
            return [{'error': str(e)}]

    def summarize_text(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Creates a concise summary of longer text while preserving key information.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary in characters
            
        Returns:
            Summary text
        """
        try:
            if not text or not text.strip():
                return ""
                
            sentences = re.split(r'[.!?]+', text.strip())
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 2:
                summary = text[:max_length] if max_length else text
                return summary.strip()
            
            # Score sentences based on word frequency
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = Counter(word for word in words if word not in self.stop_words)
            
            sentence_scores = {}
            for i, sentence in enumerate(sentences):
                sentence_words = re.findall(r'\b\w+\b', sentence.lower())
                score = sum(word_freq.get(word, 0) for word in sentence_words if word not in self.stop_words)
                sentence_scores[i] = score / len(sentence_words) if sentence_words else 0
            
            # Select top sentences
            num_sentences = max(1, len(sentences) // 3)
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            top_sentences = sorted([idx for idx, _ in top_sentences])
            
            summary = '. '.join(sentences[i] for i in top_sentences)
            if not summary.endswith('.'):
                summary += '.'
                
            if max_length and len(summary) > max_length:
                summary = summary[:max_length].rsplit(' ', 1)[0] + '...'
                
            return summary
            
        except Exception as e:
            return f"Summary error: {str(e)}"

    def analyze_text_complete(self, text: str, analysis_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Performs all NLP operations in one call returning sentiment, entities, and summary.
        
        Args:
            text: Input text to analyze
            analysis_options: Optional dictionary with analysis parameters
            
        Returns:
            Dictionary with complete analysis results
        """
        try:
            options = analysis_options or {}
            
            result = {
                'sentiment': self.analyze_sentiment(text),
                'entities': self.extract_entities(text, options.get('entity_types')),
                'summary': self.summarize_text(text, options.get('max_summary_length')),
                'keywords': self.extract_keywords(text, options.get('num_keywords')),
                'statistics': {
                    'character_count': len(text),
                    'word_count': len(re.findall(r'\b\w+\b', text)),
                    'sentence_count': len(re.split(r'[.!?]+', text.strip()))
                }
            }
            
            return result
            
        except Exception as e:
            return {'error': str(e)}

    def extract_keywords(self, text: str, num_keywords: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Identifies the most important keywords and phrases in the text.
        
        Args:
            text: Input text to analyze
            num_keywords: Number of keywords to return
            
        Returns:
            List of keywords with frequency scores
        """
        try:
            if not text or not text.strip():
                return []
                
            words = re.findall(r'\b\w{3,}\b', text.lower())
            words = [word for word in words if word not in self.stop_words]
            
            if not words:
                return []
            
            word_freq = Counter(words)
            total_words = len(words)
            
            # Calculate TF-IDF-like scores
            keywords = []
            for word, freq in word_freq.items():
                tf = freq / total_words
                # Simple IDF approximation
                idf = math.log(total_words / freq)
                score = tf * idf
                keywords.append({
                    'keyword': word,
                    'frequency': freq,
                    'score': round(score, 4)
                })
            
            keywords.sort(key=lambda x: x['score'], reverse=True)
            return keywords[:num_keywords or 10]
            
        except Exception as e:
            return [{'error': str(e)}]