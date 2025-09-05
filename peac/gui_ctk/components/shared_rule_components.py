"""
Shared Rule Components for PEaC CustomTkinter GUI
Provides reusable LocalRuleCard and WebRuleCard components
Used by both Context and Output sections
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any, Optional, Callable
import os


class LocalRuleCard(ctk.CTkFrame):
    """Card component for local rules with full feature support"""
    
    def __init__(self, parent, rule_data=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_delete = on_delete
        self.change_callback = None
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_widgets()
        
        if rule_data:
            self.load_data(rule_data)
    
    def set_change_callback(self, callback: Callable):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def create_widgets(self):
        """Create local rule card widgets"""
        row = 0
        
        # Rule name
        name_label = ctk.CTkLabel(self, text="Rule Name:", width=100)
        name_label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter rule name")
        self.name_entry.grid(row=row, column=1, sticky="ew", padx=(5, 10), pady=(10, 5))
        
        # Remove button
        remove_btn = ctk.CTkButton(
            self, 
            text="✕", 
            width=30, 
            height=30,
            command=self.remove_self,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.grid(row=row, column=2, padx=(5, 10), pady=(10, 5))
        
        row += 1
        
        # Preamble
        preamble_label = ctk.CTkLabel(self, text="Preamble:", width=100)
        preamble_label.grid(row=row, column=0, sticky="nw", padx=(10, 5), pady=5)
        
        self.preamble_text = ctk.CTkTextbox(self, height=60)
        self.preamble_text.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        
        row += 1
        
        # Source path with browse button
        source_label = ctk.CTkLabel(self, text="Source Path:", width=100)
        source_label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)
        
        source_frame = ctk.CTkFrame(self, fg_color="transparent")
        source_frame.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        source_frame.grid_columnconfigure(0, weight=1)
        
        self.source_entry = ctk.CTkEntry(source_frame, placeholder_text="Path to file or folder")
        self.source_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        browse_btn = ctk.CTkButton(
            source_frame, 
            text="📂", 
            width=40,
            command=self.browse_source
        )
        browse_btn.grid(row=0, column=1)
        
        row += 1
        
        # Options row
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=row, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        options_frame.grid_columnconfigure((1, 2), weight=1)
        
        # Recursive checkbox
        self.recursive_var = ctk.BooleanVar()
        recursive_cb = ctk.CTkCheckBox(
            options_frame, 
            text="Recursive", 
            variable=self.recursive_var
        )
        recursive_cb.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Extension filter
        ext_label = ctk.CTkLabel(options_frame, text="Extensions:")
        ext_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.extension_entry = ctk.CTkEntry(
            options_frame, 
            placeholder_text="*.py, *.txt, etc."
        )
        self.extension_entry.grid(row=0, column=2, sticky="ew", padx=5)
        
        # Filter pattern
        filter_label = ctk.CTkLabel(options_frame, text="Filter:")
        filter_label.grid(row=0, column=3, sticky="w", padx=(10, 5))
        
        self.filter_entry = ctk.CTkEntry(
            options_frame, 
            placeholder_text="Regex pattern"
        )
        self.filter_entry.grid(row=0, column=4, sticky="ew", padx=(5, 0))
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def setup_change_tracking(self):
        """Set up change tracking for all input widgets"""
        # Track changes in entry widgets
        for widget in [self.name_entry, self.source_entry, self.extension_entry, self.filter_entry]:
            widget.bind('<KeyRelease>', lambda e: self.notify_change())
            widget.bind('<FocusOut>', lambda e: self.notify_change())
        
        # Track changes in text widget
        self.preamble_text.bind('<KeyRelease>', lambda e: self.notify_change())
        self.preamble_text.bind('<FocusOut>', lambda e: self.notify_change())
        
        # Track changes in checkbox
        self.recursive_var.trace('w', lambda *args: self.notify_change())
    
    def browse_source(self):
        """Browse for source file/folder"""
        # Ask user if they want file or folder
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Type")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        result = {"choice": None}
        
        def choose_file():
            result["choice"] = "file"
            dialog.destroy()
        
        def choose_folder():
            result["choice"] = "folder"
            dialog.destroy()
        
        ctk.CTkLabel(dialog, text="Select source type:").pack(pady=20)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="File", command=choose_file).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Folder", command=choose_folder).pack(side="left", padx=10)
        
        dialog.wait_window()
        
        if result["choice"] == "file":
            file_path = filedialog.askopenfilename(title="Select Source File")
            if file_path:
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, file_path)
        elif result["choice"] == "folder":
            folder_path = filedialog.askdirectory(title="Select Source Folder")
            if folder_path:
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, folder_path)
    
    def remove_self(self):
        """Remove this rule card"""
        if self.on_delete:
            self.on_delete(self)
    
    def get_data(self) -> tuple:
        """Get rule data from inputs"""
        name = self.name_entry.get().strip()
        
        rule_data = {}
        
        preamble = self.preamble_text.get("1.0", "end-1c").strip()
        if preamble:
            rule_data['preamble'] = preamble
        
        source = self.source_entry.get().strip()
        if source:
            rule_data['source'] = source
        
        if self.recursive_var.get():
            rule_data['recursive'] = True
        
        extension = self.extension_entry.get().strip()
        if extension:
            rule_data['extension'] = extension
        
        filter_pattern = self.filter_entry.get().strip()
        if filter_pattern:
            rule_data['filter'] = filter_pattern
        
        return (name, rule_data)
    
    def load_data(self, name: str, rule_data: dict):
        """Load data into the rule card"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, name)
        
        preamble = rule_data.get('preamble', '')
        self.preamble_text.delete("1.0", "end")
        self.preamble_text.insert("1.0", preamble)
        
        source = rule_data.get('source', '')
        self.source_entry.delete(0, "end")
        self.source_entry.insert(0, source)
        
        self.recursive_var.set(rule_data.get('recursive', False))
        
        extension = rule_data.get('extension', '')
        self.extension_entry.delete(0, "end")
        self.extension_entry.insert(0, extension)
        
        filter_pattern = rule_data.get('filter', '')
        self.filter_entry.delete(0, "end")
        self.filter_entry.insert(0, filter_pattern)


