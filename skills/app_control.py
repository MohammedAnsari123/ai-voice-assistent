"""
App Control Skill Module
"""

import subprocess
import logging
import os
from typing import Dict, Any, Optional

try:
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class AppControlSkill:
    def __init__(self):
        """Initialize the app control skill."""
        self.logger = logging.getLogger("Jarves.Skills.AppControl")
        self.app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "outlook": "outlook.exe",
            "spotify": "spotify.exe",
            "vlc": "vlc.exe"
        }
        
    def open_app(self, app_name: str) -> str:
        """
        Open an application.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            Response message
        """
        app_name = app_name.lower().strip()
        
        if not app_name:
            return "Please specify which application to open."
            
        try:
            # Check if we have a mapping for this app
            if app_name in self.app_map:
                exe_name = self.app_map[app_name]
            else:
                # Try the app name directly
                exe_name = app_name
                
            # Try to open the application
            subprocess.Popen(exe_name)
            return f"Opening {app_name}."
            
        except Exception as e:
            self.logger.error(f"Failed to open {app_name}: {e}")
            return f"Sorry, I couldn't open {app_name}."
    
    def close_app(self, app_name: str) -> str:
        """
        Close an application.
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            Response message
        """
        app_name = app_name.lower().strip()
        
        if not app_name:
            return "Please specify which application to close."
            
        try:
            # Try to close the application using taskkill
            result = subprocess.run(
                ["taskkill", "/f", "/im", f"{app_name}.exe"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return f"Closed {app_name}."
            else:
                return f"Couldn't find {app_name} to close."
                
        except Exception as e:
            self.logger.error(f"Failed to close {app_name}: {e}")
            return f"Sorry, I couldn't close {app_name}."
    
    def list_apps(self) -> str:
        """
        List available applications.
        
        Returns:
            Response message with list of applications
        """
        app_list = ", ".join(self.app_map.keys())
        return f"I can help you with these applications: {app_list}"
