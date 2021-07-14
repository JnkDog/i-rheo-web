import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px

from app import app

# import components
from components.upload.upload import Upload
from components.input.input import InputValue
from components.display.spinner import Spinner
from components.oversamping.oversamping import Oversamping

# import algorithm
from algorithm.sigma import Sigma
from algorithm.oversample import Oversampling

Layout = dbc.Row([
            dbc.Col([
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
                    Oversamping], 
            width=3)
            , dbc.Col([Spinner], width=True)
])

# @app.callback(
#     [
#         Output("display", "figure"),
#         Output("upload_message", "children")
#     ],
#     Input("upload", "contents"),
#     # State("input", "value"),
#     State("upload", "filename"),
#     # dont call the func when first loaded
#     prevent_initial_call=True
# )
# def upload_process(contents, name):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     print(button_id)
#     if contents is None:
#         name = "Please chosse a file"

#     fig = Sigma.sigma_render(contents)

#     message = html.H6(name)
    
#     return [fig, message]

@app.callback(
    [
        # Output("display", "figure"),
        Output("oversamping-message", "children"),
        Output("display", "figure"),
    ],
    [
        Input("oversamping-btn", "n_clicks")
    ],
    [
        State("upload", "contents"),
        State("oversamping-input", "value"),
        State("select-oversamping", "value")
    ],
    # State("upload", "contents"),
    # dont call the func when first loaded
    prevent_initial_call=True
)
def oversamping_render(btn_click, content, points_number, option):
    fig = px.scatter()
    if option is None or points_number is None:
        return ["Choice types and input number both", fig]
    
    # test option
    option = "slinear"
    test = Oversampling(content)
    fig = test.oversamping_render(content, 1, option)
    # fig = Oversampling.oversamping_render(content, points_number, option)    
    return ["hello world", fig]
