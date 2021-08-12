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
from algorithm.saving_process import combine_as_complex, six_decimal_saving

# Using your own app name. Can't be same.
prefix_app_name = "MOT"

# Function type At or Pait
@unique
class FUNTION_TYPE(Enum):
    AT  = 0
    PAI = 1

# Selection options
@unique
class DOWNLOAD_OPTIONS(Enum):
    OVERSAMPLED_RAW_DATA  = 0
    FT_RAW_DATA = 1
    FT_OVERSAMPLED_DATA = 2

BOUNDARY_COMPONENTS_ID = [
    "MOT-g_0",
    "MOT-g_inf",
]

STIFFNESS_RADIUS_COMPONENTS_ID = [
    "MOT-kt",
    "MOT-at"
]

DEFAULT_G_0_AT = 1
DEFAULT_G_0_PAIT = 0

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
                    # html.Hr(),
                    # stiffness_radius_generate(prefix_app_name),
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
    Input("MOT-refresh-btn", "n_clicks"),
    # TODO need change later
    # Boundary conditions
    State("MOT-g_0", "value"),
    State("MOT-g_inf", "value"),
    # Trap stiffness and radius
    State("MOT-kt", "value"),
    State("MOT-at", "value"),
    State("MOT-oversampling-Nf", "value"),
    # Decide the A(t) or ∏(t)
    State("MOT-radioitems-input", "value"),
    State("MOT-upload", "filename"),
    # Get the modified time to avoid inital time operating
    # State("MOT-ft-data-store", "modified_timestamp"),
    State("MOT-raw-data-store", "data"),
    State("MOT-ft-data-store", "data"),
    prevent_initial_call=True
)
def store_raw_data(content, example_click, refresh_click, 
                   g_0, g_inf, kt, at, 
                   N_f, func_flag, file_name, 
                   prev_raw_data, prev_ft_data):
    raw_data = {}
    ft_raw_data = {}
    
    is_disable_FT = disable_FT(g_0, g_inf, kt, at, N_f, prev_ft_data)

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
    if g_0 is None:
        is_double_FT = True
        # Whatever the value is, the important value is the is_double_FT
        g_0 = 1
    else:
        is_double_FT = False
        g_0 = float(g_0)

    g_inf = 0 if g_inf is None else float(g_inf)

    N_f = 100 if N_f is None else int(N_f)

    trigger_id = get_trigger_id()

    # mot_integrated_processing could take a lot of time depending your PC
    df = pd.DataFrame()
    # get the example data from loacl
    if trigger_id == "MOT-load-example":
        path = "example_data/mot/data.txt"
        df = generate_df_from_local(path)
        raw_data, ft_raw_data = \
            upload_local_data_workflow(df, g_0, g_inf, kt, at, 
                                       N_f, file_name, is_double_FT)

    # upload the data from users
    elif trigger_id == "MOT-upload":
        df = generate_df(content)
        raw_data, ft_raw_data = \
            upload_local_data_workflow(df, g_0, g_inf, kt, at, 
                                       N_f, file_name, is_double_FT)
    else:
        data_null_prevents_updated()

        if is_disable_FT:
            raw_data = prev_raw_data
            ft_raw_data = update_ft_data(prev_ft_data, kt, at, func_flag)
        else:
            df = convert_lists_to_df(prev_raw_data)
            file_name = prev_ft_data["filename"]
            raw_data, ft_raw_data = \
                upload_local_data_workflow(df, g_0, g_inf, kt, at, N_f, is_double_FT)

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
    Input("MOT-refresh-btn", "n_clicks"),
    # TODO need change later
    # Boundary conditions
    State("MOT-g_0", "value"),
    State("MOT-g_inf", "value"),
    # Trap stiffness and radius
    State("MOT-kt", "value"),
    State("MOT-at", "value"),
    # Decide the A(t) or ∏(t)
    State("MOT-radioitems-input", "value"),
    State("MOT-raw-data-store", "data"),
    # Get ntimes
    State("MOT-oversampling-input", "value"),
    State("MOT-oversampling-Nf", "value"),
    # Get the modified time to avoid inital time operating
    # State("MOT-ft-data-store", "modified_timestamp"),
    State("MOT-oversampling-data-store", "data"),
    State("MOT-oversampled-ft-data-store", "data"),
    prevent_initial_call=True
)
def store_oversampling_data(oversampling_click, refresh_click,
                            g_0, g_inf, kt, at, func_flag, raw_data, 
                            ntimes, N_f, prev_oversampled_data, 
                            prev_ft_oversampled_data):
    if raw_data is None and ntimes is None:
        raise PreventUpdate

    is_disable_FT = disable_FT(g_0, g_inf, kt, at, N_f, prev_ft_oversampled_data)

    trigger_id = get_trigger_id()

    # avoid float number or string
    ntimes = 10 if ntimes is None else int(ntimes)
    N_f = 100 if N_f is None else int(N_f)
    func_flag = int(func_flag)

    """
    Boundary conditions (aka. Oversampling parameters)
    default g_0   : 1 as A(t), 0 as ∏(t)
            g_inf : 0 
    """
    if g_0 is None:
        is_double_FT = True
        # Whatever the value is, the important value is the is_double_FT
        g_0 = 1
    else:
        is_double_FT = False
        g_0 = float(g_0)

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

    if trigger_id == "MOT-oversampling-btn":
        df = convert_lists_to_df(raw_data)
        oversampled_data, ft_oversampled_data = \
            oversampling_button_workflow(df, kt, at, g_0, g_inf, N_f, ntimes, is_double_FT)
    else:
        if is_disable_FT:
            oversampled_data = prev_oversampled_data
            ft_oversampled_data = update_ft_data(prev_ft_oversampled_data, kt, at, func_flag)
        else:
            df = convert_lists_to_df(raw_data)
            raw_data, ft_oversampled_data = \
                oversampling_button_workflow(df, kt, at,  g_0, g_inf, N_f, ntimes, is_double_FT)


    return oversampled_data, ft_oversampled_data

