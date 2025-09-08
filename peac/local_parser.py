from enum import Enum
from pathlib import Path
import os
import re


class PathType(Enum):
    FILE = "FILE"
    DIR = "DIR"
    OTHER = "OTHER"


def check_type(source):
    if os.path.isfile(source):
        return PathType.FILE
    if os.path.isdir(source):
        return PathType.DIR
    return PathType.OTHER


def get_file_provider(file_path):
    """Get the appropriate file provider based on file extension"""
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.pdf':
        print("Entering PDF provider")
        try:
            from peac.providers.pdf import PdfProvider
            return PdfProvider()
        except ImportError:
            print("Import error")
            return None
    elif file_extension == '.docx':
        try:
            from peac.providers.docx import DocxProvider
            return DocxProvider()
        except ImportError:
            return None
    elif file_extension == '.xlsx':
        print("Entering XLSX provider")
        try:
            from peac.providers.xlsx import XlsxProvider
            return XlsxProvider()
        except ImportError:
            print("XLSX provider import error - openpyxl may not be installed")
            return None
    
    return None


def read_file(source, filter_regex=None, options=None):
    """Read the filename and parse with appropriate provider if needed

    Args:
        source (str): the filename
        filter_regex (str): regex pattern to filter lines (only for text files)
        options (dict): optional provider-specific options (e.g., pages for PDF/DOCX)
    """
    file_content = ""
    lines = []
    
    # Try to use a specialized provider first
    provider = get_file_provider(source)
    if provider:
        try:
            file_content = provider.parse(source, options)
            
            # Apply filter if provider supports it and filter is specified
            if filter_regex and hasattr(provider, 'apply_filter'):
                file_content = provider.apply_filter(file_content, filter_regex)
            
            print(f"Parsed {source} with provider {provider.__class__.__name__}")
        except Exception as e:
            # Fallback to regular text reading if provider fails
            print(f"Warning: Failed to parse {source} with provider: {e}")
            file_content = f"Error parsing file: {e}"
    else:
        # Regular text file reading
        try:
            with open(source, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if filter_regex:
                pattern = re.compile(filter_regex)
                lines = [line for line in lines if pattern.search(line)]
            
            file_content = "".join(lines)  # Keep original line breaks
        except UnicodeDecodeError:
            try:
                # Try with different encoding
                with open(source, 'r', encoding='latin-1') as f:
                    lines = f.readlines()
                
                if filter_regex:
                    pattern = re.compile(filter_regex)
                    lines = [line for line in lines if pattern.search(line)]
                
                file_content = "".join(lines)
            except Exception as e:
                file_content = f"Error reading file: {e}"
        except Exception as e:
            file_content = f"Error reading file: {e}"
    
    """ File output:
        [filename] 
        ```
        content
        ```
    """
    return f"[{source}]\n```\n{file_content}\n```" 



def read_dir(source, recursive=False, ext="*", filter_regex=None, options=None):
    """Read all files in a directory using the read_file function.

    Args:
        source (str): The directory path.
        recursive (bool): Whether to include files in subdirectories.
        ext (str): File extension to filter by (e.g., 'txt', 'py', '*' for all files).
        filter_regex (str): regex pattern to filter lines (only for text files)
        options (dict): optional provider-specific options (e.g., pages for PDF/DOCX)

    Returns:
        str: Concatenated contents of all files with headers.
    """
    file_contents = []
    source_path = Path(source)
    pattern = f"**/*.{ext}" if recursive else f"*.{ext}"
    for file_path in source_path.glob(pattern):
        file_contents.append(read_file(file_path, filter_regex, options))

    return "\n".join(file_contents)


def parse(source, recursive=False, ext='*', filter_regex=None, options=None):
    """Parse source with optional provider options
    
    Args:
        source (str): File or directory path
        recursive (bool): Whether to include files in subdirectories
        ext (str): File extension to filter by
        filter_regex (str): regex pattern to filter lines
        options (dict): optional provider-specific options (e.g., pages for PDF/DOCX)
    """
    type = check_type(source)
    if type == PathType.FILE: 
        return read_file(source, filter_regex, options)
    elif type == PathType.DIR:
        return read_dir(source, recursive, ext, filter_regex, options)