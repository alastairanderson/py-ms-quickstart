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

## Configuration

### config.json and ConfigurationService

The config/config.json file is accessed in code using the ConfigService which is
instantiated in the server.py and passed through to other services that require it.

Each config variable has a variable in the initialiser (__init__) and is read into
the application using __read_config().

Config values can be updated using the update_config() method, which takes the name
of the config value

Note: If you have any passwords or access keys, these should be stored as environment
variables and accessed using `os.environ`, examples are provided in __read_config().
Plan is to connect to a secrets vault in the future.

### logging.yml and LogService

The Services/core/LogService makes use of Python's
[in-built logging capabilities](https://docs.python.org/3/library/logging.html) to
write log messages and their metadata in a JSON format to a txt file.

The path to the txt file is configured in config/config.json (see previous section).

Each class that requires logging passes in the instance of LogService that is created
in server.py and calls get_logger() to retrieve a logger object, which you then call
.info(), .warning() or .error() to log any messages.

The send_bulk() method was designed with sending a bulk payload of log messages
over HTTP. send_bulk() locks the log text file, and sends the contents of it to the
configured third party service, such as Loggly.

Note: send_bulk() has been commented out by default, as this project has been
primarily used in a development setting so far, with no need for the extra overhead
of Loggly.

The 'dev' and 'prod' build versions of logging is determined by what is set in
config/config.json

The config/logging.yml file is the configuration file used by Python's in-built
logging system, and determines where the logs are written to.

### Configuring NoficationService

Two types of notifications are supported: email and Slack

Both are configured through a mixture of config/config.json values and for sensitive
data, these are set in environment variables, which can be seen by looking for the
'# notifications' section in the ConfigService file.

Plan is to write some scripts to connect to a secrets vault in the future.

### Configuring HttpService

HttpService was designed for retrieving web pages with web scraping in mind.
It directs HTTP requests through a TOR proxy running in a docker container, which
rotates the IP address every 25 requests and selects a random user agent string for
each request from a list.

The user agent strings file is excluded from this repo, but can be searched online.

The location of the user agent strings file is set in the self._user_agent_strings_file
variable.

Currently, this service only works with a TOR docker container, and the ID is required to
be set in config.tor_container_id - this can be the running CONTAINER ID or the NAME.

## TODO

- Use the Alpine distro in the Dockerfile to minimise the docker image size

- Create development and production builds (separate requirement.txt files)

- Template out tests using a common python testing framework

- Build out Makefile - (or remove?)

- For production builds, look at using nginx https://ianlondon.github.io/blog/deploy-flask-docker-nginx/

- Integrate with IdServ

  - https://app.pluralsight.com/player?course=python-flask-rest-api&author=sanjay-rai&name=4741808f-d7ef-4c80-8430-719f70718013&clip=0&mode=live

  - http://docs.identityserver.io/en/latest/topics/apis.html

- Connect to secret vault (Istio, Azure Secrets, etc.) to get any passwords/keys in the ConfigService

- Write a scraper to update the browser connection strings that are used.

- HttpService - make request more resilient - if TOR docker container is not available fall back to normal request with a warning. Or even add a check on startup.

- Separate requirements.txt file for production needed.
