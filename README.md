# Rule Enginee
Fastapi backend for new rule creation Using LLM, and score evaluation 



### Install dpendency
0. Kindly make sure python 3.11 higher is installed , and install poetry  `pip install poetry`
1. Clone the repo `git clone https://github.com/vyturr/rule_enginee.git`
2. cd <to_repo_directory>
3. `poetry shell` 
4. `Poetry install`

### Run the application [for development]
1. Check the .settings file and update the `RE_APP__LOG_DIRECTORY` Variable to a valid Directory , reset the other variables if needed.
2. Then Run `python build_db.py` to create a sqlite database
3. To Run the Fastapi Back end run `python main.py` and browse to `http://settings.RE_APP__HOST:settings.RE_APP__PORT/docs` .

### Remove python bytecode __pycache__ other cached files  

`pyclean -d jupyter package ruff -v .`

### Linting 

`ruff check -v .`

### Fixing linting errors

`ruff check --fix -v .`

### Source code formatting

`ruff format -v .`

### Other Scripts
`json_schema_builder.py` - Build and validate Json Schema [Should have data directory] 

`llmagent.py` - Simple test code for checking LLM is working with given model name and key