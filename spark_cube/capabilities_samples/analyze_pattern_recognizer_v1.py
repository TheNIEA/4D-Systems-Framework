import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from scipy import stats
from collections import Counter
import warnings

class AnalyzePatternRecognizer:
    """
    A pattern recognition system for analyzing and manipulating numerical data.
    Provides methods for trend detection, anomaly identification, and statistical analysis.
    """
    
    def __init__(self, data: Optional[List[Union[int, float]]] = None):
        """
        Initialize the pattern recognizer with optional data.
        
        Args:
            data: Optional list of numerical values to analyze
        """
        self.data = np.array(data) if data is not None else np.array([])
        self.patterns = {}
        
    def load_data(self, data: List[Union[int, float]]) -> None:
        """
        Load new data for analysis.
        
        Args:
            data: List of numerical values
            
        Raises:
            ValueError: If data is empty or contains non-numeric values
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        try:
            self.data = np.array(data, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Data must contain only numeric values: {e}")
    
    def detect_trend(self, window_size: int = 5) -> Dict[str, Union[str, float]]:
        """
        Detect overall trend in the data using linear regression.
        
        Args:
            window_size: Minimum number of data points required
            
        Returns:
            Dictionary containing trend direction and slope
            
        Raises:
            ValueError: If insufficient data or invalid window size
        """
        if len(self.data) < window_size:
            raise ValueError(f"Insufficient data points. Need at least {window_size}")
        
        if window_size < 2:
            raise ValueError("Window size must be at least 2")
        
        try:
            x = np.arange(len(self.data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, self.data)
            
            if abs(slope) < 1e-10:
                direction = "stable"
            elif slope > 0:
                direction = "increasing"
            else:
                direction = "decreasing"
            
            return {
                "direction": direction,
                "slope": slope,
                "correlation": r_value,
                "p_value": p_value,
                "confidence": abs(r_value)
            }
        except Exception as e:
            raise RuntimeError(f"Error detecting trend: {e}")
    
    def find_anomalies(self, method: str = "zscore", threshold: float = 2.0) -> Dict[str, List]:
        """
        Identify anomalies in the data using specified method.
        
        Args:
            method: Method to use ('zscore', 'iqr', or 'isolation')
            threshold: Threshold for anomaly detection
            
        Returns:
            Dictionary containing anomaly indices and values
            
        Raises:
            ValueError: If invalid method or insufficient data
        """
        if len(self.data) < 3:
            raise ValueError("Need at least 3 data points for anomaly detection")
        
        if method not in ['zscore', 'iqr', 'isolation']:
            raise ValueError("Method must be 'zscore', 'iqr', or 'isolation'")
        
        try:
            if method == "zscore":
                z_scores = np.abs(stats.zscore(self.data))
                anomaly_indices = np.where(z_scores > threshold)[0].tolist()
            
            elif method == "iqr":
                q1, q3 = np.percentile(self.data, [25, 75])
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                anomaly_indices = np.where((self.data < lower_bound) | (self.data > upper_bound))[0].tolist()
            
            elif method == "isolation":
                try:
                    from sklearn.ensemble import IsolationForest
                    iso_forest = IsolationForest(contamination=0.1, random_state=42)
                    outliers = iso_forest.fit_predict(self.data.reshape(-1, 1))
                    anomaly_indices = np.where(outliers == -1)[0].tolist()
                except ImportError:
                    warnings.warn("sklearn not available, falling back to z-score method")
                    z_scores = np.abs(stats.zscore(self.data))
                    anomaly_indices = np.where(z_scores > threshold)[0].tolist()
            
            anomaly_values = self.data[anomaly_indices].tolist()
            
            return {
                "indices": anomaly_indices,
                "values": anomaly_values,
                "count": len(anomaly_indices),
                "method": method,
                "threshold": threshold
            }
        except Exception as e:
            raise RuntimeError(f"Error detecting anomalies: {e}")
    
    def detect_cycles(self, min_cycle_length: int = 3) -> Dict[str, Union[List, int, float]]:
        """
        Detect cyclical patterns in the data using autocorrelation.
        
        Args:
            min_cycle_length: Minimum length of cycle to detect
            
        Returns:
            Dictionary containing cycle information
            
        Raises:
            ValueError: If insufficient data
        """
        if len(self.data) < min_cycle_length * 2:
            raise ValueError(f"Need at least {min_cycle_length * 2} data points for cycle detection")
        
        try:
            # Calculate autocorrelation
            autocorr = np.correlate(self.data - np.mean(self.data), 
                                  self.data - np.mean(self.data), mode='full')
            autocorr = autocorr[autocorr.size // 2:]
            autocorr = autocorr / autocorr[0]  # Normalize
            
            # Find peaks in autocorrelation
            peaks = []
            for i in range(min_cycle_length, len(autocorr) - 1):
                if (autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and 
                    autocorr[i] > 0.1):  # Threshold for significant correlation
                    peaks.append(i)
            
            dominant_cycle = peaks[0] if peaks else None
            cycle_strength = autocorr[dominant_cycle] if dominant_cycle else 0.0
            
            return {
                "cycles_detected": peaks,
                "dominant_cycle_length": dominant_cycle,
                "cycle_strength": cycle_strength,
                "has_cycles": len(peaks) > 0
            }
        except Exception as e:
            raise RuntimeError(f"Error detecting cycles: {e}")
    
    def find_patterns(self, pattern_length: int = 3) -> Dict[str, Union[List, int]]:
        """
        Find repeating subsequence patterns in the data.
        
        Args:
            pattern_length: Length of patterns to search for
            
        Returns:
            Dictionary containing pattern information
            
        Raises:
            ValueError: If invalid pattern length or insufficient data
        """
        if pattern_length < 2:
            raise ValueError("Pattern length must be at least 2")
        
        if len(self.data) < pattern_length * 2:
            raise ValueError(f"Need at least {pattern_length * 2} data points")
        
        try:
            # Discretize data for pattern matching
            bins = min(10, len(np.unique(self.data)))
            discretized = np.digitize(self.data, np.histogram(self.data, bins)[1])
            
            patterns = []
            pattern_counts = Counter()
            
            # Extract all subsequences of given length
            for i in range(len(discretized) - pattern_length + 1):
                pattern = tuple(discretized[i:i + pattern_length])
                patterns.append(pattern)
                pattern_counts[pattern] += 1
            
            # Find patterns that occur more than once
            repeating_patterns = {pattern: count for pattern, count in pattern_counts.items() 
                                if count > 1}
            
            most_common = pattern_counts.most_common(5)
            
            return {
                "all_patterns": list(pattern_counts.keys()),
                "repeating_patterns": repeating_patterns,
                "most_common_patterns": most_common,
                "unique_patterns": len(pattern_counts),
                "total_patterns": len(patterns)
            }
        except Exception as e:
            raise RuntimeError(f"Error finding patterns: {e}")
    
    def calculate_statistics(self) -> Dict[str, float]:
        """
        Calculate comprehensive statistics for the data.
        
        Returns:
            Dictionary containing various statistical measures
            
        Raises:
            ValueError: If no data is loaded
        """
        if len(self.data) == 0:
            raise ValueError("No data loaded")
        
        try:
            return {
                "mean": float(np.mean(self.data)),
                "median": float(np.median(self.data)),
                "std": float(np.std(self.data)),
                "variance": float(np.var(self.data)),
                "min": float(np.min(self.data)),
                "max": float(np.max(self.data)),
                "range": float(np.ptp(self.data)),
                "skewness": float(stats.skew(self.data)),
                "kurtosis": float(stats.kurtosis(self.data)),
                "q1": float(np.percentile(self.data, 25)),
                "q3": float(np.percentile(self.data, 75)),
                "iqr": float(np.percentile(self.data, 75) - np.percentile(self.data, 25))
            }
        except Exception as e:
            raise RuntimeError(f"Error calculating statistics: {e}")
    
    def smooth_data(self, method: str = "moving_average", window: int = 5) -> np.ndarray:
        """
        Apply smoothing to the data.
        
        Args:
            method: Smoothing method ('moving_average', 'exponential', 'savgol')
            window: Window size for smoothing
            
        Returns:
            Smoothed data as numpy array
            
        Raises:
            ValueError: If invalid method or window size
        """
        if len(self.data) == 0:
            raise ValueError("No data loaded")
        
        if window < 2 or window > len(self.data):
            raise ValueError(f"Window size must be between 2 and {len(self.data)}")
        
        if method not in ['moving_average', 'exponential', 'savgol']:
            raise ValueError("Method must be 'moving_average', 'exponential', or 'savgol'")
        
        try:
            if method == "moving_average":
                return np.convolve(self.data, np.ones(window)/window, mode='valid')
            
            elif method == "exponential":
                alpha = 2.0 / (window + 1)
                smoothed = np.zeros_like(self.data)
                smoothed[0] = self.data[0]
                for i in range(1, len(self.data)):
                    smoothed[i] = alpha * self.data[i] + (1 - alpha) * smoothed[i-1]
                return smoothed
            
            elif method == "savgol":
                try:
                    from scipy.signal import savgol_filter
                    poly_order = min(3, window - 1)
                    return savgol_filter(self.data, window, poly_order)
                except ImportError:
                    warnings.warn("scipy not available for savgol filter, using moving average")
                    return np.convolve(self.data, np.ones(window)/window, mode='valid')
        
        except Exception as e:
            raise RuntimeError(f"Error smoothing data: {e}")
    
    def get_summary(self) -> Dict[str, Union[int, str, Dict]]:
        """
        Get a comprehensive summary of the data and detected patterns.
        
        Returns:
            Dictionary containing summary information
        """
        if len(self.data) == 0:
            return {"status": "No data loaded"}
        
        try:
            summary = {
                "data_points": len(self.data),
                "data_range": f"{self.data.min():.2f} to {self.data.max():.2f}",
                "statistics": self.calculate_statistics(),
            }
            
            # Add pattern analysis if enough data
            if len(self.data) >= 5:
                summary["trend"] = self.detect_trend()
                summary["anomalies"] = self.find_anomalies()
                summary["cycles"] = self.detect_cycles()
                summary["patterns"] = self.find_patterns()
            
            return summary
        except Exception as e:
            return {"error": f"Error generating summary: {e}"}