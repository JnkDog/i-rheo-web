import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from enum import Enum, unique

from app import app

# import components and its generation
from components.upload.upload import upload_component_generate
from components.download.download import download_component_generate
from components.oversampling.oversampling import mot_oversampling_generate
from components.input.parameter import stiffness_radius_generate
from components.tab.tabs import mot_tabs_generate
from components.radio.radio import MOTRadioitems
from components.loglinearswitch.axisSwitch import vertical_axis_swith


# import algorithm
from algorithm.mot.mot_At_oversampling import mot_oversampling
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df
from algorithm.mot.mot import fast_mot_procressing
from algorithm.mot.mot_two_function import mot_integrated_processing, chenged_G_start_to_g

# Using your own app name. Can't be same.
prefix_app_name = "MOT"

@unique
class FUNTION_TYPE(Enum):
    AT  = 0
    PAI = 1

BOUNDARY_COMPONENTS_ID = [
    "MOT-g_0",
    "MOT-g_inf",
]

STIFFNESS_RADIUS_COMPONENTS_ID = [
    "MOT-kt",
    "MOT-at"
]

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
                                    fullscreen=True),
                        
                    ], className="btn-group me-2"),
                    html.Div([dbc.Button("Load Example data", id="MOT-load-example", 
                              color="primary", style={"margin": "5px"})],
                              className="btn-group me-2"),
                    MOTRadioitems,
                    html.Div(id="MOT-upload-message"),
                    # This is just for show the loading message
                    html.Div(id="MOT-loading-message"),
                    html.Hr(),
                    mot_oversampling_generate(prefix_app_name),
                    html.Hr(),
                    stiffness_radius_generate(prefix_app_name),
                    html.Hr(),
                    download_component_generate(prefix_app_name)
                    ], width=3), 
            dbc.Col([
                    mot_tabs_generate(prefix_app_name),
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
    Output("MOT-raw-data-store", "data"),  
    Output("MOT-ft-data-store", "data"),
    # Output("upload-message", "children"),
    Output("MOT-loading-message", "children"),
    Input("MOT-upload", "contents"),
    Input("MOT-load-example", "n_clicks"),
    # TODO need change later
    # Boundary conditions
    Input("MOT-g_0", "value"),
    Input("MOT-g_inf", "value"),
    # Trap stiffness and radius
    Input("MOT-kt", "value"),
    Input("MOT-at", "value"),
    # Decide the A(t) or ∏(t)
    State("MOT-radioitems-input", "value"),
    State("MOT-upload", "filename"),
    # Get the modified time to avoid inital time operating
    # State("MOT-ft-data-store", "modified_timestamp"),
    State("MOT-raw-data-store", "data"),
    State("MOT-ft-data-store", "data"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, g_0, g_inf, kt, at, func_flag, file_name, prev_raw_data, prev_ft_data):
    # PreventUpdate without data
    data_null_prevents_updated(prev_raw_data, prev_ft_data)

    raw_data = {}
    ft_raw_data = {}

    """
    default kt: 1e-6, at: 1e-6
    kt is the value of trap stiffness
    at is the value of radius
    """
    kt = 1e-6 if kt is None else kt
    at = 1e-6 if at is None else at

    """
    Boundary conditions (aka. Oversampling parameters)
    default g_0   : 1 as A(t), 0 as ∏(t)
            g_inf : 0 
    """
    if func_flag == FUNTION_TYPE.AT.value:
        g_0 = 1 if g_0 is None else float(g_0)
    else:
        g_0 = 0 if g_0 is None else float(g_0)

    g_inf = 0 if g_inf is None else float(g_inf)

    trigger_id = get_trigger_id()

    # mot_integrated_processing could take a lot of time depending your PC
    df = pd.DataFrame()
    # get the example data from loacl
    if trigger_id == "MOT-load-example":
        path = "example_data/mot/data.txt"
        df = generate_df_from_local(path)
        raw_data, ft_raw_data = \
            upload_local_data_workflow(df, func_flag, g_0, g_inf, kt, at, file_name)

    # upload the data from users
    elif trigger_id == "MOT-upload":
        df = generate_df(content)
        raw_data, ft_raw_data = \
            upload_local_data_workflow(df, func_flag, g_0, g_inf, kt, at, file_name)

    # only trigger when 
    elif trigger_id in STIFFNESS_RADIUS_COMPONENTS_ID:
        replacement_elements = chenged_G_start_to_g(kt, at, prev_ft_data)
        replacement_keys = ["pai_y1", "pai_y2", "at_y1", "at_y2"]
        ft_raw_data = replace_dict_value(prev_ft_data, replacement_elements, replacement_keys)
        raw_data = prev_raw_data

    elif trigger_id in BOUNDARY_COMPONENTS_ID:
        df = convert_lists_to_df(prev_raw_data)
        replacement_elements = mot_integrated_processing(df, kt, at, g_0, g_inf, False)
        replacement_keys = ["x", "pai_y1", "pai_y2", "at_y1", "at_y2", "ft_real", "ft_imag"]
        ft_raw_data = replace_dict_value(prev_ft_data, replacement_elements, replacement_keys)
        raw_data = prev_raw_data

    # return data, upload_messge, ft_data
    return raw_data, ft_raw_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("MOT-oversampling-data-store", "data"),
    Output("MOT-oversampled-ft-data-store", "data"),
    Input("MOT-oversampling-btn", "n_clicks"),
    # TODO need change later
    # Boundary conditions
    Input("MOT-g_0", "value"),
    Input("MOT-g_inf", "value"),
    # Trap stiffness and radius
    Input("MOT-kt", "value"),
    Input("MOT-at", "value"),
    # Decide the A(t) or ∏(t)
    State("MOT-radioitems-input", "value"),
    State("MOT-raw-data-store", "data"),
    # Get ntimes
    State("MOT-oversampling-input", "value"),
    # Get the modified time to avoid inital time operating
    # State("MOT-ft-data-store", "modified_timestamp"),
    State("MOT-oversampling-data-store", "data"),
    State("MOT-oversampled-ft-data-store", "data"),
)
def store_oversampling_data(n_clicks, g_0, g_inf, kt, at, func_flag, raw_data, 
                            ntimes, prev_oversampled_data, prev_oversampled_ft_data):
    if raw_data is None or ntimes is None:
        raise PreventUpdate

    # avoid float number
    ntimes = int(ntimes)

    """
    Boundary conditions (aka. Oversampling parameters)
    default g_0   : 1 as A(t), 0 as ∏(t)
            g_inf : 0 
    """
    if func_flag == FUNTION_TYPE.AT.value:
        g_0 = 1 if g_0 is None else float(g_0)
    else:
        g_0 = 0 if g_0 is None else float(g_0)

    g_inf = 0 if g_inf is None else float(g_inf) 

    """
    default kt: 1e-6, at: 1e-6
    kt is the value of trap stiffness
    at is the value of radius
    """
    kt = 1e-6 if kt is None else kt
    at = 1e-6 if at is None else at

    oversampled_data = {}
    ft_oversampled_data = {}

    trigger_id = get_trigger_id()

    if trigger_id == "MOT-oversampling-btn":
        df = convert_lists_to_df(raw_data)
        oversampled_data, ft_oversampled_data = \
            oversampling_button_workflow(df, kt, at, g_0, g_inf, ntimes)
    
    elif trigger_id in STIFFNESS_RADIUS_COMPONENTS_ID:
        # upload the data but without oversampling need to prevent update
        if prev_oversampled_data is None or prev_oversampled_ft_data is None:
            raise PreventUpdate

        replacement_elements = chenged_G_start_to_g(kt, at, prev_oversampled_ft_data)
        replacement_keys = ["pai_y1", "pai_y2", "at_y1", "at_y2"]
        ft_oversampled_data = replace_dict_value(prev_oversampled_ft_data, replacement_elements, replacement_keys)
        oversampled_data = prev_oversampled_data
    
    elif trigger_id in BOUNDARY_COMPONENTS_ID:
        # upload the data but without oversampling need to prevent update
        if prev_oversampled_data is None or prev_oversampled_ft_data is None:
            raise PreventUpdate

        df = convert_lists_to_df(raw_data)
        replacement_elements = mot_integrated_processing(df, kt, at, g_0, g_inf, False)
        replacement_keys = ["x", "pai_y1", "pai_y2", "at_y1", "at_y2", "ft_real", "ft_imag"]
        ft_oversampled_data = replace_dict_value(prev_oversampled_ft_data, replacement_elements, replacement_keys)
        oversampled_data = prev_oversampled_data

    return oversampled_data, ft_oversampled_data

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

    # avoid float number
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
        saving_file_name = "download_MOT_data.txt"

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
        namespace="clientsideMot",
        function_name="tabChangeFigRender"
    ),
    Output("MOT-A(t)-display", "figure"),
    Input("MOT-raw-data-store", "data"),
    Input("MOT-oversampling-data-store", "data"),
    Input("MOT-oversampling-render-switch", "value"),
    Input("MOT-vertical-axis-switch", "value"),
    # Due to the dcc.Stroe's storage_type is session
    # if prevent_initial_call=True, the fig cannot show
    # prevent_initial_call=True
)

