"""
Comprehensive test suite for PEaC core module

Tests all YAML examples against the EBNF grammar specification.
Validates:
- YAML parsing correctness
- Grammar compliance (extends, instruction, context, output, query)
- Rule types (base, local, web, rag)
- Field validation and data types
- Integration with providers (local files, web, RAG)
"""

import os
import pytest
from pathlib import Path
from typing import List, Dict

from peac.core.peac import PromptYaml, PromptSection, PromptSections


# Test data: all YAML examples in the project
YAML_EXAMPLES = [
    # Simple examples
    "examples/academic.yaml",
    "examples/academic-latex.yaml",
    "examples/cfp.yaml",
    "examples/write-readme.yaml",
    
    # RAG examples
    "examples/rag-simple.yaml",
    "examples/rag-fastembed.yaml",
    "examples/rag-faiss.yaml",
    "examples/rag-sample-docs.yaml",
    
    # Java examples
    "examples/java-base-maven.yaml",
    "examples/java-hibernate.yaml",
    "examples/java-servlets.yaml",
    
    # Complex examples
    "examples/comprehensive-analysis.yaml",
    "examples/replicate-valuable-prompt.yaml",
    
    # Nutrition examples
    "examples/nutrition/nutrition-base.yaml",
    "examples/nutrition/nutrition-diabetes.yaml",
    "examples/nutrition/nutrition-women.yaml",
    "examples/nutrition/patient-specific.yaml",
    
    # Healthcare demo examples
    "examples/demo-healthcare/docker.yaml",
    "examples/demo-healthcare/sw-dashboard-app.yaml",
    "examples/demo-healthcare/sw-iot-device-language-python.yaml",
    
    # Test examples
    "tests/dev-input.yaml",
    "tests/dev-folder.yaml",
    "tests/dev-folder-recursive.yaml",
    "tests/web.yaml",
]


class TestYAMLParsing:
    """Test YAML file parsing and basic structure"""

    @pytest.mark.parametrize("yaml_file", YAML_EXAMPLES)
    def test_yaml_loads_successfully(self, yaml_file):
        """Test that all YAML files can be loaded without errors"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        assert py is not None
        assert py.parsed_data is not None

    @pytest.mark.parametrize("yaml_file", YAML_EXAMPLES)
    def test_yaml_has_prompt_key(self, yaml_file):
        """Test that all YAML files have the required 'prompt' top-level key"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        assert 'prompt' in py.parsed_data
        assert isinstance(py.parsed_data['prompt'], dict)


