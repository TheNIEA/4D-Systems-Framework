# AGI-Synthesized Capability: memory_manager
# Generated: 2026-01-15T11:03:30.175215
# Gap Confidence: 0.4

import json
import sqlite3
import datetime
import hashlib
from typing import Dict, Any, List, Optional, Tuple

class MemoryManager:
    def __init__(self, db_path: str = "memory.db"):
        """Initialize the memory manager with SQLite database."""
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create the database tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory (
                        key TEXT PRIMARY KEY,
                        data TEXT NOT NULL,
                        category TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        content_hash TEXT
                    )
                ''')
                conn.commit()
        except sqlite3.Error:
            pass
    
    def store(self, key: str, data: Any, category: str = None, metadata: Dict[str, Any] = None) -> bool:
        """
        Store information with associated metadata and categorization.
        
        Args:
            key: Unique identifier for the data
            data: The data to store
            category: Optional category for organization
            metadata: Optional metadata dictionary
            
        Returns:
            boolean: True if stored successfully, False otherwise
        """
        try:
            data_json = json.dumps(data)
            metadata_json = json.dumps(metadata if metadata else {})
            content_hash = hashlib.md5(data_json.encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO memory 
                    (key, data, category, metadata, updated_at, content_hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (key, data_json, category, metadata_json, 
                      datetime.datetime.now().isoformat(), content_hash))
                conn.commit()
                return True
        except (json.JSONEncodeError, sqlite3.Error):
            return False
    
    def retrieve(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific information by key with metadata.
        
        Args:
            key: The unique identifier for the data
            
        Returns:
            stored_data_object: Dictionary containing data and metadata, or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT data, category, metadata, created_at, updated_at 
                    FROM memory WHERE key = ?
                ''', (key,))
                
                row = cursor.fetchone()
                if row:
                    data, category, metadata, created_at, updated_at = row
                    return {
                        'key': key,
                        'data': json.loads(data),
                        'category': category,
                        'metadata': json.loads(metadata),
                        'created_at': created_at,
                        'updated_at': updated_at
                    }
                return None
        except (json.JSONDecodeError, sqlite3.Error):
            return None
    
    def search(self, query: str, category_filter: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search stored information by content, category, or metadata.
        
        Args:
            query: Search query string
            category_filter: Optional category to filter results
            limit: Maximum number of results to return
            
        Returns:
            list_of_matches: List of matching stored data objects
        """
        try:
            results = []
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                sql = '''
                    SELECT key, data, category, metadata, created_at, updated_at 
                    FROM memory WHERE (
                        data LIKE ? OR 
                        metadata LIKE ? OR 
                        key LIKE ?
                    )
                '''
                params = [f'%{query}%', f'%{query}%', f'%{query}%']
                
                if category_filter:
                    sql += ' AND category = ?'
                    params.append(category_filter)
                
                sql += ' ORDER BY updated_at DESC LIMIT ?'
                params.append(limit)
                
                cursor.execute(sql, params)
                
                for row in cursor.fetchall():
                    key, data, category, metadata, created_at, updated_at = row
                    results.append({
                        'key': key,
                        'data': json.loads(data),
                        'category': category,
                        'metadata': json.loads(metadata),
                        'created_at': created_at,
                        'updated_at': updated_at
                    })
                
                return results
        except (json.JSONDecodeError, sqlite3.Error):
            return []
    
    def organize(self, category_rules: Dict[str, Any] = None, auto_categorize: bool = False) -> Dict[str, Any]:
        """
        Categorize and structure stored information automatically or by rules.
        
        Args:
            category_rules: Dictionary of rules for categorization
            auto_categorize: Whether to automatically categorize uncategorized items
            
        Returns:
            organization_summary: Summary of organization operations performed
        """
        try:
            summary = {
                'categorized_count': 0,
                'updated_categories': [],
                'total_items': 0
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total count
                cursor.execute('SELECT COUNT(*) FROM memory')
                summary['total_items'] = cursor.fetchone()[0]
                
                if auto_categorize:
                    # Auto-categorize based on data content
                    cursor.execute('SELECT key, data FROM memory WHERE category IS NULL OR category = ""')
                    uncategorized = cursor.fetchall()
                    
                    for key, data in uncategorized:
                        try:
                            data_obj = json.loads(data)
                            category = self._auto_detect_category(data_obj)
                            if category:
                                cursor.execute('UPDATE memory SET category = ? WHERE key = ?', 
                                             (category, key))
                                summary['categorized_count'] += 1
                                if category not in summary['updated_categories']:
                                    summary['updated_categories'].append(category)
                        except json.JSONDecodeError:
                            continue
                
                if category_rules:
                    # Apply custom category rules
                    for rule_name, rule_config in category_rules.items():
                        if 'keywords' in rule_config and 'category' in rule_config:
                            for keyword in rule_config['keywords']:
                                cursor.execute('''
                                    UPDATE memory SET category = ? 
                                    WHERE data LIKE ? AND (category IS NULL OR category = "")
                                ''', (rule_config['category'], f'%{keyword}%'))
                                
                                if cursor.rowcount > 0:
                                    summary['categorized_count'] += cursor.rowcount
                                    if rule_config['category'] not in summary['updated_categories']:
                                        summary['updated_categories'].append(rule_config['category'])
                
                conn.commit()
                return summary
        except sqlite3.Error:
            return {'categorized_count': 0, 'updated_categories': [], 'total_items': 0}
    
    def get_categories(self, filter_criteria: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        List available categories and their contents for organization overview.
        
        Args:
            filter_criteria: Optional criteria to filter categories
            
        Returns:
            list_of_categories: List of category information with counts and details
        """
        try:
            categories = []
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                sql = '''
                    SELECT category, COUNT(*) as count, 
                           MIN(created_at) as first_created,
                           MAX(updated_at) as last_updated
                    FROM memory 
                    WHERE category IS NOT NULL AND category != ""
                '''
                
                params = []
                if filter_criteria:
                    if 'min_count' in filter_criteria:
                        sql += ' HAVING count >= ?'
                        params.append(filter_criteria['min_count'])
                
                sql += ' GROUP BY category ORDER BY count DESC'
                
                cursor.execute(sql, params)
                
                for row in cursor.fetchall():
                    category, count, first_created, last_updated = row
                    categories.append({
                        'category': category,
                        'count': count,
                        'first_created': first_created,
                        'last_updated': last_updated
                    })
                
                return categories
        except sqlite3.Error:
            return []
    
    def _auto_detect_category(self, data: Any) -> Optional[str]:
        """Auto-detect category based on data content."""
        data_str = str(data).lower()
        
        # Simple keyword-based categorization
        category_keywords = {
            'personal': ['name', 'age', 'phone', 'email', 'address'],
            'work': ['project', 'task', 'meeting', 'deadline', 'client'],
            'financial': ['money', 'budget', 'expense', 'income', 'payment'],
            'notes': ['note', 'reminder', 'todo', 'idea', 'thought'],
            'technical': ['code', 'programming', 'software', 'system', 'database']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in data_str for keyword in keywords):
                return category
        
        return 'general'