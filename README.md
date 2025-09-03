# PEaC
PEaC is an approach for realizing the ``Prompt Engineering as Code''. It is inspired by the awesome ideas of realizing an infrastructure through code, i.e. Infrastructure as Code (IaC). 
This project is basically a command-line that implements the PEaC approach. It allows you to write yaml files, parse them, and generate prompt context and output. 

The generated text can be used as preamble for your prompts.

## Rationale
PEaC is an approach to realize modular, repeatible, portable prompts. You can write prompts in yaml format, and you can share these prompts with other people. It is an approach to organize in a structured form your prompts, by following conventions defined in several works. A prompt is composed of ([Giray (2023)](https://link.springer.com/article/10.1007/s10439-023-03272-4)):
- **Instruction** A specific task or instruction that guides the model’s behavior and directs it toward the desired output.
- **Context** External information or additional context that provides background knowledge to the model, helping it generate more accurate and relevant responses. 
- **Output**  Specifies the type or format of the desired output. It helps shape the response by defining whether we need a short answer, a paragraph, or any other specific format.
- **Input** data The input or question that we want the model to process and provide a response for. It forms the core of the prompt and drives the model’s understanding of the task.


Through PEaC you can write a yaml structure that contains information from the `context` and `output` section.

<p align="right">(<a href="#top">back to top</a>)</p>



## Installation
You need python 3.11 to run PEaC.


Clone the repository and run `pip(x) install .`. 
Now you can use with `peac <ask|prompt>`. 

### Note for the GUI
For macOS users, you need to install the following packages:

```bash
```

### Development mode
To run in development mode: 
- Fork and clone the repo
- Run `poetry install` 
- Use the cli through `poetry run peac`. 
- Send me a pull request ;-)

<p align="right">(<a href="#top">back to top</a>)</p>




## How to use
`peac` has two basic commands: 
- `prompt` : Generates a prompt from a yaml file and print it. You can copy this prompt and paste on your favourite LLM. 
- `ask` : Generate the prompt from yaml and use [g4f](https://github.com/xtekky/gpt4free) to ask questions that you can integrate in your works. > **Warning**: This command depends on the g4f stability, it could have errors. 

By using the following command:
```
peac prompt <YAML> 
```

A prompt is generated, and you can copy it in you LLM agent.
Refer to the `demo-healthcare` example for comprehensive examples.

## YAML syntax 
The base template is provided in `template.yaml` file:
```
prompt:
  extends: 
    - ...
  context:
    local: 
      localname:
        preamble: follow these guidelines
        source: filename
      
  output:
    base:
      - base A
      - base B



```

Copy this to start realizing your files.
There are four keys: 
* extends: allow to import other YAML files.  
* context: realize the `context` section 
* output: realize the `output` section (ex. formatting, colors, styles, etc.)

When extending other YAML files, the sections inside the file are imported in the base file.
Duplicated are removed (if, for example, you import the same files, the sections will not be duplicated in the final prompt).
For each key, there are several subkeys.

#### base
The most simple way to concatenate strings. 
It is a list of strings that will be concatenated in the final prompt.


#### local 
Allow to import local files.
```
local:
    <section-name>:
        (preamble): a string that is prepended to the output. Default=''
        source: the filename path (or folder). If is a directory, it imports all the files inside.
        (recursive): perform a recursive search (if the folder is used). Default=False
        (filter): apply a regex to the text in order to extract only relevant pieces. Default=None

```

Example:
```
prompt:
  context:
    local:
      example:
         preamble: extract from folder
         recursive: true
         filter: \b(public|private)\b
         extension: java
         source: tests/test-folder
```

- perform a recursive search
- filter public and private methods 
- filter extension `java` files 
- starts from `tests/test-folder` the search


#### web 
Import a file from remote.
```
    web:
        <section-name>:
            preamble: a string that is prepended to the output
            source: the remote URL resource
```


<p align="right">(<a href="#top">back to top</a>)</p>



## Contributing

Contributions to this project are welcome! If you have suggestions for improvement, please fork the repository and submit a pull request. You can also open an issue with the tag "enhancement" to discuss potential changes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Cite this work 
To cite this work, use:
```
@INPROCEEDINGS{10852434,
  author={Perrone, Gaetano and Romano, Simon Pietro},
  booktitle={2024 2nd International Conference on Foundation and Large Language Models (FLLM)}, 
  title={Prompt Engineering as Code (PEaC): an approach for building modular, reusable, and portable prompts}, 
  year={2024},
  volume={},
  number={},
  pages={289-294},
  keywords={Computer languages;Codes;Large language models;Redundancy;Natural languages;Buildings;Syntactics;Programming;Prompt engineering;Prompt Engineering;Large Language Models;Infrastructure as Code;Data Serialization},
  doi={10.1109/FLLM63129.2024.10852434}}
```

