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


def read_file(source, filter_regex=None):
    """Read the filename

    Args:
        source (str): the filename
    """
    file_content = ""
    lines = []

    with open(source) as f:
        lines = f.readlines()
    if filter_regex:
        pattern = re.compile(filter_regex)
        lines = [line for line in lines if pattern.search(line)]

    file_content = "\n".join(lines)
        
    """ File output:
        [filename] 
        ```

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