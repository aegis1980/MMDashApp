""

from app import app
import dash
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import pandas as pd
import math
import numpy as np

import costapp.app as tool
from costapp.app import my_cost_tool

@app.callback(
    Output('tableout', 'data'),
    [Input('des_life', 'value'),
     Input('fac_area', 'value'),
     Input('rep_factor', 'value'),
     Input('inflation', 'value'),
     Input('e_cost', 'value'),
     Input('e_inflation', 'value'),
     Input('tablein', 'data'),
     Input('tablein', 'columns')]
)
def update_data(des_life, area, rep_factor,
                inflation,
                e_cost, e_inflation,
                datain, colsin):
    params = {
        'design_life' : des_life,
        'area' : area,
        'rep_factor' : rep_factor/100.0, #user input is in %
        'inflation' : inflation/100.0, #user input is in %
        'e_cost' : e_cost/100.0, #user input in c/kWhr
        'e_inflation' : e_inflation/100  #user input is in %
    }
    my_cost_tool.datain_change_from_ui(datain, colsin, params)
    return my_cost_tool.dataout()


@app.callback(
    [Output('building-collapse', "is_open"),Output('cost-collapse', "is_open"),Output('e-collapse', "is_open")],
    [Input("building-toggle", "n_clicks"),Input("cost-toggle", "n_clicks"),Input("e-toggle", "n_clicks")],
    [State('building-collapse', "is_open"),State('cost-collapse', "is_open"),State('e-collapse', "is_open")],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "building-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "cost-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "e-toggle" and n3:
        return False, False, not is_open3
    return False, False, False