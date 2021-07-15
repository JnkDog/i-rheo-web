import collections
from datetime import date
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from dash_core_components.Store import Store
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

from app import app

# import components
from components.upload.upload import Upload
from components.input.input import InputValue
from components.display.spinner import Spinner
from components.oversamping.oversamping import Oversamping
from components.tab.tabs import Tabs

# import algorithm
from algorithm.sigma import Sigma
from algorithm.oversample import Oversampling
from algorithm.read_data import generate_df

Layout = dbc.Row([
            dbc.Col([
                    html.Div([
                        html.H5("Support .txt"),
                        Upload,
                        html.Div(id="upload-message"),
                        dcc.Store(id="raw-data-store"),
                        dcc.Store(id="oversamping-data-store")
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Example data"),
                        dbc.Button("Load Example data", id="load-example", color="primary", style={"margin": "5px"})
                    ]),
                    html.Hr(),
                    Oversamping], width=3)
            , dbc.Col([Tabs], width=True)
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
    Output("raw-data-store", "data"),
    Output("upload-message", "children"),
    Input("upload", "contents"),
    State("upload", "filename"),
    prevent_initial_call=True
)
def store_data(content, file_name):
    df = generate_df(content)

    data = [{
        "x" : df[0],
        "y" : df[1],
        "data_type" : "raw"
    }]

    upload_messge = "The upload file {} with {} lines".format(file_name, len(df))

    return data, upload_messge

# @app.callback(
#     Output("sigma-display", "figure"),
#     Input("raw-data-store", "data"),
#     prevent_initial_call=True
# )
# def data_render(data):
#     fig = px.scatter()
 
#     return {
        
#     }

# clientside callback test
app.clientside_callback(
    """
    function(rawData, oversampingData, switchValue=[false]) {
        let data = []

        /**
        * Only oversamping button on and oversampingData has value to render Oversamping figure.
        * You may feel wired about the switchValue is [bool] not bool.
        * It's the Dash's wired part... Just follow the framework's rule QAQ
        */
        if (switchValue[0] == true && oversampingData != undefined) {
            console.log("========= in oversamping =======")
            console.log(oversampingData)
            data = oversampingData;
        } else {
            console.log("========= in sigma =======")
            console.log(rawData)
            data = rawData;
        }

        return {
            "data" : data,
            "layout": {
                "xaxis" : {"type": "log", "title" : {"text" : "Time (s)"}},
                "yaxis" : {"title" : {"text" : "G(t) (Pa)"}}
             }
        }   
    }
    """,
    Output("sigma-display", "figure"),
    Input("raw-data-store", "data"),
    Input("oversamping-data-store", "data"),
    Input("oversamping-render-switch", "value"),
    prevent_initial_call=True
)

# @app.callback(
#     [
#         # Output("display", "figure"),
#         Output("oversamping-message", "children"),
#         Output("sigma-display", "figure"),
#     ],
#     [
#         Input("oversamping-btn", "n_clicks")
#     ],
#     [
#         State("upload", "contents"),
#         # State("oversamping-input", "value"),
#         State("select-oversamping", "value")
#     ],
#     # State("upload", "contents"),
#     # dont call the func when first loaded
#     prevent_initial_call=True
# )
# def oversamping_render(btn_click, content, option):
#     fig = px.scatter()
#     if option is None:
#         return ["Choice types", fig]
    
    # # test option
    # option = "slinear"
    # test = Oversampling(content)
    # fig = test.oversamping_render(content, option)

    # fig = Oversampling.oversamping_render(content, points_number, option)    
#     return ["oversamping OK", fig]

# switch test
# @app.callback(
#     Output("oversamping-message", "children"),
#     Input("oversamping-render-switch", "value"),
#     prevent_initial_call=True
# )
# def switch_test(switch_value):
#     switch_value.append(False) if len(switch_value) == 0 else switch_value
    
#     return "The switch is {}".format(switch_value[0])

@app.callback(
    Output("oversamping-data-store", "data"),
    Input("oversamping-btn", "n_clicks"),
    State("upload", "contents"),
    State("select-oversamping", "value")
)
def oversamping_render(n_clicks, content, option):
    if n_clicks == None or content == None:
        raise PreventUpdate

    # test demo
    option = "slinear"
    test = Oversampling(content)
    x, y = test.get_oversamping_data(content, option)

    data = [{
        "x" : x,
        "y" : y,
        "data_type" : "oversamping"
    }]

    print(type(data))
    return data



# ================ FT callback ===================


