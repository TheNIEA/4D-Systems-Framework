import json
import pickle
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import hashlib
import logging

from spark_cube.core.base_capability import StructureBuilderCapability, CapabilityResult

class ExperiencePathwayBuilder(StructureBuilderCapability):
    """
    A class to build strong pathways for learning from previous experiences.
    Manages experience storage, pattern recognition, and knowledge extraction.
    """
    
    def __init__(self, max_experiences: int = 10000, similarity_threshold: float = 0.7):
        """
        Initialize the Experience Pathway Builder.
        
        Args:
            max_experiences: Maximum number of experiences to store
            similarity_threshold: Threshold for considering experiences similar
        """
        super().__init__()
        self.experiences = {}
        self.pathways = defaultdict(list)
        self.patterns = {}
        self.max_experiences = max_experiences
        self.similarity_threshold = similarity_threshold
        self.logger = logging.getLogger(__name__)
    
    def get_description(self) -> str:
        return "Builds learning pathways from experiences by analyzing patterns, finding similarities, and recommending actions based on historical data"
    
    def process(self, data: Any) -> CapabilityResult:
        try:
            # Handle different input types and build learning structure
            if isinstance(data, dict):
                # If dict, try to extract experience or build pathway
                if all(key in data for key in ['context', 'action', 'outcome']):
                    # Add experience
                    exp_id = self.add_experience(
                        data['context'],
                        data['action'],
                        data['outcome'],
                        data.get('metadata')
                    )
                    
                    # Extract patterns after adding experience
                    patterns = self.extract_patterns()
                    
                    result = {
                        'experience_id': exp_id,
                        'patterns': patterns,
                        'stats': self.get_experience_stats(),
                        'type': 'experience_added'
                    }
                    
                    return CapabilityResult(
                        success=True,
                        output=result,
                        confidence=0.9,
                        metadata={'method': 'add_experience', 'total_experiences': len(self.experiences)}
                    )
                    
                elif 'context' in data:
                    # Get recommendations for context
                    recommendations = self.get_recommended_actions(data['context'])
                    similar = self.find_similar_experiences(data['context'])
                    
                    result = {
                        'recommendations': recommendations,
                        'similar_experiences': similar,
                        'type': 'recommendations'
                    }
                    
                    confidence = 0.8 if recommendations else 0.3
                    
                    return CapabilityResult(
                        success=True,
                        output=result,
                        confidence=confidence,
                        metadata={'method': 'get_recommendations', 'context_keys': list(data['context'].keys())}
                    )
                    
                else:
                    # Generic dict - create a synthetic experience
                    context = {'input_type': 'dict', 'keys': list(data.keys())}
                    action = 'process_dict'
                    outcome = {'processed': True, 'key_count': len(data)}
                    
                    exp_id = self.add_experience(context, action, outcome)
                    patterns = self.extract_patterns()
                    
                    result = {
                        'experience_id': exp_id,
                        'patterns': patterns,
                        'type': 'dict_processed'
                    }
                    
                    return CapabilityResult(
                        success=True,
                        output=result,
                        confidence=0.7,
                        metadata={'method': 'process_dict', 'keys': list(data.keys())}
                    )
                    
            elif isinstance(data, list):
                # Process list as a learning sequence
                context = {'input_type': 'list', 'length': len(data)}
                action = 'process_sequence'
                outcome = {'success': True, 'items_processed': len(data)}
                
                exp_id = self.add_experience(context, action, outcome)
                
                # Try to find patterns in the sequence
                pathway = []
                for i, item in enumerate(data):
                    pathway.append({
                        'step': i + 1,
                        'item': item,
                        'context': {'position': i, 'total': len(data)}
                    })
                
                patterns = self.extract_patterns()
                
                result = {
                    'experience_id': exp_id,
                    'sequence_pathway': pathway,
                    'patterns': patterns,
                    'type': 'sequence_processed'
                }
                
                return CapabilityResult(
                    success=True,
                    output=result,
                    confidence=0.8,
                    metadata={'method': 'process_sequence', 'length': len(data)}
                )
                
            elif isinstance(data, str):
                # Process string as a learning context
                context = {'input_type': 'string', 'length': len(data), 'content_type': 'text'}
                action = 'process_text'
                outcome = {'success': True, 'text_processed': True}
                
                exp_id = self.add_experience(context, action, outcome)
                
                # Look for similar text processing experiences
                similar = self.find_similar_experiences(context)
                recommendations = self.get_recommended_actions(context)
                
                patterns = self.extract_patterns()
                
                result = {
                    'experience_id': exp_id,
                    'similar_experiences': similar,
                    'recommendations': recommendations,
                    'patterns': patterns,
                    'type': 'text_processed'
                }
                
                return CapabilityResult(
                    success=True,
                    output=result,
                    confidence=0.7,
                    metadata={'method': 'process_text', 'text_length': len(data)}
                )
                
            elif isinstance(data, (int, float)):
                # Process number as a measurable outcome
                context = {'input_type': 'number', 'value_range': 'positive' if data >= 0 else 'negative'}
                action = 'process_number'
                outcome = data
                
                exp_id = self.add_experience(context, action, outcome)
                
                # Find patterns in numerical processing
                patterns = self.extract_patterns()
                stats = self.get_experience_stats()
                
                result = {
                    'experience_id': exp_id,
                    'patterns': patterns,
                    'stats': stats,
                    'type': 'number_processed'
                }
                
                return CapabilityResult(
                    success=True,
                    output=result,
                    confidence=0.8,
                    metadata={'method': 'process_number', 'value': data}
                )
                
            else:
                # Handle unknown types
                context = {'input_type': str(type(data).__name__)}
                action = 'process_unknown'
                outcome = {'success': True, 'type_handled': True}
                
                exp_id = self.add_experience(context, action, outcome)
                patterns = self.extract_patterns()
                
                result = {
                    'experience_id': exp_id,
                    'patterns': patterns,
                    'type': 'unknown_processed'
                }
                
                return CapabilityResult(
                    success=True,
                    output=result,
                    confidence=0.5,
                    metadata={'method': 'process_unknown', 'input_type': str(type(data).__name__)}
                )
                
        except Exception as e:
            return CapabilityResult(
                success=False,
                output=None,
                confidence=0.0,
                metadata={'method': 'process', 'input_type': str(type(data).__name__)},
                error=str(e)
            )
        
    def add_experience(self, context: Dict[str, Any], action: str, 
                      outcome: Any, metadata: Optional[Dict] = None) -> str:
        """
        Add a new experience to the learning system.
        
        Args:
            context: The situation or context of the experience
            action: The action taken
            outcome: The result of the action
            metadata: Additional information about the experience
            
        Returns:
            Experience ID
            
        Raises:
            ValueError: If required parameters are missing
        """
        try:
            if not context or not action:
                raise ValueError("Context and action are required")
                
            experience_id = self._generate_experience_id(context, action)
            
            experience = {
                'id': experience_id,
                'context': context,
                'action': action,
                'outcome': outcome,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {},
                'usage_count': 0,
                'success_score': self._calculate_success_score(outcome)
            }
            
            # Manage memory limits
            if len(self.experiences) >= self.max_experiences:
                self._prune_experiences()
                
            self.experiences[experience_id] = experience
            self._update_pathways(experience)
            
            return experience_id
            
        except Exception as e:
            self.logger.error(f"Error adding experience: {e}")
            raise
    
    def find_similar_experiences(self, context: Dict[str, Any], 
                               top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find experiences similar to the given context.
        
        Args:
            context: The context to match against
            top_k: Number of top similar experiences to return
            
        Returns:
            List of tuples (experience_id, similarity_score)
        """
        try:
            similarities = []
            
            for exp_id, experience in self.experiences.items():
                similarity = self._calculate_similarity(context, experience['context'])
                if similarity >= self.similarity_threshold:
                    similarities.append((exp_id, similarity))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error finding similar experiences: {e}")
            return []
    
    def get_recommended_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get recommended actions based on similar past experiences.
        
        Args:
            context: The current context
            
        Returns:
            List of recommended actions with confidence scores
        """
        try:
            similar_experiences = self.find_similar_experiences(context)
            action_scores = defaultdict(list)
            
            for exp_id, similarity in similar_experiences:
                experience = self.experiences[exp_id]
                action = experience['action']
                success_score = experience['success_score']
                
                weighted_score = similarity * success_score
                action_scores[action].append(weighted_score)
            
            recommendations = []
            for action, scores in action_scores.items():
                avg_score = sum(scores) / len(scores)
                confidence = min(avg_score, 1.0)
                
                recommendations.append({
                    'action': action,
                    'confidence': confidence,
                    'supporting_experiences': len(scores)
                })
            
            recommendations.sort(key=lambda x: x['confidence'], reverse=True)
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting recommendations: {e}")
            return []
    
    def build_pathway(self, start_context: Dict[str, Any], 
                     end_goal: Any) -> List[Dict[str, Any]]:
        """
        Build a learning pathway from start context to end goal.
        
        Args:
            start_context: Starting context
            end_goal: Desired outcome
            
        Returns:
            List of steps in the pathway
        """
        try:
            pathway = []
            current_context = start_context.copy()
            max_steps = 10
            
            for step in range(max_steps):
                recommendations = self.get_recommended_actions(current_context)
                
                if not recommendations:
                    break
                    
                best_action = recommendations[0]
                pathway.append({
                    'step': step + 1,
                    'context': current_context.copy(),
                    'recommended_action': best_action['action'],
                    'confidence': best_action['confidence']
                })
                
                # Update context based on expected outcome
                similar_exp = self.find_similar_experiences(current_context, top_k=1)
                if similar_exp:
                    exp_id = similar_exp[0][0]
                    experience = self.experiences[exp_id]
                    
                    if self._matches_goal(experience['outcome'], end_goal):
                        break
                        
                    current_context = self._update_context_with_outcome(
                        current_context, experience['outcome']
                    )
            
            return pathway
            
        except Exception as e:
            self.logger.error(f"Error building pathway: {e}")
            return []
    
    def extract_patterns(self) -> Dict[str, Any]:
        """
        Extract patterns from stored experiences.
        
        Returns:
            Dictionary of discovered patterns
        """
        try:
            patterns = {
                'successful_combinations': self._find_successful_combinations(),
                'failure_patterns': self._find_failure_patterns(),
                'context_action_correlations': self._find_correlations(),
                'temporal_patterns': self._find_temporal_patterns()
            }
            
            self.patterns.update(patterns)
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error extracting patterns: {e}")
            return {}
    
    def get_experience_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored experiences.
        
        Returns:
            Dictionary of statistics
        """
        try:
            if not self.experiences:
                return {'total_experiences': 0}
                
            success_scores = [exp['success_score'] for exp in self.experiences.values()]
            usage_counts = [exp['usage_count'] for exp in self.experiences.values()]
            
            return {
                'total_experiences': len(self.experiences),
                'avg_success_score': sum(success_scores) / len(success_scores),
                'total_pathways': len(self.pathways),
                'avg_usage_count': sum(usage_counts) / len(usage_counts),
                'patterns_discovered': len(self.patterns)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Save the experience data to a file.
        
        Args:
            filepath: Path to save the data
            
        Returns:
            Success status
        """
        try:
            data = {
                'experiences': self.experiences,
                'pathways': dict(self.pathways),
                'patterns': self.patterns,
                'config': {
                    'max_experiences': self.max_experiences,
                    'similarity_threshold': self.similarity_threshold
                }
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving to file: {e}")
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Load experience data from a file.
        
        Args:
            filepath: Path to load the data from
            
        Returns:
            Success status
        """
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            self.experiences = data.get('experiences', {})
            self.pathways = defaultdict(list, data.get('pathways', {}))
            self.patterns = data.get('patterns', {})
            
            config = data.get('config', {})
            self.max_experiences = config.get('max_experiences', 10000)
            self.similarity_threshold = config.get('similarity_threshold', 0.7)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading from file: {e}")
            return False
    
    def _generate_experience_id(self, context: Dict[str, Any], action: str) -> str:
        """Generate unique ID for an experience."""
        content = json.dumps(context, sort_keys=True) + action + str(datetime.now())
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_similarity(self, context1: Dict[str, Any], 
                            context2: Dict[str, Any]) -> float:
        """Calculate similarity between two contexts."""
        if not context1 or not context2:
            return 0.0
            
        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if context1[key] == context2[key])
        return matches / len(common_keys)
    
    def _calculate_success_score(self, outcome: Any) -> float:
        """Calculate success score based on outcome."""
        if isinstance(outcome, bool):
            return 1.0 if outcome else 0.0
        elif isinstance(outcome, (int, float)):
            return max(0.0, min(1.0, outcome))
        elif isinstance(outcome, dict) and 'success' in outcome:
            return self._calculate_success_score(outcome['success'])
        else:
            return 0.5  # Neutral score for unknown outcomes
    
    def _update_pathways(self, experience: Dict[str, Any]) -> None:
        """Update pathway connections based on new experience."""
        context_key = self._context_to_key(experience['context'])
        self.pathways[context_key].append(experience['id'])
    
    def _context_to_key(self, context: Dict[str, Any]) -> str:
        """Convert context dictionary to a string key."""
        return json.dumps(context, sort_keys=True)
    
    def _prune_experiences(self) -> None:
        """Remove least useful experiences when memory limit is reached."""
        if len(self.experiences) < self.max_experiences:
            return
            
        # Sort by usage count and success score
        sorted_exp = sorted(
            self.experiences.items(),
            key=lambda x: (x[1]['usage_count'], x[1]['success_score'])
        )
        
        # Remove bottom 10%
        to_remove = len(self.experiences) // 10
        for i in range(to_remove):
            exp_id = sorted_exp[i][0]
            del self.experiences[exp_id]
    
    def _find_successful_combinations(self) -> Dict[str, float]:
        """Find combinations of context and action that lead to success."""
        combinations = defaultdict(list)
        
        for experience in self.experiences.values():
            key = f"{self._context_to_key(experience['context'])}|{experience['action']}"
            combinations[key].append(experience['success_score'])
        
        return {k: sum(v) / len(v) for k, v in combinations.items() if len(v) > 1}
    
    def _find_failure_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns that commonly lead to failure."""
        failures = []
        for experience in self.experiences.values():
            if experience['success_score'] < 0.3:
                failures.append({
                    'context': experience['context'],
                    'action': experience['action'],
                    'success_score': experience['success_score']
                })
        return failures
    
    def _find_correlations(self) -> Dict[str, Dict[str, int]]:
        """Find correlations between context elements and actions."""
        correlations = defaultdict(lambda: defaultdict(int))
        
        for experience in self.experiences.values():
            action = experience['action']
            for key, value in experience['context'].items():
                correlations[f"{key}:{value}"][action] += 1
        
        return dict(correlations)
    
    def _find_temporal_patterns(self) -> Dict[str, Any]:
        """Find patterns based on timing of experiences."""
        return {
            'total_timespan': self._get_timespan(),
            'experience_frequency': self._get_experience_frequency()
        }
    
    def _get_timespan(self) -> str:
        """Get total timespan of experiences."""
        if not self.experiences:
            return "No experiences"
            
        timestamps = [exp['timestamp'] for exp in self.experiences.values()]
        return f"{min(timestamps)} to {max(timestamps)}"
    
    def _get_experience_frequency(self) -> float:
        """Get average frequency of experiences."""
        if len(self.experiences) < 2:
            return 0.0
        return len(self.experiences) / max(1, len(set(exp['timestamp'][:10] 
                                                    for exp in self.experiences.values())))
    
    def _matches_goal(self, outcome: Any, goal: Any) -> bool:
        """Check if outcome matches the desired goal."""
        return outcome == goal
    
    def _update_context_with_outcome(self, context: Dict[str, Any], 
                                   outcome: Any) -> Dict[str, Any]:
        """Update context based on outcome."""
        updated_context = context.copy()
        updated_context['previous_outcome'] = outcome
        return updated_context