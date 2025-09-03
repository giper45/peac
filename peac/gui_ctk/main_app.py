"""
PEaC GUI - CustomTkinter Implementation
Modern, responsive GUI for Prompt Engineering as Code
"""
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


class PeacApp(ctk.CTk):
    """Main PEaC Application with CustomTkinter"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("PEaC - Prompt Engineering as Code")
        self.geometry("1400x900")
        self.minsize(1000, 600)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid layout (responsive)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Initialize data
        self.yaml_data = {}
        self.current_file_path = None
        self.file_state = "SYNCED"  # "SYNCED" or "EDITED"
        self.original_data = {}  # Store original loaded data for comparison
        
        # Create GUI elements
        self.create_toolbar()
        self.create_main_content()
        
        # Load last file if exists
        self.load_last_file()
    
    def create_toolbar(self):
        """Create responsive toolbar"""
        toolbar_frame = ctk.CTkFrame(self, height=60)
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        toolbar_frame.grid_columnconfigure(1, weight=1)  # Spacer
        
        # Left side buttons
        left_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # File operations
        new_btn = ctk.CTkButton(
            left_frame,
            text="📄 New",
            width=80,
            command=self.new_file
        )
        new_btn.grid(row=0, column=0, padx=(0, 5))
        
        open_btn = ctk.CTkButton(
            left_frame,
            text="📂 Open",
            width=80,
            command=self.open_file
        )
        open_btn.grid(row=0, column=1, padx=5)
        
        save_btn = ctk.CTkButton(
            left_frame,
            text="💾 Save",
            width=80,
            command=self.save_file
        )
        save_btn.grid(row=0, column=2, padx=5)
        
        # Center filename display
        self.filename_label = ctk.CTkLabel(
            toolbar_frame,
            text="No file loaded",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray10", "gray90")
        )
        self.filename_label.grid(row=0, column=1, pady=10)
        
        # Right side buttons
        right_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        right_frame.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        
        self.preview_btn = ctk.CTkButton(
            right_frame,
            text="👁️ Preview",
            width=100,
            command=self.preview_prompt
        )
        self.preview_btn.grid(row=0, column=0, padx=5)
        
        self.copy_btn = ctk.CTkButton(
            right_frame,
            text="📋 Copy",
            width=100,
            command=self.copy_prompt
        )
        self.copy_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Initially disable preview and copy buttons
        self.update_action_buttons_state()
    
    def create_main_content(self):
        """Create main tabbed content area"""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # Updated for query row
        
        # Query input section
        self.create_query_input(main_frame)
        
        # Content tabs header
        tab_frame = ctk.CTkFrame(main_frame, height=50)
        tab_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 5))
        tab_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Removed Query tab
        
        # Content tab buttons (removed Query tab)
        self.tab_buttons = {}
        self.create_tab_button(tab_frame, "YAML", 0, self.show_yaml_tab)
        self.create_tab_button(tab_frame, "Context", 1, self.show_context_tab)
        self.create_tab_button(tab_frame, "Output", 2, self.show_output_tab)
        self.create_tab_button(tab_frame, "Extends", 3, self.show_extends_tab)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create tab contents
        self.create_tab_contents()
        
        # Set up change tracking
        self.setup_change_tracking()
        
        # Show initial tab
        self.current_tab = "YAML"
        self.show_yaml_tab()
    
    def create_tab_button(self, parent, text, column, command):
        """Create a tab button"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            height=35,
            command=command,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        btn.grid(row=0, column=column, padx=5, pady=5, sticky="ew")
        self.tab_buttons[text] = btn
    
    def create_query_input(self, parent):
        """Create query input section above tabs"""
        query_frame = ctk.CTkFrame(parent, height=60)
        query_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        query_frame.grid_columnconfigure(1, weight=1)
        
        # Query label
        query_label = ctk.CTkLabel(
            query_frame,
            text="Query:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=60
        )
        query_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="w")
        
        # Query input field
        self.query_entry = ctk.CTkEntry(
            query_frame,
            placeholder_text='Tell me what is the result of 2+2',
            font=ctk.CTkFont(size=12),
            height=35
        )
        self.query_entry.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="ew")
        
    def create_tab_contents(self):
        """Create all tab content widgets"""
        # YAML section
        self.create_yaml_section()
        
        # Context section
        self.context_section = ContextSection(self.content_frame)
        self.context_section.set_change_callback(self.on_section_changed)
        
        # Output section  
        self.output_section = OutputSection(self.content_frame)
        self.output_section.set_change_callback(self.on_section_changed)
        
        # Extends section
        self.extends_section = ExtendsSection(self.content_frame)
        self.extends_section.set_change_callback(self.on_section_changed)
    
    def update_yaml_title(self):
        self.yaml_title.configure(text=f"{self.file_name}")


    def create_yaml_section(self):
        """Create YAML editor section"""
        self.yaml_frame = ctk.CTkFrame(self.content_frame)
        self.yaml_frame.grid_columnconfigure(0, weight=1)
        self.yaml_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        self.yaml_title = ctk.CTkLabel(
            self.yaml_frame,
            text="YAML Preview",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.yaml_title.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=20)

        # YAML text area  
        self.yaml_text = ctk.CTkTextbox(
            self.yaml_frame,
            wrap="none",
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.yaml_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
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
        
        # Track changes in query entry
        if hasattr(self, 'query_entry'):
            self.query_entry.bind('<KeyRelease>', lambda e: on_change())
            self.query_entry.bind('<FocusOut>', lambda e: on_change())
        
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
    
    def show_yaml_tab(self):
        """Show YAML tab"""
        self.hide_all_tabs()
        self.yaml_frame.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("YAML")
        # Auto-sync GUI to YAML when showing YAML tab
        self.sync_gui_to_yaml()
    
    def show_context_tab(self):
        """Show context tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.context_section.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Context")
    
    def show_output_tab(self):
        """Show output tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.output_section.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Output")
    
    def show_extends_tab(self):
        """Show extends tab"""
        # Auto-sync YAML to GUI when leaving YAML tab
        if hasattr(self, 'current_tab') and self.current_tab == "YAML":
            self.sync_yaml_to_gui_silent()
        self.hide_all_tabs()
        self.extends_section.grid(row=0, column=0, sticky="nsew")
        self.update_tab_appearance("Extends")
    
    def hide_all_tabs(self):
        """Hide all tab contents"""
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
    
    def update_tab_appearance(self, active_tab):
        """Update tab button appearance"""
        for tab_name, button in self.tab_buttons.items():
            if tab_name == active_tab:
                button.configure(
                    fg_color=("gray75", "gray25"),
                    text_color=("gray10", "white")
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                )
        self.current_tab = active_tab
    
    def update_filename_display(self):
        """Update the filename display in toolbar"""
        if self.current_file_path:
            filename = os.path.basename(self.current_file_path)
            self.filename_label.configure(text=filename)
        else:
            self.filename_label.configure(text="No file loaded")
        
        # Update button states
        self.update_action_buttons_state()
    
    def update_action_buttons_state(self):
        """Enable/disable action buttons based on file state"""
        file_exists = (self.current_file_path is not None and 
                      os.path.exists(self.current_file_path))
        
        # Buttons are enabled when file exists AND state is SYNCED
        buttons_enabled = file_exists and self.file_state == "SYNCED"
        
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
            filename = os.path.basename(self.current_file_path)
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
    
    def new_file(self):
        """Create a new file"""
        # Clear all sections
        self.clear_all_sections()
        
        # Reset file state
        self.current_file_path = None
        self.original_data = {}
        self.file_state = "SYNCED"
        self.yaml_data = {}
        
        self.update_filename_display()
        self.update_action_buttons_state()
    
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
            self.load_yaml_file(file_path)
    
    def open_file(self):
        """Open existing YAML file"""
        from tkinter import filedialog
        
        import os
        file_path = filedialog.askopenfilename(
            title="Open PEaC Configuration",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            self.open_file_in_new_tab(file_path)

    def save_file(self):
        """Save current configuration"""
        if self.current_file_path:
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
            self.save_yaml_file(file_path)
            self.current_file_path = file_path
            self.update_filename_display()
            self.update_action_buttons_state()
    
    def preview_prompt(self):
        """Preview generated prompt"""
        if self.file_state == "EDITED":
            self.show_toast("Please save your changes first to preview the prompt", "warning")
            return
            
        if not self.current_file_path or not os.path.exists(self.current_file_path):
            self.show_toast("No file to preview. Please create or load a file first", "warning")
            return
            
        try:
            # Use the current saved file directly
            processor = PromptYaml(self.current_file_path)
            result = processor.get_prompt_sentence()
            
            # Show preview window
            self.show_preview_window(result)
        except FileNotFoundError as e:
            self.show_toast(f"Extends file not found: {str(e)}", "error")
        except Exception as e:
            self.show_toast(f"Preview error: {str(e)}", "error")
    
    def copy_prompt(self):
        """Copy generated prompt to clipboard"""
        if self.file_state == "EDITED":
            self.show_toast("Please save your changes first to copy the prompt", "warning")
            return
            
        if not self.current_file_path or not os.path.exists(self.current_file_path):
            self.show_toast("No file to copy. Please create or load a file first", "warning")
            return
            
        try:
            # Use the current saved file directly
            processor = PromptYaml(self.current_file_path)
            result = processor.get_prompt_sentence()
            
            # Copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(result)
            
            # Show success message
            self.show_toast("Prompt copied to clipboard!", "success")
        except FileNotFoundError as e:
            self.show_toast(f"Extends file not found: {str(e)}", "error")
        except Exception as e:
            self.show_toast(f"Copy error: {str(e)}", "error")
    
    def collect_data(self) -> dict:
        """Collect data from all sections"""
        data = {}
        
        # Collect from each section
        context_data = self.context_section.get_data()
        if context_data:
            data['context'] = context_data
        
        output_data = self.output_section.get_data()
        if output_data:
            data['output'] = output_data
        
        extends_data = self.extends_section.get_data()
        if extends_data:
            data['extends'] = extends_data
        
        # Query
        query_text = self.query_entry.get().strip()
        if query_text:
            data['query'] = query_text
        
        return data

    def disable_yaml_textbox(self):
        """Disable YAML text box"""
        self.yaml_text.configure(state="disabled")

    def enable_yaml_textbox(self):
        """Enable YAML text box"""
        self.yaml_text.configure(state="normal")

    def load_yaml_file(self, file_path: str):
        """Load YAML configuration file"""
        try:
            import yaml
            with open(file_path, 'r') as f:
                yaml_content = f.read()
                self.yaml_data = yaml.safe_load(yaml_content) or {}
            
            # Update YAML tab with raw content
            self.enable_yaml_textbox()
            self.yaml_text.delete("1.0", "end")
            self.yaml_text.insert("1.0", yaml_content)
            
            self.current_file_path = file_path
            self.update_ui_from_data()
            
            # Store original data for change tracking
            self.original_data = self.collect_data()
            self.mark_as_synced()  # File is synced after loading
            
            self.save_last_file(file_path)
            self.update_filename_display()
            self.disable_yaml_textbox()

        except Exception as e:
            self.show_toast(f"Failed to load file: {e}", "error")
    
    def save_yaml_file(self, file_path: str):
        """Save configuration to YAML file"""
        try:
            import yaml
            
            # Always collect data from GUI sections
            data = self.collect_data()
            
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
            
            # Update original data and mark as synced
            self.original_data = data.copy()
            self.mark_as_synced()
            
            self.save_last_file(file_path)
            self.update_filename_display()
            self.show_toast(f"Saved to {os.path.basename(file_path)}", "success")
        except Exception as e:
            self.show_toast(f"Failed to save file: {e}", "error")
    
    def update_ui_from_data(self):
        """Update UI with loaded data"""
        # Update each section
        if 'prompt' in self.yaml_data:
            yaml_data = self.yaml_data['prompt']
        else:
            yaml_data = self.yaml_data
            
        self.context_section.load_data(yaml_data.get('context', {}))
        self.output_section.load_data(yaml_data.get('output', {}))
        self.extends_section.load_data(yaml_data.get('extends', []))

        # Update query
        query = yaml_data.get('query', '')
        self.query_entry.delete(0, "end")
        self.query_entry.insert(0, query)
    
    def clear_all_sections(self):
        """Clear all sections"""
        self.enable_yaml_textbox()
        self.yaml_text.delete("1.0", "end")
        self.context_section.clear()
        self.output_section.clear()
        self.extends_section.clear()
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
                    return True
        except:
            pass  # Ignore errors when loading last file
        return False
    
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
        
        # Text area
        text_area = ctk.CTkTextbox(preview_window)
        text_area.pack(fill="both", expand=True, padx=20, pady=20)
        text_area.insert("1.0", content)
        text_area.configure(state="disabled")
    
    def show_error_dialog(self, title: str, message: str):
        """Show error dialog - use toast for simple errors, modal for complex ones"""
        # Use toast for simple, short error messages
        if len(message) < 100 and '\n' not in message:
            self.show_toast(message, "error", duration=5000)  # Longer duration for errors
        else:
            # Use modal dialog for complex error messages
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
        """Show toast notification"""
        self.show_toast(message, "success")
    
    def show_toast(self, message: str, toast_type: str = "info", duration: int = 3000):
        """Show toast notification that automatically disappears
        
        Args:
            message: Message to display
            toast_type: Type of toast ("success", "error", "info", "warning")
            duration: Duration in milliseconds before auto-hide
        """
        # Create toast frame with fixed size
        toast = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color=("gray90", "gray20"),
            border_width=2,
            width=350,
            height=60
        )
        toast.pack_propagate(False)  # Prevent size from changing based on content
        
        # Set border color based on type
        if toast_type == "success":
            toast.configure(border_color=("green", "lightgreen"))
            icon = "✅"
        elif toast_type == "error":
            toast.configure(border_color=("red", "lightcoral"))
            icon = "❌"
        elif toast_type == "warning":
            toast.configure(border_color=("orange", "yellow"))
            icon = "⚠️"
        else:  # info
            toast.configure(border_color=("blue", "lightblue"))
            icon = "ℹ️"
        
        # Create content frame
        content_frame = ctk.CTkFrame(toast, fg_color="transparent")
        content_frame.pack(padx=15, pady=10, fill="both", expand=True)
        
        # Icon and message
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=ctk.CTkFont(size=16)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        message_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=12),
            wraplength=300
        )
        message_label.pack(side="left", fill="both", expand=True)
        
        # Close button
        close_btn = ctk.CTkButton(
            content_frame,
            text="✕",
            width=25,
            height=25,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            text_color=("gray50", "gray70"),
            hover_color=("gray80", "gray40"),
            command=lambda: self.hide_toast(toast)
        )
        close_btn.pack(side="right", padx=(10, 0))
        
        # Position toast in top-right corner
        self.update_idletasks()  # Ensure window is rendered
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        toast_width = 350
        toast_height = 60
        
        x = window_width - toast_width - 20
        y = 80  # Below toolbar
        
        toast.place(x=x, y=y)
        
        # Animate in
        self.animate_toast_in(toast, x, y)
        
        # Auto-hide after duration
        if duration > 0:
            self.after(duration, lambda: self.hide_toast(toast))
    
    def animate_toast_in(self, toast, target_x, target_y):
        """Animate toast sliding in from the right"""
        start_x = target_x + 400  # Start off-screen
        steps = 15
        step_size = (start_x - target_x) / steps
        
        def animate_step(step):
            if step < steps:
                current_x = start_x - (step_size * step)
                toast.place(x=current_x, y=target_y)
                self.after(20, lambda: animate_step(step + 1))
            else:
                toast.place(x=target_x, y=target_y)
        
        animate_step(0)
    
    def hide_toast(self, toast):
        """Hide toast with animation"""
        def animate_out():
            current_x = toast.winfo_x()
            target_x = current_x + 400
            steps = 10
            step_size = (target_x - current_x) / steps
            
            def animate_step(step):
                if step < steps:
                    new_x = current_x + (step_size * step)
                    toast.place(x=new_x)
                    self.after(15, lambda: animate_step(step + 1))
                else:
                    toast.destroy()
            
            animate_step(0)
        
        animate_out()


def main():
    """Main entry point"""
    app = PeacApp()
    app.mainloop()


if __name__ == "__main__":
    main()
