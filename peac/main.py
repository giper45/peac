import typer
import importlib.resources

## UTILS
def get_template_file():
    with importlib.resources.files('peac').joinpath('template.yaml').open('r') as f:
        template_content = f.read()
        return template_content


####

from peac.core.peac import PromptYaml
from peac.gui_ctk.main_app import PeacApp


app = typer.Typer()


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

@app.command()
def gui():
    app = PeacApp()
    app.mainloop()
