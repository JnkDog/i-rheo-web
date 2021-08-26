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
from components.oversampling.oversampling import afm_oversampling_generate, oversampling_control  # use for test
from components.loglinearswitch.axisSwitch import vertical_axis_swith

# import algorithm
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df, replace_dict_value
from algorithm.afm import afm_moduli_process, afm_rawdata_oversampling
from algorithm.saving_process import combine_as_complex, six_decimal_saving

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
    State("AFM-refresh-btn", "n_clicks"),
    State("AFM-upload", "filename"),
    # TODO need change later
    State("AFM-r", "value"),
    State("AFM-v", "value"),
    State("AFM-load0", "value"),
    State("AFM-loadinf", "value"),
    State("AFM-indentation0", "value"),
    State("AFM-indentationinf", "value"),
    State("AFM-oversampling-Nf", "value"),
    State("AFM-raw-data-store", "value"),
    State("AFM-ft-data-store", "value"),
    prevent_initial_call=True
)
def store_raw_data(content, example_clicks, refresh_clicks, 
                    file_name, r, v, l0, linf, ind0, indinf, N_f, 
                    prev_raw_data, prev_ft_data):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # default v = 0.5 & r(named δ actually)
    v = 0.5 if v is None else v
    r = 20 if r is None else r
    l0 = 1 if l0 is None else l0
    linf = 0 if linf is None else linf
    ind0 = 1 if ind0 is None else ind0
    indinf = 0 if indinf is None else indinf
    N_f = 100 if N_f is None else int(N_f)

    df = pd.DataFrame()
    if button_id == "AFM-load-example":
        path = "test_rawdata/AFM/a.txt"
        df = generate_df_from_local(path)
        raw_data, ft_data = upload_local_data_workflow(df, file_name, r, v, l0, linf, ind0, indinf, N_f)

    elif button_id == "AFM-upload":
        df = generate_df(content)
        raw_data, ft_data = upload_local_data_workflow(df, file_name, r, v, l0, linf, ind0, indinf, N_f)

    elif button_id == "AFM-refresh-btn":
        if prev_raw_data is None:
            raise PreventUpdate
        else:
            df = convert_lists_to_df(prev_raw_data)
            replacement_elements = afm_moduli_process(df, r, v, l0, linf, ind0, indinf, N_f, False)
            raw_data = prev_raw_data
            replacement_keys = ["x", "y1", "y2"]
            ft_data = replace_dict_value(prev_ft_data, replacement_elements, replacement_keys)

    return raw_data, ft_data, ""


@app.callback(
    Output("AFM-raw-data-store", "data"),
    Output("AFM-oversampling-data-store", "data"),
    Output("AFM-oversampled-ft-data-store", "data"),
    Input("AFM-oversampling-btn", "n_clicks"),
    Input("AFM-refresh-btn", "n_clicks"),
    State("AFM-r", "value"),
    State("AFM-v", "value"),
    State("AFM-load0", "value"),
    State("AFM-loadinf", "value"),
    State("AFM-indentation0", "value"),
    State("AFM-indentationinf", "value"),
    State("AFM-raw-data-store", "data"),
    State("AFM-oversampling-input", "value"),
    State("AFM-oversampling-Nf", "value"),
    State("AFM-oversampling-data-store", "data"),
    State("AFM-oversampled-ft-data-store", "data"),
    prevent_initial_call=True
)
def store_oversampling_data(oversampling_clicks, refresh_clicks, 
                            r, v, l0, linf, ind0, indinf, raw_data, ntimes, N_f,
                            prev_oversampled_data, prev_oversampled_ft_data):
    if raw_data is None:
        raise PreventUpdate

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "FTAPP-refresh-btn":
        if prev_oversampled_data is None and prev_oversampled_ft_data is None:
            raise PreventUpdate
    
    ntimes = 10 if ntimes is None else int(ntimes)
    v = 0.5 if v is None else v
    r = 20 if r is None else r
    l0 = 1 if l0 is None else l0
    linf = 0 if linf is None else linf
    ind0 = 1 if ind0 is None else ind0
    indinf = 0 if indinf is None else indinf
    N_f = 100 if N_f is None else int(N_f)

    # df = convert_lists_to_df(raw_data)
    raw_data["step"] = "convert"
    # x, y, z = afm_rawdata_oversampling(df, ntimes)
    x, y, z = 1, 1, 1
    raw_data["step"] = "raw data oversampling finish"

    oversampled_data = {
        "x": x,
        "y": y,
        "z": z,
    }

    # omega, g_p, g_pp = afm_moduli_process(df, r, v, l0, linf, ind0, indinf, N_f, True, ntimes)
    omega, g_p, g_pp = 2, 2, 2
    raw_data["step"] = "ft data oversampling finish"

    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return raw_data, oversampled_data, oversampled_ft_data


# =================== Download Callback =====================
@app.callback(
    Output("AFM-download-text", "data"),
    Output("AFM-download-message", "children"),
    Input("AFM-download-btn", "n_clicks"),
    State("AFM-begin-line-number", "value"),
    State("AFM-end-line-number", "value"),
    State("AFM-oversampled-ft-data-store", "data"),
    State("FTAPP-raw-data-store", "data"),
    State("FTAPP-oversampled-ft-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, raw_data, oversampled_ft_data):
    if oversampled_ft_data is None:
        return None, "No oversampled data available!"

    file_suffix_name = raw_data.get("filename")
    saved_file_name = "AFM_oversampled_" + file_suffix_name

    complex_list = combine_as_complex(
            oversampled_ft_data["y1"],
            oversampled_ft_data["y2"]
        )

    saved_data_df = pd.DataFrame(six_decimal_saving({
        "x": oversampled_ft_data["x"],
        "y": complex_list
    }))
    return (dcc.send_data_frame(saved_data_df.to_csv, saved_file_name, 
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
    Input("AFM-oversampling-data-store", "data"),
    Input("AFM-oversampling-render-switch", "value"),
)

# output identation fig
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideAfm",
        function_name="tabChangeIdeRender"
    ),
    Output("AFM-Indentation-display", "figure"),
    Input("AFM-raw-data-store", "data"),
    Input("AFM-oversampling-data-store", "data"),
    Input("AFM-oversampling-render-switch", "value"),
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

def upload_local_data_workflow(df, file_name, r, v, l0, linf, ind0, indinf, N_f):
    # save file_name and lens for message recovering when app changing
    raw_data = {
        "x": df[0],
        "y": df[1],
        "z": df[2],
        "filename": file_name,
        "lines": len(df),
        "step": "raw",
    }

    # fast FT processing
    omega, g_p, g_pp = afm_moduli_process(df, r, v, l0, linf, ind0, indinf, N_f, False)

    ft_data = {
        "x1": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return raw_data, ft_data
