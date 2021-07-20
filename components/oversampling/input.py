import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

OversamplingInput = html.Div([
    # html.P("Input the oversampling points number"),
    dbc.Input(id="oversampling-input", placeholder="Type the number", type="number")
])