"""
Trigger when the ft data generated
"""
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMot",
        function_name="tabChangeMotRender"
    ),
    Output("MOT-Mot-display", "figure"),
    Input("MOT-ft-data-store", "data"),
    Input("MOT-oversampled-ft-data-store", "data"),
    Input("MOT-oversampling-render-switch", "value"),
    Input("MOT-radioitems-input", "value"),
    Input("MOT-vertical-axis-switch", "value"),
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

# =================== Normal function ===================

# Get the triggered component id 
def get_trigger_id():
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    return trigger_id

# Prevent updated when the datastore is NULL
def data_null_prevents_updated(raw_data, ft_raw_data):
    trigger_id = get_trigger_id()

    if trigger_id in BOUNDARY_COMPONENTS_ID+STIFFNESS_RADIUS_COMPONENTS_ID+["MOT-radioitems-input"]\
        and raw_data is None and ft_raw_data is None:
        raise PreventUpdate

# replace the dict's value
def replace_dict_value(dict, replacement, replacement_keys):
    idx = 0
    for key in dict:
        dict[key] = replacement[idx] if key in replacement_keys else dict[key]
        idx = idx + 1 if key in replacement_keys else idx

    return dict


# only the upload button and example button trigger this
def upload_local_data_workflow(df, func_flag, g_0, g_inf, kt, at, file_name):
    # save file_name and lens for message recovering when app changing
    raw_data = {
        "x": df[0],
        "y": df[1],
        "filename": file_name,
        "lines": len(df)
    }

    omega, pai_g_p, pai_g_pp, a_t_g_p, a_t_g_pp, ft_real, ft_imag = \
        mot_integrated_processing(df, kt, at, g_0, g_inf, False)
    
    ft_raw_data = {
        "x": omega,
        "pai_y1": pai_g_p,
        "pai_y2": pai_g_pp,
        "at_y1" : a_t_g_p,
        "at_y2" : a_t_g_pp,
        "ft_real": ft_real,
        "ft_imag": ft_imag
    }

    return raw_data, ft_raw_data

def oversampling_button_workflow(df, kt, at, g_0, g_inf, ntimes):
    x, y = mot_oversampling(df, ntimes)

    oversampled_data = {
        "x": x,
        "y": y,
    }

    omega, pai_g_p, pai_g_pp, a_t_g_p, a_t_g_pp, ft_real, ft_imag \
        = mot_integrated_processing(df, kt, at, g_0, g_inf, True, ntimes)

    ft_oversampled_data = {
        "x": omega,
        "pai_y1": pai_g_p,
        "pai_y2": pai_g_pp,
        "at_y1" : a_t_g_p,
        "at_y2" : a_t_g_pp,
        "ft_real": ft_real,
        "ft_imag": ft_imag
    }

    return oversampled_data, ft_oversampled_data