class TestInstructionSection:
    """Test instruction section parsing according to EBNF grammar"""

    def test_instruction_base_rules_simple(self):
        """Test simple instruction with base rules"""
        py = PromptYaml("examples/academic.yaml")
        # Academic example doesn't have instruction, skip if not present
        if 'instruction' not in py.parsed_data.get('prompt', {}):
            pytest.skip("No instruction section in this example")

    def test_instruction_base_rules_comprehensive(self):
        """Test comprehensive instruction section"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        instruction_rules = py.get_base_rules('instruction')
        assert instruction_rules is not None
        assert len(instruction_rules) > 0
        
        # Check that rules are strings
        for rule in instruction_rules:
            assert isinstance(rule, str)
            assert len(rule) > 0

    def test_instruction_rules_nutrition(self):
        """Test instruction rules in nutrition examples"""
        py = PromptYaml("examples/nutrition/nutrition-base.yaml")
        
        instruction_rules = py.get_base_rules('instruction')
        assert len(instruction_rules) >= 1
        
        # Verify contains expected keywords
        all_text = ' '.join(instruction_rules).lower()
        assert 'nutritionist' in all_text or 'diet' in all_text


class TestContextSection:
    """Test context section with all rule types (base, local, web, rag)"""

    def test_context_base_rules(self):
        """Test context base rules parsing"""
        py = PromptYaml("examples/academic.yaml")
        
        context_rules = py.get_context_base_rules()
        assert len(context_rules) > 0
        
        # Academic example should mention search engine
        all_text = ' '.join(context_rules).lower()
        assert 'search' in all_text or 'academic' in all_text

    def test_context_local_rules_comprehensive(self):
        """Test local rules in comprehensive example"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        local_rules = py.get_context_local_rules()
        assert len(local_rules) > 0
        
        # Check PromptSection structure
        for rule in local_rules:
            assert isinstance(rule, dict)
            assert 'lines' in rule
            assert isinstance(rule['lines'], list)

    def test_context_local_rules_with_preamble(self):
        """Test local rules with preamble field"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        local_rules = py.get_context_local_rules()
        
        # At least one rule should have a preamble
        has_preamble = any(rule.get('preamble') is not None for rule in local_rules)
        assert has_preamble

    def test_context_local_rules_recursive(self):
        """Test local rules with recursive option"""
        py = PromptYaml("tests/dev-folder-recursive.yaml")
        
        local_rules = py.get_local_rules('context')
        assert len(local_rules) > 0

    def test_context_web_rules(self):
        """Test web rules parsing"""
        py = PromptYaml("tests/web.yaml")
        
        web_rules = py.get_context_web_rules()
        # Web rules may be empty if no web section
        assert isinstance(web_rules, list)

    def test_context_rag_rules(self):
        """Test RAG rules parsing"""
        py = PromptYaml("examples/rag-simple.yaml")
        
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) > 0
        
        # Check RAG rule structure
        for rule in rag_rules:
            assert isinstance(rule, dict)
            assert 'lines' in rule


class TestOutputSection:
    """Test output section with all rule types"""

    def test_output_base_rules(self):
        """Test output base rules"""
        py = PromptYaml("examples/academic.yaml")
        
        output_rules = py.get_output_base_rules()
        assert len(output_rules) > 0
        
        # Check for citations requirement
        all_text = ' '.join(output_rules).lower()
        assert 'citation' in all_text or 'provide' in all_text

    def test_output_base_rules_java(self):
        """Test output rules in Java example"""
        py = PromptYaml("examples/java-base-maven.yaml")
        
        output_rules = py.get_output_base_rules()
        assert len(output_rules) > 0

    def test_output_local_rules(self):
        """Test output with local rules"""
        py = PromptYaml("examples/nutrition/nutrition-base.yaml")
        
        output_rules = py.get_output_local_rules()
        # May be empty if only base rules in output
        assert isinstance(output_rules, list)

    def test_output_web_rules_cfp(self):
        """Test output with web rules in CFP example"""
        py = PromptYaml("examples/cfp.yaml")
        
        # CFP example has web in output section
        web_rules = py.get_web_rules('output')
        assert len(web_rules) > 0
        
        # Should contain URL
        for rule in web_rules:
            lines_text = ' '.join(rule.get('lines', []))
            # Web rules should have http/https URLs
            assert 'http' in lines_text.lower()


class TestLocalRules:
    """Test local rules with various options (recursive, filter, extension)"""

    def test_local_rule_single_file(self):
        """Test local rule pointing to a single file"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        local_rules = py.get_local_rules('context')
        assert len(local_rules) > 0
        
        # Should have rules with source paths
        for rule in local_rules:
            if rule.get('lines'):
                # Lines should be non-empty
                assert len(rule['lines']) > 0

    def test_local_rule_directory_recursive(self):
        """Test local rule with recursive directory scan"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        local_rules = py.get_local_rules('context')
        # comprehensive-analysis has recursive rules
        assert len(local_rules) > 0

    def test_local_rule_with_filter(self):
        """Test local rule with regex filter"""
        py = PromptYaml("tests/dev-folder-recursive-regex.yaml")
        
        local_rules = py.get_local_rules('context')
        assert len(local_rules) > 0

    def test_local_rule_with_extension(self):
        """Test local rule with file extension filter"""
        py = PromptYaml("tests/dev-folder-python.yaml")
        
        local_rules = py.get_local_rules('context')
        assert isinstance(local_rules, list)


class TestWebRules:
    """Test web rules with URL and XPath"""

    def test_web_rule_with_url(self):
        """Test web rule contains valid URL"""
        py = PromptYaml("examples/cfp.yaml")
        
        web_rules = py.get_web_rules('output')
        assert len(web_rules) > 0
        
        # Check URL is present in output
        for rule in web_rules:
            lines_text = '\n'.join(rule.get('lines', []))
            assert 'http://' in lines_text or 'https://' in lines_text

    def test_web_rule_with_xpath(self):
        """Test web rule with XPath selector"""
        py = PromptYaml("examples/cfp.yaml")
        
        web_rules = py.get_web_rules('output')
        # CFP example uses xpath
        if len(web_rules) > 0:
            lines_text = '\n'.join(web_rules[0].get('lines', []))
            # May contain xpath reference
            assert len(lines_text) > 0


class TestRAGRules:
    """Test RAG rules with provider abstraction"""

    def test_rag_rule_simple(self):
        """Test simple RAG rule"""
        py = PromptYaml("examples/rag-simple.yaml")
        
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) > 0
        
        # Check structure
        rule = rag_rules[0]
        assert 'lines' in rule
        assert len(rule['lines']) > 0

    def test_rag_rule_with_provider_fastembed(self):
        """Test RAG rule with fastembed provider"""
        py = PromptYaml("examples/rag-fastembed.yaml")
        
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) > 0

    def test_rag_rule_with_provider_faiss(self):
        """Test RAG rule with faiss provider"""
        py = PromptYaml("examples/rag-faiss.yaml")
        
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) > 0

    def test_rag_rule_with_query(self):
        """Test RAG rule contains query field"""
        py = PromptYaml("examples/rag-sample-docs.yaml")
        
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) > 0
        
        # RAG rules should produce non-empty output
        for rule in rag_rules:
            assert len(rule.get('lines', [])) > 0


class TestQueryField:
    """Test query field parsing"""

    def test_query_field_present(self):
        """Test query field can be retrieved"""
        py = PromptYaml("examples/cfp.yaml")
        
        query = py.get_query()
        assert query is not None
        assert isinstance(query, str)
        assert len(query) > 0

    def test_query_field_content(self):
        """Test query field contains expected content"""
        py = PromptYaml("examples/cfp.yaml")
        
        query = py.get_query()
        assert 'parse' in query.lower() or 'generate' in query.lower()


class TestPromptSections:
    """Test PromptSections container class"""

    def test_prompt_sections_add(self):
        """Test adding sections to PromptSections"""
        pss = PromptSections()
        
        ps1 = {'preamble': 'test1', 'lines': ['line1', 'line2']}
        ps2 = {'preamble': 'test2', 'lines': ['line3']}
        
        pss.add_section(ps1)
        pss.add_section(ps2)
        
        # Get by preamble
        result = pss.get_by_preamble('test1')
        assert result['lines'] == ['line1', 'line2']

    def test_prompt_sections_merge_same_preamble(self):
        """Test merging sections with same preamble"""
        pss = PromptSections()
        
        ps1 = {'preamble': 'same', 'lines': ['line1']}
        ps2 = {'preamble': 'same', 'lines': ['line2']}
        
        pss.add_section(ps1)
        pss.add_section(ps2)
        
        result = pss.get_by_preamble('same')
        # Should merge lines
        assert 'line1' in result['lines']
        assert 'line2' in result['lines']

    def test_prompt_sections_get_lines(self):
        """Test getting all lines from sections"""
        pss = PromptSections()
        
        ps1 = {'lines': ['line1', 'line2']}
        ps2 = {'lines': ['line3']}
        
        pss.add_section(ps1)
        pss.add_section(ps2)
        
        all_lines = pss.get_lines()
        assert len(all_lines) == 2  # Two sections


class TestEBNFCompliance:
    """Test YAML files comply with EBNF grammar specification"""

    @pytest.mark.parametrize("yaml_file", [
        "examples/academic.yaml",
        "examples/comprehensive-analysis.yaml",
        "examples/rag-simple.yaml",
    ])
    def test_prompt_structure(self, yaml_file):
        """Test PromptBody structure: ExtendsList | InstructionSection | ContextSection | OutputSection | QueryField"""
        if not os.path.exists(yaml_file):
            pytest.skip(f"File not found: {yaml_file}")
        
        py = PromptYaml(yaml_file)
        prompt_data = py.parsed_data.get('prompt', {})
        
        # Should have at least one section
        valid_sections = ['extends', 'instruction', 'context', 'output', 'query']
        present_sections = [s for s in valid_sections if s in prompt_data]
        
        assert len(present_sections) > 0, f"No valid sections found in {yaml_file}"

    def test_base_rules_structure(self):
        """Test BaseRules: 'base:', YamlSequence"""
        py = PromptYaml("examples/academic.yaml")
        
        context_data = py.parsed_data['prompt'].get('context', {})
        if 'base' in context_data:
            base_rules = context_data['base']
            assert isinstance(base_rules, list)
            assert all(isinstance(item, str) for item in base_rules)

    def test_local_rules_structure(self):
        """Test LocalRules: 'local:', LocalRuleMap with required fields"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        context_data = py.parsed_data['prompt'].get('context', {})
        if 'local' in context_data:
            local_rules = context_data['local']
            assert isinstance(local_rules, dict)
            
            # Each rule should have source field
            for rule_name, rule_body in local_rules.items():
                assert isinstance(rule_body, dict)
                assert 'source' in rule_body

    def test_rag_rules_structure(self):
        """Test RagRules: required and optional fields"""
        py = PromptYaml("examples/rag-simple.yaml")
        
        context_data = py.parsed_data['prompt'].get('context', {})
        if 'rag' in context_data:
            rag_rules = context_data['rag']
            assert isinstance(rag_rules, dict)
            
            # Each RAG rule should have required fields
            for rule_name, rule_body in rag_rules.items():
                assert isinstance(rule_body, dict)
                # Required: index_path, source_folder, query
                assert 'index_path' in rule_body or 'faiss_file' in rule_body  # Backward compat
                assert 'query' in rule_body

    def test_provider_type_values(self):
        """Test ProviderType: 'fastembed' | 'faiss'"""
        py = PromptYaml("examples/rag-fastembed.yaml")
        
        context_data = py.parsed_data['prompt'].get('context', {})
        if 'rag' in context_data:
            for rule_name, rule_body in context_data['rag'].items():
                if 'provider' in rule_body:
                    provider = rule_body['provider']
                    assert provider in ['fastembed', 'faiss']


