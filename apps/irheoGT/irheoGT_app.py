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
from algorithm.read_data import generate_df, generate_df_from_local
from algorithm.pwft import ftdata
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df

Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        Upload, 
                        dcc.Store(id="raw-data-store", storage_type="session"),
                        dcc.Store(id="oversampling-data-store", storage_type="session"),
                        dcc.Store(id="ft-data-store", storage_type="session"),
                        dcc.Loading(dcc.Store(id="oversampled-ft-data-store", 
                                              storage_type="session"),
                                    id="full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="upload-message"),
                    # This is just for show the loading message
                    html.Div(id="loading-message"),
                    html.Hr(),
                    Oversampling,
                    html.Hr(),
                    Download
                    ], width=3), 
            dbc.Col(Tabs, width=True),
            Loading
])

# ================ Upload callback ========================

"""
Trigger when the experiental data(raw data) uploaded  
"""
@app.callback(
    Output("raw-data-store", "data"),  
    Output("ft-data-store", "data"),
    # Output("upload-message", "children"),
    Output("loading-message", "children"),
    Input("upload", "contents"),
    Input("load-example", "n_clicks"),
    # The g_0 and g_inf are not used ... 
    State("g_0", "value"),
    State("g_inf", "value"),
    State("upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, g_0, g_inf, file_name):
    # Deciding which raw_data used according to the ctx
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = pd.DataFrame()
    if button_id == "load-example":
        path = "example_data/SingExp6_5.txt"
        df = generate_df_from_local(path)
    else:
        df = generate_df(content)
    
    # save file_name and lens for message recovering when app changing
    data = {
        "x": df[0],
        "y": df[1],
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

    # upload_messge = "The upload file {} with {} lines".format(file_name, len(df))

    # return data, upload_messge, ft_data
    return data, ft_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("oversampling-data-store", "data"),
    Output("oversampled-ft-data-store", "data"),
    Input("oversampling-btn", "n_clicks"),
    State("g_0", "value"),
    State("g_inf", "value"),
    State("raw-data-store", "data"),
    # State("ft-data-store", "data"),
    State("oversampling-input", "value")
)
def store_oversampling_data(n_clicks, g_0, g_inf, data, ntimes):
    if n_clicks is None or ntimes is None:
        raise PreventUpdate

    df = pd.DataFrame()
    if data is None:
        path = "example_data/SingExp6_5.txt"
        df = generate_df_from_local(path)
    else:
        df = convert_lists_to_df(data)

    # avoid floor number
    ntimes = int(ntimes)
    x, y = get_oversampling_data(df, ntimes=ntimes)

    data = {
        "x": x,
        "y": y,
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

# ================ Download callback ========================

@app.callback(
    Output("download-text", "data"),
    Output("download-message", "children"),
    Input("download-btn", "n_clicks"),
    State("begin-line-number", "value"),
    State("end-line-number", "value"),
    State("oversampling-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, beginLineIdx, endLineIdx, data):
    if data is None:
        raise PreventUpdate

    # avoid floor number
    beginLineIdx = int(beginLineIdx)
    endLineIdx = int(endLineIdx)
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
        saving_file_name = "download_GT_data.txt"

    return (dcc.send_data_frame(saving_df.to_csv, saving_file_name, 
                                header=False, index=False, 
                                sep='\t', encoding='utf-8'), 
                                "Download OK !") 

# =================== Clientside callback ===================

"""
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideSigma",
        function_name="tabChangeFigRender"
    ),
    Output("sigma-display", "figure"),
    Input("raw-data-store", "data"),
    Input("oversampling-data-store", "data"),
    Input("oversampling-render-switch", "value"),
    # Due to the dcc.Stroe's storage_type is session
    # if prevent_initial_call=True, the fig cannot show
    # prevent_initial_call=True
)

# add to the js part and data store part
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideFT",
        function_name="tabChangeFigRender"
    ),
    Output("FT-display", "figure"),
    Input("ft-data-store", "data"),
    Input("oversampled-ft-data-store", "data"),
    Input("oversampling-render-switch", "value"),
    # prevent_initial_call=True
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMessageRec",
        function_name="uploadMessage"
    ),
    Output("upload-message", "children"),
    Input("raw-data-store", "data"),
    # prevent_initial_call=True
)

