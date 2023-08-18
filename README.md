# deep-thought

[![Linting](https://github.com/HunterGerlach/deep-thought/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/HunterGerlach/deep-thought/actions/workflows/linting.yml)
[![Unit Tests](https://github.com/HunterGerlach/deep-thought/actions/workflows/unittest.yml/badge.svg?branch=main)](https://github.com/HunterGerlach/deep-thought/actions/workflows/unittest.yml)

## Setup instructions

Setup local Python environment

```bash
python3 -m venv .venv_deep-thought
source .venv_deep-thought/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
```

## Run the code

```bash
uvicorn src.app:app --reload
```

## Run the tests

```bash
python -m unittest discover
```

## API Details

Information about the API can be found in the [API documentation](API.md).
