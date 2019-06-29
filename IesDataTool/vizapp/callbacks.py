""

from app import app
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import pandas as pd
import math
import numpy as np

from IES import IesDataTool
import vizapp.app as tool
from vizapp.app import my_ies_tool


@app.callback(
    [Output('graph-with-slider', 'figure'),
     Output('plain-heatmap', 'figure')],
    [Input('pmv-slider', 'value'),
     Input('scenario-select','value'),
     Input('zones-select','values'),
     Input('time-slider', 'value'),
     Input('n-hottest', 'value')])
def update_figure(pmv,scenario, zones, time_range, hottest_n):
    t = list(map (tool.format_time_from_slider, time_range))
    df = my_ies_tool.get_heatmap_array_df(dataset= IesDataTool.COMBINED_PMV, zones= zones, scenario=scenario, time_range = t, hottest_n=hottest_n)

    filtered_df = df.applymap(lambda x : tool.my_filter(x,pmv))

    readable_times = [str(x)[:-3] for x in df.index.tolist()] # times for y axes.
    readable_dates = [pd.to_datetime(x).strftime('%d %b') for x in df.columns.values.tolist()]



    data_plain = go.Heatmap(
                    z= df,
                    xgap = 2,
                    ygap = 1,
                    zmid = 0,
                    zmax = df.values.max(),
                    x = readable_dates,
                    y = readable_times)

    data_filtered = go.Heatmap(
                    z= filtered_df,
                    xgap = 2,
                    ygap = 1,
                    x = readable_dates,
                    y = readable_times,
                    opacity=0.5,
                    colorscale= [
                            [0, 'rgb(255,255,255)'],
                            [1, 'rgb(0,0,0)']
                        ],
                    showscale=False
                )

    return {'data': [data_plain,data_filtered]},{'data': [data_plain]}


@app.callback(
    [Output('slider-output-start', 'children'),
     Output('slider-output-end', 'children')],
    [Input('time-slider', 'value')])
def update_output(value):
    t1 = 'Start time {}:{}'.format(math.floor(value[0]/2),(value[0] % 2)*30)
    t2 = 'End time {}:{}'.format(math.floor(value[1]/2),(value[1] % 2)*30)
    return t1,t2



@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open