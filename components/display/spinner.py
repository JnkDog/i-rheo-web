import dash_bootstrap_components as dbc
import dash_core_components as dcc

Spinner = dbc.Spinner(
    dcc.Graph(id="display", style={"height" : "80vh"}),
    color="primary"
)