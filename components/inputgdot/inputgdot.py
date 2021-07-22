import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


Inputgdot = html.Div([
    dcc.Input(
        id="g_0",
        type="number",
        placeholder="Input your g(0)"
    ),
    html.Br(),
    dcc.Input(
        id="g_inf",
        type="number",
        placeholder="Input your g(∞)"
    )
]   
)