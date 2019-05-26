# python microservice quickstart

## Purpose

A quickstart set of python scripts to get up-and-running with development quickly and ability to deploy to a Docker container for production use.

## Features

- Project structure to get started writing a Python microservice running in Docker with.

## Roadmap

- Add samples/checklists for different purposes
  - Adding + using TensorFlow
  - Retrieving data with bs4
  - Feature engineering

## Pre-requisites

- Python for running code locally
- Docker and Make for container deployment
- (Optional) Visual Studio Code with EditorConfig for VS Code extension installed

## Setup environment

Run the following commands in a terminal window:

```python
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## TODO

-[] Use the Alpine distro in the Dockerfile to minimise the docker image size
-[] Create proper requirements-dev.txt file
-[] Create tests - use a common python testing framework
-[] Create a requirement-prod.txt file
-[] Get this running as a Flask service 
