
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


zone_names = ['Lower perimeter','Lower inner','Bleachers perimeter','Bleachers inner','Upper perimeter','Upper inner','Lower foyer perimeter','Lower foyer inner']
glasses = ['BECA SU', 'BECA IGU','MM SU', 'MM IGU' ]
filename = 'data\data_file.xlsx'

my_ies_tool = IesDataTool(zone_names,glasses)   
my_ies_tool.load_data(filename,load_from_pickle = True, save_to_pickle = True)


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
                value=[16,36],
                step=2,
                updatemode='drag'
                
            ),
            html.Div(id='slider-output-start'),
            html.Div(id='slider-output-end'),   

            dbc.FormGroup(
                [
                    dbc.Label("PMV range"),
                    dcc.RangeSlider(
                        id='pmv-slider',
                        min=-2,
                        max=2,
                        value=[-0.5,0.5],
                        marks= {i: '{}'.format(i) for i in np.arange(-2, 2, 0.25)},
                        step = 0.25
                    )
                ]),

            dbc.FormGroup(
                [
                    dbc.Label("N-hottest"),
                    dbc.Input(id='n-hottest', placeholder="Number...", type="number", value=30, min=1, max=50, step=1),
                    dbc.FormText("Input number"),
                ]
)
            
        ], width = 6)
    ]),

    dcc.Graph(id='plain-heatmap'),
    
   
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
    df = my_ies_tool.get_heatmap_array_df(dataset= IesDataTool.COMBINED_PMV, zones= zones, scenario=scenario, time_range = t, hottest_n=hottest_n)

    filtered_df = df.applymap(lambda x : my_filter(x,pmv))

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



