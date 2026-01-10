"""
PEaC GUI - CustomTkinter Implementation
Modern, responsive GUI for Prompt Engineering as Code
"""
import traceback
import customtkinter as ctk
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

def debug_print(*args, **kwargs):
    print(*args, **kwargs)

# Add peac to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from peac.core.peac import PromptYaml
from peac.gui_ctk.components.context_section import ContextSection
from peac.gui_ctk.components.output_section import OutputSection
from peac.gui_ctk.components.extends_section import ExtendsSection
from peac.gui_ctk.components.instruction_section import InstructionSection


class PeacApp(ctk.CTk):
    """Main PEaC Application with CustomTkinter"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PEaC - Prompt Engineering as Code")
        self.geometry("1400x900")
        self.minsize(1000, 600)
        
        # Set light theme Facebook style
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Facebook-inspired color palette
        self.colors = {
            'bg_dark': '#ffffff',
            'bg_medium': '#f0f2f5',
            'bg_light': '#e4e6eb',
            'accent': '#1877f2',
            'accent_hover': '#166fe5',
            'success': '#42b72a',
            'warning': '#f59e0b',
            'error': '#dc2626',
            'text_primary': '#050505',
            'text_secondary': '#3a3b3c',
            'border': '#dadde1'
        }
        
        # Configure grid layout (responsive)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.configure(fg_color=self.colors['bg_medium'])
        
        # Initialize multi-file data structures
        self.current_file_path = None  # Current active file
        self.open_files = {}  # Dictionary to store data for each open file
        self.file_tabs = {}  # Dictionary to store tab widgets for each file
        self.yaml_data = {}
        self.file_state = "SYNCED"  # "SYNCED" or "EDITED"
        self.original_data = {}  # Store original loaded data for comparison
        
        # Create GUI elements
        self.create_toolbar()
        self.create_main_content()
        self.create_status_bar()
        
        # Load last file if exists or create new file
        self.load_last_file()
        if not self.open_files:
            self.new_file()
    
    def create_toolbar(self):
        """Create responsive toolbar"""
        toolbar_frame = ctk.CTkFrame(
            self, 
            height=70,
            fg_color=self.colors['bg_medium'],
            corner_radius=12
        )
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))
        toolbar_frame.grid_columnconfigure(1, weight=1)  # Spacer
        
        # Left side buttons
        left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # File operations with modern styling
        new_btn = ctk.CTkButton(
            left_frame,
            text="✨ New",
            width=90,
            height=38,
            command=self.new_file,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        new_btn.grid(row=0, column=0, padx=(0, 8))
        
        open_btn = ctk.CTkButton(
            left_frame,
            text="📁 Open",
            width=90,
            height=38,
            command=self.open_file,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        open_btn.grid(row=0, column=1, padx=8)
        
        save_btn = ctk.CTkButton(
            left_frame,
            text="💾 Save",
            width=90,
            height=38,
            command=self.save_file,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        save_btn.grid(row=0, column=2, padx=8)
        self.save_btn = save_btn  # Store reference for enable/disable
        
        # Center filename display with modern styling
        self.filename_label = ctk.CTkLabel(
            toolbar_frame,
            text="No file loaded",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.filename_label.grid(row=0, column=1, pady=12)
        
        # Right side buttons
        right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        
        self.preview_btn = ctk.CTkButton(
            right_frame,
            text="👁 Preview",
            width=110,
            height=38,
            command=self.preview_prompt,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        self.preview_btn.grid(row=0, column=0, padx=8)
        
        self.copy_btn = ctk.CTkButton(
            right_frame,
            text="📋 Copy",
            width=110,
            height=38,
            command=self.copy_prompt,
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_hover'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white"
        )
        self.copy_btn.grid(row=0, column=1, padx=(8, 0))
        
        # Initially disable preview and copy buttons
        self.update_action_buttons_state()
    
    def create_main_content(self):
        """Create main content area with file tabs and content tabs"""
        # Main container with modern styling
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['bg_medium'],
            corner_radius=12
        )
        main_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(8, 15))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)  # Content area gets weight (moved to row 3)
        
        # File tabs bar (row 0)
        self.create_file_tabs_bar(main_frame)
        
        # Query field (row 1)
        self.create_query_field(main_frame)
        
        # Content tabs header (row 2) with modern styling
        tab_frame = ctk.CTkFrame(
            main_frame, 
            height=55,
            fg_color=self.colors['bg_light'],
            corner_radius=10
        )
        tab_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(8, 8))
        tab_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)  # Added one column for Instruction
        
        # Tab buttons
        self.tab_buttons = {}
        self.create_tab_button(tab_frame, "YAML", 0, self.show_yaml_tab)
        self.create_tab_button(tab_frame, "Instruction", 1, self.show_instruction_tab)
        self.create_tab_button(tab_frame, "Context", 2, self.show_context_tab)
        self.create_tab_button(tab_frame, "Output", 3, self.show_output_tab)
        self.create_tab_button(tab_frame, "Extends", 4, self.show_extends_tab)
        
        # Content area (row 3) with modern styling
        self.content_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors['bg_dark'],
            corner_radius=10
        )
        self.content_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=(8, 12))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create tab contents
        self.create_tab_contents()
        
        # Set up change tracking
        self.setup_change_tracking()
        
        # Show initial tab
        self.current_tab = "YAML"
        self.show_yaml_tab()
    
    def create_status_bar(self):
        """Create status bar for informative messages"""
        self.status_frame = ctk.CTkFrame(
            self, 
            height=40,
            fg_color=self.colors['bg_medium'],
            corner_radius=10
        )
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=self.colors['text_secondary']
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=15, pady=8)
        
        # Initially hide the status bar
        self.status_frame.grid_remove()
    
    def show_status_message(self, message: str, duration: int = 2000):
        """Show a temporary status message that disappears after duration (ms)"""
        self.status_label.configure(text=message)
        self.status_frame.grid()  # Show the status bar
        
        # Hide the status bar after the specified duration
        self.after(duration, self.hide_status_message)
    
    def hide_status_message(self):
        """Hide the status message"""
        self.status_frame.grid_remove()
        self.status_label.configure(text="")
    
    def set_status(self, message: str, status_type: str = "normal"):
        """Set status message with different types"""
        if message:
            if status_type == "error":
                self.status_label.configure(text=message, text_color="red")
            elif status_type == "success":
                self.status_label.configure(text=message, text_color="green")
            else:
                self.status_label.configure(text=message, text_color=("gray50", "gray60"))
            self.status_frame.grid()  # Show the status bar
        else:
            self.status_frame.grid_remove()
            self.status_label.configure(text="")
    
    def create_query_field(self, parent):
        """Create the query input field above the tabs"""
        query_frame = ctk.CTkFrame(
            parent, 
            height=70,
            fg_color=self.colors['bg_light'],
            corner_radius=10
        )
        query_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(8, 8))
        query_frame.grid_columnconfigure(1, weight=1)
        
        # Query label with modern styling
        query_label = ctk.CTkLabel(
            query_frame,
            text="💬 Query:",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=80,
            text_color=self.colors['text_primary']
        )
        query_label.grid(row=0, column=0, sticky="w", padx=(15, 8), pady=12)
        
        # Query text entry with modern styling
        self.query_entry = ctk.CTkEntry(
            query_frame,
            placeholder_text="Enter your query here...",
            font=ctk.CTkFont(size=12),
            height=40,
            fg_color="white",
            border_color=self.colors['border'],
            corner_radius=8,
            text_color=self.colors['text_primary']
        )
        self.query_entry.grid(row=0, column=1, sticky="ew", padx=(8, 15), pady=12)

    def create_file_tabs_bar(self, parent):
        """Create the file tabs bar at the top"""
        file_tabs_frame = ctk.CTkFrame(
            parent, 
            height=50,
            fg_color="transparent"
        )
        file_tabs_frame.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        file_tabs_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame for file tabs
        self.file_tabs_scroll = ctk.CTkScrollableFrame(
            file_tabs_frame, 
            height=35,
            orientation="horizontal"
        )
        self.file_tabs_scroll.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.file_tabs_scroll.grid_columnconfigure(0, weight=1)
        
        # Add new file button
        new_file_btn = ctk.CTkButton(
            file_tabs_frame,
            text="+ New",
            width=70,
            height=30,
            command=self.new_file,
            fg_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            hover_color=("gray60", "gray40"),
            font=ctk.CTkFont(size=11)
        )
        new_file_btn.grid(row=0, column=1, padx=(5, 10), pady=5)
    
    def create_tab_button(self, parent, text, column, command):
        """Create a tab button with modern styling"""
        # Map tab names to icons
        icons = {
            'YAML': '📄',
            'Instruction': '📝',
            'Context': '📚',
            'Output': '📤',
            'Extends': '🔗'
        }
        
        icon = icons.get(text, '')
        display_text = f"{icon} {text}" if icon else text
        
        btn = ctk.CTkButton(
            parent,
            text=display_text,
            height=40,
            command=command,
            fg_color="transparent",
            text_color=self.colors['text_secondary'],
            hover_color=self.colors['bg_dark'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        btn.grid(row=0, column=column, padx=6, pady=8, sticky="ew")
        self.tab_buttons[text] = btn
    
    def create_tab_contents(self):
        """Create all tab content widgets"""
        # YAML section
        self.create_yaml_section()
        
        # Instruction section scrollable wrapper
        self.instruction_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.instruction_scroll.grid_columnconfigure(0, weight=1)
        self.instruction_section = InstructionSection(self.instruction_scroll)
        self.instruction_section.set_change_callback(self.on_section_changed)
        self.instruction_section.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Create scrollable frames for each section
        # Context section scrollable wrapper
        self.context_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.context_scroll.grid_columnconfigure(0, weight=1)
        self.context_section = ContextSection(self.context_scroll)
        self.context_section.set_change_callback(self.on_section_changed)
        self.context_section.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Output section scrollable wrapper
        self.output_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.output_scroll.grid_columnconfigure(0, weight=1)
        self.output_section = OutputSection(self.output_scroll)
        self.output_section.set_change_callback(self.on_section_changed)
        self.output_section.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Extends section scrollable wrapper
        self.extends_scroll = ctk.CTkScrollableFrame(self.content_frame)
        self.extends_scroll.grid_columnconfigure(0, weight=1)
        self.extends_section = ExtendsSection(self.extends_scroll)
        self.extends_section.set_change_callback(self.on_section_changed)
        self.extends_section.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    def create_file_tab(self, file_path: str):
        """Create a file tab"""
        filename = os.path.basename(file_path) if file_path and not file_path.startswith("Untitled-") else file_path
        
        # Create tab container
        tab_container = ctk.CTkFrame(self.file_tabs_scroll, fg_color="transparent")
        tab_container.pack(side="left", padx=2, pady=2)
        
        # Create tab button
        tab_btn = ctk.CTkButton(
            tab_container,
            text=filename,
            height=30,
            width=120,
            command=lambda: self.switch_to_file(file_path),
            fg_color=("gray80", "gray25"),
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray35"),
            font=ctk.CTkFont(size=11)
        )
        tab_btn.pack(side="left")
        
        # Create close button
        close_btn = ctk.CTkButton(
            tab_container,
            text="✕",
            width=25,
            height=30,
            command=lambda: self.close_file_tab(file_path),
            fg_color="transparent",
            text_color=("gray50", "gray70"),
            hover_color=("red", "darkred"),
            font=ctk.CTkFont(size=10)
        )
        close_btn.pack(side="left", padx=(2, 0))
        
        # Store tab widgets
        self.file_tabs[file_path] = {
            'container': tab_container,
            'button': tab_btn,
            'close': close_btn
        }
        
        return tab_btn
    
    def switch_to_file(self, file_path: str):
        """Switch to a different open file"""
        if file_path not in self.open_files:
            debug_print(f"File not in open_files: {file_path}")
            return
            
        debug_print(f"Switching to file: {file_path}")
        
        # Save current file state
        if self.current_file_path and self.current_file_path in self.open_files:
            debug_print(f"Saving current file state: {self.current_file_path}")
            self.save_current_file_state()
        
        # Switch to new file
        old_file_path = self.current_file_path
        self.current_file_path = file_path
        debug_print(f"Loading file state for: {file_path}")
        self.load_file_state(file_path)
        
        # Update UI
        self.update_file_tab_appearances()
        self.update_filename_display()
        self.update_action_buttons_state()
        
        debug_print(f"Successfully switched from {old_file_path} to {file_path}")
    
    def close_file_tab(self, file_path: str):
        """Close a file tab"""
        if file_path not in self.open_files:
            return
        
        # Check if file has unsaved changes
        file_data = self.open_files[file_path]
        if file_data.get('state') == 'EDITED':
            from tkinter import messagebox
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                f"Save changes to {os.path.basename(file_path) if file_path and not file_path.startswith('Untitled-') else file_path}?"
            )
            if result is True:  # Save
                self.switch_to_file(file_path)
                self.save_file()
            elif result is None:  # Cancel
                return
        
        # Remove from open files
        del self.open_files[file_path]
        
        # Remove tab
        if file_path in self.file_tabs:
            self.file_tabs[file_path]['container'].destroy()
            del self.file_tabs[file_path]
        
        # Switch to another file if this was current
        if self.current_file_path == file_path:
            if self.open_files:
                # Switch to first available file
                next_file = list(self.open_files.keys())[0]
                self.switch_to_file(next_file)
            else:
                # No files open, create new
                self.new_file()
    
    def update_file_tab_appearances(self):
        """Update file tab appearances to show which is active"""
        for file_path, tab_widgets in self.file_tabs.items():
            if file_path == self.current_file_path:
                # Active tab
                tab_widgets['button'].configure(
                    fg_color=("blue", "darkblue"),
                    text_color="white"
                )
            else:
                # Inactive tab
                tab_widgets['button'].configure(
                    fg_color=("gray80", "gray25"),
                    text_color=("gray10", "gray90")
                )
            
            # Show unsaved indicator
            if file_path in self.open_files:
                file_data = self.open_files[file_path]
                filename = os.path.basename(file_path) if file_path and not file_path.startswith("Untitled-") else file_path
                if file_data.get('state') == 'EDITED':
                    tab_widgets['button'].configure(text=f"{filename} *")
                else:
                    tab_widgets['button'].configure(text=filename)
    
    def save_current_file_state(self):
        """Save current GUI state to the open file data"""
        if self.current_file_path and self.current_file_path in self.open_files:
            file_data = self.open_files[self.current_file_path]
            file_data['gui_data'] = self.collect_data()
            file_data['state'] = self.file_state
            file_data['original_data'] = self.original_data.copy()
            file_data['yaml_data'] = self.yaml_data.copy()
    
    def load_file_state(self, file_path: str):
        """Load file state into the GUI"""
        if file_path not in self.open_files:
            debug_print(f"load_file_state: File not found in open_files: {file_path}")
            return
            
        file_data = self.open_files[file_path]
        debug_print(f"load_file_state: Loading data for {file_path}")
        
        # Load data
        self.yaml_data = file_data.get('yaml_data', {})
        self.file_state = file_data.get('state', 'SYNCED')
        self.original_data = file_data.get('original_data', {})
        
        debug_print(f"load_file_state: yaml_data keys: {list(self.yaml_data.keys())}")
        
        # Update current file path in sections
        self.context_section.set_current_file_path(file_path)
        self.output_section.set_current_file_path(file_path)
        
        # Update UI
        gui_data = file_data.get('gui_data', {})
        debug_print(f"load_file_state: Using {'gui_data' if gui_data else 'yaml_data'} to update UI")
        
        if gui_data:
            self.update_ui_from_data_dict(gui_data)
        else:
            self.update_ui_from_data()
        
        # Update YAML display
        yaml_content = file_data.get('yaml_content', '')
        if yaml_content and hasattr(self, 'yaml_text'):
            self.enable_yaml_textbox()
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml_content)
            self.disable_yaml_textbox()
            
        debug_print(f"load_file_state: Completed loading {file_path}")
    
    def update_ui_from_data_dict(self, data: dict):
        """Update UI from data dictionary"""
        if not data:
            return
            
        # Update instruction section
        instruction_data = data.get('instruction', {})
        self.instruction_section.load_data(instruction_data)
            
        # Update sections
        context_data = data.get('context', {})
        self.context_section.load_data(context_data)
        
        output_data = data.get('output', {})
        self.output_section.load_data(output_data)
        
        extends_data = data.get('extends', [])
        self.extends_section.load_data(extends_data)
        
        # Update query
        query = data.get('query', '')
        if hasattr(self, 'query_entry'):
            self.query_entry.delete(0, "end")
            self.query_entry.insert(0, query)
    
    def update_yaml_title(self):
        self.yaml_title.configure(text=f"{self.file_name}")


    def create_yaml_section(self):
        """Create YAML editor section with modern styling"""
        self.yaml_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.yaml_frame.grid_columnconfigure(0, weight=1)
        self.yaml_frame.grid_rowconfigure(1, weight=1)
        
        # Title with modern styling
        self.yaml_title = ctk.CTkLabel(
            self.yaml_frame,
            text="📄 YAML Editor",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.yaml_title.grid(row=0, column=0, pady=(15, 10), sticky="w", padx=15)

        # YAML text area with modern styling
        self.yaml_text = ctk.CTkTextbox(
            self.yaml_frame,
            wrap="none",
            font=ctk.CTkFont(family="Menlo", size=12),
            fg_color="white",
            border_color=self.colors['border'],
            corner_radius=8,
            border_width=1,
            text_color=self.colors['text_primary']
        )
        self.yaml_text.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 15))
        
        # Sync button
        # sync_btn = ctk.CTkButton(
        #     self.yaml_frame,
        #     text="↻ Sync with GUI",
        #     command=self.sync_yaml_to_gui,
        #     width=150
        # )
        # sync_btn.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")
    
    def sync_yaml_to_gui(self):
        """Sync YAML content to GUI sections"""
        try:
            import yaml
            yaml_content = self.yaml_text.get("1.0", "end-1c").strip()
            if yaml_content:
                self.yaml_data = yaml.safe_load(yaml_content) or {}
                self.update_ui_from_data()
                self.show_info_dialog("Success", "YAML synced to GUI sections!")
            else:
                self.show_error_dialog("Error", "YAML content is empty")
        except Exception as e:
            self.show_error_dialog("YAML Error", f"Failed to parse YAML: {e}")
    
    def sync_gui_to_yaml(self):
        """Sync GUI sections to YAML content"""
        try:
            import yaml
            data = self.collect_data()
            if data is None:  # Validation failed
                return  # Don't sync if validation failed
            
            # Wrap in PEaC format structure
            peac_data = {
                'prompt': data
            }
            
            yaml_content = yaml.dump(peac_data, default_flow_style=False, sort_keys=False)
            self.enable_yaml_textbox()
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml_content)
            self.disable_yaml_textbox()
        except Exception as e:
            self.show_error_dialog("Sync Error", f"Failed to sync GUI to YAML: {e}")
    
    def sync_yaml_to_gui_silent(self):
        """Sync YAML content to GUI sections without showing messages"""
        try:
            import yaml
            yaml_content = self.yaml_text.get("1.0", "end-1c").strip()
            if yaml_content:
                self.yaml_data = yaml.safe_load(yaml_content) or {}
                self.update_ui_from_data()
        except Exception:
            pass  # Ignore errors in silent sync
    
    def setup_change_tracking(self):
        """Set up change tracking for all GUI components"""
        def on_change(*args):
            # Debounce change detection with a small delay
            if hasattr(self, '_change_timer'):
                self.after_cancel(self._change_timer)
            self._change_timer = self.after(500, self.check_for_changes)  # 500ms delay
        
        def on_query_change(*args):
            # Query changes don't affect file state - just update buttons
            if hasattr(self, '_query_change_timer'):
                self.after_cancel(self._query_change_timer)
            self._query_change_timer = self.after(100, self.update_action_buttons_state)
        
        # Track changes in query entry (doesn't mark file as edited)
        if hasattr(self, 'query_entry'):
            self.query_entry.bind('<KeyRelease>', lambda e: on_query_change())
            self.query_entry.bind('<Button-1>', lambda e: on_query_change())
        
        # Track changes in context section base rules
        if hasattr(self, 'context_section') and hasattr(self.context_section, 'base_rules_text'):
            self.context_section.base_rules_text.bind('<KeyRelease>', lambda e: on_change())
            self.context_section.base_rules_text.bind('<Button-1>', lambda e: on_change())
        
        # Track changes in output section base rules
        if hasattr(self, 'output_section') and hasattr(self.output_section, 'base_rules_text'):
            self.output_section.base_rules_text.bind('<KeyRelease>', lambda e: on_change())
            self.output_section.base_rules_text.bind('<Button-1>', lambda e: on_change())
        
        # Note: For more complex change tracking in rule cards and other components,
        # we would need to add methods to the component classes themselves
    
    def on_section_changed(self):
        """Called when any section is modified"""
        # Debounce change detection with a small delay
        if hasattr(self, '_change_timer'):
            self.after_cancel(self._change_timer)
        self._change_timer = self.after(300, self.check_for_changes)  # 300ms delay
        
        # Also debounce validation check
        if hasattr(self, '_validation_timer'):
            self.after_cancel(self._validation_timer)
        self._validation_timer = self.after(500, self.check_validation)  # 500ms delay for validation
    
    def check_validation(self):
        """Check validation and update UI accordingly"""
        # Collect data to trigger validation
        self.collect_data()
    
    def show_yaml_tab(self):
        """Show YAML tab"""
        self.hide_all_tabs()
        self.yaml_frame.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("YAML")
        # Auto-sync GUI to YAML when showing YAML tab
        self.sync_gui_to_yaml()
    
    def show_instruction_tab(self):
        """Show instruction tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.instruction_scroll.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Instruction")
    
    def show_context_tab(self):
        """Show context tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.context_scroll.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Context")
    
    def show_output_tab(self):
        """Show output tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.output_scroll.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Output")
    
    def show_extends_tab(self):
        """Show extends tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.extends_scroll.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Extends")
    
    def hide_all_tabs(self):
        """Hide all tab contents"""
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
    
    def update_tab_appearance(self, active_tab):
        """Update tab button appearance with modern styling"""
        for tab_name, button in self.tab_buttons.items():
            if tab_name == active_tab:
                button.configure(
                    fg_color=self.colors['accent'],
                    text_color=self.colors['text_primary'],
                    font=ctk.CTkFont(size=13, weight="bold")
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=self.colors['text_secondary'],
                    font=ctk.CTkFont(size=13, weight="bold")
                )
        self.current_tab = active_tab
    
    def update_filename_display(self):
        """Update the filename label in toolbar"""
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path) if not self.current_file_path.startswith("Untitled-") else self.current_file_path
            self.filename_label.configure(text=filename)
        else:
            self.filename_label.configure(text="No file loaded")
    
    def update_action_buttons_state(self):
        """Enable/disable action buttons based on file state"""
        file_exists = (self.current_file_path is not None and 
                      not self.current_file_path.startswith("Untitled-") and
                      os.path.exists(self.current_file_path))
        
        # Buttons are enabled when file exists (no longer require SYNCED state)
        buttons_enabled = file_exists
        
        if hasattr(self, 'preview_btn'):
            if buttons_enabled:
                self.preview_btn.configure(state="normal")
            else:
                self.preview_btn.configure(state="disabled")
        
        if hasattr(self, 'copy_btn'):
            if buttons_enabled:
                self.copy_btn.configure(state="normal")
            else:
                self.copy_btn.configure(state="disabled")
                
        # Update window title to show state
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path) if not self.current_file_path.startswith("Untitled-") else self.current_file_path
            if self.file_state == "EDITED":
                title = f"PEaC - {filename} *"
            else:
                title = f"PEaC - {filename}"
        else:
            title = "PEaC - Prompt Engineering as Code"
        self.title(title)
    
    def mark_as_edited(self):
        """Mark file as edited (unsaved changes)"""
        if self.file_state != "EDITED":
            self.file_state = "EDITED"
            self.update_action_buttons_state()
    
    def mark_as_synced(self):
        """Mark file as synced (saved)"""
        if self.file_state != "SYNCED":
            self.file_state = "SYNCED"
            self.update_action_buttons_state()
    
    def check_for_changes(self):
        """Check if current GUI data differs from original loaded data"""
        try:
            current_data = self.collect_data()
            if current_data != self.original_data:
                self.mark_as_edited()
            else:
                self.mark_as_synced()
        except Exception:
            # If there's an error collecting data, assume it's been edited
            self.mark_as_edited()
    
    def mark_as_edited(self):
        """Mark file as edited (unsaved changes)"""
        if self.file_state != "EDITED":
            self.file_state = "EDITED"
            self.update_action_buttons_state()
            self.update_file_tab_appearances()
    
    def mark_as_synced(self):
        """Mark file as synced (saved)"""
        if self.file_state != "SYNCED":
            self.file_state = "SYNCED"
            self.update_action_buttons_state()
            self.update_file_tab_appearances()
    
    def new_file(self, add_tab=True):
        """Create a new file"""
        # Save current file state if exists
        if self.current_file_path and self.current_file_path in self.open_files:
            self.save_current_file_state()
        
        # Create new file
        file_counter = 1
        while True:
            new_file_path = f"Untitled-{file_counter}"
            if new_file_path not in self.open_files:
                break
            file_counter += 1
        
        # Reset data
        self.yaml_data = {}
        self.original_data = {}
        self.file_state = "SYNCED"
        self.current_file_path = new_file_path
        
        # Add to open files
        self.open_files[new_file_path] = {
            'yaml_data': {},
            'yaml_content': '',
            'gui_data': {},
            'state': 'SYNCED',
            'original_data': {}
        }
        
        # Create tab if requested
        if add_tab:
            self.create_file_tab(new_file_path)
            self.update_file_tab_appearances()
        
        # Clear all sections
        self.clear_all_sections()
        
        # Update UI
        self.update_filename_display()
        self.update_action_buttons_state()
        self.show_yaml_tab()
    
    def open_file(self):
        """Open existing YAML file"""
        from tkinter import filedialog
        
        import os
        file_path = filedialog.askopenfilename(
            title="Open PEaC Configuration",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            self.open_file_in_new_tab(file_path)
    
    def open_file_in_new_tab(self, file_path: str):
        """Open a file in a new tab"""
        # Check if file is already open
        if file_path in self.open_files:
            self.switch_to_file(file_path)
            return
        
        # Save current file state
        if self.current_file_path and self.current_file_path in self.open_files:
            self.save_current_file_state()
        
        # Load the file
        self.load_yaml_file(file_path, create_tab=True)

    def save_file(self):
        """Save current configuration"""
        if self.current_file_path and not self.current_file_path.startswith("Untitled-"):
            self.save_yaml_file(self.current_file_path)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save configuration with new filename"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            title="Save PEaC Configuration",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if file_path:
            old_file_path = self.current_file_path
            self.save_yaml_file(file_path)
            
            # Update multi-file system for renamed file
            if old_file_path and old_file_path.startswith("Untitled-") and old_file_path != file_path:
                self.rename_file_in_multi_file_system(old_file_path, file_path)
            
            self.current_file_path = file_path
            
            # Update current file path in sections
            self.context_section.set_current_file_path(file_path)
            self.output_section.set_current_file_path(file_path)
            
            self.update_filename_display()
            self.update_action_buttons_state()
    
    def rename_file_in_multi_file_system(self, old_path: str, new_path: str):
        """Update multi-file system when a file is renamed"""
        if old_path in self.open_files:
            # Move file data to new key
            self.open_files[new_path] = self.open_files.pop(old_path)
            
        if old_path in self.file_tabs:
            # Move tab widgets to new key
            tab_widgets = self.file_tabs.pop(old_path)
            self.file_tabs[new_path] = tab_widgets
            
            # Update the lambda functions to use the new file path
            tab_widgets['button'].configure(command=lambda: self.switch_to_file(new_path))
            tab_widgets['close'].configure(command=lambda: self.close_file_tab(new_path))
            
        # Update tab appearances with new filename
        self.update_file_tab_appearances()
    
    def open_file_as_tab(self, file_path: str):
        """Open a file as a new tab in the multi-file interface"""
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False
            
            # Use the multi-file tab system
            self.open_file_in_new_tab(file_path)
            print(f"Opened: {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            print(f"Error opening file: {str(e)}")
            return False
    
    def create_processor_with_current_query(self):
        """Create a PromptYaml processor with the current query from the GUI"""
        if not self.current_file_path or not os.path.exists(self.current_file_path):
            return None
            
        # Create processor from saved file
        processor = PromptYaml(self.current_file_path)
        
        # Get current query from GUI
        current_query = ""
        if hasattr(self, 'query_entry'):
            current_query = self.query_entry.get().strip()
        
        # Update the processor's parsed_data with current query
        if 'prompt' not in processor.parsed_data:
            processor.parsed_data['prompt'] = {}
        processor.parsed_data['prompt']['query'] = current_query
        
        return processor

    def preview_prompt(self):
        """Preview generated prompt"""            
        if not self.current_file_path or not os.path.exists(self.current_file_path):
            self.show_error_dialog("Preview Error", "No file to preview. Please create or load a file first.")
            return
            
        try:
            # Create processor with current query
            processor = self.create_processor_with_current_query()
            if not processor:
                self.show_error_dialog("Preview Error", "Unable to create processor.")
                return
                
            result = processor.get_prompt_sentence()

            # Show preview window
            self.show_preview_window(result)
        except FileNotFoundError as e:
            self.show_error_dialog("Preview Error", f"Extends file not found: {str(e)}\n\nPlease check your extends paths and ensure all referenced files exist.")
        except Exception as e:
            full_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            print("Traceback (FileNotFoundError):\n", full_trace)

            tb = traceback.extract_tb(e.__traceback__)[-1]
            self.show_error_dialog(
                "Preview Error",
                f"Extends file not found: {str(e)}\n\n"
                "Please check your extends paths and ensure all referenced files exist.\n"
                f"Module: {tb.filename}\nLine: {tb.lineno}"
            )


    
    def copy_prompt(self):
        """Copy generated prompt to clipboard"""           

        if not self.current_file_path or not os.path.exists(self.current_file_path):
            self.show_error_dialog("Copy Error", "No file to copy. Please create or load a file first.")
            return
            
        try:
            # Create processor with current query
            processor = self.create_processor_with_current_query()
            if not processor:
                self.show_error_dialog("Copy Error", "Unable to create processor.")
                return
                
            result = processor.get_prompt_sentence()
            
            # Copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(result)
            
            # Show success message
            self.show_status_message("✓ Prompt copied to clipboard!")
        except FileNotFoundError as e:
            self.show_error_dialog("Copy Error", f"Extends file not found: {str(e)}\n\nPlease check your extends paths and ensure all referenced files exist.")
        except Exception as e:
            self.show_error_dialog("Copy Error", str(e))
    
    def collect_data(self) -> dict:
        """Collect data from all sections"""
        data = {}
        all_validation_errors = []
        
        # Collect from instruction section
        instruction_data = self.instruction_section.get_data()
        if instruction_data:
            data['instruction'] = instruction_data
        
        # Collect from each section
        context_data = self.context_section.get_data()
        if context_data and "_validation_errors" in context_data:
            all_validation_errors.extend([f"Context - {err}" for err in context_data["_validation_errors"]])
        elif context_data:
            data['context'] = context_data
        
        output_data = self.output_section.get_data()
        if output_data and "_validation_errors" in output_data:
            all_validation_errors.extend([f"Output - {err}" for err in output_data["_validation_errors"]])
        elif output_data:
            data['output'] = output_data
        
        extends_data = self.extends_section.get_data()
        if extends_data:
            data['extends'] = extends_data
        
        # Query
        query_text = self.query_entry.get().strip()
        if query_text:
            data['query'] = query_text
        
        # Handle validation errors
        if all_validation_errors:
            # Update status bar with validation errors
            error_message = "⚠️ Validation errors: " + "; ".join(all_validation_errors)
            self.set_status(error_message, "error")
            # Disable save button
            self.save_btn.configure(state="disabled")
            return {"_validation_errors": all_validation_errors}
        else:
            # Enable save button if no errors
            self.save_btn.configure(state="normal")
            # Clear any previous error status
            if hasattr(self, 'status_label') and "⚠️" in self.status_label.cget("text"):
                self.set_status("", "normal")
        
        return data

    def disable_yaml_textbox(self):
        """Disable YAML text box"""
        self.yaml_text.configure(state="disabled")

    def enable_yaml_textbox(self):
        """Enable YAML text box"""
        self.yaml_text.configure(state="normal")

    def load_yaml_file(self, file_path: str, create_tab: bool = True):
        """Load YAML configuration file"""
        try:
            import yaml
            with open(file_path, 'r') as f:
                yaml_content = f.read()
                yaml_data = yaml.safe_load(yaml_content) or {}
            
            # Add to open files
            self.open_files[file_path] = {
                'yaml_data': yaml_data.copy(),
                'yaml_content': yaml_content,
                'gui_data': {},
                'state': 'SYNCED',
                'original_data': {}
            }
            
            # Switch to this file
            self.current_file_path = file_path
            self.yaml_data = yaml_data
            
            # Update current file path in sections
            self.context_section.set_current_file_path(file_path)
            self.output_section.set_current_file_path(file_path)
            
            # Create tab if requested
            if create_tab:
                self.create_file_tab(file_path)
                self.update_file_tab_appearances()
            
            # Update YAML tab with raw content
            self.enable_yaml_textbox()
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml_content)
            
            self.update_ui_from_data()
            
            # Store original data for change tracking
            self.original_data = self.collect_data()
            self.open_files[file_path]['original_data'] = self.original_data.copy()
            self.mark_as_synced()  # File is synced after loading
            
            self.save_last_file(file_path)
            self.update_filename_display()
            self.update_action_buttons_state()
            self.disable_yaml_textbox()

        except Exception as e:
            self.show_error_dialog("Load Error", f"Failed to load file: {e}")
    
    def save_yaml_file(self, file_path: str):
        """Save configuration to YAML file"""
        try:
            import yaml
            
            # Always collect data from GUI sections
            data = self.collect_data()
            if data is None:  # Validation failed
                return False  # Don't save if validation failed
            if "_validation_errors" in data:  # New validation error format
                return False  # Don't save if validation failed
            
            # Wrap in PEaC format structure
            peac_data = {
                'prompt': data
            }
            
            # Save the structured YAML
            with open(file_path, 'w') as f:
                yaml.dump(peac_data, f, default_flow_style=False, sort_keys=False)
            
            # Update YAML tab with the saved content
            yaml_content = yaml.dump(peac_data, default_flow_style=False, sort_keys=False)
            self.enable_yaml_textbox()
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml_content)
            self.disable_yaml_textbox()
            
            self.current_file_path = file_path
            
            # Update multi-file system
            if file_path in self.open_files:
                self.open_files[file_path]['original_data'] = data.copy()
                self.open_files[file_path]['state'] = 'SYNCED'
            
            # Update original data and mark as synced
            self.original_data = data.copy()
            self.mark_as_synced()
            
            # Update tab appearances to reflect saved state
            self.update_file_tab_appearances()
            
            self.save_last_file(file_path)
            self.update_filename_display()
            self.show_status_message(f"✓ Saved to {os.path.basename(file_path)}")
            return True
        except Exception as e:
            self.show_error_dialog("Save Error", f"Failed to save file: {e}")
            return False
    
    def update_ui_from_data(self):
        """Update UI with loaded data"""
        # Update each section
        yaml_data = {}
        if 'prompt' in self.yaml_data:
            yaml_data = self.yaml_data['prompt']
            
        self.instruction_section.load_data(yaml_data.get('instruction', {}))
        self.context_section.load_data(yaml_data.get('context', {}))
        self.output_section.load_data(yaml_data.get('output', {}))
        self.extends_section.load_data(yaml_data.get('extends', []))

        # Update query
        query = yaml_data.get('query', '')
        if hasattr(self, 'query_entry'):
            self.query_entry.delete(0, "end")
            self.query_entry.insert(0, query)
    
    def clear_all_sections(self):
        """Clear all sections"""
        self.enable_yaml_textbox()
        self.yaml_text.delete("1.0", "end")
        self.instruction_section.clear_data()
        self.context_section.clear()
        self.output_section.clear()
        self.extends_section.clear()
        if hasattr(self, 'query_entry'):
            self.query_entry.delete(0, "end")
        self.disable_yaml_textbox()
    
    def load_last_file(self):
        """Load the last opened file"""
        try:
            last_file_path = Path.home() / ".peac_last_file"
            if last_file_path.exists():
                with open(last_file_path, 'r') as f:
                    file_path = f.read().strip()
                if file_path and Path(file_path).exists():
                    self.load_yaml_file(file_path)
        except:
            pass  # Ignore errors when loading last file
    
    def save_last_file(self, file_path: str):
        """Save the last opened file path"""
        try:
            last_file_path = Path.home() / ".peac_last_file"
            with open(last_file_path, 'w') as f:
                f.write(file_path)
        except:
            pass  # Ignore errors when saving last file
    
    def show_preview_window(self, content: str):
        """Show preview in a new window"""
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Prompt Preview")
        preview_window.geometry("800x600")
        preview_window.transient(self)
        
        # Button frame
        button_frame = ctk.CTkFrame(preview_window, height=50)
        button_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Copy to clipboard button
        copy_btn = ctk.CTkButton(
            button_frame,
            text="📋 Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(content, preview_window)
        )
        copy_btn.pack(side="right", padx=10, pady=10)
        
        # Text area
        text_area = ctk.CTkTextbox(preview_window)
        text_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        text_area.insert("1.0", content)
        text_area.configure(state="disabled")
    
    def copy_to_clipboard(self, content: str, parent_window=None):
        """Copy content to clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(content)
            # Show success message
            if parent_window:
                self.show_temp_message(parent_window, "✓ Copied to clipboard!")
            else:
                self.set_status("✓ Copied to clipboard!", "success")
                self.after(2000, lambda: self.set_status("", "normal"))  # Clear after 2 seconds
        except Exception as e:
            if parent_window:
                self.show_temp_message(parent_window, f"❌ Failed to copy: {e}", "error")
            else:
                self.set_status(f"❌ Failed to copy: {e}", "error")
    
    def show_temp_message(self, parent_window, message: str, msg_type: str = "success"):
        """Show temporary message in a window"""
        msg_label = ctk.CTkLabel(
            parent_window,
            text=message,
            text_color="green" if msg_type == "success" else "red"
        )
        msg_label.pack(pady=5)
        
        # Remove the message after 2 seconds
        parent_window.after(2000, msg_label.destroy)
    
    def show_error_dialog(self, title: str, message: str):
        """Show error dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text=message, wraplength=350)
        label.pack(pady=30)
        
        ok_btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_btn.pack(pady=10)
    
    def show_info_dialog(self, title: str, message: str):
        """Show info dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text=message)
        label.pack(pady=20)
        
        ok_btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_btn.pack(pady=10)


def main():
    """Main entry point"""
    app = PeacApp()
    app.mainloop()


if __name__ == "__main__":
    main()
