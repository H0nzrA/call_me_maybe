*This project has been created as part of the 42 curriculum by trakotoz.*


# Call-Me-Maybe: And I will call you back!
An introduction to the world of Large Language Models and structured text generation.


## Description:
A **Large Language Model (LLM)** is an artificial intelligence model trained on a vast amount of text
to perform **Natural Language Processing (NLP)** tasks such as text generation, summarization, translation,
and question answering.

While LLMs excel at understanding and generating human language, they often need to interact with external
applications to perform real-world tasks. This is where **Function Calling** comes in.


### Function Calling:
Function Calling allows an LLM to select a predefined function and generate the arguments required to execute it.
Rather than responding only with natural language, the model produces a structured representation describing
**which function should be called** and **which parameters should be passed**.

This mechanism enables LLMs to interact with external tools such as databased, APIs, search engines, calculators,
or any user-defined application.

However, allowing an LLM to freely generate structured data presents a major challenge. The model may produce
malformed JSON object, invalid parameter values, unknown function names, or outputs that do not follow the
expected schema.

### Goal of this project:
The goal of this project is very straight forward: address this problem by implementing a **constrained decoding**
algorithm.

Instead of allowing every possible token to be generated, the decoder dynamically restricts the set of valid tokens
according to the expected output format. As a result, the model is guided toward producing reliable and well-structured
function calls while preventing invalid output during generation.


# Instructions:

### Requirements:
Before running the project, make sure the following dependencies are installed:

- Python 3.10 or later
- `make`
- Internet connection (to download the selected LLM on first execution)
- (Optional) `uv` for better management (recommanded)

### Installation:

#### Manual execution:
Using `uv` is the recommanded way to install and run the project.

```bash
uv sync                 # Install and synchronize the project dependencies
uv run python -m src    # Run the Application
```

> Supported Flags:
- `-i`/ `--input`: Function-calling input file.
- `-d`/ `--functions_definition`: Function definitions file.
- `-o`/ `--output`: Output file.


#### Makefile:
A `Makefile` is provided at the root of the repository to simplity common tasks.

```bash
make install    # Installing all dependencies
make run        # Run the application
make help       # Display avaliable commands.
```

> `Note`: Additional command-line arguments can be passed through the `ARGS` Makefile variable.


#### Project Cache:
Running LLMs requires a significant amount of disk space for the virtual environment, model files, and cache directories.

The provided `Makefile` automatically configures these directories inside the project root. Their locations can be customized
using the `CACHE`, `HF`, and `VENV` Makefile variables.

If you prefer to run the project manually, the same behavior can be achieved by setting the corresponding environment variables.


```bash
# UV
export UV_PROJECT_ENVIRONMENT=<venv_directory>
export UV_CACHE_DIR=<cache_directory>

# Hugging Face
export HF_HOME=<huggingface_directory>
```

## Example usage:
```bash
export UV_CACHE_DIR=./.cache
uv run python -m src -i ./data/input/function_calling_tests.json -d ./data/input/functions_definition.json

# or
make run ARGS="--input ./data/input/function_calling_tests.json --functions_definition ./data/input/functions_definition.json"
```

![Running Example](./assets/runtime_example.gif)


## Algorithm explanation:

### Constrained Decoding:
Constrained decoding is an inference-time technique for large language models that guarantees output compilance by using token masking,
finite-state machines and context-free grammars.

In the context of function calling, unrestricted generation may produce invalid JSON objects, incorrect function names, missing parameters,
or values that do not satisfy the expected data types. Constrained decoding addressed these issues by allowing only valid tokens to be
generated at each decoding step.

### Overview of the algorithm:

> Simple pipeline:
```
User Prompt -> Prompt Engineering -> Function Selection -> Parameter Extraction -> FSM Validation -> Structured JSON
```

The project applies two independent constrained-decoding passes: one to select which function best matches the prompt, and one to fill in that
function's arguments.

#### Function Selection:
The model is prompted with the list of available functions and asked to produce the name of the best match, one token at a time.
At each step, the set of legal next tokens is computed by taking every canditate function name, keeping only the ones whose token sequence still matches everything
generated so far, and offering the *next* token of each surviving candidate as the only valid choices. Every other token is masked to `-inf`.
Generation stops the moment the accumulated tokens exactly match one full candidate name.

This guarantees the selected function is always one of the functions actually provided in the function definitions list


#### Parameter extraction:
Rather than generating an entire JSON object freely, the decoder constructs it incrementally from a predefined skeleton.

For each parameter:

1. write the parameter name;
2. determine its expected type;
3. generate only the parameter value;
4. repeat until every parameter has been generated.

The value generation process depends on the parameter type.

- Strings are constrained by a JSON string grammar.
- Numbers are constrained by a numeric grammar.
- Booleans are constrained to either `true` or `false`.

For every generated token, the current Finite State Machine determines which vocabulary tokens remain syntactically valid.
Tokens that would violate the grammar are removed before the next token is selected.


## Design Decisions:
Several important design decisions were made during development.

### Separation of Responsibilities:
Each module has a singe responsibility.

```bash
src
├── cli
│   ├── args.py
│   ├── display.py
│   └── __init__.py
├── constrained
│   ├── answer.py
│   ├── constrained.py
│   ├── __init__.py
│   ├── prompt.py
│   └── type_eval.py
├── fsm
│   ├── base.py
│   ├── filter.py
│   ├── __init__.py
│   ├── literals.py
│   └── numbers.py
├── __init__.py
├── llm
│   ├── calling_function.py
│   ├── __init__.py
│   ├── tokenizer.py
│   └── vocab.py
├── __main__.py
└── utils
    ├── file_management.py
    ├── __init__.py
    ├── models.py
    ├── others.py
    ├── parsing.py
    └── syntax.py
```

