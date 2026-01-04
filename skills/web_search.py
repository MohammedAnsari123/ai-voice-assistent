"""
Web Search Skill Module
"""

import logging
import webbrowser
import urllib.parse
from typing import Optional

try:
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class WebSearchSkill:
    def __init__(self):
        """Initialize the web search skill."""
        self.logger = logging.getLogger("Jarves.Skills.WebSearch")
        self.default_search_engine = "google"  # google, bing, duckduckgo
        self.search_engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q="
        }
        
    def search(self, query: str, engine: Optional[str] = None) -> str:
        """
        Perform a web search.
        
        Args:
            query: Search query
            engine: Search engine to use (google, bing, duckduckgo)
            
        Returns:
            Response message
        """
        if not query:
            return "Please specify what you want to search for."
            
        try:
            # Use specified engine or default
            if not engine:
                engine = self.default_search_engine
                
            # Get search URL
            if engine in self.search_engines:
                search_url = self.search_engines[engine]
            else:
                search_url = self.search_engines[self.default_search_engine]
                
            # Encode the query
            encoded_query = urllib.parse.quote_plus(query)
            full_url = search_url + encoded_query
            
            # Open the URL in the default browser
            webbrowser.open(full_url)
            
            return f"Searching for '{query}' using {engine}."
            
        except Exception as e:
            self.logger.error(f"Failed to perform web search: {e}")
            return f"Sorry, I couldn't perform the search for {query}."
    
    def set_default_engine(self, engine: str) -> str:
        """
        Set the default search engine.
        
        Args:
            engine: Search engine name
            
        Returns:
            Response message
        """
        if engine in self.search_engines:
            self.default_search_engine = engine
            return f"Default search engine set to {engine}."
        else:
            available = ", ".join(self.search_engines.keys())
            return f"Sorry, I don't support {engine}. Available engines: {available}."
    
    def list_engines(self) -> str:
        """
        List available search engines.
        
        Returns:
            Response message with list of engines
        """
        engines = ", ".join(self.search_engines.keys())
        return f"Available search engines: {engines}. Default: {self.default_search_engine}."
