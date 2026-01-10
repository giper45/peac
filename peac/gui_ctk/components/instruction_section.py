"""
Instruction Section Component for PEaC CustomTkinter GUI
Handles instruction configuration for prompts
"""
import customtkinter as ctk
from typing import Dict, List, Any


class InstructionSection(ctk.CTkFrame):
    """Instruction section for prompt configuration"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
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
        
        # Track changes in base instructions text
        if hasattr(self, 'base_instructions_text'):
            self.base_instructions_text.bind('<KeyRelease>', lambda e: on_change())
            self.base_instructions_text.bind('<Button-1>', lambda e: self.after(10, on_change))
    
    def create_widgets(self):
        """Create instruction section widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="INSTRUCTION Section",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Description
        description = ctk.CTkLabel(
            self,
            text="Define the core instructions and task for your prompt",
            font=ctk.CTkFont(size=14),
            text_color="#3a3b3c"
        )
        description.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Main content frame
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Base instructions section
        self.create_base_instructions_section(content_frame)
    
    def create_base_instructions_section(self, parent):
        """Create base instructions section"""
        # Base instructions frame
        base_frame = ctk.CTkFrame(parent)
        base_frame.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=10)
        base_frame.grid_columnconfigure(0, weight=1)
        
        # Base instructions title
        base_title = ctk.CTkLabel(
            base_frame,
            text="📝 Base Instructions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        base_title.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Base instructions description
        base_desc = ctk.CTkLabel(
            base_frame,
            text="Enter the main task instructions for your prompt (one instruction per line)",
            font=ctk.CTkFont(size=12),
            text_color="#3a3b3c"
        )
        base_desc.grid(row=1, column=0, pady=(0, 10), padx=15, sticky="w")
        
        # Base instructions text area
        self.base_instructions_text = ctk.CTkTextbox(
            base_frame,
            height=200
        )
        self.base_instructions_text.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Insert placeholder text
        self.base_instructions_text.insert("1.0", "Example:\n• You are a helpful AI assistant\n• Provide clear and concise answers\n• Use proper formatting in your responses\n• Ask for clarification if needed")
        
        # Additional instructions frame
        additional_frame = ctk.CTkFrame(parent)
        additional_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10), padx=10)
        additional_frame.grid_columnconfigure(0, weight=1)
        
        # Additional instructions title
        additional_title = ctk.CTkLabel(
            additional_frame,
            text="⚙️ Additional Instructions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        additional_title.grid(row=0, column=0, pady=(15, 10), padx=15, sticky="w")
        
        # Additional instructions description
        additional_desc = ctk.CTkLabel(
            additional_frame,
            text="Optional: Additional behavioral instructions or constraints",
            font=ctk.CTkFont(size=12),
            text_color="#3a3b3c"
        )
        additional_desc.grid(row=1, column=0, pady=(0, 10), padx=15, sticky="w")
        
        # Additional instructions text area
        self.additional_instructions_text = ctk.CTkTextbox(
            additional_frame,
            height=120
        )
        self.additional_instructions_text.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Insert placeholder text
        self.additional_instructions_text.insert("1.0", "Example:\n• Use technical language for expert users\n• Include code examples when relevant\n• Prioritize security considerations")
        
        # Set up change tracking for additional instructions
        self.additional_instructions_text.bind('<KeyRelease>', lambda e: self.notify_change())
        self.additional_instructions_text.bind('<Button-1>', lambda e: self.after(10, self.notify_change))
    
    def get_data(self) -> Dict[str, Any]:
        """Get instruction data"""
        data = {}
        
        # Get base instructions
        base_text = self.base_instructions_text.get("1.0", "end-1c").strip()
        if base_text:
            # Split by lines and filter empty lines
            base_instructions = [line.strip() for line in base_text.split('\n') if line.strip()]
            if base_instructions:
                data['base'] = base_instructions
        
        # Get additional instructions
        additional_text = self.additional_instructions_text.get("1.0", "end-1c").strip()
        if additional_text:
            # Split by lines and filter empty lines
            additional_instructions = [line.strip() for line in additional_text.split('\n') if line.strip()]
            if additional_instructions:
                data['additional'] = additional_instructions
        
        return data
    
    def load_data(self, instruction_data: Dict[str, Any]):
        """Load instruction data into the section"""
        if not instruction_data:
            return
        
        # Load base instructions
        if 'base' in instruction_data:
            base_instructions = instruction_data['base']
            if isinstance(base_instructions, list):
                base_text = '\n'.join(base_instructions)
            else:
                base_text = str(base_instructions)
            
            self.base_instructions_text.delete("1.0", "end")
            self.base_instructions_text.insert("1.0", base_text)
        
        # Load additional instructions
        if 'additional' in instruction_data:
            additional_instructions = instruction_data['additional']
            if isinstance(additional_instructions, list):
                additional_text = '\n'.join(additional_instructions)
            else:
                additional_text = str(additional_instructions)
            
            self.additional_instructions_text.delete("1.0", "end")
            self.additional_instructions_text.insert("1.0", additional_text)
    
    def clear_data(self):
        """Clear all instruction data"""
        self.base_instructions_text.delete("1.0", "end")
        self.additional_instructions_text.delete("1.0", "end")
