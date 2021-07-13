import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

options_list = [
    {"label": "Linear", "value": 1},
    {"label": "Slinear", "value": 2},
    {"label": "Nearest", "value": 3},
]

SelectOversamping = dbc.Select(
    options=options_list,
    placeholder="Type"
)
