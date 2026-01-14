"""
Test for hierarchical extends bug verification and fix
"""
import os
import pytest
from peac.core.peac import PromptYaml


class TestHierarchicalExtends:
    """Test that hierarchical extends (A extends B extends C) works correctly"""
    
    def test_hierarchical_extends_instructions(self):
        """Test: nutrizione-base -> nutrizione-pcos -> test-hierarchical-extends
        
        Should include:
        - Instructions from nutrizione-base (parent of parent)
        - Instructions from nutrizione-pcos (parent)
        - Instructions from test-hierarchical-extends (self)
        """
        yaml_file = "examples/usecase/test-hierarchical-extends.yaml"
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_sentence = py.get_prompt_sentence()
        
        # Get instruction output
        assert '[Instruction]' in prompt_sentence, "Missing [Instruction] section"
        
        # Check for instructions from self
        assert "Test instruction from test-hierarchical-extends.yaml" in prompt_sentence, \
            "Missing self instructions"
        
        # Check for instructions from parent (nutrizione-pcos)
        assert "Indice glicemico basso" in prompt_sentence, \
            "Missing parent (nutrizione-pcos) instructions"
        
        # BUG: Check for instructions from grandparent (nutrizione-base)
        # These should appear but currently don't!
        missing_from_base = [
            "Usa emoticon di cibo per un tocco visivo",  # From nutrizione-base output
            "Struttura il piano alimentare per giorni della settimana",  # From nutrizione-base output
            "Includi 5 pasti giornalieri",  # From nutrizione-base output
        ]
        
        for instr in missing_from_base:
            assert instr in prompt_sentence, \
                f"BUG: Missing grandparent (nutrizione-base) instruction: '{instr}'"
    
    def test_hierarchical_extends_output_rules(self):
        """Test that output rules are inherited through the hierarchy"""
        yaml_file = "examples/usecase/test-hierarchical-extends.yaml"
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_sentence = py.get_prompt_sentence()
        
        # Check for output instructions from grandparent (nutrizione-base)
        assert "Usa emoticon di cibo" in prompt_sentence or \
               "emoticon di cibo" in prompt_sentence, \
            "BUG: Missing emoji instruction from nutrizione-base"
        
        # Check for output instructions from parent (nutrizione-pcos)
        assert "Piano settimanale con focus low-GI" in prompt_sentence, \
            "Missing parent output instructions"
    
    def test_no_duplicates_in_hierarchical_extends(self):
        """Test that duplicate instructions don't appear multiple times in hierarchy"""
        yaml_file = "examples/usecase/test-hierarchical-extends.yaml"
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_sentence = py.get_prompt_sentence()
        
        # Extract output section
        output_start = prompt_sentence.find("[Output]")
        assert output_start != -1, "Missing [Output] section"
        
        output_section = prompt_sentence[output_start:]
        
        # Count occurrences of a unique instruction from nutrizione-base
        # that should appear only once, not duplicated
        unique_instruction = "Usa emoticon di cibo per un tocco visivo"
        count = output_section.count(unique_instruction)
        assert count == 1, \
            f"Duplicate instruction found! '{unique_instruction}' appears {count} times instead of 1"
        
        # Check another unique instruction from nutrizione-pcos
        unique_instruction2 = "Porzioni: pesate, CHO controllati"
        count2 = output_section.count(unique_instruction2)
        assert count2 == 1, \
            f"Duplicate instruction found! '{unique_instruction2}' appears {count2} times instead of 1"
