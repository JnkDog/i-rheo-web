from dash_bootstrap_components._components.Button import Button
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components.B import B
from dash_html_components.Br import Br

from components.oversampling.input import OversamplingInput, oversampling_input_generate, oversampling_output_generate
# from components.oversampling.select import SelectOversampling
from components.oversampling.switch import Switch, switch_component_generate, FT_rendering_switch_generate
from components.inputgdot.inputgdot import Inputgdot, input_gdot_generate, mot_input_generate, afm_parameter_input_generate, afm_dot_input_generate

OVERSAMPLING_BUTTON_SUFFIX = "-oversampling-btn"
REOVERSAMPLING_BUTTON_SUFFIX = "-refresh-btn"
INPUT_ID_SUFFIX = "-oversampling-input"
OUTPUT_ID_SUFFIX = "-oversampling-Nf"

# This is templates but used in irheo GT
Oversampling = html.Div([
    html.H5("Boundary conditions"),
    Inputgdot,
    html.Br(),
    html.H5("Oversampling operation"),
    dbc.InputGroup(
        id="oversampling-control-components",
        children=[
            OversamplingInput,
            dbc.Button("oversampling", id="oversampling-btn", 
                       color="primary", className="ml-3"),
    ]),
    # html.H5(id="oversampling-message", className="text-warning"),
    # html.P("switch it", className="mb-1"),
    Switch
])


def oversampling_component_generate(prefix_app_name):
    button_id = prefix_app_name + OVERSAMPLING_BUTTON_SUFFIX
    Oversampling = html.Div([
                   html.H5("Boundary conditions"),
                   input_gdot_generate(prefix_app_name),
                   html.Br(),
                   html.H5("Oversampling operation"),
                   dbc.InputGroup(
                        # id="oversampling-control-components",
                        children=[
                            oversampling_input_generate(prefix_app_name),
                            dbc.Button("oversampling", id=button_id, 
                                       color="primary", className="ml-3"),
                        ]),
                    # html.H5(id="oversampling-message", className="text-warning"),
                    # html.P("switch it", className="mb-1"),
                    html.Br(),
                    switch_component_generate(prefix_app_name),
                    FT_rendering_switch_generate(prefix_app_name)          
    ])

    return Oversampling


def oversampling_control(prefix_app_name, button_id, secondbutton_id):
    input_id = prefix_app_name + INPUT_ID_SUFFIX
    output_id = prefix_app_name + OUTPUT_ID_SUFFIX

    Control_Component = dbc.Form(
        [
            dbc.FormGroup(
                [
                    dbc.Label("Oversampling times number", className="mr-2"),
                    dbc.Input(id=input_id, type="number", placeholder="default 10"),
                ],
                className="mr-3",
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Output points number", className="mr-2"),
                    dbc.Input(id=output_id, type="number", placeholder="default 100"),
                ],
                className="mr-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(dbc.Button("Oversampling", id=button_id, color="primary")), 
                        # width=2
                    ),
                    dbc.Col(
                        html.Div(dbc.Button("Refresh", id=secondbutton_id, color="secondary")),
                        # width=2,
                    ),
                ],
            ),
            # dbc.FormGroup(dbc.Button("Oversampling/Refresh", id=button_id, color="primary")),
        ],
        # inline=False,
    )
    return Control_Component


def afm_oversampling_generate(prefix_app_name):
    button_id = prefix_app_name + OVERSAMPLING_BUTTON_SUFFIX
    secondbutton_id = prefix_app_name + REOVERSAMPLING_BUTTON_SUFFIX
    Oversampling = html.Div([
        html.H5("Boundary conditions"),
        afm_dot_input_generate(prefix_app_name),
        html.Br(),
        html.H5("Input parameter Radius and V"),
        afm_parameter_input_generate(prefix_app_name),
        html.Br(),
        html.H5("Oversampling Operation"),
        oversampling_control(prefix_app_name, button_id, secondbutton_id),
        # html.P("switch it", className="mb-1"),
        html.Br(),
        switch_component_generate(prefix_app_name)
    ])

    return Oversampling


def mot_oversampling_generate(prefix_app_name):
    button_id = prefix_app_name + OVERSAMPLING_BUTTON_SUFFIX
    Oversampling = html.Div([
                   html.H5("Boundary conditions"),
                   input_gdot_generate(prefix_app_name),
                   html.Br(),
                   html.H5("Oversampling operation"),
                   dbc.InputGroup(
                        # id="oversampling-control-components",
                        children=[
                            oversampling_input_generate(prefix_app_name),
                            dbc.Button("oversampling", id=button_id, 
                                       color="primary", className="ml-3"),
                        ]),
                    # html.H5(id="oversampling-message", className="text-warning"),
                    # html.P("switch it", className="mb-1"),
                    html.Br(),
                    switch_component_generate(prefix_app_name)
    ])

    return Oversampling
