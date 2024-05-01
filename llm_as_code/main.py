import typer
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots
import yaml



import g4f.debug
# g4f.debug.logging = True
# Utils
def _create_answer_line(prompt_element, information):
        return "{}: {}".format(prompt_element, "; ".join(information))



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


class PromptYaml:
    def find_index(self, keyword):
        for idx, element in enumerate(self.parsed_data['prompt']):
            if keyword in element: 
                return idx

    def get_context_rules(self):
        context_rules_keyword = 'context_rules'
        context_rules_index = self.find_index(context_rules_keyword)
        return _create_answer_line("Context", self.parsed_data['prompt'][context_rules_index][context_rules_keyword])

    def get_output_rules(self):
        return _create_answer_line("Output rules", self.parsed_data['prompt'][1]['output_rules'])


    def __init__(self, yaml_path):
        # Read YAML data from file
        with open(yaml_path, "r") as file:
            yaml_data = file.read()
            self.parsed_data = yaml.safe_load(yaml_data)
        print(self.get_context_rules())
        print(self.get_output_rules())

        

@app.command()
def main(yaml_path: str):
    client = ChatClient()
    py = PromptYaml(yaml_path)

    # response = client.ask(f"{py.get_context_rules()} {py.get_output_rules()}")
    while True:
        print("> ", end="")
        question = input()
        if question.lower() == "exit":
            print("Exiting chat...")
            break  # Exit the loop to end the conversation
        response = client.ask(f"{py.get_context_rules()} {py.get_output_rules()}; ${question}")
        print(response)






# @app.command()
# def goodbye(name: str, formal: bool = False):
#     if formal:
#         print(f"Goodbye Ms. {name}. Have a good day.")
#     else:
#         print(f"Bye {name}!")

