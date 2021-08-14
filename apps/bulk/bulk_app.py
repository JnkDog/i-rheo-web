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
from components.loglinearswitch.axisSwitch import vertical_axis_swith

# import algorithm
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df
from algorithm.bulk.bulk import bulk_ft
from algorithm.saving_process import combine_as_complex, six_decimal_saving

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
                        dcc.Store(id="BULKAPP-raw-data-store", storage_type="session"),
                        dcc.Store(id="BULKAPP-oversampling-data-store", storage_type="session"),
                        dcc.Store(id="BULKAPP-FT-data-store", storage_type="session"),
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
            dbc.Col([
                    tabs_component_generate(prefix_app_name),
                    vertical_axis_swith(prefix_app_name)
                    ]
                    ,width=True),
            # Loading
])

# ================ Upload callback ========================

"""
Trigger when the experiental data(raw data) uploaded  
"""
@app.callback(
    Output("BULKAPP-raw-data-store", "data"),
    # Output("BULKAPP-upload-message", "children"),
    Output("BULKAPP-FT-data-store", "data"),
    Output("BULKAPP-loading-message", "children"),
    Input("BULKAPP-upload", "contents"),
    Input("BULKAPP-load-example", "n_clicks"),
    Input("BULKAPP-refresh-btn", "n_clicks"),
    State("BULKAPP-g_0", "value"),
    State("BULKAPP-g_inf", "value"),
    State("BULKAPP-oversampling-Nf", "value"),
    State("BULKAPP-upload", "filename"),
    State("BULKAPP-raw-data-store", "data"),
    prevent_initial_call=True
)
def store_raw_data(content, example_click, refresh_click,
                   g_0, g_inf, N_f, file_name, prev_raw_data):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = pd.DataFrame()
    if button_id == "BULKAPP-load-example":
        path = "./example_data/bulk/example.txt"
        df = generate_df_from_local(path)
    elif button_id == "BULKAPP-upload":
        df = generate_df(content)

    raw_data = {
        "x": df[0],
        "y": df[1],
        "z": df[2],
        "filename": file_name,
        "lines": len(df)
    }

    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else int(g_0)
    g_inf = 0 if g_inf is None else int(g_inf)
    N_f = 100 if N_f is None else int(N_f)

    omega, g_p, g_pp = bulk_ft(df, g_0, g_inf, True, N_f)

    ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    """
    Don't pass any string to this return. This component only for loading message.
    """
    return raw_data, ft_data, ""

"""
Trigger when the experiental data(raw data) has already uploaded
and the oversampling button clicked with the oversampling ntimes.
"""
@app.callback(
    Output("BULKAPP-oversampling-data-store", "data"),
    Output("BULKAPP-oversampled-ft-data-store", "data"),
    Input("BULKAPP-oversampling-btn", "n_clicks"),
    Input("BULKAPP-refresh-btn", "n_clicks"),
    State("BULKAPP-g_0", "value"),
    State("BULKAPP-g_inf", "value"),
    State("BULKAPP-raw-data-store", "data"),
    State("BULKAPP-oversampling-input", "value"),
    State("BULKAPP-oversampling-Nf", "value"),
    prevent_initial_call=True
)
def store_oversampling_data(oversampling_click, refresh_click,
                            g_0, g_inf, raw_data, ntimes, N_f):
    if raw_data is None:
        raise dash.exceptions.PreventUpdate

    # avoid float number
    ntimes = 10 if ntimes is None else int(ntimes)
    N_f = 100 if N_f is None else int(N_f)
    # default g_0: 1, g_inf: 0
    g_0 = 1 if g_0 is None else int(g_0)
    g_inf = 0 if g_inf is None else int(g_inf)

    df = convert_lists_to_df(raw_data)
    x, y, z = bulk_ft(df, g_0, g_inf, False, N_f)

    # x, y = get_oversampling_data(content=content, ntimes=ntimes)

    oversampled_data = {
        "x" : x,
        "y" : y,
        "z" : z
    }
    
    # This function takes lots of time
    omega, g_p, g_pp = bulk_ft(df, g_0, g_inf, True, N_f, ntimes)

    oversampled_ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

    return oversampled_data, oversampled_ft_data

