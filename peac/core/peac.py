import os
import re
from typing import List
from xml.etree import ElementTree
import requests
from bs4 import BeautifulSoup

import markdown


import yaml
import validators
from peac import local_parser

from typing import TypedDict, Optional, List
import importlib.resources

## UTILS
def get_template_file():
    with importlib.resources.files('peac').joinpath('template.yaml').open('r') as f:
        template_content = f.read()
        return template_content


class PromptSection(TypedDict):
    preamble: Optional[str]
    lines: List[str]


class PromptSections:

    def __init__(self):
        self.prompt_sections = []



    def already_present(self, preamble):
        return self.get_by_preamble(preamble) != None

    def get_by_preamble(self, preamble):
        for p in self.prompt_sections:
            if preamble is None:
                if 'preamble' not in p:
                    return p
                elif p['preamble'] == None:
                    return p
            else:
                if 'preamble' in p and p['preamble'] == preamble:
                    return p
        return None

    def add_section(self, ps: PromptSection):
        if self.already_present(ps['preamble'] if 'preamble' in ps else None):
            preamble = self.get_by_preamble(ps['preamble'] if 'preamble' in ps else None)
            preamble['lines'].extend(ps['lines'])
            seen = set()
            preamble['lines'] = [line for line in preamble['lines'] if not (line in seen or seen.add(line))]
        else:
            self.prompt_sections.append(ps)

    def add_sections(self, pss: List[PromptSection]):
        for ps in pss:
            self.add_section(ps)

    def get_lines(self):
        lines = []
        for p in self.prompt_sections:
            if 'preamble' in p and p['preamble'] != None and p['preamble'].strip() != '':
                # Append the preamble to the first string in p['lines']
                if p['lines'] and p['lines'][0] is not None:
                    p['lines'][0] = f"{p['preamble']} - {p['lines'][0]}"
            lines.extend(p['lines'])
        # Filter out None values and apply regex cleanup
        lines = [re.sub(r'\n+', '\n', l) for l in lines if l is not None]
        return lines





# Utils


