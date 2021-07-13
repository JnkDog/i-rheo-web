# os package
import datetime
import base64
from unicodedata import name

# framework package
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# delay js after loading components rendered
# import dash_defer_js_import as defer_load

# team components
from components.nav.nav import NavBar
from components.upload.upload import Upload
from components.input.input import InputValue
from components.display.spinner import Spinner
from components.oversamping.oversamping import Oversamping

# Algorithms
from algorithm.drawing import drawing, drawing_demo_data

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        NavBar,
        dbc.Row([
            dbc.Col(
                [
                    html.Div([
                        html.H5("Support .txt"),
                        Upload,
                        html.Div(id="upload_message")
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Example data"),
                        dbc.Button("Load Example data", id="load_example", color="primary", style={"margin": "5px"})
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Key Parameters"),
                        InputValue
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Commands"),
                        dbc.Button("Calculate", id="calculate", color="primary", style={"margin": "5px"})
                    ]),
                    html.Hr(),
                    Oversamping
                ], 
            width=3
            )
        , dbc.Col([Spinner], width=True)
        ])
    ],
    className="container-fluid"
)

# Be caution about the different between [Output] and Output
# Also the Input and Output !!!
@app.callback(
    [
        Output("display", "figure"),
        Output("upload_message", "children")
    ],
    Input("calculate", "n_clicks"),
    Input("load_example", "n_clicks"),
    State("upload", "contents"),
    State("input", "value"),
    State("upload", "filename"),
    # dont call the func when first loaded
    prevent_initial_call=True
)
def data_process(calculate_btn, sample_btn, contents, input_value, name):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # print(button_id)

    if button_id == "load_example":
        fig = drawing_demo_data()
        message = "Demo data"
        return fig, message

    fig = drawing(contents, input_value)

    if contents is None:
        name = "Please chosse a file"

    message = html.Div([
        html.H6(name)
    ])

    return [fig, message]

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.layout = html.Article(defer_load.Import(src="./assets/js/nav-menu.js"))
