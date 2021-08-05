from algorithm.oversample import get_oversampling_data
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

# import algorithm
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df
from algorithm.pwft import ftdata

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
                        dcc.Store(id="BULKAPP-FT-data-store"),
                        dcc.Loading(dcc.Store(id="BULKAPP-oversampled-ft-data-store", 
                                              storage_type="session"),
                                    id="full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="BULKAPP-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="BULKAPP-upload-message"),
                    # This is just for show the loading message
                    html.Div(id="BULKAPP-loading-message"),
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
    Output("BULKAPP-raw-data-store", "data"),
    # Output("BULKAPP-upload-message", "children"),
    Output("BULKAPP-loading-message", "children"),
    Input("BULKAPP-upload", "contents"),
    Input("BULKAPPload-example", "n_clicks"),
    State("BULKAPP-g_0", "value"),
    State("BULKAPP-g_inf", "value"),
    State("BULKAPP-upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks,  g_0, g_inf, file_name):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = pd.DataFrame()
    if button_id == "load-example":
        path = "./example_data/bulk/example.txt"
        df = generate_df_from_local(path)
    else:
        df = generate_df(content)

    data = {
        "x": df[0],
        "y": df[1],
        "z": df[2],
        "filename": file_name,
        "lines": len(df)
    }

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else int(g_0)
    g_inf = 0 if g_inf is None else int(g_inf)

    omega, g_p, g_pp = ftdata(df, g_0, g_inf, False)

    ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    """
    Don't pass any string to this return. This component only for loading message.
    """
    return data, ft_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("BULKAPP-oversampling-data-store", "data"),
    Output("BULKAPP-oversampled-ft-data-store", "data"),
    Input("BULKAPP-oversampling-btn", "n_clicks"),
    State("BULKAPP-g_0", "value"),
    State("BULKAPP-g_inf", "value"),
    State("BULKAPP-raw-data-store", "data"),
    State("BULKAPP-oversampling-input", "value")
)
def store_oversampling_data(n_clicks, g_0, g_inf, data, ntimes):
    if n_clicks is None or data is None or ntimes is None:
        raise dash.exceptions.PreventUpdate

    # avoid float number
    ntimes = int(ntimes)    
    df = convert_lists_to_df(data)
    x, y = get_oversampling_data(df, ntimes)
    # x, y = get_oversampling_data(content=content, ntimes=ntimes)

    data = {
        "x" : x,
        "y" : y,
    }

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else int(g_0)
    g_inf = 0 if g_inf is None else int(g_inf)
    
    # This function takes lots of time
    omega, g_p, g_pp = ftdata(df, g_0, g_inf, True, ntimes)

    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return data, oversampled_ft_data

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

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMessageRec",
        function_name="uploadMessage"
    ),
    Output("BULKAPP-upload-message", "children"),
    Input("BULKAPP-raw-data-store", "data"),
    # prevent_initial_call=True
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

    # avoid float number
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

