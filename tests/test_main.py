from peac.main import PromptYaml
import os


def test_answer():
    py = PromptYaml(os.path.join('tests', 'dev-input.yaml'))
    expected_context = "Context - use these rules for all next questions: write code in Python language; for each class, create a test class"
    expected_output = "Output - use these rules for all next questions: only write code; use camel case conventions for methods and functions; only create classes"
    context_rules = py.get_context_base_rules()
    output_rules = py.get_output_base_rules()

    local_rules = py.get_context_local_rules() 
    assert expected_context == py.get_sentence('context', context_rules)
    assert expected_output == py.get_sentence('output', output_rules)

