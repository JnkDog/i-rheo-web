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
from components.oversampling.oversampling import oversampling_component_generate
from components.tab.tabs import tabs_component_generate

# import algorithm
from algorithm.oversample import get_oversampling_data
from algorithm.read_data import generate_df, generate_df_from_local
from algorithm.pwft import ftdata

# Using your own app name. Can't be same.
prefix_app_name = "MOT"

Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        upload_component_generate("MOT-upload"), 
                        dcc.Store(id="MOT-raw-data-store", storage_type="session"),
                        dcc.Store(id="MOT-oversampling-data-store", storage_type="session"),
                        dcc.Store(id="MOT-ft-data-store", storage_type="session"),
                        dcc.Loading(dcc.Store(id="MOT-oversampled-ft-data-store", 
                                              storage_type="session"),
                                    id="MOT-full-screen-mask",
                                    fullscreen=True)
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="MOT-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    html.Div(id="MOT-upload-message"),
                    # This is just for show the loading message
                    html.Div(id="MOT-loading-message"),
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
    Output("MOT-raw-data-store", "data"),  
    Output("MOT-ft-data-store", "data"),
    # Output("upload-message", "children"),
    Output("MOT-loading-message", "children"),
    Input("MOT-upload", "contents"),
    Input("MOT-load-example", "n_clicks"),
    # The g_0 and g_inf are not used ... 
    Input("MOT-g_0", "value"),
    Input("MOT-g_inf", "value"),
    State("MOT-upload", "filename"),
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
    Output("MOT-oversampling-data-store", "data"),
    Output("MOT-oversampled-ft-data-store", "data"),
    Input("MOT-oversampling-btn", "n_clicks"),
    State("MOT-g_0", "value"),
    State("MOT-g_inf", "value"),
    State("MOT-upload", "contents"),
    State("MOT-oversampling-input", "value")
)
def store_oversampling_data(n_clicks, g_0, g_inf, content, ntimes):
    if n_clicks is None or content is None or ntimes is None:
        raise PreventUpdate

    # avoid floor number
    ntimes = int(ntimes)
    x, y = get_oversampling_data(content=content, ntimes=ntimes)

    data = {
        "x": x,
        "y": y,
    }

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else int(g_0)
    g_inf = 0 if g_inf is None else int(g_inf)

    df = generate_df(content)
    
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
    Output("MOT-download-text", "data"),
    Output("MOT-download-message", "children"),
    Input("MOT-download-btn", "n_clicks"),
    State("MOT-begin-line-number", "value"),
    State("MOT-end-line-number", "value"),
    State("MOT-oversampling-data-store", "data"),
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

    return (dcc.send_data_frame(saving_df.to_csv, "data.txt", 
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
    Output("MOT-sigma-display", "figure"),
    Input("MOT-raw-data-store", "data"),
    Input("MOT-oversampling-data-store", "data"),
    Input("MOT-oversampling-render-switch", "value"),
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
    Output("MOT-FT-display", "figure"),
    Input("MOT-ft-data-store", "data"),
    Input("MOT-oversampled-ft-data-store", "data"),
    Input("MOT-oversampling-render-switch", "value"),
    # prevent_initial_call=True
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMessageRec",
        function_name="uploadMessage"
    ),
    Output("MOT-upload-message", "children"),
    Input("MOT-raw-data-store", "data"),
    # prevent_initial_call=True
)

# ================ Loading mask ========================

# @app.callback(
#     Output("loading-test", "children"),
#     Input("begin-line-number", "value"),
#     prevent_initial_call=True,
# )
# def loading_test(number):
#     time.sleep(30)
#     return number

