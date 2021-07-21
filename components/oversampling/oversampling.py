from dash_bootstrap_components._components.Button import Button
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.oversampling.input import OversamplingInput, oversampling_input_generate
# from components.oversampling.select import SelectOversampling
from components.oversampling.switch import Switch, switch_component_generate

OVERSAMPLING_BUTTON_SUFFIX = "-oversampling-btn"

# This is templates but used in irheo GT
Oversampling = html.Div([
    html.H5("Oversampling"),
    dbc.InputGroup(
        id="oversampling-control-components",
        children=[
            OversamplingInput,
            dbc.Button("oversampling", id="oversampling-btn", color="primary"),
    ]),
    # html.H5(id="oversampling-message", className="text-warning"),
    Switch
])


def oversampling_component_generate(prefix_app_name):
    button_id = prefix_app_name + OVERSAMPLING_BUTTON_SUFFIX
    Oversampling = html.Div([
                   html.H5("Oversampling"),
                   dbc.InputGroup(
                        # id="oversampling-control-components",
                        children=[
                            oversampling_input_generate(prefix_app_name),
                            dbc.Button("oversampling", id=button_id, color="primary"),
                        ]),
                    # html.H5(id="oversampling-message", className="text-warning"),
                    switch_component_generate(prefix_app_name)
    ])

    return Oversampling
 