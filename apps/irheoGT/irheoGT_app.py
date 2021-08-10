import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from enum import Enum, unique

from app import app

# import components
from components.upload.upload import Upload
from components.download.download import Download
# from components.oversampling.oversampling import Oversampling
from components.oversampling.oversampling import oversampling_component_generate
from components.tab.tabs import Tabs
from components.display.loading import Loading
from components.inputgdot.inputgdot import Inputgdot
from components.loglinearswitch.axisSwitch import vertical_axis_swith

# import algorithm
from algorithm.oversample import get_oversampling_data
from algorithm.read_data import generate_df, generate_df_from_local
from algorithm.pwft import fast_ftdata
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df

# Selection options
@unique
class DOWNLOAD_OPTIONS(Enum):
    OVERSAMPLED_RAW_DATA = 0
    FT_RAW_DATA = 1
    FT_OVERSAMPLED_DATA = 2


prefix_app_name = "GT"

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
                    oversampling_component_generate(prefix_app_name),
                    html.Hr(),
                    Download
                    ], width=3), 
            dbc.Col([
                    Tabs,
                    vertical_axis_swith("GT")],
                    width=True),
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
    State("GT-g_0", "value"),
    State("GT-g_inf", "value"),
    State("GT-oversampling-Nf", "value"),
    State("upload", "filename"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, g_0, g_inf, N_f, file_name):
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
    g_0 = 1 if g_0 is None else float(g_0)
    g_inf = 0 if g_inf is None else float(g_inf)
    N_f = 100 if N_f is None else int(N_f)

    # slow FT 
    # omega, g_p, g_pp = ftdata(df, g_0, g_inf, False)
    # fast FT
    omega, g_p, g_pp, _, _ = fast_ftdata(df, g_0, g_inf, N_f, False)

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
    Input("GT-oversampling-btn", "n_clicks"),
    State("GT-g_0", "value"),
    State("GT-g_inf", "value"),
    State("raw-data-store", "data"),
    # State("ft-data-store", "data"),
    State("GT-oversampling-input", "value"),
    State("GT-oversampling-Nf", "value"),
)
def store_oversampling_data(n_clicks, g_0, g_inf, data, ntimes, N_f):
    if n_clicks is None or data is None or ntimes is None:
        raise PreventUpdate

    df = convert_lists_to_df(data)

    # avoid float number
    ntimes = int(ntimes)
    N_f = 100 if N_f is None else int(N_f)
    x, y = get_oversampling_data(df, ntimes=ntimes)

    data = {
        "x": x,
        "y": y,
    }

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else float(g_0)
    g_inf = 0 if g_inf is None else float(g_inf)
    
    # This function takes lots of time
    # omega, g_p, g_pp = ftdata(df, g_0, g_inf, True, ntimes)
    # fast FT
    omega, g_p, g_pp, _, _ = fast_ftdata(df, g_0, g_inf, N_f, True, ntimes)

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
    State("downlaod-selection", "value"),
    State("raw-data-store", "data"),
    State("oversampling-data-store", "data"),
    State("ft-data-store", "data"),
    State("oversampled-ft-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, option, raw_data, oversampled_raw_data, ft_raw_data, ft_oversampled_data):
    if option is None or raw_data is None:
        raise PreventUpdate

    # Covert the option from string to int
    option = int(option)
    file_suffix_name = raw_data.get("filename")
    saved_file_name = ""
    saved_data_df = pd.DataFrame()

    if option == DOWNLOAD_OPTIONS.OVERSAMPLED_RAW_DATA.value \
        and oversampled_raw_data is not None:
        saved_file_name = "Oversampled_raw_data_" + file_suffix_name
        saved_data_df = pd.DataFrame(oversampled_raw_data)
    elif option == DOWNLOAD_OPTIONS.FT_RAW_DATA.value \
        and ft_raw_data is not None:
        saved_file_name = "FT_raw_data_" + file_suffix_name
        saved_data_df = pd.DataFrame(ft_raw_data)
    elif option == DOWNLOAD_OPTIONS.FT_OVERSAMPLED_DATA.value \
        and ft_oversampled_data is not None:
        saved_file_name = "FT_oversampled_data_" + file_suffix_name
        saved_data_df = pd.DataFrame(ft_oversampled_data)
    else:
        return None, "No data available!"

    return (dcc.send_data_frame(saved_data_df.to_csv, saved_file_name, 
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
    Input("GT-oversampling-render-switch", "value"),
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
    Input("GT-oversampling-render-switch", "value"),
    Input("GT-vertical-axis-switch", "value"),
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

