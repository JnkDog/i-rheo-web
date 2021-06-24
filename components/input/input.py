import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

InputValue = html.Div([
    html.P("Input the x value"),
    dbc.Input(id="input", placeholder="Type something...", type="number")
])