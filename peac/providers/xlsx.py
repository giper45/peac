from .base import FileProvider
from typing import Dict, Any, Optional
import re

class XlsxProvider(FileProvider):
    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Parse XLSX file with optional sheet filtering
        
        Args:
            file_path: Path to the XLSX file
            options: Optional dictionary with:
                - sheets: String specifying sheets to extract (e.g., "1-3", "1,3,5", "Sheet1,Sheet3")
                  Can be sheet indices (1-based) or sheet names
        
        Returns:
            Extracted text content
        """
        try:
            import openpyxl
        except ImportError:
            return "Error: openpyxl library not installed. Install with: pip install openpyxl"
        
        try:
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            all_sheets = workbook.worksheets
            sheet_names = [sheet.title for sheet in all_sheets]
            
            # Determine which sheets to extract
            sheets_to_extract = []
            
            if options and 'sheets' in options:
                sheets_option = options['sheets']
                
                # Check if sheets_option contains sheet names or indices
                if any(name in sheets_option for name in sheet_names):
                    # Contains sheet names
                    requested_names = [name.strip() for name in sheets_option.split(',')]
                    for name in requested_names:
                        if name in sheet_names:
                            sheet_index = sheet_names.index(name)
                            sheets_to_extract.append(all_sheets[sheet_index])
                else:
                    # Contains sheet indices
                    sheet_indices = self.parse_page_range(sheets_option)
                    for i in sheet_indices:
                        if 0 <= i < len(all_sheets):
                            sheets_to_extract.append(all_sheets[i])
            else:
                # No filtering, extract all sheets
                sheets_to_extract = all_sheets
            
            # Extract data from selected sheets
            extracted_text = ""
            
            for sheet in sheets_to_extract:
                extracted_text += f"\n=== Sheet: {sheet.title} ===\n"
                
                # Get all rows with data
                for row in sheet.iter_rows(values_only=True):
                    # Filter out completely empty rows
                    if any(cell is not None and str(cell).strip() for cell in row):
                        # Convert None values to empty strings and join with tabs
                        row_text = "\t".join(str(cell) if cell is not None else "" for cell in row)
                        extracted_text += row_text + "\n"
                
                extracted_text += "\n"
            
            return extracted_text.strip()
            
        except Exception as e:
            return f"Error parsing XLSX file: {str(e)}"
    
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
