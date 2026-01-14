"""
Test suite for all nutrizione-* YAML files in usecase folder
Verifies that all nutrition-related YAML files can be parsed and generate prompts without errors
"""
import os
import glob
import pytest
from peac.core.peac import PromptYaml


class TestNutrizioneFiles:
    """Test all nutrizione-*.yaml files for correctness"""
    
    # Collect all nutrizione-*.yaml files
    NUTRIZIONE_FILES = sorted(glob.glob("examples/usecase/nutrizione-*.yaml"))
    
    @pytest.mark.parametrize("yaml_file", NUTRIZIONE_FILES)
    def test_nutrizione_file_parsing(self, yaml_file):
        """Test that each nutrizione YAML file can be parsed without errors"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        # Should not raise any exception during parsing
        py = PromptYaml(yaml_file)
        assert py is not None
        assert py.parsed_data is not None
        assert 'prompt' in py.parsed_data
    
    @pytest.mark.parametrize("yaml_file", NUTRIZIONE_FILES)
    def test_nutrizione_file_prompt_generation(self, yaml_file):
        """Test that each nutrizione YAML file can generate a prompt sentence"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        
        # Should generate prompt without KeyError or other exceptions
        try:
            prompt_sentence = py.get_prompt_sentence()
            
            # Verify basic structure
            assert prompt_sentence is not None
            assert len(prompt_sentence) > 0
            
            # Should not contain error messages from malformed rules
            assert "Error in" not in prompt_sentence or "missing required 'source' field" not in prompt_sentence, \
                f"Found validation errors in {yaml_file}"
            
        except KeyError as e:
            pytest.fail(f"KeyError in {yaml_file}: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error in {yaml_file}: {type(e).__name__}: {e}")
    
    @pytest.mark.parametrize("yaml_file", NUTRIZIONE_FILES)
    def test_nutrizione_file_has_required_sections(self, yaml_file):
        """Test that each nutrizione YAML file has expected sections"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_data = py.parsed_data.get('prompt', {})
        
        # Each file should have at least a query
        assert 'query' in prompt_data, f"{yaml_file} missing 'query' field"
        assert isinstance(prompt_data['query'], str), f"{yaml_file} query must be a string"
        assert len(prompt_data['query']) > 0, f"{yaml_file} query cannot be empty"
        
        # Should have at least one of: instruction, context, output, or extends
        has_content = any(key in prompt_data for key in ['instruction', 'context', 'output', 'extends'])
        assert has_content, f"{yaml_file} has no instruction, context, output, or extends sections"
    
    @pytest.mark.parametrize("yaml_file", NUTRIZIONE_FILES)
    def test_nutrizione_file_local_rules_valid(self, yaml_file):
        """Test that all local rules in nutrizione files have required 'source' field"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_data = py.parsed_data.get('prompt', {})
        
        # Check all sections that might have local rules
        for section in ['instruction', 'context', 'output']:
            if section in prompt_data:
                section_data = prompt_data[section]
                if isinstance(section_data, dict) and 'local' in section_data:
                    local_rules = section_data['local']
                    assert isinstance(local_rules, dict), \
                        f"{yaml_file}: {section}.local must be a dict"
                    
                    for rule_name, rule_data in local_rules.items():
                        assert isinstance(rule_data, dict), \
                            f"{yaml_file}: {section}.local.{rule_name} must be a dict, got {type(rule_data)}"
                        assert 'source' in rule_data, \
                            f"{yaml_file}: {section}.local.{rule_name} missing required 'source' field"
    
    def test_all_nutrizione_files_found(self):
        """Verify that we found nutrizione files to test"""
        assert len(self.NUTRIZIONE_FILES) > 0, "No nutrizione-*.yaml files found in examples/usecase/"
        
        # List all found files for visibility
        print(f"\nFound {len(self.NUTRIZIONE_FILES)} nutrizione files:")
        for f in self.NUTRIZIONE_FILES:
            print(f"  - {f}")
