
# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from IES import IesDataTool 
import numpy as np
import math




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



zone_names = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8']
glasses = ['BECA SU', 'BECA IGU','MM IGU', 'MM SG' ]
filename = 'C:/data/full_pmv_summer_clo.csv'

my_ies_tool = IesDataTool(zone_names,glasses)   
my_ies_tool.load_pmv_data([filename],load_from_pickle = True, save_to_pickle = True)


def format_time_from_slider(slider_time):
    t =  '{}:{}:00'.format(math.floor(slider_time/2),(slider_time % 2)*30)
    return pd.datetime.strptime(t,'%H:%M:%S').time()


def my_filter(x, pmv):
    mid = 0.5*(pmv[0]+pmv[1])
    if x<=pmv[0]:
        return pmv[0]
    elif x>=pmv[1]:
        return pmv[1]
    return mid


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Comfort",
    brand_href="#",
    sticky="top",
    dark=True
)

body = dbc.Container([
  

   dbc.Row([
        dbc.Col([
            dbc.Label("Scenarios select"),
            dbc.RadioItems(
                id='scenario-select',
                options=[{'label': i, 'value': i} for i in glasses],
                value=glasses[0]
            )
        ], width=3),

       dbc.Col([
            dbc.Label("Zone(s) select"),
            dbc.Checklist(
                id='zones-select',
                options=[{'label': i, 'value': i} for i in zone_names],
                values=zone_names
            )
        ], width = 3),

       dbc.Col([
            dbc.Label("Time range select"),
                dcc.RangeSlider(
                id='time-slider',
                min=0,
                max=48,
                value=[8,20],
                step=1,
                updatemode='drag'
                
            ),
            html.Div(id='slider-output-start'),
            html.Div(id='slider-output-end'),   

            dbc.FormGroup(
                [
                    dbc.Label("N-hottest"),
                    dbc.Input(id='n-hottest', placeholder="Number...", type="number", min=1, max=50, step=1),
                    dbc.FormText("Input number"),
                ]
)
            
        ], width = 6)
    ]),

    dcc.Graph(id='plain-heatmap'),
    
    dcc.RangeSlider(
        id='pmv-slider',
        min=-3,
        max=3,
        value=[-0.5,0.5],
        marks= {i: 'PMV {}'.format(i) for i in np.arange(-2, 2, 0.25)},
        step = 0.25
    ),
     dcc.Graph(id='graph-with-slider'),
])

app.layout = html.Div([navbar, body])

@app.callback(
    [Output('graph-with-slider', 'figure'),
     Output('plain-heatmap', 'figure')],
    [Input('pmv-slider', 'value'),
     Input('scenario-select','value'),
     Input('zones-select','values'),
     Input('time-slider', 'value'),
     Input('n-hottest', 'value')])
def update_figure(pmv,scenario, zones, time_range, hottest_n):
    t = list(map (format_time_from_slider, time_range))
    df = my_ies_tool.get_heatmap_array_df(zones= zones, scenario=scenario, time_range = t, hottest_n=hottest_n)

    t= marks= {i: '{}:{}:00'.format(math.floor(i/2),(i % 2)*30) for i in range(0, 23*2)}

    filtered_df = df.applymap(lambda x : my_filter(x,pmv))
    mid = 0.5*(pmv[0]+pmv[1])
    marks= {i: '{}:{}:00'.format(math.floor(i/2),(i % 2)*30) for i in range(0, 24*2)},

    readable_times = [str(x)[:-3] for x in df.index.tolist()] # times for y axes.

    data_plain = go.Heatmap(
                    z= df,
                    zmin = -2.0,
                    zmax = 2.0,
                    y = readable_times)
        
    data_filtered = go.Heatmap(
                    z= filtered_df,
                    y = readable_times,
                    colorscale= [
                            [0, 'rgb(0,0,255)'],
                            [0.5, 'rgb(255,255,255)'],
                            [1, 'rgb(255,0,0)']
                        ],
                    showscale=False
                )

    return {'data': [data_filtered]},{'data': [data_plain]}


@app.callback(
    [Output('slider-output-start', 'children'),
     Output('slider-output-end', 'children')],
    [Input('time-slider', 'value')])
def update_output(value):
    t1 = 'Start time {}:{}'.format(math.floor(value[0]/2),(value[0] % 2)*30)
    t2 = 'End time {}:{}'.format(math.floor(value[1]/2),(value[1] % 2)*30)
    return t1,t2



if __name__ == '__main__':
    app.run_server(debug=True)



