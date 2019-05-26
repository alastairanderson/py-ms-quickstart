#coding: utf-8

import http

from flask import Flask, request


config_file_path = ".config/config.json"
config_service = ConfigService(config_file_path)

# Instantiate additional services here

app = Flask(__name__)

@app.route("/", methods=['POST'])
def root():
    # Call any required services
    return '', http.HTTPStatus.NO_CONTENT

app.run(port=config_service.hosting_port)