# ================ Download callback ========================

@app.callback(
    Output("MOT-download-text", "data"),
    Output("MOT-download-message", "children"),
    Input("MOT-download-btn", "n_clicks"),
    # State("MOT-downlaod-selection", "value"),
    State("MOT-raw-data-store","data"),
    # State("MOT-oversampling-data-store", "data"),
    # State("MOT-ft-data-store", "data"),
    State("MOT-oversampled-ft-data-store", "data"),
    State("MOT-radioitems-input", "value"),
    prevent_initial_call=True,
)
def download(n_clicks, raw_data, ft_oversampled_data, func_flag):
    if ft_oversampled_data is None:
        return None, "No data available!"

    file_suffix_name = raw_data.get("filename")
    saved_file_name = "FT_oversampled_" + file_suffix_name

    # TODO At or Pai t's download data convert...
    # Covert the option from string to int
    if int(func_flag) == FUNTION_TYPE.AT.value:
        saved_omega = ft_oversampled_data["at_x"]
        complex_list = combine_as_complex(
            ft_oversampled_data["at_y1"],
            ft_oversampled_data["at_y2"]
        )
    else:
        saved_omega = ft_oversampled_data["pai_x"]
        complex_list = combine_as_complex(
            ft_oversampled_data["pai_y1"],
            ft_oversampled_data["pai_y2"]
        )
    
    saved_data_df = pd.DataFrame(six_decimal_saving({
        "x": saved_omega,
        "y": complex_list
    }))

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
def data_null_prevents_updated(data):
    if data is None:
        raise PreventUpdate

# If the data exists and the g_o is None with the g_inf
def disable_FT(g_0, g_inf, kt, at, N_f, prev_data):
    if all([g_0, g_inf, N_f]) is False and prev_data is not None:
        return True
    else:
        return False
       
# replace the dict's value
def replace_dict_value(dict, replacement, replacement_keys):
    idx = 0
    for key in dict:
        dict[key] = replacement[idx] if key in replacement_keys else dict[key]
        idx = idx + 1 if key in replacement_keys else idx

    return dict

# Extract data
def extract_from_prev_data(original_data, func_flag):
    if func_flag == FUNTION_TYPE.AT.value:
        data = {
            "x": original_data["at_x"],
            "ft_real": original_data["at_ft_real"],
            "ft_imag": original_data["at_ft_imag"],
        }
    else:
        data = {
            "x": original_data["pai_x"],
            "ft_real": original_data["pait_ft_real"],
            "ft_imag": original_data["pait_ft_imag"],
        }

    return data

