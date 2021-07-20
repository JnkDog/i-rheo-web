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
from algorithm.oversample import Oversampling
from algorithm.read_data import generate_df
from algorithm.pwft import ftdata

Layout = dbc.Row([
            dbc.Col([
                    html.Div([
                        html.H5("Support .txt"),
                        Upload,
                        html.Div(id="upload-message"),
                        dcc.Store(id="raw-data-store"),
                        dcc.Store(id="oversamping-data-store"),
                        dcc.Store(id="ft-data-store"),
                        dcc.Store(id="oversampled-ft-data-store")
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
    Output("ft-data-store", "data"),
    Input("upload", "contents"),
    State("upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, file_name):
    df = generate_df(content)

    data = {
        "x": df[0],
        "y": df[1],
    }
    omega, g_p, g_pp = ftdata(df, False)
    ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    upload_messge = "The upload file {} with {} lines".format(file_name, len(df))

    return data, upload_messge, ft_data

@app.callback(
    Output("oversamping-data-store", "data"),
    Output("oversampled-ft-data-store", "data"),
    Input("oversamping-btn", "n_clicks"),
    State("upload", "contents"),
    State("oversamping-input", "value")
)
def store_oversamping_data(n_clicks, content, oversamping_number):
    if n_clicks is None or content is None or oversamping_number is None:
        raise PreventUpdate

    # test demo
    option = "slinear"
    test = Oversampling(content)
    x, y = test.get_oversamping_data(content, option)

    data = {
        "x": x,
        "y": y,
    }
    df = generate_df(content)
    omega, g_p, g_pp = ftdata(df, True, oversamping_number)
    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }
    return data, oversampled_ft_data


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
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideFT",
        function_name="tabChangeFigRender"
    ),
    Output("FT-display", "figure"),
    Input("ft-data-store", "data"),
    Input("oversampled-ft-data-store", "data"),
    Input("oversamping-render-switch", "value"),
    prevent_initial_call=True
)
