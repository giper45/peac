"""
Output Section Component for PEaC CustomTkinter GUI
Handles output configuration with base rules and local/web rules
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any
import threading
import os

# Import shared rule components
from .shared_rule_components import LocalRuleCard, WebRuleCard, RagRuleCard


class OutputSection(ctk.CTkFrame):
    """Card component for individual output rules"""
    
    def __init__(self, parent, rule_data=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_delete = on_delete
        self.change_callback = None
        self.create_widgets()
        
        if rule_data:
            self.load_rule_data(rule_data)
    
    def set_change_callback(self, callback):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def create_widgets(self):
        """Create rule card widgets"""
        self.grid_columnconfigure(1, weight=1)
        
        # Name field
        name_label = ctk.CTkLabel(self, text="Name:", width=80)
        name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Rule name")
        self.name_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="ew")
        
        # Preamble field
        preamble_label = ctk.CTkLabel(self, text="Preamble:", width=80)
        preamble_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        
        self.preamble_text = ctk.CTkTextbox(self, height=60)
        self.preamble_text.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # Source field
        source_label = ctk.CTkLabel(self, text="Source:", width=80)
        source_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        source_frame = ctk.CTkFrame(self, fg_color="transparent")
        source_frame.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="ew")
        source_frame.grid_columnconfigure(0, weight=1)
        
        self.source_entry = ctk.CTkEntry(source_frame, placeholder_text="Source path or URL")
        self.source_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        browse_btn = ctk.CTkButton(source_frame, text="📁", width=30, command=self.browse_source)
        browse_btn.grid(row=0, column=1)
        
        # Delete button
        if self.on_delete:
            delete_btn = ctk.CTkButton(
                self, 
                text="🗑️", 
                width=30, 
                fg_color="red", 
                hover_color="darkred",
                command=self.on_delete
            )
            delete_btn.grid(row=2, column=2, padx=10, pady=5)
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def setup_change_tracking(self):
        """Set up change tracking for all input widgets"""
        # Track changes in entry widgets
        for widget in [self.name_entry, self.source_entry]:
            widget.bind('<KeyRelease>', lambda e: self.notify_change())
            widget.bind('<FocusOut>', lambda e: self.notify_change())
        
        # Track changes in text widget
        self.preamble_text.bind('<KeyRelease>', lambda e: self.notify_change())
        self.preamble_text.bind('<FocusOut>', lambda e: self.notify_change())
    
    def browse_source(self):
        """Browse for source file"""
        file_path = filedialog.askopenfilename(
            title="Select Source File",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, file_path)
    
    def get_rule_data(self):
        """Get rule data from inputs"""
        return {
            'name': self.name_entry.get().strip(),
            'preamble': self.preamble_text.get("1.0", "end-1c").strip(),
            'source': self.source_entry.get().strip()
        }
    
    def load_rule_data(self, data):
        """Load rule data into inputs"""
        if isinstance(data, dict):
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, data.get('name', ''))
            
            self.preamble_text.delete("1.0", "end")
            self.preamble_text.insert("1.0", data.get('preamble', ''))
            
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, data.get('source', ''))


class WebRuleCard(ctk.CTkFrame):
    """Card component for web-specific output rules with XPath support"""
    
    def __init__(self, parent, rule_data=None, on_delete=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_delete = on_delete
        self.change_callback = None
        self.create_widgets()
        
        if rule_data:
            self.load_rule_data(rule_data)
    
    def set_change_callback(self, callback):
        """Set callback function to call when content changes"""
        self.change_callback = callback
    
    def notify_change(self):
        """Notify that content has changed"""
        if self.change_callback:
            self.change_callback()
    
    def create_widgets(self):
        """Create web rule card widgets with XPath support"""
        self.grid_columnconfigure(1, weight=1)
        
        # Name field
        name_label = ctk.CTkLabel(self, text="Name:", width=80)
        name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Rule name")
        self.name_entry.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="ew")
        
        # Preamble field
        preamble_label = ctk.CTkLabel(self, text="Preamble:", width=80)
        preamble_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        
        self.preamble_text = ctk.CTkTextbox(self, height=60)
        self.preamble_text.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # URL field
        url_label = ctk.CTkLabel(self, text="URL:", width=80)
        url_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.source_entry = ctk.CTkEntry(self, placeholder_text="https://example.com")
        self.source_entry.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # XPath field
        xpath_label = ctk.CTkLabel(self, text="XPath:", width=80)
        xpath_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.xpath_entry = ctk.CTkEntry(self, placeholder_text="//div[@class='content'] (optional)")
        self.xpath_entry.grid(row=3, column=1, padx=(5, 10), pady=5, sticky="ew")
        
        # Delete button
        if self.on_delete:
            delete_btn = ctk.CTkButton(
                self, 
                text="🗑️", 
                width=30, 
                fg_color="red", 
                hover_color="darkred",
                command=self.on_delete
            )
            delete_btn.grid(row=3, column=2, padx=10, pady=5)
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def setup_change_tracking(self):
        """Set up change tracking for all input widgets"""
        # Track changes in entry widgets
        for widget in [self.name_entry, self.source_entry, self.xpath_entry]:
            widget.bind('<KeyRelease>', lambda e: self.notify_change())
            widget.bind('<FocusOut>', lambda e: self.notify_change())
        
        # Track changes in text widget
        self.preamble_text.bind('<KeyRelease>', lambda e: self.notify_change())
        self.preamble_text.bind('<FocusOut>', lambda e: self.notify_change())
    
    def get_rule_data(self):
        """Get rule data from inputs"""
        data = {
            'name': self.name_entry.get().strip(),
            'preamble': self.preamble_text.get("1.0", "end-1c").strip(),
            'source': self.source_entry.get().strip()
        }
        
        xpath = self.xpath_entry.get().strip()
        if xpath:
            data['xpath'] = xpath
            
        return data
    
    def load_rule_data(self, data):
        """Load rule data into inputs"""
        if isinstance(data, dict):
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, data.get('name', ''))
            
            self.preamble_text.delete("1.0", "end")
            self.preamble_text.insert("1.0", data.get('preamble', ''))
            
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, data.get('source', ''))
            
            self.xpath_entry.delete(0, "end")
            self.xpath_entry.insert(0, data.get('xpath', ''))


class OutputSection(ctk.CTkFrame):
    """Output section with base rules and local/web rules tabs"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize rule lists
        self.local_rules = []
        self.web_rules = []
        self.rag_rules = []
        
        # Initialize change callback and current file path
        self.change_callback = None
        self.current_file_path = None
        
        # Create widgets
        self.create_widgets()
        
        # Set up change tracking
        self.setup_change_tracking()
    
    def set_current_file_path(self, current_file_path: str):
        """Set the current file path for relative path calculations"""
        self.current_file_path = current_file_path
        
        # Update all existing local rule cards
        for card in self.local_rules:
            if hasattr(card, 'update_current_file_path'):
                card.update_current_file_path(current_file_path)
    
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
    
    def generate_default_rule_name(self, rule_type="local"):
        """Generate a default rule name based on existing rules"""
        if rule_type == "local":
            existing_names = []
            for card in self.local_rules:
                name = card.name_entry.get().strip()
                if name:
                    existing_names.append(name)
        elif rule_type == "web":
            existing_names = []
            for card in self.web_rules:
                name = card.name_entry.get().strip()
                if name:
                    existing_names.append(name)
        else:  # rag
            existing_names = []
            for card in self.rag_rules:
                name = card.name_entry.get().strip()
                if name:
                    existing_names.append(name)
        
        # Find the next available rule number
        base_name = f"{rule_type}-rule"
        counter = 1
        while f"{base_name}-{counter}" in existing_names:
            counter += 1
        
        return f"{base_name}-{counter}"
    
    def create_widgets(self):
        """Create output section widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="OUTPUT Section",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)
        
        # Base rules section
        self.create_base_rules_section()
        
        # Rules tabs section
        self.create_rules_tabs()
    
    
    def create_base_rules_section(self):
        """Create base rules text area section"""
        base_frame = ctk.CTkFrame(self)
        base_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        base_frame.grid_columnconfigure(0, weight=1)
        base_frame.grid_rowconfigure(1, weight=1)
        
        # Base rules title
        base_label = ctk.CTkLabel(
            base_frame,
            text="Base Output Rules:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        base_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        # Base rules text area
        self.base_rules_text = ctk.CTkTextbox(
            base_frame,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.base_rules_text.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
    
    def create_rules_tabs(self):
        """Create local and web rules tabs"""
        # Create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Add tabs
        self.local_tab = self.tabview.add("Local Rules")
        self.web_tab = self.tabview.add("Web Rules")
        self.rag_tab = self.tabview.add("RAG Rules")
        
        # Configure tab grids
        self.local_tab.grid_columnconfigure(0, weight=1)
        self.local_tab.grid_rowconfigure(1, weight=1)
        self.web_tab.grid_columnconfigure(0, weight=1)
        self.web_tab.grid_rowconfigure(1, weight=1)
        self.rag_tab.grid_columnconfigure(0, weight=1)
        self.rag_tab.grid_rowconfigure(1, weight=1)
        
        # Create local rules tab content
        self.create_local_rules_tab()
        
        # Create web rules tab content
        self.create_web_rules_tab()
        
        # Create RAG rules tab content
        self.create_rag_rules_tab()
    
    def create_local_rules_tab(self):
        """Create local rules tab content"""
        # Header with add button
        header_frame = ctk.CTkFrame(self.local_tab, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        local_label = ctk.CTkLabel(
            header_frame,
            text="Local Output Rules",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        local_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        add_local_btn = ctk.CTkButton(
            header_frame,
            text="+ Add Local Rule",
            command=self.add_local_rule
        )
        add_local_btn.grid(row=0, column=1, padx=15, pady=15)
        
        # Scrollable frame for rules
        self.local_scroll = ctk.CTkScrollableFrame(self.local_tab, height=400)
        self.local_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.local_scroll.grid_columnconfigure(0, weight=1)
    
    def create_web_rules_tab(self):
        """Create web rules tab content"""
        # Header with add button
        header_frame = ctk.CTkFrame(self.web_tab, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        web_label = ctk.CTkLabel(
            header_frame,
            text="Web Output Rules",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        web_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        add_web_btn = ctk.CTkButton(
            header_frame,
            text="+ Add Web Rule",
            command=self.add_web_rule
        )
        add_web_btn.grid(row=0, column=1, padx=15, pady=15)
        
        # Scrollable frame for rules
        self.web_scroll = ctk.CTkScrollableFrame(self.web_tab, height=400)
        self.web_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.web_scroll.grid_columnconfigure(0, weight=1)
    
    def create_rag_rules_tab(self):
        """Create RAG rules tab content"""
        # Header with add button
        header_frame = ctk.CTkFrame(self.rag_tab, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        rag_label = ctk.CTkLabel(
            header_frame,
            text="RAG Output Rules",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        rag_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        add_rag_btn = ctk.CTkButton(
            header_frame,
            text="+ Add RAG Rule",
            command=self.add_rag_rule
        )
        add_rag_btn.grid(row=0, column=1, padx=15, pady=15)
        
        # Scrollable frame for rules
        self.rag_scroll = ctk.CTkScrollableFrame(self.rag_tab, height=400)
        self.rag_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.rag_scroll.grid_columnconfigure(0, weight=1)
    
    def add_local_rule(self):
        """Add a new local rule"""
        default_name = self.generate_default_rule_name("local")
        rule_card = LocalRuleCard(
            self.local_scroll,
            on_delete=lambda card: self.delete_local_rule(card),
            default_name=default_name,
            current_file_path=self.current_file_path
        )
        rule_card.set_change_callback(self.notify_change)
        rule_card.grid(row=len(self.local_rules), column=0, sticky="ew", padx=5, pady=5)
        self.local_rules.append(rule_card)
        
        # Notify about change
        self.notify_change()
    
    def delete_local_rule(self, rule_card):
        """Delete a local rule"""
        if rule_card in self.local_rules:
            self.local_rules.remove(rule_card)
            rule_card.destroy()
            # Re-grid remaining cards
            for i, card in enumerate(self.local_rules):
                card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            
            # Notify about change
            self.notify_change()
    
    def add_web_rule(self):
        """Add a new web rule"""
        default_name = self.generate_default_rule_name("web")
        rule_card = WebRuleCard(
            self.web_scroll,
            on_delete=lambda: self.delete_web_rule(rule_card),
            default_name=default_name
        )
        rule_card.set_change_callback(self.notify_change)
        rule_card.grid(row=len(self.web_rules), column=0, sticky="ew", padx=5, pady=5)
        self.web_rules.append(rule_card)
        
        # Notify about change
        self.notify_change()
    
    def delete_web_rule(self, rule_card):
        """Delete a web rule"""
        if rule_card in self.web_rules:
            self.web_rules.remove(rule_card)
            rule_card.destroy()
            # Re-grid remaining cards
            for i, card in enumerate(self.web_rules):
                card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            
            # Notify about change
            self.notify_change()
    
    def add_rag_rule(self):
        """Add a new RAG rule"""
        default_name = self.generate_default_rule_name("rag")
        rule_card = RagRuleCard(
            self.rag_scroll,
            on_delete=lambda: self.delete_rag_rule(rule_card),
            default_name=default_name,
            current_file_path=self.current_file_path
        )
        rule_card.set_change_callback(self.notify_change)
        rule_card.grid(row=len(self.rag_rules), column=0, sticky="ew", padx=5, pady=5)
        self.rag_rules.append(rule_card)
        
        # Notify about change
        self.notify_change()
    
    def delete_rag_rule(self, rule_card):
        """Delete a RAG rule"""
        if rule_card in self.rag_rules:
            self.rag_rules.remove(rule_card)
            rule_card.destroy()
            # Re-grid remaining cards
            for i, card in enumerate(self.rag_rules):
                card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            
            # Notify about change
            self.notify_change()
    
    def get_data(self) -> dict:
        """Get output configuration data in original PEaC format"""
        # First validate all rules
        validation_errors = []
        
        # Validate local rules
        for i, card in enumerate(self.local_rules):
            is_valid, error_msg = card.validate()
            if not is_valid:
                validation_errors.append(f"Local rule {i+1}: {error_msg}")
        
        # Validate web rules
        for i, card in enumerate(self.web_rules):
            is_valid, error_msg = card.validate()
            if not is_valid:
                validation_errors.append(f"Web rule {i+1}: {error_msg}")
        
        # Validate RAG rules
        for i, card in enumerate(self.rag_rules):
            is_valid, error_msg = card.validate()
            if not is_valid:
                validation_errors.append(f"RAG rule {i+1}: {error_msg}")
        
        # Return validation errors if any (don't show dialog)
        if validation_errors:
            return {"_validation_errors": validation_errors}
        
        data = {}
        
        # Base rules - in original format this could be 'base' as a list
        base_rules = self.base_rules_text.get("1.0", "end-1c").strip()
        if base_rules:
            # Convert to list format if multiple lines
            base_lines = [line.strip() for line in base_rules.split('\n') if line.strip()]
            if len(base_lines) == 1:
                data['base'] = base_lines[0]
            elif len(base_lines) > 1:
                data['base'] = base_lines
        
        # Local rules - convert to original PEaC format (dict with rule names as keys)
        local_dict = {}
        for rule_card in self.local_rules:
            result = rule_card.get_data()
            if result:
                name, rule_config = result
                if name and (rule_config.get('preamble') or rule_config.get('source')):
                    local_dict[name] = rule_config
        
        if local_dict:
            data['local'] = local_dict
        
        # Web rules - convert to original PEaC format (dict with rule names as keys)
        web_dict = {}
        for rule_card in self.web_rules:
            result = rule_card.get_data()
            if result:
                name, rule_config = result
                if name and (rule_config.get('preamble') or rule_config.get('source') or rule_config.get('xpath')):
                    web_dict[name] = rule_config
        
        if web_dict:
            data['web'] = web_dict
        
        # RAG rules - convert to original PEaC format (dict with rule names as keys)
        rag_dict = {}
        for rule_card in self.rag_rules:
            result = rule_card.get_data()
            if result:
                name, rule_config = result
                if name and (rule_config.get('preamble') or rule_config.get('faiss_file') or rule_config.get('query')):
                    rag_dict[name] = rule_config
        
        if rag_dict:
            data['rag'] = rag_dict
        
        return data
    
    def load_data(self, data):
        """Load output configuration data"""
        # Defensive: handle if data is not a dict
        if not isinstance(data, dict):
            from tkinter import messagebox
            messagebox.showerror(
                "YAML Format Error",
                "The 'output' section in your YAML file must be a dictionary/object."
            )
            return
        
        # Clear existing data
        self.clear_all_rules()
        
        # Load base rules - support both 'base_rules' and 'base' fields
        base_rules = data.get('base_rules', '') or data.get('base', '')
        if isinstance(base_rules, list):
            base_rules = '\n'.join(base_rules)
        elif not isinstance(base_rules, str):
            base_rules = str(base_rules) if base_rules else ''
        self.base_rules_text.delete("1.0", "end")
        self.base_rules_text.insert("1.0", base_rules)
        
        # Load local rules - support both new format (local_rules) and old format (local)
        local_rules = data.get('local_rules', [])
        if not local_rules:
            # Try old format: local as a dict
            local_dict = data.get('local', {})
            for name, rule_config in local_dict.items():
                self.add_local_rule()
                if self.local_rules:
                    # Load data using the shared component's method
                    self.local_rules[-1].load_data(name, rule_config)
        else:
            # New format: local_rules as a list
            if isinstance(local_rules, list):
                for rule_data in local_rules:
                    self.add_local_rule()
                    if self.local_rules:
                        self.local_rules[-1].load_rule_data(rule_data)
        
        # Load web rules - support both new format (web_rules) and old format (web)
        web_rules = data.get('web_rules', [])
        if not web_rules:
            # Try old format: web as a dict
            web_dict = data.get('web', {})
            for name, rule_config in web_dict.items():
                self.add_web_rule()
                if self.web_rules:
                    # Load data using the shared component's method
                    self.web_rules[-1].load_data(name, rule_config)
        else:
            # New format: web_rules as a list
            if isinstance(web_rules, list):
                for rule_data in web_rules:
                    self.add_web_rule()
                    if self.web_rules:
                        self.web_rules[-1].load_rule_data(rule_data)
        
        # Load RAG rules
        rag_rules = data.get('rag_rules', [])
        if not rag_rules:
            # Try old format: rag as a dict
            rag_dict = data.get('rag', {})
            for name, rule_config in rag_dict.items():
                self.add_rag_rule()
                if self.rag_rules:
                    # Load data using the shared component's method
                    self.rag_rules[-1].load_data(name, rule_config)
        else:
            # New format: rag_rules as a list
            if isinstance(rag_rules, list):
                for rule_data in rag_rules:
                    self.add_rag_rule()
                    if self.rag_rules:
                        self.rag_rules[-1].load_rule_data(rule_data)
    
    def clear_all_rules(self):
        """Clear all rules"""
        # Clear local rules
        for rule_card in self.local_rules[:]:
            rule_card.destroy()
        self.local_rules.clear()
        
        # Clear web rules
        for rule_card in self.web_rules[:]:
            rule_card.destroy()
        self.web_rules.clear()
        
        # Clear RAG rules
        for rule_card in self.rag_rules[:]:
            rule_card.destroy()
        self.rag_rules.clear()
    
    def clear(self):
        """Clear all content in the output section"""
        # Clear base rules
        if hasattr(self, 'base_format_text'):
            self.base_format_text.delete("1.0", "end")
        if hasattr(self, 'base_save_path_entry'):
            self.base_save_path_entry.delete(0, "end")
        if hasattr(self, 'base_save_filename_entry'):
            self.base_save_filename_entry.delete(0, "end")
        
        # Clear all rules
        self.clear_all_rules()
