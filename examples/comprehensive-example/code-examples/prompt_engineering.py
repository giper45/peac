"""
Prompt Engineering Module

This module provides utilities for constructing, managing, and optimizing prompts
for large language models (LLMs).
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class PromptRole(Enum):
    """Roles for different parts of a prompt."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    CONTEXT = "context"


@dataclass
class PromptSection:
    """
    Represents a section of a prompt with metadata.
    
    Attributes:
        role: The role of this section (system, user, etc.)
        content: The actual text content
        priority: Priority level for ordering (higher = more important)
        tokens: Estimated token count
        metadata: Additional metadata
    """
    role: PromptRole
    content: str
    priority: int = 0
    tokens: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def estimate_tokens(self) -> int:
        """
        Estimate token count for this section.
        Uses rough estimation: ~4 characters per token.
        
        Returns:
            Estimated token count
        """
        if self.tokens is None:
            # Rough estimation
            self.tokens = len(self.content) // 4
        return self.tokens


@dataclass
class PromptTemplate:
    """
    A template for constructing prompts with placeholders.
    
    Example:
        template = PromptTemplate(
            template="Analyze this code:\n\n{code}\n\nFocus on: {focus_areas}",
            variables={"focus_areas": "security, performance"}
        )
        prompt = template.render(code="def foo(): pass")
    """
    template: str
    variables: Dict[str, Any] = field(default_factory=dict)
    
    def render(self, **kwargs) -> str:
        """
        Render the template with provided variables.
        
        Args:
            **kwargs: Variables to substitute in the template
            
        Returns:
            Rendered prompt string
        """
        # Merge provided kwargs with default variables
        context = {**self.variables, **kwargs}
        return self.template.format(**context)
    
    def get_required_variables(self) -> List[str]:
        """
        Extract required variable names from template.
        
        Returns:
            List of variable names
        """
        import re
        pattern = r'\{(\w+)\}'
        return re.findall(pattern, self.template)


