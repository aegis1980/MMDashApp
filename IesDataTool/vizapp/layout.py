
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output

import numpy as np
from vizapp.app import glasses,zone_names

settings = dbc.Row([

       dbc.Col([
           dbc.Card(
                [
            html.H4("Zone(s) select"),
            dbc.Checklist(
                id='zones-select',
                options=[{'label': i, 'value': i} for i in zone_names],
                values=zone_names
            )
        ]
                , body=True)], width = 3),

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
                    dcc.Slider(
                        id='pmv-slider',
                        min=-2,
                        max=2,
                        value=0.5,
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
    ])

def scenario_row(name):
    div = dbc.Row([
        dbc.Col([
            html.H3("Scenario " + name),
            dbc.RadioItems(
                id='scenario-select',
                options=[{'label': i, 'value': i} for i in glasses],
                value=glasses[0]
            ),    
        ], width = 2),
        dbc.Col([
             dcc.Graph(id='plain-heatmap')
        ], width = 10 )
    ])
    return div

""" app page"""
app_page = html.Div([
    dbc.Row([
        dbc.Col([dbc.Button(
                "Show settings",
                id="collapse-button", 
                className ="glyphicon glyphicon-cog"
        ) ],width =3),
        dbc.Col("Currently showing: settings",width =9)
      
    ]),

    dbc.Collapse(
        [settings],
        id = 'collapse'
    ),
    scenario_row('A')
    ,
    
    dcc.Graph(id='graph-with-slider')
]) # end of index_page

