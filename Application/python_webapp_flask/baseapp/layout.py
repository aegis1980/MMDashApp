import os

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output, State
import pandas as pd

import numpy as np
from python_webapp_flask import ASSETS_PATH


""" app page
this is content is nested into Bootstrap fluid=true container in index.py"""
app_page = dbc.Container([
    dbc.Row([
        dbc.Col([],width =3),
        dbc.Col([],width =9),
 
    ],className = 'mt-4')
]) # end of index_page

