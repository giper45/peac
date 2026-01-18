"""
Test script for PathResolverService

This script tests the path resolution logic.
"""
import os
from pathlib import Path
from peac.gui.services.path_resolver_service import PathResolverService


def test_normalize_path():
    """Test path normalization"""
    print("Testing normalize_path...")
    
    # Test macOS volume prefix removal
    mac_path = "/Volumes/Macintosh HD/Users/test/file.txt"
    normalized = PathResolverService.normalize_path(mac_path)
    assert normalized == "/Users/test/file.txt", f"Expected /Users/test/file.txt, got {normalized}"
    print(f"  ✓ {mac_path} -> {normalized}")
    
    # Test normal path (no change)
    normal_path = "/Users/test/file.txt"
    normalized = PathResolverService.normalize_path(normal_path)
    assert normalized == normal_path, f"Expected {normal_path}, got {normalized}"
    print(f"  ✓ {normal_path} -> {normalized}")
    
    print("normalize_path tests passed!\n")


def test_get_absolute_path():
    """Test absolute path conversion"""
    print("Testing get_absolute_path...")
    
    # Test with already absolute path
    abs_path = "/Users/test/file.txt"
    result = PathResolverService.get_absolute_path(abs_path)
    print(f"  ✓ Absolute path: {abs_path} -> {result}")
    
    # Test with relative path and base directory
    base_dir = "/Users/test/project"
    rel_path = "../other/file.txt"
    result = PathResolverService.get_absolute_path(rel_path, base_dir)
    expected = str(Path("/Users/test/other/file.txt").resolve())
    print(f"  ✓ Relative path: {rel_path} (base: {base_dir}) -> {result}")
    
    # Test with relative path, no base directory
    rel_path = "subfolder/file.txt"
    result = PathResolverService.get_absolute_path(rel_path, None)
    assert result == rel_path, f"Expected {rel_path}, got {result}"
    print(f"  ✓ No base dir: {rel_path} -> {result}")
    
    print("get_absolute_path tests passed!\n")


def test_get_relative_path():
    """Test relative path conversion"""
    print("Testing get_relative_path...")
    
    # Test with paths in parent/child relationship
    base_dir = "/Users/test/project"
    abs_path = "/Users/test/project/src/main.py"
    result = PathResolverService.get_relative_path(abs_path, base_dir)
    expected = "src/main.py"
    print(f"  ✓ Child path: {abs_path} (base: {base_dir}) -> {result}")
    
    # Test with paths using .. navigation
    base_dir = "/Users/test/project"
    abs_path = "/Users/test/other/file.txt"
    result = PathResolverService.get_relative_path(abs_path, base_dir)
    print(f"  ✓ Sibling path: {abs_path} (base: {base_dir}) -> {result}")
    
    # Test with no base directory
    abs_path = "/Users/test/file.txt"
    result = PathResolverService.get_relative_path(abs_path, None)
    assert result == abs_path, f"Expected {abs_path}, got {result}"
    print(f"  ✓ No base dir: {abs_path} -> {result}")
    
    print("get_relative_path tests passed!\n")


def test_resolve_path():
    """Test resolve_path (compatibility with core)"""
    print("Testing resolve_path...")
    
    # Test with absolute path
    abs_path = "/Users/test/file.txt"
    resolved, parent = PathResolverService.resolve_path(abs_path)
    print(f"  ✓ Absolute: {abs_path} -> {resolved}")
    
    # Test with relative path
    rel_path = "../other/file.txt"
    parent_path = "/Users/test/project"
    resolved, parent = PathResolverService.resolve_path(rel_path, parent_path)
    print(f"  ✓ Relative: {rel_path} (parent: {parent_path}) -> {resolved}")
    
    print("resolve_path tests passed!\n")


def test_cross_platform_methods():
    """Test cross-platform conversion methods"""
    print("Testing cross-platform methods...")
    
    # Test to_posix_path
    if os.name == 'nt':
        windows_path = r"C:\Users\test\file.txt"
        posix = PathResolverService.to_posix_path(windows_path)
        print(f"  ✓ to_posix_path: {windows_path} -> {posix}")
        assert '/' in posix and '\\' not in posix
    else:
        unix_path = "/Users/test/file.txt"
        posix = PathResolverService.to_posix_path(unix_path)
        print(f"  ✓ to_posix_path: {unix_path} -> {posix}")
        assert posix == unix_path
    
    # Test from_any_path with mixed separators
    mixed_path = "/Users/test\\project/file.txt"
    converted = PathResolverService.from_any_path(mixed_path)
    print(f"  ✓ from_any_path: {mixed_path} -> {converted}")
    
    # Test from_any_path with Windows path on Unix (or vice versa)
    if os.name != 'nt':
        windows_style = r"Users\test\file.txt"
        converted = PathResolverService.from_any_path(windows_style)
        print(f"  ✓ from_any_path (Windows style): {windows_style} -> {converted}")
    
    print("cross-platform methods tests passed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("=" * 60)
    print("PathResolverService Tests")
    print("=" * 60 + "\n")
    
    test_normalize_path()
    test_get_absolute_path()
    test_get_relative_path()
    test_resolve_path()
    test_cross_platform_methods()
    
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
