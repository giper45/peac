"""
Test for local rules validation
"""
import os
import pytest
from peac.core.peac import PromptYaml


class TestLocalRulesValidation:
    """Test that local rules are properly validated"""
    
    def test_local_rule_missing_source(self):
        """Test that missing 'source' field in local rule is handled gracefully"""
        # Create a temporary yaml with malformed local rule
        test_yaml_content = """prompt:
  context:
    local:
      test-rule:
        preamble: "Test preamble"
        # Missing 'source' field - should trigger error
  query: "Test query"
"""
        test_file = "tests/test_malformed_local.yaml"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_yaml_content)
        
        try:
            py = PromptYaml(test_file)
            prompt = py.get_prompt_sentence()
            
            # Should include error message, not crash with KeyError
            assert "Error in 'context.local.test-rule': missing required 'source' field" in prompt
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)
    
    def test_local_rule_with_valid_source(self):
        """Test that valid local rule works correctly"""
        # Use existing valid yaml file
        yaml_file = "examples/usecase/nutrizione-base.yaml"
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        # This should not raise KeyError
        py = PromptYaml(yaml_file)
        prompt = py.get_prompt_sentence()
        
        # Should generate prompt without errors
        assert len(prompt) > 0
        assert "[Output]" in prompt or "[Context]" in prompt
