"""
Context Section Component for PEaC CustomTkinter GUI
Handles local rules, web rules configuration
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any

# Import shared rule components
from .shared_rule_components import LocalRuleCard, WebRuleCard


class ContextSection(ctk.CTkFrame):
    """Context section with local and web rules"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize rule cards - separate lists for local and web
        self.local_rules = []
        self.web_rules = []
        
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
            card.update_current_file_path(current_file_path)
    
    def generate_default_rule_name(self, rule_type="local"):
        """Generate a default rule name based on existing rules"""
        if rule_type == "local":
            existing_names = []
            for card in self.local_rules:
                name = card.name_entry.get().strip()
                if name:
                    existing_names.append(name)
        else:  # web
            existing_names = []
            for card in self.web_rules:
                name = card.name_entry.get().strip()
                if name:
                    existing_names.append(name)
        
        # Find the next available rule number
        base_name = f"{rule_type}-rule"
        counter = 1
        while f"{base_name}-{counter}" in existing_names:
            counter += 1
        
        return f"{base_name}-{counter}"
    
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
        for card in self.local_rules + self.web_rules:
            card.grid_forget()
        
        # Hide add buttons
        self.local_add_btn.grid_forget()
        self.web_add_btn.grid_forget()
        
        # Show appropriate cards and add button
        row = 0
        if self.current_rule_type == "local":
            for card in self.local_rules:
                card.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
                row += 1
            self.local_add_btn.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
        else:  # web
            for card in self.web_rules:
                card.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
                row += 1
            self.web_add_btn.grid(row=row, column=0, sticky="ew", padx=5, pady=10)
    
    def add_local_rule(self):
        """Add new local rule"""
        default_name = self.generate_default_rule_name("local")
        card = LocalRuleCard(
            self.rules_content, 
            on_delete=self.remove_rule_card, 
            default_name=default_name,
            current_file_path=self.current_file_path
        )
        card.set_change_callback(self.notify_change)
        self.local_rules.append(card)
        self.refresh_rules_display()
        
        # Notify about change
        self.notify_change()
    
    def add_web_rule(self):
        """Add new web rule"""
        default_name = self.generate_default_rule_name("web")
        card = WebRuleCard(self.rules_content, on_delete=self.remove_rule_card, default_name=default_name)
        card.set_change_callback(self.notify_change)
        self.web_rules.append(card)
        self.refresh_rules_display()
        
        # Notify about change
        self.notify_change()
    
    def remove_rule_card(self, card):
        """Remove a rule card"""
        removed = False
        if card in self.local_rules:
            self.local_rules.remove(card)
            removed = True
        elif card in self.web_rules:
            self.web_rules.remove(card)
            removed = True
        
        if removed:
            card.destroy()
            self.refresh_rules_display()
            
            # Notify about change
            self.notify_change()
    
    def get_data(self) -> dict:
        """Get all context data"""
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
        
        # Return validation errors if any (don't show dialog)
        if validation_errors:
            return {"_validation_errors": validation_errors}
        
        data = {}
        
        # Base rules
        base_text = self.base_rules_text.get("1.0", "end-1c").strip()
        if base_text:
            base_rules = [line.strip() for line in base_text.split('\n') if line.strip()]
            if base_rules:
                data['base'] = base_rules
        
        # Local rules
        local_rules = {}
        for card in self.local_rules:
            rule_data = card.get_data()
            if rule_data:
                name, rule_config = rule_data
                local_rules[name] = rule_config
        
        if local_rules:
            data['local'] = local_rules
        
        # Web rules
        web_rules = {}
        for card in self.web_rules:
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
            card = LocalRuleCard(
                self.rules_content, 
                on_delete=self.remove_rule_card,
                current_file_path=self.current_file_path
            )
            card.set_change_callback(self.notify_change)
            card.load_data(name, rule_config)
            self.local_rules.append(card)
        
        # Web rules
        web_rules = data.get('web', {})
        for name, rule_config in web_rules.items():
            card = WebRuleCard(self.rules_content, on_delete=self.remove_rule_card)
            card.set_change_callback(self.notify_change)
            card.load_data(name, rule_config)
            self.web_rules.append(card)
        self.refresh_rules_display()
    
    def clear(self):
        """Clear all context data"""
        self.base_rules_text.delete("1.0", "end")
        
        for card in self.local_rules:
            card.destroy()
        self.local_rules.clear()
        
        for card in self.web_rules:
            card.destroy()
        self.web_rules.clear()
        
        self.refresh_rules_display()
