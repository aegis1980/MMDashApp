import dash
import flask
import dash_bootstrap_components as dbc
from os import environ
import os

ASSETS_PATH = os.path.join(os.getcwd(),'python_webapp_flask','assets')

# styling:
# LUX is a bootswatch theme which is included in dash-bootstrap
# additional styling in assets/styling.css (which overides bootstrap theme) 

dash_app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
dash_app.config.suppress_callback_exceptions = True
dash_app.enable_dev_tools(debug=True)

#get reference to flask.
app = dash_app.server

import python_webapp_flask.index