
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output, State
import pandas as pd

import numpy as np
from costapp.app import my_cost_tool,glasses,zone_names, glass_info
import costapp.app as tool


outline_color = "secondary"

RED_COLOR = '#d9534f'
BLUE_COLOR = '#1F9BCF'

params = [
    'Rate($)', 'Area(m2)', 'Upfront cost($)', 'Service life(y)', 'Life Cost($)'
]
df = pd.read_csv('data\cost_data.csv')

""" app page
this is content is nested into Bootstrap fluid=true container in index.py"""
app_page = dbc.Container([
    dbc.Row([
        dbc.Col([
#            dbc.Card(
 #               [
  #                  html.H5("Scenarios"),
 #                   dbc.Checklist(
 #                       id='scenario-select',
 #                       options=[{'label': glass_info[i]['short_name'], 'value': i} for i in glasses],
 #                       values = glasses
 #                   )
#                ], body=True,color=outline_color, outline=True, className= 'small-box'),
             
                html.H5("Parameters"),
                
                dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Button(
                            'Building properties',
                            color='link',
                            id='building-toggle',
                        )
                    ),
                    dbc.Collapse([
                    dbc.CardBody([

                    dbc.FormGroup([
                        dbc.Label("Building design life", html_for="des_life"),
                        dbc.Input(id='des_life', className = "w-75", type="number", min=0, value = 50),
                        dbc.FormText("years"),
                    ]), 
                    dbc.FormGroup([
                        dbc.Label("Facade area", html_for="area"),
                        dbc.Input(id='fac_area', className = "w-75", type="number", min=0, value = 750),
                        dbc.FormText("msqr"),
                    ]),
                    dbc.FormGroup([
                        dbc.Label("IGU Replacement factor", html_for="rep_factor"),
                        dbc.Input(id='rep_factor', className = "w-75", type="number", min=0, max = 100, value = 60),
                        dbc.FormText("%"),
                    ]),   
                    ])
                    ],id='building-collapse')
                ],color=outline_color, outline=True),


                dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Button(
                            'Costs',
                            color='link',
                            id='cost-toggle',
                        )
                    ),
                    dbc.Collapse([
                        dbc.CardBody([
                            dbc.FormGroup([
                                dbc.Label("Annual inflation", html_for="inflation"),
                                dbc.Input(id='inflation', className = "w-75", type="number", min=0, value = 2.1),
                                dbc.FormText("%"),
                            ]),
                        ])
                    ],id='cost-collapse')
                ],color=outline_color, outline=True),


                dbc.Card(
                [
                   dbc.CardHeader(
                        dbc.Button(
                            'Energy',
                            color='link',
                            id='e-toggle',
                        )
                    ),
                    dbc.Collapse([
                        dbc.CardBody([
                            dbc.FormGroup([
                                dbc.Label("Energy cost (Year 1)", html_for="e_cost"),
                                dbc.Input(id='e_cost', className = "w-75", type="number", min=0, value = tool.DEFAULT_NZ_COMMERCIAL_ERATE),
                                dbc.FormText("c/kWhr"),
                            ]),  
                            dbc.FormGroup([
                                dbc.Label("Energy cost inflation", html_for="e_inflation"),
                                dbc.Input(id='e_inflation', className = "w-75", type="number", min=0, value = 2.1),
                                dbc.FormText("%"),
                            ]),
                        ])
                    ],id='e-collapse')
                ],color=outline_color, outline=True)

            ],width =3),
        dbc.Col([

            dbc.Row([
                html.Div([
                    html.H3('Input: scenario parameters'),
                    html.P('Note, these parameters are editable'),
                ]),
                dash_table.DataTable(
                    id='tablein',
                    columns=[{"name": i, "id": i} for i in my_cost_tool.columnsin()],
                    data=my_cost_tool.datain(),
                    editable=True)
             ]),

            dbc.Row([
                html.H3('Output: Dollar lifecycle costs'),
                dbc.Alert('''
                    Values do not include the initial cost, maintenance cost and replacement cost of the HVAC system.
                ''', color="danger"),
             dash_table.DataTable(
                id='tableout',
                columns=[{"name": i, "id": i} for i in my_cost_tool.columnsout()],
                data=my_cost_tool.dataout(),
                editable=False)
            ], className = 'mt-4'),


         #   dbc.Row([
         #       dcc.Graph(id='my-graph'),
         #   ], className = 'mt-4')

        ],width =9),
 
    ],className = 'mt-4')
]) # end of index_page

