from dash_bootstrap_components._components.Button import Button
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components.Br import Br

from components.oversampling.input import OversamplingInput, oversampling_input_generate
# from components.oversampling.select import SelectOversampling
from components.oversampling.switch import Switch, switch_component_generate, FT_rendering_switch_generate
from components.inputgdot.inputgdot import Inputgdot, input_gdot_generate, mot_input_generate

OVERSAMPLING_BUTTON_SUFFIX = "-oversampling-btn"

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
    html.P("switch it", className="mb-1"),
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
                    html.P("switch it", className="mb-1"),
                    switch_component_generate(prefix_app_name),
                    FT_rendering_switch_generate(prefix_app_name)          
    ])

    return Oversampling
 
def mot_oversampling_generate(prefix_app_name):
    button_id = prefix_app_name + OVERSAMPLING_BUTTON_SUFFIX
    Oversampling = html.Div([
                   html.H5("Input kt and at"),
                   mot_input_generate(prefix_app_name),
                   html.Br(),
                   dbc.InputGroup(
                        # id="oversampling-control-components",
                        children=[
                            oversampling_input_generate(prefix_app_name),
                            dbc.Button("oversampling", id=button_id, 
                                       color="primary", className="ml-3"),
                        ]),
                    # html.H5(id="oversampling-message", className="text-warning"),
                    html.P("switch it", className="mb-1"),
                    switch_component_generate(prefix_app_name)
    ])

    return Oversampling
