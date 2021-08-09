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
        placeholder="Input your ġ(∞), default 0"
    )
])


def input_gdot_generate(prefix_app_name):
    g_0_id   = prefix_app_name + "-g_0"
    g_inf_id = prefix_app_name + "-g_inf"

    Inputgdot = html.Div([
        dbc.Input(
            id=g_0_id,
            type="number",
            placeholder="Input your g(0), default 1 as A(t), 0 as ∏(t)"
        ),
        html.Br(),
        dbc.Input(
            id=g_inf_id,
            type="number",
            placeholder="Input your ġ(∞), default 0"
        )
    ])

    return Inputgdot


def afm_parameter_input_generate(prefix_app_name):
    r_id = prefix_app_name + "-r"
    v_id = prefix_app_name + "-v"

    AFMInput = html.Div([
        dbc.Input(id=r_id, type="number", placeholder="Input radius, default 20"),
        html.Br(),
        dbc.Input(id=v_id, type="number", placeholder="Input v, default 0.5"),
        # html.Br(),
    ])

    return AFMInput


def afm_dot_input_generate(prefix_app_name):
    ind0_id = prefix_app_name + "-indentation0"
    indinf_id = prefix_app_name + "-indentationinf"
    load0_id = prefix_app_name + "-load0"
    loadinf_id = prefix_app_name + "-loadinf"

    AFMDotInput = html.Div([
        dbc.Input(id=load0_id, type="number", placeholder="Input Load(0), default 1"),
        html.Br(),
        dbc.Input(id=loadinf_id, type="number", placeholder="Input Load(inf), default 0"),
        html.Br(),
        dbc.Input(id=ind0_id, type="number", placeholder="Input Indentation(0), default 1"),
        html.Br(),
        dbc.Input(id=indinf_id, type="number", placeholder="Input Indentation(∞), default 0"),
    ])
    
    return AFMDotInput


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
            placeholder="Input at, default 1e1"
        )
    ])

    return MOTInput
