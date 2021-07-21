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
prefix_app_name = "FTAPP"

# TODO need modify and change the algorithm plus with function
Layout = dbc.Row([
            dbc.Col([
                    html.Div([
                        html.H5("Support .txt"),
                        upload_component_generate("FTAPP-upload"),
                        html.Div(id="FTAPP-upload-message"),
                        dcc.Store(id="FTAPP-raw-data-store"),
                        dcc.Store(id="FTAPP-oversampling-data-store"),
                        dcc.Store(id="FTAPP-FT-data-store")
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Example data"),
                        dbc.Button("Load Example data", id="FTAPP-load-example", 
                                   color="primary", style={"margin": "5px"})
                    ]),
                    html.Hr(),
                    oversampling_component_generate(prefix_app_name),
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
    Output("FTAPP-upload-message", "children"),
    Input("FTAPP-upload", "contents"),
    State("FTAPP-upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, file_name):
    # df = generate_df(content)

    data = {
        "x" : [1, 2, 3],
        "y" : [1, 2, 3],
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

    return (dcc.send_data_frame(saving_df.to_csv, "data.txt", 
                                header=False, index=False, 
                                sep='\t', encoding='utf-8'), 
                                "Download OK !") 

