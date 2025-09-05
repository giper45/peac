"""
Context Section Component for PEaC CustomTkinter GUI
Handles local rules, web rules configuration
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any
import os


class RuleCard(ctk.CTkFrame):
    """Individual rule card component"""
    
    def __init__(self, parent, rule_type="local", **kwargs):
        super().__init__(parent, **kwargs)
        self.rule_type = rule_type
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Create widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create rule card widgets"""
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
        
        if self.rule_type == "local":
            self.create_local_widgets(row)
        else:
            self.create_web_widgets(row)
    
    def create_local_widgets(self, start_row):
        """Create widgets specific to local rules"""
        row = start_row
        
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
    
    def create_web_widgets(self, start_row):
        """Create widgets specific to web rules"""
        row = start_row
        
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
    
    def browse_source(self):
        """Browse for source file/folder"""
        # Ask user if they want file or folder
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Type")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        label = ctk.CTkLabel(dialog, text="What would you like to select?")
        label.pack(pady=20)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        def select_file():
            dialog.destroy()
            file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[("All files", "*.*")]
            )
            if file_path:
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, file_path)
        
        def select_folder():
            dialog.destroy()
            folder_path = filedialog.askdirectory(title="Select Folder")
            if folder_path:
                self.source_entry.delete(0, "end")
                self.source_entry.insert(0, folder_path)
        
        file_btn = ctk.CTkButton(button_frame, text="File", command=select_file)
        file_btn.pack(side="left", padx=5)
        
        folder_btn = ctk.CTkButton(button_frame, text="Folder", command=select_folder)
        folder_btn.pack(side="left", padx=5)
    
    def remove_self(self):
        """Remove this rule card"""
        if hasattr(self.master, 'remove_rule_card'):
            self.master.remove_rule_card(self)
        else:
            self.destroy()
    
    def get_data(self) -> tuple:
        """Get rule data"""
        name = self.name_entry.get().strip()
        if not name:
            return None
        
        rule_data = {
            'preamble': self.preamble_text.get("1.0", "end-1c").strip()
        }
        
        if self.rule_type == "local":
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
        else:
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
        
        if self.rule_type == "local":
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
        else:
            source = rule_data.get('source', '')
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, source)
            
            xpath = rule_data.get('xpath', '')
            self.xpath_entry.delete(0, "end")
            self.xpath_entry.insert(0, xpath)


