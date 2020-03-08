# python microservice quickstart

## Purpose

A quickstart set of python scripts to get up-and-running with development quickly and ability to deploy to a Docker container for production use.

## Features

- Project structure to get started writing a Python microservice running in Docker with.
- Uses [pytest](https://docs.pytest.org/en/latest/) as the testing framework. Others are [available](https://pythontesting.net/start-here/).

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

- Use the Alpine distro in the Dockerfile to minimise the docker image size

- Create development and production builds (separate requirement.txt files)

- Template out tests using a common python testing framework

- Build out Makefile

- For production builds, look at using nginx https://ianlondon.github.io/blog/deploy-flask-docker-nginx/

- Integrate with IdServ 
  - https://app.pluralsight.com/player?course=python-flask-rest-api&author=sanjay-rai&name=4741808f-d7ef-4c80-8430-719f70718013&clip=0&mode=live

  - http://docs.identityserver.io/en/latest/topics/apis.html


