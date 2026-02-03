class GreetingSystemBuilder:
    """A structure builder for creating and managing greeting systems with strong pathways."""
    
    def __init__(self):
        """Initialize the greeting system builder."""
        self._greeting_templates = {}
        self._languages = set()
        self._default_language = 'english'
        self._fallback_greeting = "Hello!"
        
    def add_greeting_template(self, language, template, greeting_type='default'):
        """
        Add a greeting template for a specific language and type.
        
        Args:
            language (str): The language identifier
            template (str): The greeting template (can include {name} placeholder)
            greeting_type (str): Type of greeting (default, formal, casual)
            
        Raises:
            ValueError: If language or template is empty
        """
        if not language or not isinstance(language, str):
            raise ValueError("Language must be a non-empty string")
        if not template or not isinstance(template, str):
            raise ValueError("Template must be a non-empty string")
            
        language = language.lower().strip()
        greeting_type = greeting_type.lower().strip()
        
        if language not in self._greeting_templates:
            self._greeting_templates[language] = {}
            
        self._greeting_templates[language][greeting_type] = template.strip()
        self._languages.add(language)
    
    def set_default_language(self, language):
        """
        Set the default language for greetings.
        
        Args:
            language (str): The default language identifier
            
        Raises:
            ValueError: If language is not available
        """
        if not language or not isinstance(language, str):
            raise ValueError("Language must be a non-empty string")
            
        language = language.lower().strip()
        if language not in self._languages:
            raise ValueError(f"Language '{language}' not available. Add templates first.")
            
        self._default_language = language
    
    def build_greeting(self, name=None, language=None, greeting_type='default'):
        """
        Build a personalized greeting.
        
        Args:
            name (str, optional): Name to include in greeting
            language (str, optional): Language for greeting (uses default if None)
            greeting_type (str): Type of greeting to use
            
        Returns:
            str: The formatted greeting
        """
        try:
            target_language = (language or self._default_language).lower().strip()
            greeting_type = greeting_type.lower().strip()
            
            # Get template with fallback chain
            template = self._get_template_with_fallback(target_language, greeting_type)
            
            # Format template with name if provided
            if name and isinstance(name, str) and '{name}' in template:
                return template.format(name=name.strip())
            elif name and isinstance(name, str):
                return f"{template} {name.strip()}!"
            else:
                return template
                
        except Exception:
            return self._fallback_greeting
    
    def _get_template_with_fallback(self, language, greeting_type):
        """
        Get template with fallback logic.
        
        Args:
            language (str): Target language
            greeting_type (str): Target greeting type
            
        Returns:
            str: The greeting template
        """
        # Try exact match
        if (language in self._greeting_templates and 
            greeting_type in self._greeting_templates[language]):
            return self._greeting_templates[language][greeting_type]
        
        # Try same language, default type
        if (language in self._greeting_templates and 
            'default' in self._greeting_templates[language]):
            return self._greeting_templates[language]['default']
        
        # Try default language, same type
        if (self._default_language in self._greeting_templates and 
            greeting_type in self._greeting_templates[self._default_language]):
            return self._greeting_templates[self._default_language][greeting_type]
        
        # Try default language, default type
        if (self._default_language in self._greeting_templates and 
            'default' in self._greeting_templates[self._default_language]):
            return self._greeting_templates[self._default_language]['default']
        
        # Final fallback
        return self._fallback_greeting
    
    def get_available_languages(self):
        """
        Get list of available languages.
        
        Returns:
            list: Available languages
        """
        return sorted(list(self._languages))
    
    def get_greeting_types(self, language=None):
        """
        Get available greeting types for a language.
        
        Args:
            language (str, optional): Language to check (uses default if None)
            
        Returns:
            list: Available greeting types
        """
        target_language = (language or self._default_language).lower().strip()
        
        if target_language not in self._greeting_templates:
            return []
            
        return sorted(list(self._greeting_templates[target_language].keys()))
    
    def remove_language(self, language):
        """
        Remove a language and all its templates.
        
        Args:
            language (str): Language to remove
            
        Raises:
            ValueError: If trying to remove the default language
        """
        if not language or not isinstance(language, str):
            raise ValueError("Language must be a non-empty string")
            
        language = language.lower().strip()
        
        if language == self._default_language:
            raise ValueError("Cannot remove default language")
            
        if language in self._greeting_templates:
            del self._greeting_templates[language]
            self._languages.discard(language)
    
    def clear_all(self):
        """Clear all greeting templates and reset to initial state."""
        self._greeting_templates.clear()
        self._languages.clear()
        self._default_language = 'english'