class ContextSection(ctk.CTkFrame):
    """Context section with local and web rules"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize rule cards
        self.rule_cards = []
        
        # Initialize change callback
        self.change_callback = None
        
        # Create widgets
        self.create_widgets()
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def set_change_callback(self, callback):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def setup_change_tracking(self):
        """Set up change tracking for text widgets"""
        def on_change(*args):
            self.notify_change()
        
        # Track changes in base rules text
        if hasattr(self, 'base_rules_text'):
            self.base_rules_text.bind('<KeyRelease>', lambda e: on_change())
            self.base_rules_text.bind('<Button-1>', lambda e: self.after(10, on_change))
    
    def create_widgets(self):
        """Create context section widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="CONTEXT Section",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Base rules
        base_frame = ctk.CTkFrame(self)
        base_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        base_frame.grid_columnconfigure(0, weight=1)
        
        base_label = ctk.CTkLabel(
            base_frame,
            text="Base Rules (one per line):",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        base_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        self.base_rules_text = ctk.CTkTextbox(
            base_frame,
            height=100
        )
        self.base_rules_text.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        # Rules container with tabs
        rules_container = ctk.CTkFrame(self)
        rules_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        rules_container.grid_columnconfigure(0, weight=1)
        rules_container.grid_rowconfigure(1, weight=1)
        
        # Tab buttons
        tab_frame = ctk.CTkFrame(rules_container, height=40)
        tab_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        tab_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.local_tab_btn = ctk.CTkButton(
            tab_frame,
            text="📁 Local Rules",
            height=35,
            command=self.show_local_tab
        )
        self.local_tab_btn.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky="ew")
        
        self.web_tab_btn = ctk.CTkButton(
            tab_frame,
            text="🌐 Web Rules",
            height=35,
            command=self.show_web_tab,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        self.web_tab_btn.grid(row=0, column=1, padx=(2.5, 5), pady=5, sticky="ew")
        
        # Rules content area
        self.rules_content = ctk.CTkScrollableFrame(rules_container, height=400)
        self.rules_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.rules_content.grid_columnconfigure(0, weight=1)
        
        # Add buttons
        self.create_add_buttons()
        
        # Start with local tab
        self.current_rule_type = "local"
        self.show_local_tab()
    
    def create_add_buttons(self):
        """Create add rule buttons"""
        self.local_add_btn = ctk.CTkButton(
            self.rules_content,
            text="➕ Add Local Rule",
            command=self.add_local_rule,
            height=40
        )
        
        self.web_add_btn = ctk.CTkButton(
            self.rules_content,
            text="➕ Add Web Rule",
            command=self.add_web_rule,
            height=40
        )
    
    def show_local_tab(self):
        """Show local rules tab"""
        self.current_rule_type = "local"
        
        # Update button appearance
        self.local_tab_btn.configure(
            fg_color=("gray75", "gray25"),
            text_color=("gray10", "white")
        )
        self.web_tab_btn.configure(
            fg_color="transparent",
            text_color=("gray10", "gray90")
        )
        
        # Show/hide appropriate content
        self.refresh_rules_display()
    
    def show_web_tab(self):
        """Show web rules tab"""
        self.current_rule_type = "web"
        
        # Update button appearance
        self.web_tab_btn.configure(
            fg_color=("gray75", "gray25"),
            text_color=("gray10", "white")
        )
        self.local_tab_btn.configure(
            fg_color="transparent",
            text_color=("gray10", "gray90")
        )
        
        # Show/hide appropriate content
        self.refresh_rules_display()
    
    def refresh_rules_display(self):
        """Refresh the display of rules based on current tab"""
        # Hide all rule cards first
        for card in self.rule_cards:
            card.grid_forget()
        
        # Hide add buttons
        self.local_add_btn.grid_forget()
        self.web_add_btn.grid_forget()
        
        # Show appropriate cards and add button
        row = 0
        for card in self.rule_cards:
            if card.rule_type == self.current_rule_type:
                card.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
                row += 1
        
        # Show appropriate add button
        if self.current_rule_type == "local":
            self.local_add_btn.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
        else:
            self.web_add_btn.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
    
    def add_local_rule(self):
        """Add new local rule"""
        card = RuleCard(self.rules_content, rule_type="local")
        self.rule_cards.append(card)
        self.refresh_rules_display()
        
        # Notify about change
        self.notify_change()
    
    def add_web_rule(self):
        """Add new web rule"""
        card = RuleCard(self.rules_content, rule_type="web")
        self.rule_cards.append(card)
        self.refresh_rules_display()
        
        # Notify about change
        self.notify_change()
    
    def remove_rule_card(self, card):
        """Remove a rule card"""
        if card in self.rule_cards:
            self.rule_cards.remove(card)
            card.destroy()
            self.refresh_rules_display()
            
            # Notify about change
            self.notify_change()
    
    def get_data(self) -> dict:
        """Get all context data"""
        data = {}
        
        # Base rules
        base_text = self.base_rules_text.get("1.0", "end-1c").strip()
        if base_text:
            base_rules = [line.strip() for line in base_text.split('\n') if line.strip()]
            if base_rules:
                data['base'] = base_rules
        
        # Local rules
        local_rules = {}
        for card in self.rule_cards:
            if card.rule_type == "local":
                rule_data = card.get_data()
                if rule_data:
                    name, rule_config = rule_data
                    local_rules[name] = rule_config
        
        if local_rules:
            data['local'] = local_rules
        
        # Web rules
        web_rules = {}
        for card in self.rule_cards:
            if card.rule_type == "web":
                rule_data = card.get_data()
                if rule_data:
                    name, rule_config = rule_data
                    web_rules[name] = rule_config
        
        if web_rules:
            data['web'] = web_rules
        
        return data
    
    def load_data(self, data: dict):
        """Load data into context section"""
        # Defensive: handle if data is a list (invalid format)
        if isinstance(data, list):
            from tkinter import messagebox
            messagebox.showerror(
                "YAML Format Error",
                "The 'context' section in your YAML file is a list, but it must be a dictionary/object. Please fix the file."
            )
            self.clear()
            return
        # Clear existing
        self.clear()
        # Base rules
        base_rules = data.get('base', [])
        if base_rules:
            base_text = '\n'.join(base_rules)
            self.base_rules_text.delete("1.0", "end")
            self.base_rules_text.insert("1.0", base_text)
        # Local rules
        local_rules = data.get('local', {})
        for name, rule_config in local_rules.items():
            card = RuleCard(self.rules_content, rule_type="local")
            card.load_data(name, rule_config)
            self.rule_cards.append(card)
        # Web rules
        web_rules = data.get('web', {})
        for name, rule_config in web_rules.items():
            card = RuleCard(self.rules_content, rule_type="web")
            card.load_data(name, rule_config)
            self.rule_cards.append(card)
        self.refresh_rules_display()
    
    def clear(self):
        """Clear all context data"""
        self.base_rules_text.delete("1.0", "end")
        
        for card in self.rule_cards:
            card.destroy()
        self.rule_cards.clear()
        
        self.refresh_rules_display()
