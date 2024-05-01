# peac



## How to use
`peac` has two basic commands: 
- `prompt` : Generates a prompt from a yaml file and print it. You can copy this prompt and paste on your favourite LLM. 
- `ask` : Generate the prompt from yaml and use [g4f](https://github.com/xtekky/gpt4free) to ask questions that you can integrate in your works.


## Available environment variables
Some environment variables allows to preprocess the external input variables.
- `LLM_AS_CODE_ONLY_TEXT` : when markdown or HTML pages are converted in plain-text. Default to false

