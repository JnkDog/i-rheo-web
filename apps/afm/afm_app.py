import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

from app import app

# import components and its generation
from components.upload.upload import upload_component_generate
from components.download.download import download_component_generate

# import algorithm
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df

prefix_app_name = "AFM"

Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        upload_component_generate("AFM-upload"), 
                        dcc.Store(id="AFM-raw-data-store", storage_type="session"),
                        dcc.Store(id="AFM-oversampling-data-store", storage_type="session"),
                        dcc.Store(id="AFM-ft-data-store", storage_type="session"),
                        dcc.Loading(dcc.Store(id="AFM-oversampled-ft-data-store", storage_type="session"),
                                    id="full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="AFM-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="AFM-upload-message"),
                    html.Div(id="AFM-loading-message"),
                    html.Hr(),
                    afm_oversampling_generate(prefix_app_name),
                    html.Hr(),
                    download_component_generate(prefix_app_name)
                    ], width=3), 
            dbc.Col(Tabs, width=True),
])

