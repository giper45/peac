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
        try:
            from peac.providers.pdf import PdfProvider
            return PdfProvider()
        except ImportError:
            return None
    elif file_extension == '.docx':
        try:
            from peac.providers.docx import DocxProvider
            return DocxProvider()
        except ImportError:
            return None
    
    return None


def read_file(source, filter_regex=None):
    """Read the filename and parse with appropriate provider if needed

    Args:
        source (str): the filename
        filter_regex (str): regex pattern to filter lines (only for text files)
    """
    file_content = ""
    lines = []
    
    # Try to use a specialized provider first
    provider = get_file_provider(source)
    if provider:
        try:
            file_content = provider.parse(source)
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



def read_dir(source, recursive=False, ext="*", filter_regex=None):
    """Read all files in a directory using the read_file function.

    Args:
        source (str): The directory path.
        recursive (bool): Whether to include files in subdirectories.
        ext (str): File extension to filter by (e.g., 'txt', 'py', '*' for all files).

    Returns:
        dict: A dictionary with file paths as keys and their contents as values,
              where each file's content is prepended with "[<FILENAME>]\n".
    """
    file_contents = []
    source_path = Path(source)
    pattern = f"**/*.{ext}" if recursive else f"*.{ext}"
    for file_path in source_path.glob(pattern):
        file_contents.append(read_file(file_path, filter_regex))

    return "\n".join(file_contents)





def parse(source, recursive = False, ext='*', filter_regex=None):
    type = check_type(source)
    if type == PathType.FILE: 
        return read_file(source, filter_regex)
    elif type == PathType.DIR:
        return read_dir(source, recursive, ext, filter_regex)