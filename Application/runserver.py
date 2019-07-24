"""
This script runs the webapp application using a development server.
"""

from os import environ
from python_webapp_flask import flask_app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    flask_app.run(HOST, PORT)
