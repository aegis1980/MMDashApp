"""
index.py loads different apps/subapps on different urls
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

from vizapp.layout import app_page as vizapp_page 
from costapp.layout import app_page as costapp_page 
import vizapp.callbacks
import costapp.callbacks

MOTTS_LOGO = "static/img/mm_logo.svg"

navbar = dbc.Navbar(
    dbc.Container(
        children = [
            html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=MOTTS_LOGO, height="65px")),
                    dbc.Col(dbc.NavbarBrand("IES Data viewer", className="ml-2")),
                    dbc.Col("UoA Rec Centre Atrium")
                ],
                align="center",
                no_gutters=True,
            ),
        ),
    ]),
    color="dark",
    dark=True,
    sticky="top",
)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    navbar,

    # content will be rendered in this element
    dbc.Container(id='page-content', fluid=True)
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pmv':
        return vizapp_page
    elif pathname == '/cost':
        return costapp_page
    else:
        return vizapp_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True)