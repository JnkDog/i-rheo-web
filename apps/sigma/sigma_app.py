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
                        dcc.Store(id="oversamping-data-store"),
                        dcc.Store(id="FT-data-store")
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
            # console.log(oversampingData)
            data = oversampingData;
        } else {
            console.log("========= in sigma =============")
            # console.log(rawData)
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

    return data

# ================ FT callback ========================