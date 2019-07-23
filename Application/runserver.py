"""
This script runs the webapp application using a development server.
"""

from os import environ
from python_webapp_flask import app, server

if __name__ == '__main__':
    print('Running server')
    server.serve_forever()
