
# -*- coding: utf-8 -*-
import dash
import flask
import dash_bootstrap_components as dbc



# styling:
# LUX is a bootswatch theme which is included in dash-bootstrap
# additional styling in assets/styling.css (which overides bootstrap theme) 

# this mean we create our our instance of flask, the underlying framework to Dash
server = flask.Flask(__name__)

#and pass that to the dash instance
app = dash.Dash(
    __name__, 
    server = server,
    external_stylesheets=[dbc.themes.LUX])

app.config.suppress_callback_exceptions = True