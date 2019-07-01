
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output, State

import numpy as np
from vizapp.app import glasses,zone_names, glass_info

outline_color = "secondary"

RED_COLOR = '#d9534f'
BLUE_COLOR = '#1F9BCF'

settings = dbc.Card(
                [
dbc.Row([

       dbc.Col([
           dbc.Card(
                [
                    html.H5("Zone(s)"),
                    dbc.Checklist(
                        id='zones-select',
                        options=[{'label': i, 'value': i} for i in zone_names],
                        values=zone_names
                    )
                ], body=True,color=outline_color, outline=True)
        ], width = 3),

        dbc.Col([
           dbc.Card(
                [
                    html.H5("Time range"),
                    html.Div(id='slider-output-start'),
                    html.Div(id='slider-output-end'), 
                    html.Hr(),
                    dcc.RangeSlider(
                        id='time-slider',
                        min=0,
                        max=48,
                        value=[18,36],
                        step=2,
                        updatemode='drag'            
                    ),
                ], body=True,color=outline_color, outline=True)
        ], width = 3),

        dbc.Col([
           dbc.Card(
                [

                    html.H5("PMV filter", className= 'float-left'),
                    daq.PowerButton(
                            id = 'filter-btn',
                            on='True',
                            color = RED_COLOR,
                    ), 
                    html.Hr(),
                    dbc.FormGroup([
                        dbc.Label("Filter value"),
                        dbc.Input(id='pmv-input', className = "w-75", placeholder="pmv", type="number", value=0.5, min=-3, max=3, step=0.05),
                        dbc.FormText("Input number"),
                    ]),                  
                    html.Br(),
                    html.Div(children = [
                        html.Span("Cold", className='float-left'),
                        html.Span("Warm" , className='float-right'),
                        daq.ToggleSwitch(
                            id='filter-mode',
                            label='pick mode',
                            labelPosition='bottom',
                            color = RED_COLOR,
                            value = True
                        )
                    ])
                ], body=True, color=outline_color, outline=True)
        ], width = 3),


       dbc.Col([
            dbc.Card(
                [
                    html.H5("Data Display"),
                    dcc.Dropdown(
                        id = 'data-mode',
                        options=[
                            {'label': 'Heatmap: N-warmest in year', 'value': 'NH'},
                            {'label': 'Heatmap: N-coolest in year', 'value': 'NC'},
                            {'label': 'HeatMap: Whole year', 'value': 'Y'},
                        ],
                        value='NH',
                        clearable=False,
                    ),  

                    html.Hr(),   
                    dbc.FormGroup(
                        [
                            dbc.Label("Number of days"),
                            dbc.Input(id='n-hottest', className = "w-50", placeholder="Number...", type="number", value=30, min=1, max=50, step=1),
                            dbc.FormText("Input number"),
                        ])
                ], body=True,color=outline_color, outline=True)
            
        ], width = 3)
    ])
 ], body=True,color='dark')

def scenario_card(name):
    div = html.Div([
        dbc.Row([
             dbc.Col([
                html.H5("Scenario " + name),
             ], width = 12 )
        ]),
        dbc.Row([                    
            dbc.Col([
                dcc.Dropdown(
                    id='scenario-select'+name,
                    options=[{'label': glass_info[i]['short_name'], 'value': i} for i in glasses],
                    value=glasses[0],
                    clearable = False,
                )
            ], width = 4 ),
            dbc.Col([
                dcc.Markdown(
                    glass_info[glasses[0]]['markdown'],
                    id = 'scenario-description'+name,
                    dangerously_allow_html = True)
            ], width = 8 )
        ] ),
        dbc.Row([
            
            dbc.Col([
                 dcc.Graph(id='heatmap'+name)
            ], width = 12 )
        ])
    ])
    return div

""" app page
this is content is nested into Bootstrap fluid=true container in index.py"""
app_page = html.Div([
    dbc.Container([
    dbc.Row([
        dbc.Col([dbc.Button(
                "Show settings",
                id="collapse-button", 
                color="secondary"
        ) ],width =3)
      
    ]),

    dbc.Collapse(
        [settings],
        id = 'collapse'
    )]),

    dbc.Row([
        dbc.Col(scenario_card('A'),width =6),
        dbc.Col(scenario_card('B'),width =6)
    ], className = 'mt-4'),


]) # end of index_page

