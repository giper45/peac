from .base import FileProvider
from typing import Dict, Any, Optional
from docx import Document
import re

class DocxProvider(FileProvider):
    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse DOCX file with optional paragraph filtering
        
        Args:
            file_path: Path to the DOCX file
            options: Optional dictionary with:
                - pages: String specifying paragraph ranges to extract (e.g., "1-5", "1,3,5")
                  Note: For DOCX, "pages" refers to paragraph numbers
        
        Returns:
            Extracted text content
        """
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        
        # Get paragraphs to extract
        if options and 'pages' in options:
            paragraph_indices = self.parse_page_range(options['pages'])
            if paragraph_indices:
                # Filter paragraphs based on specified range
                filtered_paragraphs = []
                for i in paragraph_indices:
                    if 0 <= i < len(paragraphs):
                        filtered_paragraphs.append(paragraphs[i])
                return "\n".join(filtered_paragraphs)
        
        # No filtering or invalid range, return all paragraphs
        return "\n".join(paragraphs)
    
    def apply_filter(self, text: str, filter_regex: str) -> str:
        """
        Apply regex filter to extracted text
        
        Args:
            text: Extracted text content
            filter_regex: Regex pattern to match lines
            
        Returns:
            Filtered text content
        """
        if not filter_regex:
            return text
            
        try:
            pattern = re.compile(filter_regex, re.MULTILINE)
            lines = text.split('\n')
            filtered_lines = [line for line in lines if pattern.search(line)]
            return '\n'.join(filtered_lines)
        except re.error:
            # If regex is invalid, return original text
            return text