class WebRuleCard(ctk.CTkFrame):
    """Card component for web rules with XPath support"""
    
    def __init__(self, parent, rule_data=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_delete = on_delete
        self.change_callback = None
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_widgets()
        
        if rule_data:
            self.load_data(rule_data)
    
    def set_change_callback(self, callback: Callable):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def create_widgets(self):
        """Create web rule card widgets"""
        row = 0
        
        # Rule name
        name_label = ctk.CTkLabel(self, text="Rule Name:", width=100)
        name_label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter rule name")
        self.name_entry.grid(row=row, column=1, sticky="ew", padx=(5, 10), pady=(10, 5))
        
        # Remove button
        remove_btn = ctk.CTkButton(
            self, 
            text="✕", 
            width=30, 
            height=30,
            command=self.remove_self,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.grid(row=row, column=2, padx=(5, 10), pady=(10, 5))
        
        row += 1
        
        # Preamble
        preamble_label = ctk.CTkLabel(self, text="Preamble:", width=100)
        preamble_label.grid(row=row, column=0, sticky="nw", padx=(10, 5), pady=5)
        
        self.preamble_text = ctk.CTkTextbox(self, height=60)
        self.preamble_text.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        
        row += 1
        
        # URL
        url_label = ctk.CTkLabel(self, text="URL:", width=100)
        url_label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)
        
        self.url_entry = ctk.CTkEntry(self, placeholder_text="https://example.com")
        self.url_entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        
        row += 1
        
        # XPath (optional)
        xpath_label = ctk.CTkLabel(self, text="XPath:", width=100)
        xpath_label.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)
        
        self.xpath_entry = ctk.CTkEntry(self, placeholder_text="//div[@class='content'] (optional)")
        self.xpath_entry.grid(row=row, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def setup_change_tracking(self):
        """Set up change tracking for all input widgets"""
        # Track changes in entry widgets
        for widget in [self.name_entry, self.url_entry, self.xpath_entry]:
            widget.bind('<KeyRelease>', lambda e: self.notify_change())
            widget.bind('<FocusOut>', lambda e: self.notify_change())
        
        # Track changes in text widget
        self.preamble_text.bind('<KeyRelease>', lambda e: self.notify_change())
        self.preamble_text.bind('<FocusOut>', lambda e: self.notify_change())
    
    def remove_self(self):
        """Remove this rule card"""
        if self.on_delete:
            self.on_delete(self)
    
    def get_data(self) -> tuple:
        """Get rule data from inputs"""
        name = self.name_entry.get().strip()
        
        rule_data = {}
        
        preamble = self.preamble_text.get("1.0", "end-1c").strip()
        if preamble:
            rule_data['preamble'] = preamble
        
        url = self.url_entry.get().strip()
        if url:
            rule_data['source'] = url
        
        xpath = self.xpath_entry.get().strip()
        if xpath:
            rule_data['xpath'] = xpath
        
        return (name, rule_data)
    
    def load_data(self, name: str, rule_data: dict):
        """Load data into the rule card"""
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, name)
        
        preamble = rule_data.get('preamble', '')
        self.preamble_text.delete("1.0", "end")
        self.preamble_text.insert("1.0", preamble)
        
        source = rule_data.get('source', '')
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, source)
        
        xpath = rule_data.get('xpath', '')
        self.xpath_entry.delete(0, "end")
        self.xpath_entry.insert(0, xpath)
