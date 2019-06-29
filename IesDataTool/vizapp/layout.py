
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import numpy as np
from vizapp.app import glasses,zone_names


""" app page"""
app_page = html.Div([
   
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
    
   
    dcc.Graph(id='graph-with-slider')
]) # end of index_page

