from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class FileProvider(ABC):
    @abstractmethod
    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse a file with optional configuration
        
        Args:
            file_path: Path to the file to parse
            options: Optional dictionary of provider-specific options
        
        Returns:
            Parsed text content
        """
        pass
    
    def parse_page_range(self, pages_option: str) -> list:
        """
        Parse page range string into list of page numbers
        
        Args:
            pages_option: String like "1-5", "1,3,5", "1-3,7,9-11"
            
        Returns:
            List of page numbers (0-indexed for internal use)
        """
        if not pages_option:
            return []
            
        pages = set()
        parts = pages_option.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                # Range like "1-5"
                start, end = part.split('-', 1)
                try:
                    start_num = int(start.strip())
                    end_num = int(end.strip())
                    # Convert to 0-indexed and add to set
                    pages.update(range(start_num - 1, end_num))
                except ValueError:
                    continue
            else:
                # Single page like "3"
                try:
                    page_num = int(part.strip())
                    # Convert to 0-indexed
                    pages.add(page_num - 1)
                except ValueError:
                    continue
        
        return sorted(list(pages))