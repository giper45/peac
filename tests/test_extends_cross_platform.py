"""
Test cross-platform path handling in extends

This test verifies that YAML files with extends can use both Windows and Unix path separators
and still work correctly on any platform.
"""
import pytest
import os
import tempfile
from pathlib import Path
from peac.core.peac import PromptYaml, find_path


class TestExtendsCrossPlatform:
    """Test extends with cross-platform paths"""
    
    def test_find_path_with_windows_separators(self):
        """Test that find_path handles Windows-style separators on Unix"""
        # Simulate a Windows-style path
        windows_path = "subfolder\\file.txt"
        parent = "/Users/test/project"
        
        resolved, _ = find_path(windows_path, parent)
        
        # Should resolve correctly regardless of separator
        assert "subfolder" in resolved
        assert "file.txt" in resolved
        # On Unix, Path will convert \ to /
        if os.name != 'nt':
            # The path should exist conceptually (even if the file doesn't)
            assert Path(resolved).parent.name == "subfolder"
    
    def test_find_path_with_unix_separators(self):
        """Test that find_path handles Unix-style separators on Windows"""
        # Simulate a Unix-style path
        unix_path = "subfolder/file.txt"
        
        if os.name == 'nt':
            parent = "C:\\Users\\test\\project"
        else:
            parent = "/Users/test/project"
        
        resolved, _ = find_path(unix_path, parent)
        
        # Should resolve correctly regardless of separator
        assert "subfolder" in resolved
        assert "file.txt" in resolved
    
    def test_find_path_with_mixed_separators(self):
        """Test that find_path handles mixed separators"""
        mixed_path = "subfolder\\nested/file.txt"
        parent = "/Users/test/project"
        
        resolved, _ = find_path(mixed_path, parent)
        
        # Path should handle this gracefully
        assert "file.txt" in resolved
    
    def test_extends_with_windows_paths(self, tmp_path):
        """Test that YAML extends work with Windows-style paths"""
        # Create a temporary directory structure
        base_dir = tmp_path / "test_project"
        base_dir.mkdir()
        
        subfolder = base_dir / "nutrizione"
        subfolder.mkdir()
        
        # Create base YAML file
        base_yaml = subfolder / "base.yaml"
        base_yaml.write_text("""prompt:
  instruction:
    base:
      - "Base instruction"
  query: "Base query"
""")
        
        # Create child YAML with Windows-style path in extends
        child_yaml = base_dir / "child.yaml"
        # Use Windows-style backslash even on Unix
        child_yaml.write_text("""prompt:
  extends:
    - nutrizione\\base.yaml
  instruction:
    base:
      - "Child instruction"
  query: "Child query"
""")
        
        # Load the child YAML
        prompt = PromptYaml(str(child_yaml))
        
        # Verify it loaded correctly and found the parent
        assert len(prompt.parents) == 1
        # Check that both child and parent instructions are accessible
        child_instructions = prompt.get_instruction_base_rules()
        parent_instructions = prompt.parents[0].get_instruction_base_rules()
        assert "Child instruction" in str(child_instructions)
        assert "Base instruction" in str(parent_instructions)
    
    def test_extends_with_unix_paths(self, tmp_path):
        """Test that YAML extends work with Unix-style paths"""
        # Create a temporary directory structure
        base_dir = tmp_path / "test_project"
        base_dir.mkdir()
        
        subfolder = base_dir / "nutrizione"
        subfolder.mkdir()
        
        # Create base YAML file
        base_yaml = subfolder / "base.yaml"
        base_yaml.write_text("""prompt:
  instruction:
    base:
      - "Base instruction"
  query: "Base query"
""")
        
        # Create child YAML with Unix-style path in extends
        child_yaml = base_dir / "child.yaml"
        # Use Unix-style forward slash
        child_yaml.write_text("""prompt:
  extends:
    - nutrizione/base.yaml
  instruction:
    base:
      - "Child instruction"
  query: "Child query"
""")
        
        # Load the child YAML
        prompt = PromptYaml(str(child_yaml))
        
        # Verify it loaded correctly and found the parent
        assert len(prompt.parents) == 1
        # Check that both child and parent instructions are accessible
        child_instructions = prompt.get_instruction_base_rules()
        parent_instructions = prompt.parents[0].get_instruction_base_rules()
        assert "Child instruction" in str(child_instructions)
        assert "Base instruction" in str(parent_instructions)
    
    def test_hierarchical_extends_with_mixed_paths(self, tmp_path):
        """Test that hierarchical extends work with mixed path styles"""
        # Create a temporary directory structure
        base_dir = tmp_path / "test_project"
        base_dir.mkdir()
        
        subfolder = base_dir / "nutrizione"
        subfolder.mkdir()
        
        # Create grandparent YAML
        grandparent_yaml = subfolder / "grandparent.yaml"
        grandparent_yaml.write_text("""prompt:
  instruction:
    base:
      - "Grandparent instruction"
  query: "Grandparent query"
""")
        
        # Create parent YAML with Windows-style path
        parent_yaml = subfolder / "parent.yaml"
        parent_yaml.write_text("""prompt:
  extends:
    - grandparent.yaml
  instruction:
    base:
      - "Parent instruction"
  query: "Parent query"
""")
        
        # Create child YAML with Windows-style path (from root)
        child_yaml = base_dir / "child.yaml"
        child_yaml.write_text("""prompt:
  extends:
    - nutrizione\\parent.yaml
  instruction:
    base:
      - "Child instruction"
  query: "Child query"
""")
        
        # Load the child YAML
        prompt = PromptYaml(str(child_yaml))
        
        # Verify hierarchical inheritance works
        assert len(prompt.parents) == 1
        # Check child, parent, and grandparent
        child_instructions = prompt.get_instruction_base_rules()
        parent_instructions = prompt.parents[0].get_instruction_base_rules()
        grandparent_instructions = prompt.parents[0].parents[0].get_instruction_base_rules()
        
        assert "Child instruction" in str(child_instructions)
        assert "Parent instruction" in str(parent_instructions)
        assert "Grandparent instruction" in str(grandparent_instructions)
    
    def test_real_usecase_nutrizione_vegetariana(self):
        """Test the actual nutrizione-vegetariana.yaml file from usecase"""
        usecase_dir = Path(__file__).parent.parent / "examples" / "usecase"
        
        if not usecase_dir.exists():
            pytest.skip(f"Usecase directory not found at {usecase_dir}")
        
        vegetariana_yaml = usecase_dir / "nutrizione-vegetariana.yaml"
        
        if not vegetariana_yaml.exists():
            pytest.skip(f"nutrizione-vegetariana.yaml not found at {vegetariana_yaml}")
        
        # This should work even if nutrizione-base.yaml uses Windows paths
        try:
            prompt = PromptYaml(str(vegetariana_yaml))
            
            # Verify it loaded correctly
            assert prompt is not None
            
            # Should have parent (nutrizione-base.yaml)
            assert len(prompt.parents) > 0
            
            # Should be able to get instructions
            instructions = str(prompt.get_instruction_base_rules())
            assert len(instructions) > 0
            
        except FileNotFoundError as e:
            pytest.fail(f"Failed to load YAML with extends: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
