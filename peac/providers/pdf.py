from .base import FileProvider
from typing import Dict, Any, Optional
import pdfplumber
import re

class PdfProvider(FileProvider):
    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse PDF file with optional page filtering
        
        Args:
            file_path: Path to the PDF file
            options: Optional dictionary with:
                - pages: String specifying pages to extract (e.g., "1-5", "1,3,5", "1-3,7,9-11")
        
        Returns:
            Extracted text content
        """
        text = ""
        
        with pdfplumber.open(file_path) as pdf:
            # Get pages to extract
            if options and 'pages' in options:
                page_indices = self.parse_page_range(options['pages'])
                if page_indices:
                    # Filter pages based on specified range
                    pages_to_extract = []
                    for i in page_indices:
                        if 0 <= i < len(pdf.pages):
                            pages_to_extract.append(pdf.pages[i])
                else:
                    # If page parsing failed, extract all pages
                    pages_to_extract = pdf.pages
            else:
                # No page filtering, extract all pages
                pages_to_extract = pdf.pages
            
            # Extract text from selected pages
            for page in pages_to_extract:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    
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