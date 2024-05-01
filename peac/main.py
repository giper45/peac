import os
import re
import requests
from bs4 import BeautifulSoup
import markdown


import typer
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots
import yaml
import validators



import g4f.debug
# g4f.debug.logging = True
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

def get_text_from_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
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
        return "{} {}".format(get_preamble_phrase(prompt_element), "; ".join(information))

class PromptYaml:
    def find_index(self, keyword):
        for idx, element in enumerate(self.parsed_data['prompt']):
            if keyword in element: 
                return idx

    def get_base_sentences(self, prompt_element):
        return self.parsed_data['prompt'][prompt_element]['base']

    def get_local_rules(self, prompt_element):
        rules = self.parsed_data['prompt'][prompt_element]['local']
        lines = []
        for name, rule in rules.items():
            preamble = rule['preamble'] if 'preamble' in rule else ''
            source = rule['source']
            with open(source) as f:
                file_content = "\n".join(f.readlines())
            lines.append("{}{}{}".format(preamble, ":" if preamble else "", file_content))
        return lines



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

        

    def get_context_base_rules(self):
        return self.get_base_rules('context')

    def get_context_local_rules(self):
        return self.get_local_rules('context')

    def get_output_base_rules(self):
        return self.get_base_rules('output')

    def get_output_local_rules(self):
        return self.get_local_rules('output')



    def get_prompt_sentence(self):
        base_context = self.get_context_base_rules()
        local_context = self.get_context_local_rules()
        base_output = self.get_output_base_rules()
        local_output = self.get_output_local_rules()
        return self.get_sentence('context', base_context + local_context) +  self.get_sentence('output', base_output + local_output)

    def __init__(self, yaml_path):
        # Read YAML data from file
        with open(yaml_path, "r") as file:
            yaml_data = file.read()
            self.parsed_data = yaml.safe_load(yaml_data)
        # context lines
        print(self.get_prompt_sentence())



        

@app.command()
def ask(yaml_path: str):
    client = ChatClient()
    py = PromptYaml(yaml_path)

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
    PromptYaml(yaml_path)

