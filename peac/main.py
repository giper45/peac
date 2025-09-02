import os
import re
from typing import List
from xml.etree import ElementTree
import requests
from bs4 import BeautifulSoup
from lxml import html

import g4f.debug
import markdown


import typer
from g4f.client import Client
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


####

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
            if 'preamble'in p and p['preamble'] != None:
                # Append the preamble to the first string in p['lines']
                p['lines'][0] = f"{p['preamble']} - {p['lines'][0]}"
            lines.extend(p['lines'])
        lines = [re.sub(r'\n+', '\n', l) for l in lines]
        return lines





g4f.debug.logging = True
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



app = typer.Typer()

class ChatClient:
    def __init__(self):
        # self.client = Client()
        self.messages = []
        self.client = Client(
            # provider=RetryProvider([Phind, FreeChatgpt, Liaobots], shuffle=False)
        )


    def ask(self, question):
        self.messages.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            # model="",
            model="gpt-3.5-turbo",
            # model="claude-3-opus",
            # provider="",
            messages=self.messages,
        )
        return response.choices[0].message.content




def get_preamble_phrase(prompt_element: str):
    return f"{prompt_element.capitalize()} - use these rules for all next questions:"

def _create_answer_line(prompt_element, information):
    lines = []
    index = 1
    for i, line in enumerate(information, 1):
        lines.append(f"({i}) {line}")

    return "{} {}".format(get_preamble_phrase(prompt_element), "; ".join(lines))

def find_path(p, parent_path = ''):
    if parent_path == '':
        parent_path = os.path.dirname(p)
    if not os.path.exists(p):
        p = os.path.join(parent_path, os.path.basename(p))
    return p, parent_path

class PromptYaml:
    def __init__(self, yaml_path, parent_path = ''):
        # If not exist try to find in the folder folder of the first path
        yaml_path, parent_path= find_path(yaml_path, parent_path)
        self.parent_path = parent_path


        # Read YAML data from file
        with open(yaml_path, "r") as file:
            yaml_data = file.read()
            self.parsed_data = yaml.safe_load(yaml_data)
        # context lines
        self.parents : List[PromptYaml] = PromptYaml.find_dependencies(self.parsed_data, parent_path)


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
        return _create_answer_line(prompt_element, lines)



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
                preamble = rule['preamble'] if 'preamble' in rule else ''
                # Apply filters
                recursive = rule['recursive'] if 'recursive' in rule else False
                extension = rule['extension'] if 'extension' in rule else '*'
                filter = rule['filter'] if 'filter' in rule else None

                source = rule['source']
                source, parent_path = find_path(source, self.parent_path)
                file_content = local_parser.parse(source, recursive, extension, filter)
                lines.append(file_content)
                prompt_sections.append({
                    'preamble': preamble, 
                    'lines': lines
                })
        return prompt_sections

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
                tree = html.fromstring(html_content)
                # if preamble != '':
                #     lines.insert(0, preamble)


                if xpath != '':
                #     soup = BeautifulSoup(html_content, 'html.parser')
                #     print("XPATH")
                    code_elements = tree.xpath(xpath)
                    for c in code_elements: 
                        if isinstance(c, html.HtmlElement):
                            lines.append(ElementTree.tostring(c, 'utf-8').decode('utf-8'))
                        else:
                            lines.append(c)
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

    def get_output_base_rules(self):
        return self.get_base_rules('output')

    def get_output_local_rules(self):
        return self.get_local_rules('output')

    def get_output_web_rules(self):
        return self.get_web_rules('output')


    def find_dependencies(yaml_data, parent_path):
        other_prompts = []
        prompt = yaml_data['prompt']
        if 'extends' in prompt: 
            others_yaml = prompt['extends']
            for o in others_yaml:
                other_prompts.append(PromptYaml(o, parent_path))

        return other_prompts





    def get_prompt_sentence(self):
        base_context = self.get_context_base_rules()
        local_context = PromptSections()
        local_context.add_sections(self.get_context_local_rules())
        # local_context = self.get_context_local_rules()
        web_context = PromptSections()
        web_context.add_sections(self.get_context_web_rules())
        # web_context = self.get_context_web_rules()


        base_output = self.get_output_base_rules()
        local_output = PromptSections()
        local_output.add_sections(self.get_output_local_rules())
        web_output = PromptSections()
        web_output.add_sections(self.get_output_web_rules())
        # web_output = self.get_output_web_rules()
        query = self.get_query()

        for p in self.parents:
            base_context += p.get_context_base_rules()
            local_context.add_sections(p.get_context_local_rules())
            web_context.add_sections(p.get_context_web_rules())
            # web_context.add_section(p.get_context_web_rules())
            # web_context += 
            # p.get_context_web_rules()


            base_output += p.get_output_base_rules()
            local_output.add_sections(p.get_output_local_rules())
            web_output.add_sections(p.get_output_web_rules())
            # web_output += p.get_output_web_rules()
            # web_output.add_section(p.get_output_web_rules())


        base_context = list(set(base_context))
        local_context = local_context.get_lines()
        web_context = web_context.get_lines()
        base_output = list(set(base_output))
        local_output = local_output.get_lines()
        web_output = web_output.get_lines()






        return '\n'.join([self.get_sentence('context', base_context + local_context + web_context), self.get_sentence('output', base_output + local_output + web_output),
                        query])



    def print(self):
        print(self.get_prompt_sentence())


        

@app.command()
def ask(yaml_path: str):
    client = ChatClient()
    py = PromptYaml(yaml_path)
    py.print()

    # response = client.ask(f"{py.get_context_rules()} {py.get_output_rules()}")
    while True:
        print("> ", end="")
        question = input()
        if question.lower() == "exit" or question.lower() == "e" or question.lower() == "quit" or question.lower() == "q":
            print("Exiting chat...")
            break  # Exit the loop to end the conversation
        response = client.ask(f"{py.get_prompt_sentence()}; ${question}")
        print(response)




@app.command()
def prompt(yaml_path: str):
    py = PromptYaml(yaml_path)
    py.print()


@app.command()
def init(name: str):
    template_content = get_template_file()
    new_file_name = f"{name}.yaml"
    with open(new_file_name, 'w') as new_file:
        new_file.write(template_content)

    typer.echo(f"File '{new_file_name}' has been created based on the template.")
