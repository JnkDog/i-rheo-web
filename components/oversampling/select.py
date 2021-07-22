import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

options_list = [
    {"label": "Linear", "value": "linear"},
    {"label": "Slinear", "value": "slinear"},
    {"label": "Nearest", "value": "nearest"},
]

Selectoversampling = dbc.Select(
    id="select-oversampling",
    options=options_list,
    placeholder="Choose a type ..."
)
