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
from components.tab.tabs import afm_tabs_generate
from components.oversampling.oversampling import afm_oversampling_generate   # use for test
from components.loglinearswitch.axisSwitch import vertical_axis_swith

# import algorithm
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df
from algorithm.afm import afm_moduli_process, oversample_function

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
            dbc.Col([
                    afm_tabs_generate(prefix_app_name),
                    vertical_axis_swith(prefix_app_name)
                    ], width=True),
            ])

# ======upload callback========
@app.callback(
    Output("AFM-raw-data-store", "data"),  
    Output("AFM-ft-data-store", "data"),
    Output("AFM-loading-message", "children"),
    Input("AFM-upload", "contents"),
    Input("AFM-load-example", "n_clicks"),
    State("AFM-upload", "filename"),
    # TODO need change later
    State("AFM-r", "value"),
    State("AFM-v", "value"),
    State("AFM-load0", "value"),
    State("AFM-loadinf", "value"),
    State("AFM-indentation0", "value"),
    State("AFM-indentationinf", "value"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, file_name, r, v, l0, linf, ind0, indinf):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = pd.DataFrame()
    if button_id == "AFM-load-example":
        path = "test_data/AFM/Agarose_gel.txt"
        df = generate_df_from_local(path)
    else:
        df = generate_df(content)
    
    # save file_name and lens for message recovering when app changing
    data = {
        "x": df[0],
        "y": df[1],
        "z": df[2],
        "filename": file_name,
        "lines": len(df)
    }
    # default v = 0.5 & r(named δ actually)
    v = 0.5 if v is None else v
    r = 20 if r is None else r
    l0 = 1 if l0 is None else l0
    linf = 0 if linf is None else linf
    ind0 = 1 if ind0 is None else ind0
    indinf = 0 if indinf is None else indinf

    omega, g_p, g_pp = afm_moduli_process(df, r, v, l0, linf, ind0, indinf, False)

    ft_data = {
        "x1": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return data, ft_data, ""


@app.callback(
    # Output("AFM-oversampling-data-store", "data"),
    Output("AFM-oversampled-ft-data-store", "data"),
    Input("AFM-oversampling-btn", "n_clicks"),
    State("AFM-r", "value"),
    State("AFM-v", "value"),
    State("AFM-load0", "value"),
    State("AFM-loadinf", "value"),
    State("AFM-indentation0", "value"),
    State("AFM-indentationinf", "value"),
    State("AFM-raw-data-store", "data"),
    State("AFM-oversampling-input", "value")
)
def store_oversampling_data(n_clicks, r, v, l0, linf, ind0, indinf, data, ntimes):
    if n_clicks is None or data is None or ntimes is None:
        raise PreventUpdate

    # avoid float number
    ntimes = int(ntimes)
    df = convert_lists_to_df(data)
    # oversample force and identation data
    # x, y, z = oversample_function(df, ntimes)
    # ftdata = data
    v = 0.5 if v is None else v
    r = 20 if r is None else r
    l0 = 1 if l0 is None else l0
    linf = 0 if linf is None else linf
    ind0 = 1 if ind0 is None else ind0
    indinf = 0 if indinf is None else indinf
    
    omega, g_p, g_pp = afm_moduli_process(df, r, v, l0, linf, ind0, indinf, True, ntimes)

    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return oversampled_ft_data


# =================== Download Callback =====================
@app.callback(
    Output("AFM-download-text", "data"),
    Output("AFM-download-message", "children"),
    Input("AFM-download-btn", "n_clicks"),
    State("AFM-begin-line-number", "value"),
    State("AFM-end-line-number", "value"),
    State("AFM-oversampled-ft-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, beginLineIdx, endLineIdx, data):
    if data is None:
        raise PreventUpdate

    # avoid float number
    beginLineIdx = int(beginLineIdx)
    endLineIdx = int(endLineIdx)
    if beginLineIdx >= endLineIdx:
        return None, "Invaild parameters"

    try:
        saving_x_list = data.get("x")[beginLineIdx:endLineIdx+1]
        saving_y_list = data.get("y1")[beginLineIdx:endLineIdx+1]
        saving_z_list = data.get("y2")[beginLineIdx:endLineIdx+1]
    except:
        # if the idx is out of range, say, endLineIdx > len(x)
        saving_x_list = data.get("x")[beginLineIdx:]
        saving_y_list = data.get("y1")[beginLineIdx:]
        saving_z_list = data.get("y2")[beginLineIdx:]
    else:
        saving_df = pd.DataFrame({"x": saving_x_list, "y1": saving_y_list, "y2": saving_z_list})
        saving_file_name = "download_AFM_data.txt"

    return (dcc.send_data_frame(saving_df.to_csv, saving_file_name, 
                                header=False, index=False, 
                                sep='\t', encoding='utf-8'), 
                                "Download OK !") 


# =================== Clientside callback ===================

# ouput force fig
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideAfm",
        function_name="tabChangeForRender"
    ),
    Output("AFM-Force-display", "figure"),
    Input("AFM-raw-data-store", "data"),
    # Input("AFM-oversampling-data-store", "data"),
    # Input("AFM-oversampling-render-switch", "value"),
)

# output identation fig
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideAfm",
        function_name="tabChangeIdeRender"
    ),
    Output("AFM-Indentation-display", "figure"),
    Input("AFM-raw-data-store", "data"),
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideAfm",
        function_name="tabChangeFunRender"
    ),
    Output("AFM-Classic-Moduli-display", "figure"),
    Input("AFM-ft-data-store", "data"),
    Input("AFM-oversampled-ft-data-store", "data"),
    Input("AFM-oversampling-render-switch", "value"),
    Input("AFM-vertical-axis-switch", "value"),
    # prevent_initial_call=True
)

app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMessageRec",
        function_name="uploadMessage"
    ),
    Output("AFM-upload-message", "children"),
    Input("AFM-raw-data-store", "data"),
    # prevent_initial_call=True
)

