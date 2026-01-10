"""
File Service

This service handles all file operations for the PEaC GUI application.
It centralizes file picker interactions, path resolution, extension management,
and file I/O operations.
"""
from __future__ import annotations
import os
from typing import Callable, Optional
from pathlib import Path
import flet as ft

from peac.gui.services.yaml_service import YamlService
from peac.gui.services.path_resolver_service import PathResolverService


class FileService:
    """Service for managing file operations: opening, saving, and picking files."""

    @staticmethod
    def ensure_yaml_extension(filepath: str) -> str:
        """
        Ensure the filepath has a .yaml extension. If missing, adds it.
        
        Args:
            filepath: Path to file (may or may not have extension)
            
        Returns:
            Path with .yaml extension guaranteed
        """
        if not filepath:
            return filepath
        
        lower_path = filepath.lower()
        if not (lower_path.endswith('.yaml') or lower_path.endswith('.yml')):
            return filepath + '.yaml'
        return filepath

    @staticmethod
    def open_yaml_file_picker(
        page: ft.Page,
        callback: Callable[[Optional[str]], None],
        initial_directory: Optional[str] = None,
        dialog_title: str = "Open YAML file"
    ) -> None:
        """
        Open a file picker dialog to select a YAML file.
        
        Args:
            page: Flet page object
            callback: Function to call with selected filepath (or None if cancelled)
            initial_directory: Directory to open picker in
            dialog_title: Title for the dialog
        """
        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                selected_path = e.files[0].path
                # Normalize the path
                selected_path = PathResolverService.normalize_path(selected_path)
                callback(selected_path)
            else:
                callback(None)

        picker = ft.FilePicker(on_result=pick_file_result)
        page.overlay.append(picker)
        page.update()
        
        # Use wildcard on Windows to show all files, including folders
        # This works around the Windows file picker issue that hides files
        picker.pick_files(
            allowed_extensions=["yaml", "yml", "*"],
            dialog_title=dialog_title,
            initial_directory=initial_directory
        )

    @staticmethod
    def save_yaml_file_picker(
        page: ft.Page,
        callback: Callable[[Optional[str]], None],
        initial_directory: Optional[str] = None,
        file_name: str = "untitled.yaml",
        dialog_title: str = "Save YAML file"
    ) -> None:
        """
        Open a save file picker dialog for YAML files.
        Ensures .yaml extension is added if user doesn't provide it.
        
        Args:
            page: Flet page object
            callback: Function to call with selected filepath (or None if cancelled)
            initial_directory: Directory to open picker in
            file_name: Default filename to suggest
            dialog_title: Title for the dialog
        """
        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                # Ensure .yaml extension
                filepath = FileService.ensure_yaml_extension(e.path)
                callback(filepath)
            else:
                callback(None)

        picker = ft.FilePicker(on_result=save_file_result)
        page.overlay.append(picker)
        page.update()
        
        # Use wildcard on Windows to allow all file types, extension will be added automatically
        picker.save_file(
            allowed_extensions=["yaml", "yml", "*"],
            dialog_title=dialog_title,
            file_name=file_name,
            initial_directory=initial_directory
        )

    @staticmethod
    def pick_yaml_file_for_extends(
        page: ft.Page,
        callback: Callable[[Optional[str]], None],
        initial_directory: Optional[str] = None
    ) -> None:
        """
        Open a file picker specifically for selecting YAML files to extend.
        Returns relative path based on initial_directory.
        
        Args:
            page: Flet page object
            callback: Function to call with relative path (or None if cancelled)
            initial_directory: Directory to base relative path calculations on
        """
        def pick_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                selected_path = e.files[0].path
                # Normalize path
                selected_path = PathResolverService.normalize_path(selected_path)
                
                # Convert to relative path if initial_directory provided
                if initial_directory:
                    selected_path = PathResolverService.get_relative_path(
                        selected_path, 
                        initial_directory
                    )
                
                callback(selected_path)
            else:
                callback(None)

        picker = ft.FilePicker(on_result=pick_file_result)
        page.overlay.append(picker)
        page.update()
        
        # Use wildcard on Windows to show all files, including folders
        picker.pick_files(
            allowed_extensions=["yaml", "yml", "*"],
            dialog_title="Select YAML file to extend",
            initial_directory=initial_directory
        )

    @staticmethod
    def load_yaml_file(filepath: str) -> dict:
        """
        Load YAML file from disk.
        
        Args:
            filepath: Path to YAML file
            
        Returns:
            Parsed YAML data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If parsing fails
        """
        return YamlService.load_file(filepath)

    @staticmethod
    def save_yaml_file(filepath: str, data: dict) -> None:
        """
        Save data to YAML file.
        
        Args:
            filepath: Path to save to (will add .yaml extension if missing)
            data: Dictionary to save as YAML
            
        Raises:
            Exception: If writing fails
        """
        # Ensure .yaml extension
        filepath = FileService.ensure_yaml_extension(filepath)
        YamlService.save_file(filepath, data)