class PromptBuilder:
    """
    Builder class for constructing complex prompts from multiple sections.
    
    Example:
        builder = PromptBuilder()
        builder.add_system("You are a helpful assistant.")
        builder.add_context("Project uses Python 3.11")
        builder.add_user("How do I optimize this code?")
        prompt = builder.build()
    """
    
    def __init__(self, max_tokens: Optional[int] = None):
        """
        Initialize the prompt builder.
        
        Args:
            max_tokens: Maximum token limit for the prompt
        """
        self.sections: List[PromptSection] = []
        self.max_tokens = max_tokens
        self.total_tokens = 0
    
    def add_section(self, section: PromptSection) -> 'PromptBuilder':
        """
        Add a section to the prompt.
        
        Args:
            section: PromptSection to add
            
        Returns:
            Self for method chaining
        """
        self.sections.append(section)
        self.total_tokens += section.estimate_tokens()
        return self
    
    def add_system(self, content: str, priority: int = 100) -> 'PromptBuilder':
        """Add a system instruction section."""
        section = PromptSection(PromptRole.SYSTEM, content, priority)
        return self.add_section(section)
    
    def add_context(self, content: str, priority: int = 50, 
                    metadata: Optional[Dict] = None) -> 'PromptBuilder':
        """Add a context section."""
        section = PromptSection(
            PromptRole.CONTEXT, 
            content, 
            priority,
            metadata=metadata or {}
        )
        return self.add_section(section)
    
    def add_user(self, content: str, priority: int = 10) -> 'PromptBuilder':
        """Add a user query section."""
        section = PromptSection(PromptRole.USER, content, priority)
        return self.add_section(section)
    
    def optimize(self) -> 'PromptBuilder':
        """
        Optimize the prompt by removing low-priority sections if over token limit.
        
        Returns:
            Self for method chaining
        """
        if self.max_tokens is None or self.total_tokens <= self.max_tokens:
            return self
        
        # Sort by priority (ascending) to remove lowest priority first
        sorted_sections = sorted(self.sections, key=lambda s: s.priority)
        
        kept_sections = []
        current_tokens = 0
        
        # Keep highest priority sections that fit
        for section in reversed(sorted_sections):
            section_tokens = section.estimate_tokens()
            if current_tokens + section_tokens <= self.max_tokens:
                kept_sections.append(section)
                current_tokens += section_tokens
        
        self.sections = list(reversed(kept_sections))
        self.total_tokens = current_tokens
        
        return self
    
    def build(self, separator: str = "\n\n") -> str:
        """
        Build the final prompt string.
        
        Args:
            separator: String to use between sections
            
        Returns:
            Complete prompt string
        """
        # Sort by priority (descending) for output
        sorted_sections = sorted(self.sections, key=lambda s: s.priority, reverse=True)
        
        # Group by role
        role_groups: Dict[PromptRole, List[str]] = {}
        for section in sorted_sections:
            if section.role not in role_groups:
                role_groups[section.role] = []
            role_groups[section.role].append(section.content)
        
        # Build prompt with role headers
        parts = []
        
        # System instructions first
        if PromptRole.SYSTEM in role_groups:
            parts.append("# System Instructions")
            parts.extend(role_groups[PromptRole.SYSTEM])
        
        # Context next
        if PromptRole.CONTEXT in role_groups:
            parts.append("# Context")
            parts.extend(role_groups[PromptRole.CONTEXT])
        
        # User query last
        if PromptRole.USER in role_groups:
            parts.append("# Query")
            parts.extend(role_groups[PromptRole.USER])
        
        return separator.join(parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the prompt.
        
        Returns:
            Dictionary with stats (tokens, sections, roles)
        """
        role_counts = {}
        for section in self.sections:
            role = section.role.value
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            'total_tokens': self.total_tokens,
            'total_sections': len(self.sections),
            'role_distribution': role_counts,
            'max_tokens': self.max_tokens,
            'token_usage_percent': (self.total_tokens / self.max_tokens * 100) 
                                   if self.max_tokens else None
        }


class PromptLibrary:
    """
    A library for storing and retrieving reusable prompt templates.
    """
    
    def __init__(self):
        """Initialize an empty prompt library."""
        self.templates: Dict[str, PromptTemplate] = {}
    
    def register(self, name: str, template: PromptTemplate):
        """
        Register a template in the library.
        
        Args:
            name: Unique name for the template
            template: PromptTemplate to register
        """
        self.templates[name] = template
    
    def get(self, name: str) -> Optional[PromptTemplate]:
        """
        Retrieve a template by name.
        
        Args:
            name: Template name
            
        Returns:
            PromptTemplate or None if not found
        """
        return self.templates.get(name)
    
    def render(self, name: str, **kwargs) -> Optional[str]:
        """
        Render a template directly.
        
        Args:
            name: Template name
            **kwargs: Variables for rendering
            
        Returns:
            Rendered prompt or None if template not found
        """
        template = self.get(name)
        return template.render(**kwargs) if template else None
    
    def list_templates(self) -> List[str]:
        """
        List all registered template names.
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())


# Example usage
if __name__ == "__main__":
    # Create a prompt builder
    builder = PromptBuilder(max_tokens=1000)
    
    # Add sections
    builder.add_system(
        "You are an expert code reviewer with deep knowledge of Python best practices."
    )
    
    builder.add_context(
        "This is a Python CLI application that processes YAML configurations.",
        metadata={"source": "README.md"}
    )
    
    builder.add_context(
        "The codebase follows PEP 8 style guidelines and uses type hints.",
        priority=40
    )
    
    builder.add_user(
        "Review the following code and suggest improvements:\n\n"
        "def process_config(config):\n"
        "    return config['settings']['value']"
    )
    
    # Build and print
    prompt = builder.build()
    print(prompt)
    print("\n" + "="*50)
    print("Stats:", builder.get_stats())
