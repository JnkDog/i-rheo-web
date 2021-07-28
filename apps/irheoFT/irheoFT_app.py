import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

# import components and its generation
from components.upload.upload import upload_component_generate
from components.download.download import download_component_generate
from components.oversampling.oversampling import oversampling_component_generate
from components.tab.tabs import tabs_component_generate

# import algorithm
from algorithm.oversample import get_oversampling_data
from algorithm.read_data import generate_df, generate_df_from_local
from algorithm.pwft import ftdata

"""
The orginal version is the i-Rheo virtual instrument (VI) LABVIEW.
"""

# Using your own app name. Can't be same.
prefix_app_name = "FTAPP"

# TODO need modify and change the algorithm plus with function
Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        upload_component_generate("FTAPP-upload"),
                        dcc.Store(id="FTAPP-raw-data-store", storage_type="session"),
                        dcc.Store(id="FTAPP-oversampling-data-store", storage_type="session"),
                        dcc.Store(id="FTAPP-FT-data-store", storage_type="session"),
                        dcc.Loading(dcc.Store(id="FTAPP-oversampled-ft-data-store", 
                                              storage_type="session"),
                                    id="full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="FTAPP-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="FTAPP-upload-message"),
                    # This is just for show the loading message
                    html.Div(id="FTAPP-loading-message"),
                    html.Hr(),
                    oversampling_component_generate(prefix_app_name),
                    html.Hr(),
                    html.Div([
                        dbc.Button("Divide by 100", id="FTAPP-divide-example", 
                                   color="primary", style={"margin": "5px"}),
                        dbc.Button("Use slope", id="FTAPP-slope-example", 
                                   color="primary", style={"margin": "5px"}),           
                    ], className="btn-group me-2"),
                    html.Div([
                        dbc.Input(id="FTAPP-strain-input"),
                        dbc.Button("Strain con", id="FTAPP-strain-example", 
                                   color="primary", className="ml-2")], 
                        className="input-group", style={"width": "300px"}),
                    html.Div([
                        dbc.Input(id="FTAPP-fixed-input"),
                        dbc.Button("Fixed x", id="FTAPP-fixed-example", 
                                color="primary", className="ml-2", style={"width": "99.84px"})], 
                        className="input-group mt-2", style={"width": "300px"}),
                    html.Hr(),
                    download_component_generate(prefix_app_name)
                    ], width=3), 
            dbc.Col(tabs_component_generate(prefix_app_name), width=True),
            # Loading
])

# ================ Upload callback ========================

"""
Trigger when the experiental data(raw data) uploaded  
"""
@app.callback(
    Output("FTAPP-raw-data-store", "data"),
    # Output("FTAPP-upload-message", "children"),
    Output("FTAPP-loading-message", "children"),
    Input("FTAPP-upload", "contents"),
    Input("FTAPP-load-example", "n_clicks"),
    State("FTAPP-upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, file_name):
    # df = generate_df(content)
    # Deciding which raw_data used according to the ctx 
    # ctx = dash.callback_context
    # button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # df = pd.DataFrame()
    # if button_id == "load-example":
    #     path = "xxx"
    #     df = generate_df_from_local(path)
    # else:
    #     df = generate_df(content)

    raw_data = {
        "x": [i for i in range(0, 50)],
        "y": [i for i in range(0, 50)],
        "z": [i for i in range (50, 100)],
        "file_name": file_name,
        "lines": 10
    }

    # save file_name and lens for message recovering when app changing
    # data = {
    #     "x": df[0],
    #     "y": df[1],
    #     "filename": file_name,
    #     "lines": len(df)
    # }

    # original 
    # upload_messge = "The upload file {} with {} lines".format(file_name, len(df))
    # upload_messge = "The upload file {} with {} lines".format(file_name, 1)
    
    """
    Don't pass any string to this return. This component only for loading message.
    """
    return raw_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("FTAPP-oversampling-data-store", "data"),
    Input("FTAPP-oversampling-btn", "n_clicks"),
    State("FTAPP-upload", "contents"),
    State("FTAPP-oversampling-input", "value")
)
def store_oversampling_data(n_clicks, content, ntimes):
    if n_clicks is None or content is None or ntimes is None:
        raise dash.exceptions.PreventUpdate

    # avoid floor number
    ntimes = int(ntimes)
    # x, y = get_oversampling_data(content=content, ntimes=ntimes)

    data = {
        "x" : [1],
        "y" : [1],
    }

    return data

"""
Sigma Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideSigma",
        function_name="tabChangeFigRender"
    ),
    Output("FTAPP-sigma-display", "figure"),
    Input("FTAPP-raw-data-store", "data"),
    Input("FTAPP-oversampling-data-store", "data"),
    Input("FTAPP-oversampling-render-switch", "value"),
    prevent_initial_call=True
)

"""
Gamma Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideGamma",
        function_name="tabChangeFigRender"
    ),
    Output("FTAPP-gamma-display", "figure"),
    Input("FTAPP-raw-data-store", "data"),
    Input("FTAPP-oversampling-data-store", "data"),
    Input("FTAPP-oversampling-render-switch", "value"),
    prevent_initial_call=True
)

"""
Eta Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideEta",
        function_name="tabChangeFigRender"
    ),
    Output("FTAPP-eta-display", "figure"),
    Input("FTAPP-raw-data-store", "data"),
    Input("FTAPP-oversampling-data-store", "data"),
    Input("FTAPP-oversampling-render-switch", "value"),
    prevent_initial_call=True
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMessageRec",
        function_name="uploadMessage"
    ),
    Output("FTAPP-upload-message", "children"),
    Input("FTAPP-raw-data-store", "data"),
    # prevent_initial_call=True
)

# ================ Download callback ========================

@app.callback(
    Output("FTAPP-download-text", "data"),
    Output("FTAPP-download-message", "children"),
    Input("FTAPP-download-btn", "n_clicks"),
    State("FTAPP-begin-line-number", "value"),
    State("FTAPP-end-line-number", "value"),
    State("FTAPP-oversampling-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, beginLineIdx, endLineIdx, data):
    if data is None:
        raise dash.exceptions.PreventUpdate

    # avoid floor number
    beginLineIdx = int(beginLineIdx)
    endLineIdx   = int(endLineIdx)
    if beginLineIdx >= endLineIdx:
        return None, "Invaild parameters"

    try:
        saving_x_list = data.get("x")[beginLineIdx:endLineIdx+1]
        saving_y_list = data.get("y")[beginLineIdx:endLineIdx+1]
    except:
        # if the idx is out of range, say, endLineIdx > len(x)
        saving_x_list = data.get("x")[beginLineIdx:]
        saving_y_list = data.get("y")[beginLineIdx:]
    else:
        saving_df = pd.DataFrame({"x": saving_x_list, "y": saving_y_list})
        saving_file_name = data.get("file_name") + "_Complex Moduli.txt"

    return (dcc.send_data_frame(saving_df.to_csv,saving_file_name, 
                                header=False, index=False, 
                                sep='\t', encoding='utf-8'), 
                                "Download OK !") 