- `llm`: handles model interation.
- `fsm`: validates generated text.
- `constrained`: implements decoding.
- `cli`: manage user interation.
- `utils`: contains shared functionality.

This separation keeps the implementation modular and easy to maintain.

### Pydantic Models:
Every structured object is represented using Pydantic models.
This provides:

- automatic validation,
- runtime type checking,
- cleaner interfaces,
- improved maintainability.

### Finite State Machines:
Finite state machines were chosen instead of regular-expression post-processing.

Validation therfore happens **during generation**, preventing invalid outputs instead of correcting them afterwards.


## Performance analysis:

### Accuracy:
The constrained decoder significantly reduces hallucinations because only valid tokens are available during generation.

Function selection achieved high accurracy across the provided evaluation dataset.

Parameter extraction also performs reliably for primitive data types.

### Speed:
Vocabulary filtering introduces additional computation compared to uncostrained decoding.

However, caching grammar-valid tokens  greatly reduces repeated FSM evaluations and keeps decoding responsive.

### Reliability:
Because generation is grammar-constrained:

- malformed numbers cannot be produces,
- invalid booleans cannot appear,
- unterminated strings are rejected,
- unknown function names cannot be generated.


## Challenges faced:
Several technical challenges were encountered during development of this project.
Most of them required multiple iterations before reaching the final implementation.

### Understanding LLM Tokenization:
One of the first challenges was understanding how model LLM tokenizers actually work.

Rather than splitting text into words, the models used in this project rely on **Byte Pair Encoding (BPE)**.
This required implementing several components from scratch, including:

- byte-to-Unicode mapping,
- vocabulary loader,
- BPE merge algorithm,
- both the `encode()` and `decode()` procedures.

To validate the implementation, the custom tokenizer was continuously compared against the tokenizer provided by
the reference models until both produced identical token sequences.

### Designing the Constrained Decoder:
The constrained decoding algorithm went through several iterations before reaching its final architecture.

The first implementations attempted to  generate the complete function call using a single decoding process.
While functional, thes designs quickly becam difficult to maintain, expensive to execute, and increasingly
complex as additional constraints were introduced.

After experimenting with multiple approaches, the decoder was redesigned into two independent stages:

1. constrained function selection,
2. constrained parameter extraction.

Each parameter is generated independently according to irs expected type, greatly simplifying both the implementation
and future extensions.

### Grammar-Constrained Generation:
A major challenge was ensuring that every generated value remained sytactically valid.

Instead of validating the generated output afterward, the decoder validates every token **before it is produced** using
dedicated Finite State Machines.

### Token Validation:
One unexpected difficulty came from the tokenizer itself.

A single vocabulary token may contain several characters rather than just one. Consequently, validating only
the token boudary is insufficient.

To solve this problem, every character contained inside a candidate token is processed sequentially by the corresponding
Finite State Machine. A token is accepted only if every character produces a valid state transition.

### Performance Optimization:
The first versions of the decoder performed many redundant computations.

In particular, the set of valid vocabulary tokens was recomputed repeatedly for identical FSM states.

Introducing a cache keyed by the FSM type and current state eliminated these repeated computations and significantly reduced
the overall decoding time while preserving identical behavior.


## Testing strategy:

The project was validated through multiple levels of testing, from individual components to complete function-calling scenarios.

### Component Testing:

Each major components was tested independently:

- **Tokenizer**: verified BPE encoding/decoding, byte-to-Unicode mapping, and merge operations by comparing results with the
reference tokenizer.

- **Finite State Machine**: tested each grammar independently to ensure valid sequences were accepted and invalid transition were
rejected for strings, numbers, integers, and booleans.

### Constrained Decoding Testing:

The decoder was tested with function definitions of increasing complexity to verity:

- valid function selection,
- correct parameter extraction,
- type compliance,
- valid JSON generation.

### End-to-End Testing:

Complete function-calling examples were used to test the whole pipeline, including simple requests, complex prompts, mukltiple parameters,
and mixed data types.

Generated output were validated using JSON parsing and Pydantic models to ensure they matched the expected structure.


## Resources

### Documentation

* Python Documentation — https://docs.python.org/
* Pydantic Documentation — https://docs.pydantic.dev/
* Hugging Face Documentation — https://huggingface.co/docs
* JSON Specification — https://www.json.org/
* Python `regex` Documentation — https://pypi.org/project/regex/

### Articles

* *Language Models are Few-Shot Learners* (Brown et al.)
* *Attention Is All You Need* (Vaswani et al.)
* GPT-2 Byte Pair Encoding implementation by OpenAI.

### AI Usage

Artificial intelligence was used as a development assistant throughout the project.

It was primarily used for:

* discussing software architecture,
* reviewing algorithms,
* improving code readability,
* explaining Python concepts,
* debugging implementation issues,
* writing and improving documentation,
* proofreading comments and docstrings.

All implementation decisions, tokenizer logic, constrained decoding algorithm, finite state machines, and overall software design were
implemented and validated by the project author.

---

<div align="center">

### Call-Me-Maybe

Created by [trakotoz](mailto:trakotoz@student.42antananarivo.mg)

42 Antananarivo

<img src="./assets/42_tana_logo.png" width="120" />

</div>
