import collections
from datetime import date
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
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
from algorithm.oversample import get_oversamping_data
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
def store_raw_data(content, file_name):
    df = generate_df(content)

    data = {
        "x" : df[0],
        "y" : df[1],
    }

    upload_messge = "The upload file {} with {} lines".format(file_name, len(df))

    return data, upload_messge

@app.callback(
    Output("oversamping-data-store", "data"),
    Input("oversamping-btn", "n_clicks"),
    State("upload", "contents"),
    State("oversamping-input", "value")
)
def store_oversamping_data(n_clicks, content, ntimes):
    if n_clicks is None or content is None or ntimes is None:
        raise PreventUpdate

    # avoid floor number
    ntimes = int(ntimes)
    x, y = get_oversamping_data(content=content, ntimes=ntimes)

    data = {
        "x" : x,
        "y" : y,
    }

    return data

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideSigma",
        function_name="tabChangeFigRender"
    ),
    Output("sigma-display", "figure"),
    Input("raw-data-store", "data"),
    Input("oversamping-data-store", "data"),
    Input("oversamping-render-switch", "value"),
    prevent_initial_call=True
)

# ================ FT callback ========================

