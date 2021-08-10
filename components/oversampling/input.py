import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

INPUT_ID_SUFFIX = "-oversampling-input"
OUTPUT_ID_SUFFIX = "-oversampling-output"

OversamplingInput = html.Div([
    # html.P("Input the oversampling points number and use the switch"),
    dbc.Input(id="oversampling-input", placeholder="Type the number", type="number")
])


def oversampling_input_generate(prefix_app_name, placeholder0="Type the number", placeholder1="Number of points output"):
    input_id = prefix_app_name + INPUT_ID_SUFFIX
    output_id = prefix_app_name + OUTPUT_ID_SUFFIX

    return html.Div([
            dbc.Input(id=input_id, placeholder=placeholder0, type="number"),
            html.Br(),
            dbc.Input(id=output_id, placeholder=placeholder1, type="number"),
    ])

def oversampling_output_generate(prefix_app_name, placeholder0="Type the number"):  # placeholder1="Number of points output"
    input_id = prefix_app_name + INPUT_ID_SUFFIX
    # output_id = prefix_app_name + OUTPUT_ID_SUFFIX

    return html.Div([
            dbc.Input(id=input_id, placeholder=placeholder0, type="number"),
            html.Br(),
            # dbc.Input(id=output_id, placeholder=placeholder1, type="number"),
    ])