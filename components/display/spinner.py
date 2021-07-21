import dash_bootstrap_components as dbc
import dash_core_components as dcc

Spinner = dbc.Spinner(
    dcc.Graph(id="display", style={"height" : "80vh"}),
    color="primary"
)

Spinner_sigma = dbc.Spinner(
    dcc.Graph(id="sigma-display", style={"height" : "80vh"}),
    color="primary"
)

Spinner_FT = dbc.Spinner(
    dcc.Graph(id="FT-display", style={"height" : "80vh"}),
    color="primary"
)

Spinner_gamma = dbc.Spinner(
    dcc.Graph(id="gamma-display", style={"height" : "80vh"}),
    color="primary"
)

Spinner_eta = dbc.Spinner(
    dcc.Graph(id="gamma-display", style={"height" : "80vh"}),
    color="primary"
)

def spinner_generate(id):
    id += "-display"
    spinner = dbc.Spinner(
        dcc.Graph(id=id, style={"height" : "80vh"}),
        color="primary"
    )

    return spinner