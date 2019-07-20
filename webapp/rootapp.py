
# -*- coding: utf-8 -*-
import dash
import flask
import dash_bootstrap_components as dbc


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
server = pywsgi.WSGIServer(('', 5000), app.server, handler_class=WebSocketHandler)

