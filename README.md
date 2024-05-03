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
Clone the repository and run `pip install .`. 
Now you can use with `peac <ask|prompt>`. 

Just run `pip install peac`. 
To run in development mode: 
- Clone this repo
- Run `poetry install` 
- Use the cli through `poetry run peac`. 

<p align="right">(<a href="#top">back to top</a>)</p>




## How to use
`peac` has two basic commands: 
- `prompt` : Generates a prompt from a yaml file and print it. You can copy this prompt and paste on your favourite LLM. 
- `ask` : Generate the prompt from yaml and use [g4f](https://github.com/xtekky/gpt4free) to ask questions that you can integrate in your works. 

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

