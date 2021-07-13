import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

OversampingInput = html.Div([
    # html.P("Input the oversamping points number"),
    dbc.Input(id="oversamping-input", placeholder="Type the number", type="number")
])