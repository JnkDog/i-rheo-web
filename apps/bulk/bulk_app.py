import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

# import components
from components.upload.upload import upload_component_generate
from components.download.download import download_component_generate
from components.oversampling.oversampling import oversampling_component_generate
from components.tab.tabs import tabs_component_generate
from components.display.loading import Loading

"""
The orginal version is the i-Rheo virtual instrument (VI) LABVIEW.
"""

# Using your own app name. Can't be same.
prefix_app_name = "BULKAPP"

# TODO need modify and change the algorithm plus with function
Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        upload_component_generate("BULKAPP-upload"),
                        dcc.Store(id="BULKAPP-raw-data-store"),
                        dcc.Store(id="BULKAPP-oversampling-data-store"),
                        dcc.Store(id="BULKAPP-FT-data-store")
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="BULKAPP-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="BULKAPP-upload-message"),
                    html.Hr(),
                    oversampling_component_generate(prefix_app_name),
                    html.Hr(),
                    html.Div([
                        dbc.Button("Divide by 100", id="BULKAPP-divide-example", 
                                   color="primary", style={"margin": "5px"}),
                        dbc.Button("Use slope", id="BULKAPP-slope-example", 
                                   color="primary", style={"margin": "5px"}),           
                    ], className="btn-group me-2"),
                    html.Div([
                        dbc.Input(id="BULKAPP-strain-input"),
                        dbc.Button("Strain con", id="BULKAPP-strain-example", 
                                   color="primary", className="ml-2")], 
                        className="input-group", style={"width": "300px"}),
                    html.Div([
                        dbc.Input(id="BULKAPP-fixed-input"),
                        dbc.Button("Fixed x", id="BULKAPP-fixed-example", 
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
    Output("BULKAPP-raw-data-store", "data"),
    Output("BULKAPP-upload-message", "children"),
    Input("BULKAPP-upload", "contents"),
    State("BULKAPP-upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, file_name):
    # df = generate_df(content)

    data = {
        "x": [i for i in range(0, 50)],
        "y": [i for i in range(0, 50)],
        "z": [i for i in range (50, 100)],
        "file_name": file_name
    }

    # original 
    # upload_messge = "The upload file {} with {} lines".format(file_name, len(df))
    upload_messge = "The upload file {} with {} lines".format(file_name, 1)

    return data, upload_messge

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-btn", "n_clicks"),
    State("BULKAPP-upload", "contents"),
    State("BULKAPP-oversampling-input", "value")
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
    Output("BULKAPP-sigma-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
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
    Output("BULKAPP-gamma-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
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
    Output("BULKAPP-eta-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
    prevent_initial_call=True
)

# ================ Download callback ========================

@app.callback(
    Output("BULKAPP-download-text", "data"),
    Output("BULKAPP-download-message", "children"),
    Input("BULKAPP-download-btn", "n_clicks"),
    State("BULKAPP-begin-line-number", "value"),
    State("BULKAPP-end-line-number", "value"),
    State("BULKAPP-oversampling-data-store", "data"),
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

