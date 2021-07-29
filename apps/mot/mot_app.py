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
from components.oversampling.oversampling import mot_oversampling_generate
from components.tab.tabs import mot_tabs_generate

# import algorithm
from algorithm.mot_At_oversampling import mot_oversampling
from algorithm.read_data import generate_df, generate_df_from_local, convert_lists_to_df
from algorithm.mot import mot_processing
from algorithm.pai import pai_processing

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
                    mot_oversampling_generate(prefix_app_name),
                    html.Hr(),
                    download_component_generate(prefix_app_name)
                    ], width=3), 
            dbc.Col(mot_tabs_generate(prefix_app_name), width=True),
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
    State("MOT-upload", "filename"),
    # TODO need change later
    State("MOT-kt", "value"),
    State("MOT-at", "value"),
    prevent_initial_call=True
)
def store_raw_data(content, n_clicks, file_name, kt, at):
    # Deciding which raw_data used according to the ctx 
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = pd.DataFrame()
    if button_id == "MOT-load-example":
        path = "example_data/mot/data.txt"
        df = generate_df_from_local(path)
    else:
        df = generate_df(content)
    
    # save file_name and lens for message recovering when app changing
    data = {
        "x": df[0],
        "y": df[1],
        "pai": pai_processing(df)["pai"],
        "filename": file_name,
        "lines": len(df)
    }  

    # default kt: 1e-6, at: 1e6
    kt = 1e-6 if kt is None else kt
    at = 1e6 if at is None else at

    # This function takes lots of time
    omega, g_p, g_pp = mot_processing(df, kt, at, False)

    ft_data = {
        "x": omega,
        "y1": g_p,
        "y2": g_pp
    }

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
    State("MOT-kt", "value"),
    State("MOT-at", "value"),
    State("MOT-raw-data-store", "data"),
    State("MOT-oversampling-input", "value")
)
def store_oversampling_data(n_clicks, kt, at, data, ntimes):
    if n_clicks is None or data is None or ntimes is None:
        raise PreventUpdate

    # avoid floor number
    ntimes = int(ntimes)
    df = convert_lists_to_df(data)
    x, y = mot_oversampling(df, ntimes)

    data = {
        "x": x,
        "y": y,
    }

    # default kt: 1e-6, at: 1e6
    kt = 1e-6 if kt is None else kt
    at = 1e6 if at is None else at

    # This function takes lots of time
    omega, g_p, g_pp = mot_processing(df, kt, at, True, ntimes)

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
        namespace="clientsideMot",
        function_name="tabChangeFigRender"
    ),
    Output("MOT-A(t)-display", "figure"),
    Input("MOT-raw-data-store", "data"),
    Input("MOT-oversampling-data-store", "data"),
    Input("MOT-oversampling-render-switch", "value"),
    # Due to the dcc.Stroe's storage_type is session
    # if prevent_initial_call=True, the fig cannot show
    # prevent_initial_call=True
)

# pai figure render
app.clientside_callback(
    """
    function(rawData) {
        if (rawData == undefined) {
            return;
        }
        let data = [];
        let layout = {
            "xaxis": {"tick0": -2, "dtick": 1,
                    "type": "log", "title": {"text": "t (sec)"}, 
                    "ticks": "outside" 
            },
            "yaxis": {"title": {"text": "Π(t)"}, 
                    // "range": [0, 1.0],
                    "rangemode": "tozero", "ticks": "outside"
            },
        }

        let rawDataTrace = {
            "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            "name": "Experiental Data",
            "mode": "markers",
            "marker": {color:"orange", "symbol": "circle-open", 
                    "size": 10, "maxdisplayed": 200},
            "x": rawData.x,
            "y": rawData.pai
        }

        data.push(rawDataTrace)

        return {
            "data": data,
            "layout": layout
        }
    }
    """,
    Output("MOT-pai-display", "figure"),
    Input("MOT-raw-data-store", "data")
)

# add to the js part and data store part
app.clientside_callback(
    ClientsideFunction(
        namespace="clientsideMot",
        function_name="tabChangeMotRender"
    ),
    Output("MOT-Mot-display", "figure"),
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

