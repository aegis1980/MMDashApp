
# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc

# styling:
# LUX is a bootswatch theme which is included in dash-bootstrap
# additional styling in assets/styling.css (which overides bootstrap theme) 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server
app.config.suppress_callback_exceptions = True