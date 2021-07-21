import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

INPUT_ID_SUFFIX = "-oversampling-input"

OversamplingInput = html.Div([
    # html.P("Input the oversampling points number"),
    dbc.Input(id="oversampling-input", placeholder="Type the number", type="number")
])

def oversampling_input_generate(prefix_app_name, placeholder="Type the number"):
    input_id = prefix_app_name + INPUT_ID_SUFFIX

    return html.Div([
            dbc.Input(id=input_id, placeholder=placeholder, type="number")
    ])