from spark_cube.core.base_capability import PatternRecognizerCapability, CapabilityResult
from typing import Any, Dict, List, Tuple, Optional, Union
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import pandas as pd
import json
import re
import io
import base64

class PatternRecognizer(PatternRecognizerCapability):
    """
    A class for pattern recognition and visual representation of data patterns.
    
    This class provides methods for detecting patterns in data and creating
    visualizations to represent those patterns effectively.
    """
    
    def __init__(self):
        super().__init__()
        self.random_state = 42
        self.scaler = StandardScaler()
        self.patterns_ = {}
        self.fitted_models_ = {}
    
    def process(self, data: Any) -> CapabilityResult:
        try:
            # Convert input data to analyzable format
            processed_data, data_type = self._convert_input_to_data(data)
            
            if processed_data is None:
                return CapabilityResult(
                    success=False,
                    output=None,
                    confidence=0.0,
                    metadata={"data_type": str(type(data))},
                    error="Could not convert input data to analyzable format"
                )
            
            # Detect patterns based on data type
            patterns = {}
            confidence = 0.0
            
            if data_type == "numerical":
                # Numerical data analysis
                patterns.update(self._analyze_numerical_patterns(processed_data))
                confidence = 0.9
            elif data_type == "text":
                # Text pattern analysis
                patterns.update(self._analyze_text_patterns(processed_data))
                confidence = 0.7
            elif data_type == "categorical":
                # Categorical data analysis
                patterns.update(self._analyze_categorical_patterns(processed_data))
                confidence = 0.8
            else:
                # Mixed or complex data
                patterns.update(self._analyze_mixed_patterns(processed_data))
                confidence = 0.6
            
            # Generate summary
            summary = self._generate_summary(patterns, data_type)
            
            return CapabilityResult(
                success=True,
                output=summary,
                confidence=confidence,
                metadata={
                    "data_type": data_type,
                    "input_type": str(type(data)),
                    "patterns_found": list(patterns.keys()),
                    "data_shape": getattr(processed_data, 'shape', None) if hasattr(processed_data, 'shape') else None
                }
            )
            
        except Exception as e:
            return CapabilityResult(
                success=False,
                output=None,
                confidence=0.0,
                metadata={"input_type": str(type(data))},
                error=f"Error in pattern recognition: {str(e)}"
            )
    
    def get_description(self) -> str:
        return "Analyzes input data to detect patterns, clusters, and relationships. Supports numerical arrays, text, categorical data, and mixed data types. Provides statistical analysis, clustering, dimensionality reduction, and pattern summaries."
    
    def _convert_input_to_data(self, data: Any) -> Tuple[Any, str]:
        """Convert various input types to analyzable data."""
        try:
            if isinstance(data, (list, tuple)):
                # Check if it's a list of numbers
                if all(isinstance(x, (int, float)) for x in data):
                    return np.array(data).reshape(-1, 1), "numerical"
                # Check if it's a list of strings
                elif all(isinstance(x, str) for x in data):
                    return data, "text"
                # Mixed list
                else:
                    return data, "mixed"
            
            elif isinstance(data, str):
                # Single string - analyze text patterns
                return data, "text"
            
            elif isinstance(data, dict):
                # Dictionary - convert to analyzable format
                values = list(data.values())
                if all(isinstance(v, (int, float)) for v in values):
                    return np.array(values).reshape(-1, 1), "numerical"
                else:
                    return data, "categorical"
            
            elif isinstance(data, (int, float)):
                # Single number
                return np.array([[data]]), "numerical"
            
            elif isinstance(data, np.ndarray):
                return data, "numerical"
            
            elif isinstance(data, pd.DataFrame):
                return data, "numerical"
            
            else:
                # Try to convert to string for basic analysis
                return str(data), "text"
                
        except Exception:
            return None, "unknown"
    
    def _analyze_numerical_patterns(self, data: np.ndarray) -> Dict:
        """Analyze numerical data patterns."""
        patterns = {}
        
        try:
            # Ensure 2D array
            if len(data.shape) == 1:
                data = data.reshape(-1, 1)
            
            # Basic statistics
            patterns['statistics'] = {
                'mean': float(np.mean(data)),
                'std': float(np.std(data)),
                'min': float(np.min(data)),
                'max': float(np.max(data)),
                'shape': data.shape
            }
            
            # If enough data points, try clustering
            if data.shape[0] >= 3:
                try:
                    n_clusters = min(3, data.shape[0] - 1)
                    cluster_info = self.detect_clusters(data, n_clusters)
                    patterns['clusters'] = cluster_info
                except:
                    pass
            
            # If multivariate, try PCA
            if data.shape[1] > 1 and data.shape[0] >= 2:
                try:
                    pca_info = self.detect_dimensionality_patterns(data)
                    patterns['dimensionality'] = pca_info
                except:
                    pass
            
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns
    
    def _analyze_text_patterns(self, data: Union[str, List[str]]) -> Dict:
        """Analyze text patterns."""
        patterns = {}
        
        try:
            if isinstance(data, str):
                text = data
            else:
                text = ' '.join(str(x) for x in data)
            
            # Basic text statistics
            patterns['text_stats'] = {
                'length': len(text),
                'word_count': len(text.split()),
                'unique_chars': len(set(text)),
                'has_numbers': bool(re.search(r'\d', text)),
                'has_special_chars': bool(re.search(r'[^a-zA-Z0-9\s]', text))
            }
            
            # Character frequency patterns
            char_freq = {}
            for char in text.lower():
                if char.isalnum():
                    char_freq[char] = char_freq.get(char, 0) + 1
            
            patterns['character_patterns'] = {
                'most_frequent_chars': sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:5],
                'vowel_consonant_ratio': self._calculate_vowel_ratio(text)
            }
            
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns
    
    def _analyze_categorical_patterns(self, data: Dict) -> Dict:
        """Analyze categorical/dictionary patterns."""
        patterns = {}
        
        try:
            patterns['structure'] = {
                'key_count': len(data),
                'keys': list(data.keys()),
                'value_types': [type(v).__name__ for v in data.values()]
            }
            
            # Value frequency analysis
            value_types = {}
            for v in data.values():
                vtype = type(v).__name__
                value_types[vtype] = value_types.get(vtype, 0) + 1
            
            patterns['value_distribution'] = value_types
            
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns
    
    def _analyze_mixed_patterns(self, data: Any) -> Dict:
        """Analyze mixed or complex data patterns."""
        patterns = {}
        
        try:
            patterns['data_info'] = {
                'type': str(type(data)),
                'length': len(data) if hasattr(data, '__len__') else 1,
                'is_iterable': hasattr(data, '__iter__')
            }
            
            if hasattr(data, '__iter__') and not isinstance(data, str):
                # Analyze element types
                element_types = {}
                for item in data:
                    item_type = type(item).__name__
                    element_types[item_type] = element_types.get(item_type, 0) + 1
                
                patterns['element_distribution'] = element_types
            
        except Exception as e:
            patterns['error'] = str(e)
        
        return patterns
    
    def _calculate_vowel_ratio(self, text: str) -> float:
        """Calculate vowel to consonant ratio in text."""
        vowels = 'aeiou'
        vowel_count = sum(1 for char in text.lower() if char in vowels)
        consonant_count = sum(1 for char in text.lower() if char.isalpha() and char not in vowels)
        
        if consonant_count == 0:
            return float('inf') if vowel_count > 0 else 0
        
        return vowel_count / consonant_count
    
    def _generate_summary(self, patterns: Dict, data_type: str) -> Dict:
        """Generate a comprehensive summary of detected patterns."""
        summary = {
            'data_type': data_type,
            'patterns_detected': list(patterns.keys()),
            'analysis_summary': {}
        }
        
        if 'statistics' in patterns:
            stats = patterns['statistics']
            summary['analysis_summary']['numerical_insights'] = {
                'data_range': stats['max'] - stats['min'],
                'variability': 'high' if stats['std'] > stats['mean'] else 'low',
                'distribution': 'centered' if abs(stats['mean'] - (stats['max'] + stats['min']) / 2) < stats['std'] else 'skewed'
            }
        
        if 'text_stats' in patterns:
            text_stats = patterns['text_stats']
            summary['analysis_summary']['text_insights'] = {
                'complexity': 'high' if text_stats['unique_chars'] > 20 else 'low',
                'content_type': 'mixed' if text_stats['has_numbers'] and text_stats['has_special_chars'] else 'simple'
            }
        
        if 'clusters' in patterns:
            summary['analysis_summary']['clustering'] = {
                'clusters_found': patterns['clusters']['n_clusters'],
                'clustering_quality': 'good' if patterns['clusters']['inertia'] < 1000 else 'moderate'
            }
        
        return summary
    
    def detect_clusters(self, data: Union[np.ndarray, pd.DataFrame], 
                       n_clusters: int = 3) -> Dict:
        """
        Detect cluster patterns in the data.
        
        Args:
            data: Input data for clustering
            n_clusters: Number of clusters to identify
            
        Returns:
            Dictionary containing cluster information and labels
        """
        try:
            data_array = self._validate_and_convert_data(data)
            
            # Scale the data
            scaled_data = self.scaler.fit_transform(data_array)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
            cluster_labels = kmeans.fit_predict(scaled_data)
            
            # Store results
            cluster_info = {
                'labels': cluster_labels,
                'centers': kmeans.cluster_centers_,
                'inertia': kmeans.inertia_,
                'n_clusters': n_clusters
            }
            
            self.patterns_['clusters'] = cluster_info
            self.fitted_models_['kmeans'] = kmeans
            
            return cluster_info
            
        except Exception as e:
            raise ValueError(f"Error in cluster detection: {str(e)}")
    
    def detect_dimensionality_patterns(self, data: Union[np.ndarray, pd.DataFrame], 
                                     n_components: int = 2) -> Dict:
        """
        Detect patterns through dimensionality reduction.
        
        Args:
            data: Input data for dimensionality reduction
            n_components: Number of principal components
            
        Returns:
            Dictionary containing PCA results and transformed data
        """
        try:
            data_array = self._validate_and_convert_data(data)
            
            # Scale the data
            scaled_data = self.scaler.fit_transform(data_array)
            
            # Apply PCA
            pca = PCA(n_components=n_components, random_state=self.random_state)
            transformed_data = pca.fit_transform(scaled_data)
            
            # Store results
            pca_info = {
                'transformed_data': transformed_data,
                'explained_variance_ratio': pca.explained_variance_ratio_,
                'cumulative_variance_ratio': np.cumsum(pca.explained_variance_ratio_),
                'components': pca.components_,
                'n_components': n_components
            }
            
            self.patterns_['pca'] = pca_info
            self.fitted_models_['pca'] = pca
            
            return pca_info
            
        except Exception as e:
            raise ValueError(f"Error in dimensionality pattern detection: {str(e)}")
    
    def visualize_clusters(self, data: Union[np.ndarray, pd.DataFrame], 
                          figsize: Tuple[int, int] = (12, 5)) -> plt.Figure:
        """
        Create visualizations for cluster patterns.
        
        Args:
            data: Input data
            figsize: Figure size for the plots
            
        Returns:
            Matplotlib figure object
        """
        try:
            if 'clusters' not in self.patterns_:
                self.detect_clusters(data)
            
            data_array = self._validate_and_convert_data(data)
            cluster_info = self.patterns_['clusters']
            
            fig, axes = plt.subplots(1, 2, figsize=figsize)
            
            # If data has more than 2 dimensions, use PCA for visualization
            if data_array.shape[1] > 2:
                if 'pca' not in self.patterns_:
                    self.detect_dimensionality_patterns(data, n_components=2)
                plot_data = self.patterns_['pca']['transformed_data']
                axes[0].set_xlabel('First Principal Component')
                axes[0].set_ylabel('Second Principal Component')
            else:
                plot_data = self.scaler.transform(data_array)
                axes[0].set_xlabel('Feature 1')
                axes[0].set_ylabel('Feature 2')
            
            # Scatter plot with cluster colors
            scatter = axes[0].scatter(plot_data[:, 0], plot_data[:, 1], 
                                    c=cluster_info['labels'], cmap='viridis', alpha=0.7)
            axes[0].set_title('Cluster Patterns')
            axes[0].grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=axes[0])
            
            # Cluster size distribution
            unique_labels, counts = np.unique(cluster_info['labels'], return_counts=True)
            axes[1].bar(unique_labels, counts, alpha=0.7, color='skyblue')
            axes[1].set_xlabel('Cluster')
            axes[1].set_ylabel('Number of Points')
            axes[1].set_title('Cluster Size Distribution')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            raise ValueError(f"Error in cluster visualization: {str(e)}")
    
    def visualize_dimensionality_patterns(self, data: Union[np.ndarray, pd.DataFrame],
                                        figsize: Tuple[int, int] = (15, 5)) -> plt.Figure:
        """
        Create visualizations for dimensionality patterns.
        
        Args:
            data: Input data
            figsize: Figure size for the plots
            
        Returns:
            Matplotlib figure object
        """
        try:
            if 'pca' not in self.patterns_:
                self.detect_dimensionality_patterns(data)
            
            pca_info = self.patterns_['pca']
            
            fig, axes = plt.subplots(1, 3, figsize=figsize)
            
            # PCA scatter plot
            transformed_data = pca_info['transformed_data']
            axes[0].scatter(transformed_data[:, 0], transformed_data[:, 1], 
                          alpha=0.7, c='steelblue')
            axes[0].set_xlabel('First Principal Component')
            axes[0].set_ylabel('Second Principal Component')
            axes[0].set_title('PCA Projection')
            axes[0].grid(True, alpha=0.3)
            
            # Explained variance ratio
            components = range(1, len(pca_info['explained_variance_ratio']) + 1)
            axes[1].bar(components, pca_info['explained_variance_ratio'], 
                       alpha=0.7, color='lightcoral')
            axes[1].set_xlabel('Principal Component')
            axes[1].set_ylabel('Explained Variance Ratio')
            axes[1].set_title('Explained Variance by Component')
            axes[1].grid(True, alpha=0.3)
            
            # Cumulative explained variance
            axes[2].plot(components, pca_info['cumulative_variance_ratio'], 
                        marker='o', linewidth=2, color='green')
            axes[2].set_xlabel('Number of Components')
            axes[2].set_ylabel('Cumulative Explained Variance')
            axes[2].set_title('Cumulative Explained Variance')
            axes[2].grid(True, alpha=0.3)
            axes[2].axhline(y=0.95, color='red', linestyle='--', alpha=0.7, label='95%')
            axes[2].legend()
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            raise ValueError(f"Error in dimensionality visualization: {str(e)}")
    
    def create_correlation_heatmap(self, data: Union[np.ndarray, pd.DataFrame],
                                  figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Create a correlation heatmap to visualize feature relationships.
        
        Args:
            data: Input data
            figsize: Figure size for the plot
            
        Returns:
            Matplotlib figure object
        """
        try:
            # Convert to DataFrame if necessary
            if isinstance(data, np.ndarray):
                df = pd.DataFrame(data, columns=[f'Feature_{i}' for i in range(data.shape[1])])
            else:
                df = data.copy()
            
            # Calculate correlation matrix
            corr_matrix = df.corr()
            
            # Create heatmap
            fig, ax = plt.subplots(figsize=figsize)
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=ax, cbar_kws={'shrink': 0.8})
            ax.set_title('Feature Correlation Heatmap')
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            raise ValueError(f"Error in correlation heatmap creation: {str(e)}")
    
    def generate_pattern_summary(self) -> Dict:
        """
        Generate a summary of detected patterns.
        
        Returns:
            Dictionary containing pattern summary information
        """
        try:
            summary = {
                'detected_patterns': list(self.patterns_.keys()),
                'pattern_details': {}
            }
            
            if 'clusters' in self.patterns_:
                cluster_info = self.patterns_['clusters']
                summary['pattern_details']['clusters'] = {
                    'n_clusters': cluster_info['n_clusters'],
                    'inertia': cluster_info['inertia'],
                    'cluster_sizes': np.bincount(cluster_info['labels']).tolist()
                }
            
            if 'pca' in self.patterns_:
                pca_info = self.patterns_['pca']
                summary['pattern_details']['dimensionality'] = {
                    'n_components': pca_info['n_components'],
                    'total_variance_explained': float(pca_info['cumulative_variance_ratio'][-1]),
                    'component_variance': pca_info['explained_variance_ratio'].tolist()
                }
            
            return summary
            
        except Exception as e:
            raise ValueError(f"Error in pattern summary generation: {str(e)}")
    
    def _validate_and_convert_data(self, data: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """
        Validate and convert input data to numpy array.
        
        Args:
            data: Input data to validate and convert
            
        Returns:
            Validated numpy array
        """
        if data is None:
            raise ValueError("Data cannot be None")
        
        if isinstance(data, pd.DataFrame):
            # Select only numeric columns
            numeric_data = data.select_dtypes(include=[np.number])
            if numeric_data.empty:
                raise ValueError("No numeric columns found in DataFrame")
            data_array = numeric_data.values
        elif isinstance(data, np.ndarray):
            data_array = data
        else:
            try:
                data_array = np.array(data)
            except Exception:
                raise ValueError("Data must be a numpy array, pandas DataFrame, or convertible to numpy array")
        
        if data_array.size == 0:
            raise ValueError("Data array is empty")
        
        if len(data_array.shape) == 1:
            data_array = data_array.reshape(-1, 1)
        
        if len(data_array.shape) != 2:
            raise ValueError("Data must be 2-dimensional or convertible to 2D")
        
        if np.any(np.isnan(data_array)) or np.any(np.isinf(data_array)):
            raise ValueError("Data contains NaN or infinite values")
        
        return data_array