from peac.main import PromptSection, PromptSections, PromptYaml
import os

def test_prompt_sections():
    ps = PromptSection()

    expected_one : PromptSection = {
        'preamble': 'preamble',
        'lines': ['one', 'two', 'three', 'four']
    }

    pss = PromptSections()
    ps['preamble'] = 'preamble'
    ps['lines'] = ['one', 'two']


    ps2  : PromptSection = {
        'lines' : ['none one', 'none two']
    }

    ps3: PromptSection = {
        'preamble' : 'preamble', 
        'lines' : ['three', 'four']
    }

    pss.add_section(ps)
    pss.add_section(ps2)
    pss.add_section(ps3)
    pss.add_section(ps3)


    assert pss.get_by_preamble('preamble') == expected_one
    assert pss.get_by_preamble(None) == ps2





def test_answer():
    py = PromptYaml(os.path.join('tests', 'dev-input.yaml'))
    expected_context = "Context - use these rules for all next questions: (1) write code in Python language; (2) for each class, create a test class"
    expected_output = "Output - use these rules for all next questions: (1) only write code; (2) use camel case conventions for methods and functions; (3) only create classes"
    context_rules = py.get_context_base_rules()
    output_rules = py.get_output_base_rules()

    local_rules = py.get_context_local_rules() 
    assert expected_context == py.get_sentence('context', context_rules)
    assert expected_output == py.get_sentence('output', output_rules)



