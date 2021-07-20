import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.oversampling.input import OversamplingInput
# from components.oversampling.select import SelectOversamping
from components.oversampling.switch import Switch

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
 