"""Configuration service for PEaC GUI - handles persistent settings"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Dict, Any
import logging


class GuiConfig:
    """Manages persistent GUI configuration"""
    
    CONFIG_DIR = Path.home() / ".peac"
    CONFIG_FILE = CONFIG_DIR / "gui_config.json"
    
    def __init__(self):
        self.last_directory: Optional[str] = None
        self.open_files: list[str] = []  # List of file paths opened in previous session
        # Add more config options here in the future
        # self.theme: str = "light"
        # self.window_size: tuple = (1600, 1000)
        # etc.
        
        self._load()
    
    def _load(self):
        """Load configuration from file"""
        if not self.CONFIG_FILE.exists():
            logging.debug(f"Config file not found: {self.CONFIG_FILE}")
            return
        
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.last_directory = data.get('last_directory')
            self.open_files = data.get('open_files', [])
            # Load other options here
            # self.theme = data.get('theme', 'light')
            
            logging.debug(f"Loaded config: last_directory={self.last_directory}, open_files={self.open_files}")
        except Exception as e:
            logging.error(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file"""
        try:
            # Create directory if it doesn't exist
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Build config dict
            data: Dict[str, Any] = {}
            
            if self.last_directory:
                data['last_directory'] = self.last_directory
            
            if self.open_files:
                data['open_files'] = self.open_files
            
            # Add other options here
            # data['theme'] = self.theme
            
            # Write to file
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.debug(f"Saved config: {data}")
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def set_last_directory(self, directory: Optional[str]):
        """Update last directory and save"""
        if directory:
            self.last_directory = directory
            self.save()
    
    def get_last_directory(self) -> Optional[str]:
        """Get last directory"""
        return self.last_directory
    
    def set_open_files(self, files: list[str]):
        """Update open files list and save (includes untitled files)"""
        # Save all files, including untitled ones
        self.open_files = [f for f in files if f]
        self.save()
    
    def get_open_files(self) -> list[str]:
        """Get list of files to restore from previous session (only existing files)"""
        # Filter to only existing files, excluding untitled files that may have been deleted
        valid_files = []
        for f in self.open_files:
            if f and Path(f).exists() and not f.startswith("untitled_") and not f.startswith("untitle_"):
                valid_files.append(f)
        return valid_files
