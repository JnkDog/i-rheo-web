import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
from enum import Enum, unique

from app import app

# import components and its generation
from components.upload.upload import upload_component_generate
from components.download.download import download_component_generate
from components.oversampling.oversampling import oversampling_component_generate
from components.tab.tabs import ft_tabs_generate
from components.loglinearswitch.axisSwitch import vertical_axis_swith

# import algorithm
from algorithm.oversample import get_oversampling_data
from algorithm.read_data import convert_lists_to_df, generate_df, generate_df_from_local, replace_dict_value
from algorithm.pwft import fast_ftdata
from algorithm.saving_process import combine_as_complex, six_decimal_saving

# Using your own app name. Can't be same.
prefix_app_name = "FTAPP"

# Selection options
@unique
class DOWNLOAD_OPTIONS(Enum):
    OVERSAMPLED_RAW_DATA  = 0
    FT_RAW_DATA = 1
    FT_OVERSAMPLED_DATA = 2

@unique
class TIME_DERIVATED(Enum):
    NONTIME_DERIVATED = False
    TIME_DERIVATED = True

# TODO need modify and change the algorithm plus with function
Layout = dbc.Row([
            dbc.Col([
                    html.H5("Support .txt"),
                    html.Div([
                        upload_component_generate("FTAPP-upload"),
                        dcc.Store(id="FTAPP-raw-data-store", storage_type="session"),
                        dcc.Store(id="FTAPP-oversampling-data-store", storage_type="session"),
                        dcc.Store(id="FTAPP-ft-data-store", storage_type="session"),
                        dcc.Loading([dcc.Store(id="FTAPP-oversampled-ft-data-store", storage_type="session")],
                            id="FTAPP-full-screen-mask", fullscreen=True)
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
                    download_component_generate(prefix_app_name)
                    ], width=3),
            dbc.Col([
                    ft_tabs_generate(prefix_app_name),
                    vertical_axis_swith(prefix_app_name),
                    ],
                    width=True),
            # Loading
])

# ================ Upload callback ========================

"""
Trigger when the experiental data(raw data) uploaded  
"""
@app.callback(
    Output("FTAPP-raw-data-store", "data"),
    Output("FTAPP-ft-data-store", "data"),
    # Output("FTAPP-upload-message", "children"),
    Output("FTAPP-loading-message", "children"),
    Input("FTAPP-upload", "contents"),
    Input("FTAPP-load-example", "n_clicks"),
    Input("FTAPP-refresh-btn", "n_clicks"),
    State("FTAPP-g_0", "value"),
    State("FTAPP-g_inf", "value"),
    State("FTAPP-oversampling-Nf", "value"),
    State("FTAPP-upload", "filename"),
    State("FTAPP-raw-data-store", "data"),
    State("FTAPP-ft-data-store", "data"),
    prevent_initial_call=True
)
def store_raw_data(content, example_click, refresh_click, 
                    g_0, g_inf, N_f, file_name, 
                    prev_raw_data, prev_ft_raw_data):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If all the input value is default, it means no update
    # if g_0 is None and g_inf is None and N_f is None:
    #     disable_refresh_updated = True
    # else:
    #     disable_refresh_updated = False

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else float(g_0)
    g_inf = 0 if g_inf is None else float(g_inf)
    N_f = 100 if N_f is None else int(N_f)

    df = pd.DataFrame()
    if button_id == "FTAPP-load-example":
        path = "./example_data/ft/example.txt"
        df = generate_df_from_local(path)
        raw_data, ft_raw_data = upload_local_data_workflow(df, g_0, g_inf, N_f, file_name)

    elif button_id == "FTAPP-upload":        
        df = generate_df(content)
        raw_data, ft_raw_data = upload_local_data_workflow(df, g_0, g_inf, N_f, file_name)

    elif button_id == "FTAPP-refresh-btn":
        if prev_raw_data is None:
            raise PreventUpdate
        else:
            df = convert_lists_to_df(prev_raw_data)
            replacement_elements = fast_ftdata(df, g_0, g_inf, N_f, False)
            raw_data = prev_raw_data
            replacement_keys = ["x", "y1", "y2", "non_time_y1", "non_time_y2"]
            ft_raw_data = replace_dict_value(prev_ft_raw_data, replacement_elements, replacement_keys)

    """
    Don't pass any string to this return. This component only for loading message.
    """
    return raw_data, ft_raw_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("FTAPP-oversampling-data-store", "data"),
    Output("FTAPP-oversampled-ft-data-store", "data"),
    Input("FTAPP-oversampling-btn", "n_clicks"),
    Input("FTAPP-refresh-btn", "n_clicks"),
    State("FTAPP-g_0", "value"),
    State("FTAPP-g_inf", "value"),
    State("FTAPP-raw-data-store", "data"),
    State("FTAPP-oversampling-input", "value"),
    State("FTAPP-oversampling-Nf", "value"),
    State("FTAPP-oversampling-data-store", "data"),
    State("FTAPP-oversampled-ft-data-store", "data"),
)
def store_oversampling_data(oversampling_click, refresh_click, 
                            g_0, g_inf, raw_data, ntimes, N_f,
                            prev_oversampled_data, prev_ft_oversampled_data):
    if raw_data is None:
        raise PreventUpdate
    
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "FTAPP-refresh-btn":
        if prev_oversampled_data is None and prev_ft_oversampled_data is None:
            raise PreventUpdate
    
    # If all the input value is default, it means no update
    # if g_0 is None and g_inf is None and N_f is None and ntimes is None:
    #     disable_refresh_updated = True
    # else:
    #     disable_refresh_updated = False

    # avoid float number
    ntimes = 10 if ntimes is None else int(ntimes)
    N_f = 100 if N_f is None else int(N_f)
    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else float(g_0)
    g_inf = 0 if g_inf is None else float(g_inf)

    df = convert_lists_to_df(raw_data)
    x, y = get_oversampling_data(df, ntimes)

    oversampled_data = {
        "x": x,
        "y": y,
    }

    # fast FT
    omega, g_p, g_pp, non_time_g_p, non_time_g_pp = fast_ftdata(df, g_0, g_inf, N_f, True, ntimes)

    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp,
        "non_time_y1": non_time_g_p,
        "non_time_y2": non_time_g_pp
    }

    return oversampled_data, oversampled_ft_data