# Updata FT data acroding the func_flag
def update_ft_data(ft_data, kt, at, func_flag):
    data = extract_from_prev_data(ft_data, func_flag)
    if func_flag == FUNTION_TYPE.AT.value:
        _, _, replace_g_p, replace_g_pp = chenged_G_start_to_g(kt, at, data)
        replacement_keys = ["at_y1", "at_y2"]
        replacement_elements = [replace_g_p, replace_g_pp]
    else:
        replace_g_p, replace_g_pp, _, _ = chenged_G_start_to_g(kt, at, data)
        replacement_keys = ["pai_y1", "pai_y2"]
        replacement_elements = [replace_g_p, replace_g_pp]

    updated_data = replace_dict_value(ft_data, replacement_elements, replacement_keys)

    return updated_data

# only the upload button and example button trigger this
def upload_local_data_workflow(df, g_0, g_inf, kt, at, 
                                N_f, file_name, is_double_FT):
    # save file_name and lens for message recovering when app changing
    raw_data = {
        "x": df[0],
        "y": df[1],
        "filename": file_name,
        "lines": len(df)
    }

    if is_double_FT:
        # At
        omega_at, _, _, a_t_g_p, a_t_g_pp, at_ft_real, at_ft_imag = \
            mot_integrated_processing(df, kt, at, DEFAULT_G_0_AT, g_inf, N_f, False)

        # Pait
        omega_pait, pai_g_p, pai_g_pp, _, _, pait_ft_real, pait_ft_imag = \
            mot_integrated_processing(df, kt, at, g_0, g_inf, N_f, False)

        ft_raw_data = {
            "at_x": omega_at,
            "pai_x": omega_pait,
            "pai_y1": pai_g_p,
            "pai_y2": pai_g_pp,
            "pai_ft_real": pait_ft_real,
            "pai_ft_imag": pait_ft_imag,
            "at_y1" : a_t_g_p,
            "at_y2" : a_t_g_pp,
            "at_ft_real": at_ft_real,
            "at_ft_imag": at_ft_imag
        }
    else:
        omega, pai_g_p, pai_g_pp, a_t_g_p, a_t_g_pp, ft_real, ft_imag = \
            mot_integrated_processing(df, kt, at, g_0, g_inf, N_f, False)

        ft_raw_data = {
            "at_x": omega,
            "pai_x": omega,
            "pai_y1": pai_g_p,
            "pai_y2": pai_g_pp,
            "pai_ft_real": ft_real,
            "pai_ft_imag": ft_imag,
            "at_y1" : a_t_g_p,
            "at_y2" : a_t_g_pp,
            "at_ft_real": ft_real,
            "at_ft_imag": ft_imag
        }

    return raw_data, ft_raw_data

def oversampling_button_workflow(df, kt, at, g_0, g_inf, N_f, ntimes, is_double_FT):
    x, y = mot_oversampling(df, ntimes)

    oversampled_data = {
        "x": x,
        "y": y,
    }

    if is_double_FT:
        # At
        omega_at, _, _, a_t_g_p, a_t_g_pp, at_ft_real, at_ft_imag = \
            mot_integrated_processing(df, kt, at, DEFAULT_G_0_AT, g_inf, N_f, True, ntimes)

        # Pait
        omega_pait, pai_g_p, pai_g_pp, _, _, pait_ft_real, pait_ft_imag = \
            mot_integrated_processing(df, kt, at, g_0, g_inf, N_f, True, ntimes)

        ft_oversampled_data = {
            "at_x": omega_at,
            "pai_x": omega_pait,
            "pai_y1": pai_g_p,
            "pai_y2": pai_g_pp,
            "pai_ft_real": pait_ft_real,
            "pai_ft_imag": pait_ft_imag,
            "at_y1" : a_t_g_p,
            "at_y2" : a_t_g_pp,
            "at_ft_real": at_ft_real,
            "at_ft_imag": at_ft_imag
        }
    else:
        omega, pai_g_p, pai_g_pp, a_t_g_p, a_t_g_pp, ft_real, ft_imag = \
            mot_integrated_processing(df, kt, at, g_0, g_inf, N_f, True, ntimes)

        ft_oversampled_data = {
            "at_x": omega,
            "pai_x": omega,
            "pai_y1": pai_g_p,
            "pai_y2": pai_g_pp,
            "pai_ft_real": ft_real,
            "pai_ft_imag": ft_imag,
            "at_y1" : a_t_g_p,
            "at_y2" : a_t_g_pp,
            "at_ft_real": ft_real,
            "at_ft_imag": ft_imag
        }


    return oversampled_data, ft_oversampled_data