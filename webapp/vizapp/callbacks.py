""

from rootapp import app
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

import pandas as pd
import math
import numpy as np

from IES import IesDataTool
import vizapp.app as tool
from vizapp.app import my_ies_tool, glass_info


from vizapp.layout import RED_COLOR,BLUE_COLOR


@app.callback(
    [Output('heatmapA', 'figure'),
     Output('heatmapB', 'figure')],
    [Input('filter-btn','on'), Input('pmv-input', 'value'), Input('filter-mode', 'value'),
     Input('scenario-selectA','value'),Input('scenario-selectB','value'),    
     Input('zones-select','values'),
     Input('time-slider', 'value'),
     Input('data-mode', 'value'),Input('n-hottest', 'value')])
def update_heatmaps(
            filter, pmv, filter_mode,
            scenarioA,scenarioB, 
            zones, 
            time_range, 
            data_mode,n
        ):
    
    t = list(map (tool.format_time_from_slider, time_range))

    figA = tool.generate_heatmap_figure(zones,scenarioA,t,data_mode, n, filter, pmv, filter_mode)
    figB = tool.generate_heatmap_figure(zones,scenarioB,t,data_mode, n, filter, pmv, filter_mode)

    return figA, figB


@app.callback(
    [Output('slider-output-start', 'children'),
     Output('slider-output-end', 'children')],
    [Input('time-slider', 'value')])
def update_output(value):
    t1 = 'Start time {}:{}'.format(math.floor(value[0]/2),(value[0] % 2)*30)
    t2 = 'End time {}:{}'.format(math.floor(value[1]/2),(value[1] % 2)*30)
    return t1,t2



@app.callback(
    [Output("collapse", "is_open"),Output("collapse-button", "children")],
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if is_open is None or not is_open:
        btn_text = "Hide settings"
    else:
        btn_text =  "Show settings"
    if n:
        return not is_open, btn_text
    return is_open, btn_text


@app.callback(
    [Output("filter-mode", "disabled"),
     Output("pmv-input", "disabled")],
    [Input("filter-btn", "on")]
)
def toggle_pmv_filter_ui(on_off):
    off_on = not on_off
    return off_on,off_on


@app.callback(
    Output("filter-mode", "color"),
    [Input("filter-mode", "value")]
)
def toggle_switch_color(warm):
    return (BLUE_COLOR , RED_COLOR)[warm]


@app.callback(
    Output('scenario-descriptionA', 'children'),
    [Input('scenario-selectA','value')]
)
def update_scenario_detailsA(s):
    return glass_info[s]['markdown']


@app.callback(
    Output('scenario-descriptionB', 'children'),
    [Input('scenario-selectB','value')]
)
def update_scenario_detailsB(s):
    return glass_info[s]['markdown']