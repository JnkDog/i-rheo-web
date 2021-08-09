import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_html_components.Br import Br

from components.input.input import input_component_generate
from components.selection.select import download_selection_generate, DownloadSelection

INPUT_ID_SUFFIX_DICT = {
    "BEGIN_INPUT": "-begin-line-number",
    "END_INPUT":   "-end-line-number",
}

OUTPUT_ID_SUFFIX_DICT = {
    "MESSAGE":     "-download-message",
    "BUTTON":      "-download-btn", 
    "TEXT":        "-download-text",
}

# This is templates but used in irheo GT
# begin_line_input_cfg = {
#     "id": "begin-line-number",
#     "placeholder": "Type begin number ...",
#     "type": "number"
# }

# This is templates but used in irheo GT
# end_line_input_cfg = {
#     "id": "end-line-number",
#     "placeholder": "Type end number ...",
#     "type": "number"
# }

# This is templates but used in irheo GT
# BeginLineInput = input_component_generate(**begin_line_input_cfg)
# EndLineInput   = input_component_generate(**end_line_input_cfg)

# This is templates but used in irheo GT
Download = html.Div([
    html.H5("Download Data"),
    dbc.InputGroup([
        DownloadSelection,
        html.Button("Download File", id="download-btn", className="btn btn-primary")
    ]),
    dcc.Download(id="download-text"),
    html.Div(id="download-message")   
])

def download_component_generate(prefix_app_name):
    # BeginLineInput = input_component_generate(
    #                  prefix_app_name
    #                  +INPUT_ID_SUFFIX_DICT["BEGIN_INPUT"],
    #                  placeholder="Type cut bottom number ...")
    # EndLineInput   = input_component_generate(
    #                  prefix_app_name
    #                  +INPUT_ID_SUFFIX_DICT["END_INPUT"],
    #                  placeholder="Type cut top number ...")

    btn_id      = prefix_app_name + OUTPUT_ID_SUFFIX_DICT["BUTTON"]
    message_id  = prefix_app_name + OUTPUT_ID_SUFFIX_DICT["MESSAGE"]
    download_id = prefix_app_name + OUTPUT_ID_SUFFIX_DICT["TEXT"]
    
    Selection = download_selection_generate(prefix_app_name)

    Download = html.Div([
        html.H5("Download Data"),
        dbc.InputGroup([
            Selection,
            html.Button("Download File", id=btn_id, className="btn btn-primary")
        ]),
        dcc.Download(id=download_id),
        html.Div(id=message_id)   
    ])

    return Download