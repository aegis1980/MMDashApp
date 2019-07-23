import dash
import flask
import dash_bootstrap_components as dbc
from os import environ

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler


# styling:
# LUX is a bootswatch theme which is included in dash-bootstrap
# additional styling in assets/styling.css (which overides bootstrap theme) 

# this mean we create our our instance of flask, the underlying framework to Dash
#server = flask.Flask(__name__)

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.LUX])

app.config.suppress_callback_exceptions = True
app.enable_dev_tools(debug=True)

HOST = environ.get('SERVER_HOST', 'localhost')
try:
    PORT = int(environ.get('SERVER_PORT', '5000'))
except ValueError:
    PORT = 5000

server = pywsgi.WSGIServer((HOST, PORT), app.server, handler_class=WebSocketHandler)

import python_webapp_flask.index