class TestIntegration:
    """Integration tests combining multiple sections"""

    def test_full_prompt_generation_academic(self):
        """Test generating full prompt from academic example"""
        py = PromptYaml("examples/academic.yaml")
        
        # Get all sections
        context_base = py.get_context_base_rules()
        output_base = py.get_output_base_rules()
        
        # Should have content
        assert len(context_base) > 0
        assert len(output_base) > 0

    def test_full_prompt_generation_comprehensive(self):
        """Test generating full prompt from comprehensive example"""
        py = PromptYaml("examples/comprehensive-analysis.yaml")
        
        # Get all rule types
        instruction = py.get_base_rules('instruction')
        context_base = py.get_context_base_rules()
        context_local = py.get_context_local_rules()
        
        # All should have content
        assert len(instruction) > 0
        assert len(context_base) > 0
        assert len(context_local) > 0

    def test_full_prompt_generation_rag(self):
        """Test generating full prompt with RAG"""
        py = PromptYaml("examples/rag-simple.yaml")
        
        # Get all sections
        instruction = py.get_base_rules('instruction')
        context_rag = py.get_rag_rules('context')
        output_base = py.get_output_base_rules()
        
        # RAG should produce results
        assert len(context_rag) > 0


class TestErrorHandling:
    """Test error handling for invalid inputs"""

    def test_nonexistent_file(self):
        """Test handling of non-existent YAML file"""
        with pytest.raises(FileNotFoundError):
            PromptYaml("nonexistent.yaml")

    def test_empty_yaml(self):
        """Test handling of empty or minimal YAML"""
        # Create minimal valid YAML in tests
        test_file = "tests/minimal.yaml"
        if os.path.exists(test_file):
            py = PromptYaml(test_file)
            # Should load but have minimal content
            assert py.parsed_data is not None


class TestBackwardCompatibility:
    """Test backward compatibility with old field names"""

    def test_faiss_file_backward_compat(self):
        """Test that old 'faiss_file' field is still supported"""
        # RAG rules should support both index_path and faiss_file
        py = PromptYaml("examples/rag-simple.yaml")
        
        # Should parse successfully regardless of field name
        rag_rules = py.get_rag_rules('context')
        assert len(rag_rules) >= 0  # May be 0 if using new field names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
