import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

from app import app

# import components
from components.upload.upload import Upload
from components.download.download import Download
from components.oversampling.oversampling import Oversampling
from components.tab.tabs import Tabs
from components.display.loading import Loading
from components.inputgdot.inputgdot import Inputgdot

# import algorithm
from algorithm.oversample import get_oversampling_data
from algorithm.read_data import generate_df
from algorithm.pwft import ftdata

prefix_app_name = "MOT"

Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        Upload, 
                        dcc.Store(id="raw-data-store"),
                        dcc.Store(id="oversampling-data-store"),
                        dcc.Store(id="ft-data-store"),
                        dcc.Loading(dcc.Store(id="oversampled-ft-data-store"),
                                    id="full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="upload-message"),
                    html.Hr(),
                    html.Div([
                        # html.H5("Example data"),
                    ]),
                    html.Hr(),
                    Oversampling,
                    html.Hr(),
                    Download
                    ], width=3), 
            dbc.Col(Tabs, width=True),
            Loading
])

