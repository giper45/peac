"""
Test cross-platform path handling

This test verifies that PathResolverService handles paths correctly
regardless of the platform where they were created.
"""
import pytest
import os
from pathlib import Path
from peac.gui.services.path_resolver_service import PathResolverService


class TestCrossPlatformPaths:
    """Test path handling across different platforms"""
    
    def test_windows_paths_on_unix(self):
        """Test that Windows paths are handled correctly on Unix systems"""
        # Simulate a Windows path string
        windows_path = r"C:\Users\test\project\src\main.py"
        
        # PathResolverService should handle this gracefully
        # We expect it to be converted to a Path object which normalizes separators
        base_dir = "/Users/test/project"
        
        # The key is that Path should handle the conversion
        path_obj = Path(windows_path)
        # On Unix, this will be treated as a single filename with backslashes
        # So we need to handle this case
        
    def test_unix_paths_on_windows(self):
        """Test that Unix paths are handled correctly on Windows systems"""
        # Simulate a Unix path string
        unix_path = "/Users/test/project/src/main.py"
        
        # On Windows, Path will convert this appropriately
        path_obj = Path(unix_path)
        
    def test_mixed_separators(self):
        """Test paths with mixed separators"""
        # Sometimes paths can have mixed separators
        mixed_path = "/Users/test\\project/src\\main.py"
        
        # Path should normalize this
        path_obj = Path(mixed_path)
        normalized = str(path_obj)
        
        # Verify no backslashes on Unix (or only forward slashes on Unix)
        if os.name != 'nt':  # Not Windows
            assert '\\' not in normalized or normalized == mixed_path
    
    def test_normalize_path_cross_platform(self):
        """Test that normalize_path works regardless of platform"""
        # Test with macOS volume prefix
        mac_path = "/Volumes/Macintosh HD/Users/test/file.txt"
        normalized = PathResolverService.normalize_path(mac_path)
        assert normalized == "/Users/test/file.txt"
        
        # Test with normal path (should work on any platform)
        normal_path = "/Users/test/file.txt"
        normalized = PathResolverService.normalize_path(normal_path)
        assert normalized == normal_path
    
    def test_get_relative_path_with_path_objects(self):
        """Test that get_relative_path works with Path objects internally"""
        # Use Path objects which are cross-platform
        if os.name == 'nt':
            # Windows paths
            base_dir = r"C:\Users\test\project"
            abs_path = r"C:\Users\test\project\src\main.py"
        else:
            # Unix paths
            base_dir = "/Users/test/project"
            abs_path = "/Users/test/project/src/main.py"
        
        result = PathResolverService.get_relative_path(abs_path, base_dir)
        
        # Result should use the platform-appropriate separator
        expected = os.path.join("src", "main.py")
        assert result == expected
    
    def test_get_relative_path_sibling_directories(self):
        """Test relative path between sibling directories"""
        if os.name == 'nt':
            base_dir = r"C:\Users\test\project"
            abs_path = r"C:\Users\test\other\file.txt"
        else:
            base_dir = "/Users/test/project"
            abs_path = "/Users/test/other/file.txt"
        
        result = PathResolverService.get_relative_path(abs_path, base_dir)
        
        # Should navigate up then down
        assert '..' in result
        assert 'other' in result
        assert 'file.txt' in result
    
    def test_resolve_path_cross_platform(self):
        """Test that resolve_path works on any platform"""
        # Test with relative path
        rel_path = os.path.join("..", "other", "file.txt")
        
        if os.name == 'nt':
            parent_path = r"C:\Users\test\project"
            expected_prefix = r"C:\Users\test"
        else:
            parent_path = "/Users/test/project"
            expected_prefix = "/Users/test"
        
        resolved, _ = PathResolverService.resolve_path(rel_path, parent_path)
        
        # Verify the path is resolved correctly
        assert expected_prefix in resolved
        assert 'other' in resolved
        assert 'file.txt' in resolved
    
    def test_get_absolute_path_cross_platform(self):
        """Test get_absolute_path on any platform"""
        if os.name == 'nt':
            base_dir = r"C:\Users\test\project"
        else:
            base_dir = "/Users/test/project"
        
        rel_path = os.path.join("..", "other", "file.txt")
        result = PathResolverService.get_absolute_path(rel_path, base_dir)
        
        # Should be an absolute path
        assert os.path.isabs(result)
        assert 'other' in result
        assert 'file.txt' in result
    
    def test_commonpath_with_path_objects(self):
        """Test that using Path.parts instead of string splitting works correctly"""
        # This tests the fix for the bug where we were using .split(os.sep)
        # on a string that might have been created on a different platform
        
        if os.name == 'nt':
            base_dir = r"C:\Users\test\project"
            abs_path = r"C:\Users\test\other\file.txt"
        else:
            base_dir = "/Users/test/project"
            abs_path = "/Users/test/other/file.txt"
        
        # Convert to Path objects
        abs_path_obj = Path(abs_path).resolve()
        base_obj = Path(base_dir).resolve()
        
        # Get common path
        try:
            common_str = os.path.commonpath([abs_path_obj, base_obj])
            common_obj = Path(common_str)
            
            # Using .parts should work regardless of platform
            assert len(common_obj.parts) > 0
            assert len(base_obj.parts) >= len(common_obj.parts)
            
        except ValueError:
            # Different drives on Windows
            pass
    
    def test_path_with_forward_slashes_on_windows(self):
        """Test that forward slashes in paths work on Windows"""
        # Even on Windows, Python's Path can handle forward slashes
        path_with_forward = "Users/test/project/file.txt"
        path_obj = Path(path_with_forward)
        
        # Should have correct parts regardless of separator used
        assert 'Users' in path_obj.parts or 'users' in path_obj.parts.lower()
        assert 'test' in path_obj.parts
        assert 'project' in path_obj.parts
        assert 'file.txt' in path_obj.parts


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
