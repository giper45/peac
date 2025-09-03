"""
Extends Section Component for PEaC CustomTkinter GUI
Handles extends/inheritance configuration
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any
import os


class ExtendsCard(ctk.CTkFrame):
    """Individual extends card component"""
    
    def __init__(self, parent, section=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Store reference to parent section for removal
        self.section = section
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create extends card widgets"""
        row = 0
        
        # Remove button at the top right
        remove_btn = ctk.CTkButton(
            self,
            text="✕",
            width=30,
            height=30,
            command=self.remove_self,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.grid(row=0, column=2, padx=(5, 15), pady=(15, 5))
        
        # Source path with browse button
        source_label = ctk.CTkLabel(self, text="Source:", width=80)
        source_label.grid(row=row, column=0, sticky="w", padx=(15, 5), pady=(15, 5))
        
        source_frame = ctk.CTkFrame(self, fg_color="transparent")
        source_frame.grid(row=row, column=1, sticky="ew", padx=(5, 10), pady=(15, 5))
        source_frame.grid_columnconfigure(0, weight=1)
        
        self.source_entry = ctk.CTkEntry(
            source_frame, 
            placeholder_text="Path to YAML file or URL"
        )
        self.source_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        browse_btn = ctk.CTkButton(
            source_frame,
            text="📂",
            width=40,
            command=self.browse_source
        )
        browse_btn.grid(row=0, column=1)
        
        # Open file button
        open_btn = ctk.CTkButton(
            source_frame,
            text="📄",
            width=40,
            command=self.open_source_file,
            fg_color=("green", "darkgreen"),
            hover_color=("darkgreen", "green")
        )
        open_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Relative path toggle
        self.relative_path_var = ctk.BooleanVar(value=True)
        relative_btn = ctk.CTkButton(
            source_frame,
            text="📍",
            width=30,
            command=self.toggle_relative_path,
            fg_color=("gray70", "gray30")
        )
        relative_btn.grid(row=0, column=3, padx=(5, 0))
        
        row += 1
        
        # Override options (optional advanced settings)
        override_frame = ctk.CTkFrame(self, fg_color="transparent")
        override_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=15, pady=(5, 15))
        override_frame.grid_columnconfigure(1, weight=1)
        
        # Override checkbox
        self.override_var = ctk.BooleanVar()
        override_cb = ctk.CTkCheckBox(
            override_frame,
            text="Allow Override",
            variable=self.override_var
        )
        override_cb.grid(row=0, column=0, sticky="w", padx=(0, 15))
        
        # Priority
        priority_label = ctk.CTkLabel(override_frame, text="Priority:")
        priority_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.priority_var = ctk.StringVar(value="normal")
        priority_menu = ctk.CTkOptionMenu(
            override_frame,
            variable=self.priority_var,
            values=["low", "normal", "high"],
            width=100
        )
        priority_menu.grid(row=0, column=2, padx=5)
    
    def browse_source(self):
        """Browse for source file"""
        file_path = filedialog.askopenfilename(
            title="Select YAML Configuration File",
            filetypes=[
                ("YAML files", "*.yaml"),
                ("YAML files", "*.yml"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            # Use relative or absolute path based on toggle
            if self.relative_path_var.get():
                display_path = self.get_relative_path(file_path)
            else:
                display_path = file_path
            
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, display_path)
    
    def toggle_relative_path(self):
        """Toggle between relative and absolute paths"""
        current_path = self.source_entry.get().strip()
        if not current_path:
            return
        
        try:
            main_app = self.get_main_app()
            if not main_app or not hasattr(main_app, 'current_file_path') or not main_app.current_file_path:
                return
            
            current_dir = os.path.dirname(main_app.current_file_path)
            
            if self.relative_path_var.get():
                # Switch to relative path
                if os.path.isabs(current_path):
                    relative_path = os.path.relpath(current_path, current_dir)
                    self.source_entry.delete(0, "end")
                    self.source_entry.insert(0, relative_path)
            else:
                # Switch to absolute path
                if not os.path.isabs(current_path):
                    absolute_path = os.path.abspath(os.path.join(current_dir, current_path))
                    self.source_entry.delete(0, "end")
                    self.source_entry.insert(0, absolute_path)
        except Exception as e:
            print(f"Error toggling path: {e}")
    
    def get_relative_path(self, file_path):
        """Convert absolute path to relative path if possible"""
        try:
            # Get main app reference through widget hierarchy
            main_app = self.get_main_app()
            if main_app and hasattr(main_app, 'current_file_path') and main_app.current_file_path:
                # Get directory of current file
                current_dir = os.path.dirname(main_app.current_file_path)
                # Calculate relative path
                relative_path = os.path.relpath(file_path, current_dir)
                return relative_path
        except Exception:
            pass
        
        # Return absolute path if relative conversion fails
        return file_path
    
    def get_main_app(self):
        """Get reference to main app through widget hierarchy"""
        widget = self
        while widget:
            if hasattr(widget, 'current_file_path'):
                return widget
            widget = getattr(widget, 'master', None)
        return None
    
    def open_source_file(self):
        """Open the source file"""
        source_path = self.source_entry.get().strip()
        if not source_path:
            messagebox.showwarning("No File", "Please specify a source file path first.")
            return
        
        try:
            # Get main app reference
            main_app = self.get_main_app()
            if not main_app:
                messagebox.showerror("Error", "Could not access main application.")
                return
            
            # Resolve path (handle relative paths)
            if not os.path.isabs(source_path) and main_app.current_file_path:
                # Relative to current file
                current_dir = os.path.dirname(main_app.current_file_path)
                full_path = os.path.abspath(os.path.join(current_dir, source_path))
            else:
                full_path = source_path
            
            # Check if file exists
            if not os.path.exists(full_path):
                messagebox.showerror("File Not Found", f"The file '{full_path}' does not exist.")
                return
            
            # Open in main app as a tab
            if hasattr(main_app, 'open_file_as_tab'):
                success = main_app.open_file_as_tab(full_path)
                if not success:
                    messagebox.showerror("Error", f"Failed to open '{os.path.basename(full_path)}'.")
            else:
                # Fallback to old method
                main_app.load_yaml_file(full_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def remove_self(self):
        """Remove this extends card"""
        print(f"remove extends card, section: {self.section}")
        if self.section and hasattr(self.section, 'remove_extends_card'):
            self.section.remove_extends_card(self)
        elif hasattr(self.master, 'remove_extends_card'):
            self.master.remove_extends_card(self)
        else:
            # Fallback: just destroy the widget
            self.destroy()
    
    def get_data(self):
        """Get extends data"""
        source = self.source_entry.get().strip()
        if not source:
            return None
        
        # If only source is specified with default options, return just the string
        if (not self.override_var.get() and 
            self.priority_var.get() == "normal"):
            return source
        
        # If additional options are specified, return object format
        extends_data = {'source': source}
        
        if self.override_var.get():
            extends_data['override'] = True
        
        priority = self.priority_var.get()
        if priority != "normal":
            extends_data['priority'] = priority
        
        return extends_data
    
    def load_data(self, extends_data):
        """Load data into the extends card"""
        if isinstance(extends_data, str):
            # Simple string format
            source = extends_data
            override = False
            priority = "normal"
        elif isinstance(extends_data, dict):
            # Object format
            source = extends_data.get('source', '')
            override = extends_data.get('override', False)
            priority = extends_data.get('priority', 'normal')
        else:
            return
        
        self.source_entry.delete(0, "end")
        self.source_entry.insert(0, source)
        
        self.override_var.set(override)
        self.priority_var.set(priority)


class ExtendsSection(ctk.CTkFrame):
    """Extends section with inheritance configuration"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize extends cards
        self.extends_cards = []
        
        # Initialize change callback
        self.change_callback = None
        
        # Create widgets
        self.create_widgets()
    
    def set_change_callback(self, callback):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def create_widgets(self):
        """Create extends section widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="EXTENDS Section",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Description
        desc_frame = ctk.CTkFrame(self)
        desc_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        desc_frame.grid_columnconfigure(0, weight=1)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Configure inheritance from other YAML configuration files:",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        desc_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)
        
        # Examples info
        examples_text = (
            "• Local file: /path/to/config.yaml or ./relative/config.yaml\n"
            "• Remote URL: https://example.com/config.yaml\n"
            "• Priority determines override precedence (high > normal > low)\n"
            "• Use 📍 button to toggle between relative and absolute paths"
        )
        examples_label = ctk.CTkLabel(
            desc_frame,
            text=examples_text,
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray60"),
            justify="left"
        )
        examples_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 15))
        
        # Extends container
        extends_container = ctk.CTkFrame(self)
        extends_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        extends_container.grid_columnconfigure(0, weight=1)
        extends_container.grid_rowconfigure(1, weight=1)
        
        # Header with add button
        header_frame = ctk.CTkFrame(extends_container, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        extends_label = ctk.CTkLabel(
            header_frame,
            text="Inheritance Configuration:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        extends_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Add Extends",
            command=self.add_extends,
            height=35
        )
        add_btn.grid(row=0, column=1, padx=15, pady=10)
        
        # Extends content area
        self.extends_content = ctk.CTkScrollableFrame(extends_container)
        self.extends_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.extends_content.grid_columnconfigure(0, weight=1)
        
        # Empty state message
        self.empty_label = ctk.CTkLabel(
            self.extends_content,
            text="No inheritance configured.\nClick 'Add Extends' to inherit from other configurations.",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        self.empty_label.grid(row=0, column=0, pady=50)
        
        # Advanced options
        self.create_advanced_options(extends_container)
    
    def create_advanced_options(self, parent):
        """Create advanced extends options"""
        advanced_frame = ctk.CTkFrame(parent)
        advanced_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        advanced_frame.grid_columnconfigure((1, 2), weight=1)
        
        # Advanced options title
        advanced_label = ctk.CTkLabel(
            advanced_frame,
            text="Advanced Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        advanced_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(15, 10))
        
        # Merge strategy
        merge_label = ctk.CTkLabel(advanced_frame, text="Merge Strategy:")
        merge_label.grid(row=1, column=0, sticky="w", padx=(15, 5), pady=5)
        
        self.merge_strategy_var = ctk.StringVar(value="deep")
        merge_menu = ctk.CTkOptionMenu(
            advanced_frame,
            variable=self.merge_strategy_var,
            values=["shallow", "deep", "replace"],
            width=120
        )
        merge_menu.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Conflict resolution
        conflict_label = ctk.CTkLabel(advanced_frame, text="Conflict Resolution:")
        conflict_label.grid(row=1, column=2, sticky="w", padx=(15, 5), pady=5)
        
        self.conflict_var = ctk.StringVar(value="auto")
        conflict_menu = ctk.CTkOptionMenu(
            advanced_frame,
            variable=self.conflict_var,
            values=["auto", "manual", "skip"],
            width=120
        )
        conflict_menu.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Options checkboxes
        options_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        options_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=15, pady=(10, 15))
        
        # Validate sources
        self.validate_sources_var = ctk.BooleanVar(value=True)
        validate_cb = ctk.CTkCheckBox(
            options_frame,
            text="Validate Sources",
            variable=self.validate_sources_var
        )
        validate_cb.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Cache remote
        self.cache_remote_var = ctk.BooleanVar(value=True)
        cache_cb = ctk.CTkCheckBox(
            options_frame,
            text="Cache Remote Files",
            variable=self.cache_remote_var
        )
        cache_cb.grid(row=0, column=1, sticky="w", padx=20)
        
        # Allow circular
        self.allow_circular_var = ctk.BooleanVar(value=False)
        circular_cb = ctk.CTkCheckBox(
            options_frame,
            text="Allow Circular References",
            variable=self.allow_circular_var
        )
        circular_cb.grid(row=0, column=2, sticky="w", padx=20)
    
    def add_extends(self):
        """Add new extends card"""
        # Hide empty label if visible
        if self.extends_cards == []:
            self.empty_label.grid_forget()
        
        card = ExtendsCard(self.extends_content, section=self)
        self.extends_cards.append(card)
        self.refresh_extends_display()
        
        # Notify about change
        self.notify_change()
    
    def remove_extends_card(self, card):
        """Remove an extends card"""
        if card in self.extends_cards:
            self.extends_cards.remove(card)
            card.destroy()
            self.refresh_extends_display()
            
            # Notify about change
            self.notify_change()
        
        # Show empty label if no cards
        if not self.extends_cards:
            self.empty_label.grid(row=0, column=0, pady=50)
    
    def refresh_extends_display(self):
        """Refresh the display of extends cards"""
        for i, card in enumerate(self.extends_cards):
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
    
    def validate_configuration(self) -> bool:
        """Validate extends configuration"""
        if not self.extends_cards:
            return True
        
        # Check for valid sources
        if self.validate_sources_var.get():
            for i, card in enumerate(self.extends_cards):
                data = card.get_data()
                if data:
                    if isinstance(data, str):
                        source = data
                    elif isinstance(data, dict):
                        source = data.get('source', '')
                    else:
                        continue
                    
                    # Check if local file exists
                    if not source.startswith(('http://', 'https://')):
                        if not os.path.exists(source):
                            result = messagebox.askyesno(
                                "Validation Warning",
                                f"Source file not found: '{source}'\nfor extends #{i+1}\n\nContinue anyway?"
                            )
                            if not result:
                                return False
        
        return True
    
    def get_data(self) -> dict:
        """Get all extends data"""
        if not self.extends_cards:
            return {}
        
        extends_list = []
        
        # Get extends configurations as a list
        for card in self.extends_cards:
            data = card.get_data()
            if data is not None:
                extends_list.append(data)
        
        if not extends_list:
            return {}
        
        # Return just the extends list - the main app will wrap it in the prompt structure
        return extends_list
    
    def load_data(self, data):
        """Load data into extends section"""
        # Clear existing
        self.clear()
        
        # Handle the new list format
        if isinstance(data, list):
            # Direct list of extends items
            for item in data:
                card = ExtendsCard(self.extends_content, section=self)
                card.load_data(item)
                self.extends_cards.append(card)
        elif isinstance(data, dict):
            # Handle legacy dict format for backward compatibility
            extends_data = data.get('extends', [])
            if isinstance(extends_data, list):
                for item in extends_data:
                    card = ExtendsCard(self.extends_content, section=self)
                    card.load_data(item)
                    self.extends_cards.append(card)
            elif isinstance(extends_data, dict):
                # Old dict format {name: config}
                for name, config in extends_data.items():
                    card = ExtendsCard(self.extends_content, section=self)
                    if isinstance(config, dict):
                        card.load_data(config)
                    else:
                        card.load_data(config)  # String format
                    self.extends_cards.append(card)
        
        # Refresh display
        if self.extends_cards:
            self.empty_label.grid_forget()
            self.refresh_extends_display()
        else:
            self.empty_label.grid(row=0, column=0, pady=50)
    
    def clear(self):
        """Clear all extends data"""
        for card in self.extends_cards:
            card.destroy()
        self.extends_cards.clear()
        
        # Reset advanced options
        self.merge_strategy_var.set("deep")
        self.conflict_var.set("auto")
        self.validate_sources_var.set(True)
        self.cache_remote_var.set(True)
        self.allow_circular_var.set(False)
        
        # Show empty label
        self.empty_label.grid(row=0, column=0, pady=50)
    
    def get_extends_count(self) -> int:
        """Get number of configured extends"""
        return len([card for card in self.extends_cards if card.get_data() is not None])
    
    def has_remote_sources(self) -> bool:
        """Check if any extends use remote sources"""
        for card in self.extends_cards:
            data = card.get_data()
            if data:
                _, extends_data = data
                source = extends_data.get('source', '')
                if source.startswith(('http://', 'https://')):
                    return True
        return False