"""
Input(Sigma) Renedr ----- First tab
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
    # prevent_initial_call=True
)

"""
Re & Im Renedr ----- Second tab
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideFT",
        function_name="tabChangeFTfigRender"
    ),
    Output("FTAPP-FT-display", "figure"),
    Input("FTAPP-ft-data-store", "data"),
    Input("FTAPP-oversampled-ft-data-store", "data"),
    Input("FTAPP-oversampling-render-switch", "value"),
    Input("FTAPP-time-derivative", "value"),
    Input("FTAPP-vertical-axis-switch", "value")
    # prevent_initial_call=True
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
# State("FTAPP-download-selection", "value"),
# State("FTAPP-oversampling-data-store", "data"),
# State("FTAPP-ft-data-store", "data"),
State("FTAPP-time-derivative", "value"),
State("FTAPP-raw-data-store","data"),
State("FTAPP-oversampled-ft-data-store", "data"),
prevent_initial_call=True,
)
def download(n_clicks, time_derivatived_option, raw_data, ft_oversampled_data):
    if ft_oversampled_data is None:
        return None, "No data available!"

    option = time_derivatived_option[0] if time_derivatived_option \
        is not None and time_derivatived_option != [] else False

    file_suffix_name = raw_data.get("filename")
    saved_file_name = "FT_oversampled_" + file_suffix_name

    if option == TIME_DERIVATED.NONTIME_DERIVATED.value:
        complex_list = combine_as_complex(
            ft_oversampled_data["non_time_y1"],
            ft_oversampled_data["non_time_y2"]
        )
    else:
        complex_list = combine_as_complex(
            ft_oversampled_data["y1"],
            ft_oversampled_data["y2"]
        )

    saved_data_df = pd.DataFrame(six_decimal_saving({
        "x": ft_oversampled_data["x"],
        "y": complex_list
    }))

    return (dcc.send_data_frame(saved_data_df.to_csv, saved_file_name, 
                                header=False, index=False, 
                                sep='\t', encoding='utf-8'), 
                                "Download OK !") 

# =================== Normal function ===================

# only the upload and example button and example button trigger this
def upload_local_data_workflow(df, g_0, g_inf, N_f, file_name):
    # save file_name and lens for message recovering when app changing
    raw_data = {
        "x": df[0],
        "y": df[1],
        "filename": file_name,
        "lines": len(df)
    }

    # fast FT processing
    omega, g_p, g_pp, non_time_g_p, non_time_g_pp = fast_ftdata(df, g_0, g_inf, N_f, False)

    ft_raw_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp,
        "non_time_y1": non_time_g_p,
        "non_time_y2": non_time_g_pp
    }

    return raw_data, ft_raw_data