def get_text_from_markdown(md_content: str) -> str:
    html_content = markdown.markdown(md_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove scripts, styles, and other non-text elements
    for script in soup(['script', 'style']):
        script.extract()
    return soup.get_text()

def get_text_from_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        # Remove scripts, styles, and other non-text elements from body
        for script in body_content(['script', 'style']):
            script.extract()
        text = body_content.get_text(separator='\n')
        text = "\n".join(line for line in text.split("\n") if line.strip())
        return text

    else:
        return ""
    # soup = BeautifulSoup(html_content, 'html.parser')
    # # Remove scripts, styles, and other non-text elements
    # for script in soup(['script', 'style']):
    #     script.extract()
    # return soup.get_text()

def should_extract_text():
    return 'LLM_AS_CODE_ONLY_TEXT' in os.environ and os.environ['LLM_AS_CODE_ONLY_TEXT'].lower() in ['true', '1']

import re

def js_comment_clean(js):
    js = re.sub("<!--[\\s\\S]*?(?:-->)?","",js)
    js = re.sub("<!--[\\s\\S]*?-->?","",js)
    js = re.sub('<!---+>?','',js)
    # js = re.sub("|<!(?![dD][oO][cC][tT][yY][pP][eE]|\\[CDATA\\[)[^>]*>?","",js)
    # js = re.sub("|<[?][^>]*>?","",js)
    return js

def get_text_from_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return js_comment_clean(response.text)
        content_type = response.headers.get('Content-Type')
        if should_extract_text() and  content_type and 'text/markdown' in content_type:
            return get_text_from_markdown(response.text)
        elif should_extract_text() and content_type and 'text/html' in content_type:
            return get_text_from_html(response.text)
        else:
            return response.text
    else:
        print(f"Failed to fetch content from URL: {url}")
        return ""


def is_url(url: str) -> bool:
    return validators.url(url)


def parse_input_string(input_string):
    """Find content of input() snippets

    Args:
        input_string (str): The input() string

    Returns:
        str: The content inside input
    """
    # Find the position of the opening and closing parentheses
    start_index = input_string.find('input(')
    end_index = input_string.find(')')

    # Extract the content within the parentheses
    if start_index != -1 and end_index != -1:
        content = input_string[len("input("):-1]
        return content
    else:
        return None




#class ChatClient:
#    def __init__(self):
#        # self.client = Client()
#        self.messages = []
#        self.client = Client(
#            # provider=RetryProvider([Phind, FreeChatgpt, Liaobots], shuffle=False)
#        )
#
#
#    def ask(self, question):
#        self.messages.append({"role": "user", "content": question})
#        response = self.client.chat.completions.create(
#            # model="",
#            model="gpt-3.5-turbo",
#            # model="claude-3-opus",
#            # provider="",
#            messages=self.messages,
#        )
#        return response.choices[0].message.content




def get_preamble_phrase(prompt_element: str, add_section_headers=True):
    # return f"{prompt_element.capitalize()} - use these rules for all next questions:"
    if not add_section_headers:
        return ""
    return f"[{prompt_element.capitalize()}]\n"

def _create_answer_line(prompt_element, information, add_section_headers=True):
    lines = []
    index = 1
    for i, line in enumerate(information, 1):
        lines.append(f"{line}")

    return "{}{}".format(get_preamble_phrase(prompt_element, add_section_headers), "\n".join(lines))

def find_path(p, parent_path = ''):
    """
    Resolve path relative to parent_path if it's a relative path,
    otherwise return the absolute path as-is.
    """
    if parent_path == '':
        parent_path = os.path.dirname(p)
    
    # If path is already absolute, return as-is
    if os.path.isabs(p):
        return p, parent_path
    
    # For relative paths, resolve them relative to parent_path
    resolved_path = os.path.normpath(os.path.join(parent_path, p))
    return resolved_path, parent_path

class PromptYaml:
    def __init__(self, yaml_path, parent_path = '', add_section_headers=True):
        # Resolve the YAML file path and set parent_path to its directory
        if not os.path.isabs(yaml_path) and parent_path:
            yaml_path = os.path.normpath(os.path.join(parent_path, yaml_path))
        
        self.add_section_headers = add_section_headers
        # Set parent_path to the directory containing the YAML file
        self.parent_path = os.path.dirname(os.path.abspath(yaml_path))

        # Read YAML data from file
        with open(yaml_path, "r") as file:
            yaml_data = file.read()
            self.parsed_data = yaml.safe_load(yaml_data)
        # context lines
        self.parents : List[PromptYaml] = PromptYaml.find_dependencies(self.parsed_data, self.parent_path, self.add_section_headers)


    def find_index(self, keyword):
        for idx, element in enumerate(self.parsed_data['prompt']):
            if keyword in element:
                return idx

    def get_base_sentences(self, prompt_element):
        if 'prompt' in self.parsed_data and prompt_element in self.parsed_data['prompt']:
            prompt_data = self.parsed_data['prompt'][prompt_element]
            return prompt_data.get('base', [])
        else:
            return []

    def get_query(self):
        if 'prompt' in self.parsed_data and 'query' in self.parsed_data['prompt']:
            return self.parsed_data['prompt']['query']
        return ''



    def get_sentence(self, prompt_element, lines):
        return _create_answer_line(prompt_element, lines, self.add_section_headers)



    def get_base_rules(self, prompt_element):
        lines = self.get_base_sentences(prompt_element)
        return lines
        index = self.find_index(keyword)
        for l in lines:
            input_string = parse_input_string(l)
            if input_string:
                if is_url(input_string):
                    url_content = get_text_from_url(input_string)
                    print(url_content)


    def get_local_rules(self, prompt_element) -> List[PromptSection]:
        prompt_sections : List[PromptSection] = []
        if 'prompt' in self.parsed_data and prompt_element in self.parsed_data['prompt']:
            prompt_data = self.parsed_data['prompt'][prompt_element]
            rules = prompt_data.get('local', {})
            for name, rule in rules.items():
                lines = []
                preamble = rule.get('preamble', None)
                # Apply filters
                recursive = rule['recursive'] if 'recursive' in rule else False
                extension = rule['extension'] if 'extension' in rule else '*'
                filter = rule['filter'] if 'filter' in rule else None
                
                # Get provider options (e.g., pages for PDF/DOCX)
                options = rule.get('options', {}) if 'options' in rule else None

                source = rule['source']
                source, parent_path = find_path(source, self.parent_path)
                file_content = local_parser.parse(source, recursive, extension, filter, options)
                
                # Ensure file_content is not None
                if file_content is not None:
                    lines.append(file_content)
                else:
                    lines.append(f"Error: Could not read file {source}")
                    
                prompt_sections.append({
                    'preamble': preamble,
                    'lines': lines
                })
        return prompt_sections

    def get_rag_rules(self, prompt_element) -> List[PromptSection]:
        """Get RAG (Retrieval-Augmented Generation) rules"""
        prompt_sections: List[PromptSection] = []
        if 'prompt' in self.parsed_data and prompt_element in self.parsed_data['prompt']:
            prompt_data = self.parsed_data['prompt'][prompt_element]
            rules = prompt_data.get('rag', {})
            for name, rule in rules.items():
                lines = []
                preamble = rule.get('preamble', None)
                
                # RAG specific options
                faiss_file = rule.get('faiss_file', '')
                query = rule.get('query', '')
                source_folder = rule.get('source_folder', '')
                top_k = rule.get('top_k', 5)
                chunk_size = rule.get('chunk_size', 512)
                overlap = rule.get('overlap', 50)
                filter_regex = rule.get('filter', None)
                
                if not faiss_file:
                    lines.append(f"Error: No FAISS file specified for RAG rule '{name}'")
                elif not query:
                    lines.append(f"Error: No query specified for RAG rule '{name}'")
                else:
                    # Build options dictionary
                    rag_options = {
                        'query': query,
                        'source_folder': source_folder,
                        'top_k': top_k,
                        'chunk_size': chunk_size,
                        'overlap': overlap
                    }
                    if filter_regex:
                        rag_options['filter'] = filter_regex
                    
                    # Resolve faiss_file path relative to YAML file
                    faiss_file, _ = find_path(faiss_file, self.parent_path)
                    
                    # Process RAG request
                    rag_content = local_parser.parse_rag(faiss_file, rag_options)
                    lines.append(rag_content)
                
                prompt_sections.append({
                    'preamble': preamble,
                    'lines': lines
                })
        return prompt_sections

    def _find_elements_by_xpath(self, soup, xpath):
        """
        Convert basic XPath expressions to BeautifulSoup operations.
        This is an enhanced conversion that handles more XPath patterns.
        """
        elements = []
        
        try:
            # Handle some common XPath patterns
            if xpath.startswith('//'):
                # Remove leading //
                xpath_remainder = xpath[2:]
                
                # Handle attribute extraction: //tag[@attr='value']/@attr_name
                if '/@' in xpath_remainder:
                    xpath_part, attr_name = xpath_remainder.rsplit('/@', 1)
                    # Find elements first, then extract attribute
                    temp_elements = self._parse_xpath_selector(soup, xpath_part)
                    elements = []
                    for elem in temp_elements:
                        if hasattr(elem, 'get') and elem.get(attr_name):
                            elements.append(elem.get(attr_name))
                    return elements
                
                # Handle text content selection: //tag/text()
                elif xpath_remainder.endswith('/text()'):
                    xpath_part = xpath_remainder[:-7]  # Remove /text()
                    temp_elements = self._parse_xpath_selector(soup, xpath_part)
                    elements = [elem.get_text() for elem in temp_elements if hasattr(elem, 'get_text')]
                    return elements
                
                # Regular element selection
                else:
                    elements = self._parse_xpath_selector(soup, xpath_remainder)
            else:
                # Relative XPath or other patterns
                elements = self._parse_xpath_selector(soup, xpath)
                    
        except Exception as e:
            print(f"Warning: Could not parse XPath '{xpath}': {e}")
            # Fallback: return empty list
            elements = []
            
        return elements

    def _parse_xpath_selector(self, soup, xpath_part):
        """Parse XPath selector part and return matching elements"""
        elements = []
        
        # Simple tag selection: tag
        if '/' not in xpath_part and '[' not in xpath_part:
            elements = soup.find_all(xpath_part)
        
        # Contains function: tag[contains(@attr, 'value')]
        elif 'contains(' in xpath_part:
            # Extract tag and contains condition
            if '[contains(' in xpath_part:
                tag = xpath_part.split('[contains(')[0]
                contains_part = xpath_part.split('[contains(')[1].rstrip(')]')
                
                # Parse contains(@attr, 'value')
                if contains_part.startswith('@') and ', ' in contains_part:
                    attr_part, value_part = contains_part.split(', ', 1)
                    attr_name = attr_part[1:]  # Remove @
                    search_value = value_part.strip("'\"")  # Remove quotes
                    
                    # Find all elements of this tag that have the attribute containing the value
                    all_elements = soup.find_all(tag)
                    for elem in all_elements:
                        attr_value = elem.get(attr_name, '')
                        if search_value in attr_value:
                            elements.append(elem)
        
        # Class selection: tag[@class='classname'] 
        elif "[@class='" in xpath_part and xpath_part.endswith("']"):
            tag = xpath_part.split('[@class=')[0]
            class_name = xpath_part.split("[@class='")[1].split("']")[0]
            elements = soup.find_all(tag, class_=class_name)
        
        # ID selection: tag[@id='idname']
        elif "[@id='" in xpath_part and xpath_part.endswith("']"):
            tag = xpath_part.split('[@id=')[0]
            id_name = xpath_part.split("[@id='")[1].split("']")[0]
            elements = soup.find_all(tag, id=id_name)
        
        # General attribute selection: tag[@attr='value']
        elif "[@" in xpath_part and "='" in xpath_part and xpath_part.endswith("']"):
            tag = xpath_part.split('[@')[0]
            attr_part = xpath_part.split('[@')[1][:-2]  # Remove ']
            attr_name, attr_value = attr_part.split("='", 1)
            attr_value = attr_value.rstrip("'")
            
            # Use a lambda function to match the exact attribute value
            elements = soup.find_all(tag, attrs={attr_name: attr_value})
        
        else:
            # For other complex patterns, try to find by tag name only
            tag = xpath_part.split('/')[0].split('[')[0]
            if tag:
                elements = soup.find_all(tag)
                print(f"Warning: Complex XPath pattern '{xpath_part}' simplified to tag '{tag}'. Full XPath support is limited.")
        
        return elements

    def get_web_rules(self, prompt_element) -> List[PromptSection]:
        prompt_sections : List[PromptSection] = []
        if 'prompt' in self.parsed_data and prompt_element in self.parsed_data['prompt']:
            prompt_data = self.parsed_data['prompt'][prompt_element]
            rules = prompt_data.get('web', {})
            for name, rule in rules.items():
                preamble = rule['preamble'] if 'preamble' in rule else ''
                lines = []
                xpath = rule['xpath'] if 'xpath' in rule else ''
                source = rule['source']
                html_content = get_text_from_url(source)
                soup = BeautifulSoup(html_content, 'html.parser')
                # if preamble != '':
                #     lines.insert(0, preamble)

                if xpath != '':
                    # Convert basic XPath expressions to BeautifulSoup navigation
                    # Note: This is a simplified XPath to CSS conversion for common cases
                    elements = self._find_elements_by_xpath(soup, xpath)
                    for element in elements:
                        if hasattr(element, 'get_text'):
                            # If it's a BeautifulSoup element, get its HTML string
                            lines.append(str(element))
                        else:
                            # If it's just text content
                            lines.append(str(element))
                else:
                    lines.append(html_content)
                # Generate prompt section
                prompt_sections.append({
                    'preamble': preamble,
                    'lines': lines
                })
        return prompt_sections

    def get_context_base_rules(self):
        return self.get_base_rules('context')

    def get_context_local_rules(self):
        return self.get_local_rules('context')

    def get_context_web_rules(self):
        return self.get_web_rules('context')

    def get_context_rag_rules(self):
        return self.get_rag_rules('context')

    def get_output_base_rules(self):
        return self.get_base_rules('output')

    def get_output_local_rules(self):
        return self.get_local_rules('output')

    def get_output_web_rules(self):
        return self.get_web_rules('output')

    def get_output_rag_rules(self):
        return self.get_rag_rules('output')

    def get_instruction_base_rules(self):
        return self.get_base_rules('instruction')

    def get_instruction_local_rules(self):
        return self.get_local_rules('instruction')

    def get_instruction_web_rules(self):
        return self.get_web_rules('instruction')

    def get_instruction_rag_rules(self):
        return self.get_rag_rules('instruction')


    def find_dependencies(yaml_data, parent_path, add_section_headers=True):
        other_prompts = []
        prompt = yaml_data['prompt']
        if 'extends' in prompt:
            others_yaml = prompt['extends']
            for o in others_yaml:
                other_prompts.append(PromptYaml(o, parent_path, add_section_headers))

        return other_prompts





    def get_prompt_sentence(self):
        # Get instruction rules
        base_instruction = self.get_instruction_base_rules()
        local_instruction = PromptSections()
        local_instruction.add_sections(self.get_instruction_local_rules())
        web_instruction = PromptSections()
        web_instruction.add_sections(self.get_instruction_web_rules())
        rag_instruction = PromptSections()
        rag_instruction.add_sections(self.get_instruction_rag_rules())

        # Get context rules
        base_context = self.get_context_base_rules()
        local_context = PromptSections()
        local_context.add_sections(self.get_context_local_rules())
        web_context = PromptSections()
        web_context.add_sections(self.get_context_web_rules())
        rag_context = PromptSections()
        rag_context.add_sections(self.get_context_rag_rules())

        # Get output rules
        base_output = self.get_output_base_rules()
        local_output = PromptSections()
        local_output.add_sections(self.get_output_local_rules())
        web_output = PromptSections()
        web_output.add_sections(self.get_output_web_rules())
        rag_output = PromptSections()
        rag_output.add_sections(self.get_output_rag_rules())
        
        query = self.get_query()

        # Process parent dependencies
        for p in self.parents:
            base_instruction += p.get_instruction_base_rules()
            local_instruction.add_sections(p.get_instruction_local_rules())
            web_instruction.add_sections(p.get_instruction_web_rules())
            rag_instruction.add_sections(p.get_instruction_rag_rules())

            base_context += p.get_context_base_rules()
            local_context.add_sections(p.get_context_local_rules())
            web_context.add_sections(p.get_context_web_rules())
            rag_context.add_sections(p.get_context_rag_rules())

            base_output += p.get_output_base_rules()
            local_output.add_sections(p.get_output_local_rules())
            web_output.add_sections(p.get_output_web_rules())
            rag_output.add_sections(p.get_output_rag_rules())

        # Process instruction data
        def dedup_preserve_order(seq):
            seen = set()
            return [x for x in seq if not (x in seen or seen.add(x))]

        base_instruction = dedup_preserve_order(base_instruction) if isinstance(base_instruction, list) else [base_instruction] if base_instruction else []
        local_instruction = local_instruction.get_lines()
        web_instruction = web_instruction.get_lines()
        rag_instruction = rag_instruction.get_lines()

        # Process context data
        base_context = list(set(base_context)) if isinstance(base_context, list) else [base_context] if base_context else []
        local_context = local_context.get_lines()
        web_context = web_context.get_lines()
        rag_context = rag_context.get_lines()
        
        # Process output data
        base_output = list(set(base_output)) if isinstance(base_output, list) else [base_output] if base_output else []
        local_output = local_output.get_lines()
        web_output = web_output.get_lines()
        rag_output = rag_output.get_lines()

        # Combine all sections
        all_instruction = base_instruction + local_instruction + web_instruction + rag_instruction
        all_context = base_context + local_context + web_context + rag_context
        all_output = base_output + local_output + web_output + rag_output

        # Build final prompt
        prompt_parts = []
        if all_instruction:
            prompt_parts.append(self.get_sentence('instruction', all_instruction))
        if all_context:
            prompt_parts.append(self.get_sentence('context', all_context))
        if all_output:
            prompt_parts.append(self.get_sentence('output', all_output))
        if query:
            prompt_parts.append(query)
        return '\n'.join(prompt_parts)



    def print(self):
        print(self.get_prompt_sentence())




# @app.command()
# def ask(yaml_path: str):
#     client = ChatClient()
#     py = PromptYaml(yaml_path)
#     py.print()

#     # response = client.ask(f"{py.get_context_rules()} {py.get_output_rules()}")
#     while True:
#         print("> ", end="")
#         question = input()
#         if question.lower() == "exit" or question.lower() == "e" or question.lower() == "quit" or question.lower() == "q":
#             print("Exiting chat...")
#             break  # Exit the loop to end the conversation
#         response = client.ask(f"{py.get_prompt_sentence()}; ${question}")
#         print(response)