"""
Stress Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    """
    function(rawData, oversamplingData, switchValue=[false]) {
        if (rawData == undefined) {
            return;
        }

        let data = [];
        let layout = {
            "xaxis": {"tick0": -2, "dtick": 1,
                        "type": "log", "title": {"text": "Time [s]"}, 
                        "ticks": "outside" 
            },
            "yaxis": {"title": {"text" : "σ [Pa]"}, "range": [0, 1.0],
                        "rangemode": "tozero", "ticks": "outside"
            },
        }
        let rawDataTrace = {
            "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            "name": "Experiental Data",
            "mode": "markers",
            "marker": {color:"green", "symbol": "circle-open", 
                        "size": 10, "maxdisplayed": 200},
            "x": rawData.x,
            "y": rawData.y
        }

        if (switchValue[0] == true && oversamplingData != undefined) {
            let oversamplingDataTrace = {
                "name": "Oversampling Data",
                "mode": "markers",
                "marker": {color:"darkgreen", "symbol": "circle-x", 
                            "size": 6, "maxdisplayed": 200},
                "x": oversamplingData.x,
                "y": oversamplingData.y
            }
            
            data.push(rawDataTrace, oversamplingDataTrace);
        } else {
            data.push(rawDataTrace);
        }

        return {
            "data" : data,
            "layout": layout
        }   
    }
    """,
    Output("BULKAPP-stress-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
    Input("BULKAPP-vertical-axis-switch", "value"),
    # prevent_initial_call=True
)

"""
Strain Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    """
    function(rawData, oversamplingData, switchValue=[false]) {
        if (rawData == undefined) {
            return;
        }

        let data = [];
        let layout = {
            "xaxis": {"tick0": -2, "dtick": 1,
                        "type": "log", "title": {"text": "Time [s]"}, 
                        "ticks": "outside" 
            },
            "yaxis": { "title": {"text" : "γ"}, 
                       "rangemode": "tozero", 
                      "ticks": "outside"},
        }
        let rawDataTrace = {
            "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            "name": "Experiental Data",
            "mode": "markers",
            "marker": {color:"green", "symbol": "circle-open", 
                        "size": 10, "maxdisplayed": 200},
            "x": rawData.x,
            "y": rawData.z
        }

        if (switchValue[0] == true && oversamplingData != undefined) {
            let oversamplingDataTrace = {
                "name": "Oversampling Data",
                "mode": "markers",
                "marker": {color:"darkgreen", "symbol": "circle-x", 
                            "size": 6, "maxdisplayed": 200},
                "x": oversamplingData.x,
                "y": oversamplingData.z
            }
            
            data.push(rawDataTrace, oversamplingDataTrace);
        } else {
            data.push(rawDataTrace);
        }

        return {
            "data" : data,
            "layout": layout
        }   
    }
    """,
    Output("BULKAPP-strain-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
    Input("BULKAPP-vertical-axis-switch", "value"),
    # prevent_initial_call=True
)

"""
Viscoelastic moduli Renedr
Trigger when the experiental data(raw data) or oversampling data changed
"""
app.clientside_callback(
    """
    function(ftData, oversampledftData, switchValue=[false], verticalAxisSwitch) {
        if (ftData == undefined) {
            return;
        }

        let data = [];
        let layoutLinear = {
            "xaxis": {"dtick": 1, "tick0": -12, 
                        "type": "log", "title": {"text": "ω [rad/s]"},
                        "ticks": "outside"},
            "yaxis": { "type": "linear", "title": {"text" : "G′ G′′ [Pa]"},
                        "ticks": "outside"},
        }
        let layoutLog = {
            "xaxis": {"dtick": 1, "tick0": -12, 
                        "type": "log", "title": {"text": "ω [rad/s]"},
                        "ticks": "outside"},
            "yaxis": {"dtick": 1, "tick0": -7, 
                        "type": "log", "title": {"text" : "G′ G′′ [Pa]"},
                        "ticks": "outside"},
        }
        let ftDataTrace0 = {
            "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            "name": "G\'",
            "mode": "lines",
            "line": {color:"black", "width": "8"},
            // "marker": {"color": "black", "symbol": "square", "size": 7},
            "x": ftData.x,
            "y": ftData.y1,
        }
        let ftDataTrace1 = {
            "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            "name": "G\'\'",
            "mode": "lines",
            "line": {"color": "red"},
            "x": ftData.x,
            "y": ftData.y2,
        }

        if (switchValue[0] == true && oversampledftData != undefined) {
            let oversampledftDataTrace0 = {
                "name": "oversampled-G\'",
                "mode": "lines",
                "line": {color:"black", "width": "8"},
                // "marker": {"color": "black"},
                "x": oversampledftData.x,
                "y": oversampledftData.y1,
            }
            let oversampledftDataTrace1 = {
                "name": "oversampled-G\'\'",
                "mode": "lines",
                "line": {"color": "red"},
                "x": oversampledftData.x,
                "y": oversampledftData.y2,
            }
            
            data.push(oversampledftDataTrace0, oversampledftDataTrace1);
        } else {
            data.push(ftDataTrace0, ftDataTrace1);  
        }
        
        let layout = [];
        if (verticalAxisSwitch == VERTICAL_AXIS_TYPE.LINEAR) {
            layout = layoutLinear;
        } else {
            layout = layoutLog;
        }

        return {
            "data" : data,
            "layout": layout
        }
    } 
    """,
    Output("BULKAPP-vm-display", "figure"),
    Input("BULKAPP-raw-data-store", "data"),
    Input("BULKAPP-oversampling-data-store", "data"),
    Input("BULKAPP-oversampling-render-switch", "value"),
    Input("BULKAPP-vertical-axis-switch", "value"),
    # prevent_initial_call=True
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
    State("BULKAPP-raw-data-store", "data"),
    State("BULKAPP-oversampling-data-store", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, raw_data, ft_oversampled_data):
    if ft_oversampled_data is None:
        return None, "No data available!"

    file_suffix_name = raw_data.get("filename")
    saved_file_name = "FT_oversampled_" + file_suffix_name

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

