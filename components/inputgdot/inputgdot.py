import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# This is an example, but uesd in irheo GT
Inputgdot = html.Div([
    dbc.Input(
        id="g_0",
        type="number",
        placeholder="Input your g(0), default 1"
    ),
    html.Br(),
    dbc.Input(
        id="g_inf",
        type="number",
        placeholder="Input your g(∞), default 0"
    )
])

def input_gdot_generate(prefix_app_name):
    g_0_id   = prefix_app_name + "-g_0"
    g_inf_id = prefix_app_name + "-g_inf"

    Inputgdot = html.Div([
        dbc.Input(
            id=g_0_id,
            type="number",
            placeholder="Input your g(0), default 1"
        ),
        html.Br(),
        dbc.Input(
            id=g_inf_id,
            type="number",
            placeholder="Input your g(∞), default 0"
        )
    ])

    return Inputgdot

def mot_input_generate(prefix_app_name):
    kt_id = prefix_app_name + "-kt"
    at_id = prefix_app_name + "-at"

    MOTInput = html.Div([
        dbc.Input(
            id=kt_id,
            type="number",
            placeholder="Input kt, default 1e-6"
        ),
        html.Br(),
        dbc.Input(
            id=at_id,
            type="number",
            placeholder="Input at, default 1e6"
        )
    ])

    return MOTInput