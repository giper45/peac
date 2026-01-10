"""
Path Resolver Service

This service provides centralized path resolution logic for the PEaC GUI application.
It handles:
- Converting relative paths to absolute paths
- Converting absolute paths to relative paths
- Normalizing paths (removing platform-specific prefixes)
- Path resolution relative to a base directory
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional


class PathResolverService:
    """Service for resolving and converting file paths between relative and absolute formats."""
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        Normalize path by removing platform-specific prefixes.
        
        On macOS, this removes '/Volumes/Macintosh HD/' prefix if present.
        
        Args:
            path: The path to normalize
            
        Returns:
            Normalized path string
        """
        if path.startswith('/Volumes/Macintosh HD/'):
            normalized = path.replace('/Volumes/Macintosh HD/', '/', 1)
            return normalized
        return path
    
    @staticmethod
    def get_absolute_path(path: str, base_dir: Optional[str] = None) -> str:
        """
        Convert a relative path to an absolute path based on a base directory.
        
        If the path is already absolute, returns it as-is (after resolving).
        If the path is relative and base_dir is provided, resolves it relative to base_dir.
        
        Args:
            path: The path to convert (can be relative or absolute)
            base_dir: Base directory for resolution (should be a directory, not a file path)
            
        Returns:
            Absolute path string
        """
        path_obj = Path(path)
        
        # If already absolute, resolve and return
        if path_obj.is_absolute():
            return str(path_obj.resolve())
        
        # If no base directory provided, return the path as-is
        if not base_dir:
            return path
        
        # Resolve relative to base directory
        base = Path(base_dir)
        abs_path = (base / path_obj).resolve()
        return str(abs_path)
    
    @staticmethod
    def get_relative_path(absolute_path: str, base_dir: Optional[str] = None) -> str:
        """
        Convert an absolute path to a relative path based on a base directory.
        
        Calculates the relative path from base_dir to absolute_path.
        Uses .. navigation if paths are not in a parent/child relationship.
        
        Args:
            absolute_path: The absolute path to convert
            base_dir: Base directory for relative path calculation (should be a directory)
            
        Returns:
            Relative path string, or the original absolute path if conversion fails
        """
        if not base_dir:
            return absolute_path
        
        try:
            # Use pathlib for proper path handling
            abs_path = Path(absolute_path).resolve()
            base = Path(base_dir).resolve()
            
            # Try direct relative_to first (works when abs_path is under base)
            try:
                rel_path = abs_path.relative_to(base)
                return str(rel_path)
            except ValueError:
                # Paths not in parent/child relationship, calculate using common path
                pass
            
            # Find common ancestor and build relative path with .. navigation
            try:
                common = Path(*os.path.commonpath([abs_path, base]).split(os.sep))
                
                # Count how many levels up from base to common
                up_levels = len(base.parts) - len(common.parts)
                
                # Build relative path: ../../../... then down to target
                rel_parts = ['..'] * up_levels
                rel_parts.extend(abs_path.parts[len(common.parts):])
                
                return os.path.join(*rel_parts) if rel_parts else '.'
            except (ValueError, OSError):
                # Cannot find common path (e.g., different drives on Windows)
                return absolute_path
                
        except (ValueError, OSError):
            # Any other path resolution error
            return absolute_path
    
    @staticmethod
    def resolve_path(path: str, parent_path: str = '') -> tuple[str, str]:
        """
        Resolve a path relative to parent_path if it's relative, otherwise return absolute.
        
        This method is compatible with the find_path function in peac.core.peac.
        
        Args:
            path: The path to resolve
            parent_path: Parent directory path (defaults to directory of path if empty)
            
        Returns:
            Tuple of (resolved_path, parent_path)
        """
        if parent_path == '':
            parent_path = os.path.dirname(path)
        
        # If path is already absolute, return as-is
        if os.path.isabs(path):
            return path, parent_path
        
        # For relative paths, resolve them relative to parent_path
        resolved_path = os.path.normpath(os.path.join(parent_path, path))
        return resolved_path, parent_path
