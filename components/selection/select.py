import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

downlaod_options_list = [
    {"label": "Oversampled data", "value": 0},
    {"label": "FT data", "value": 1},
    {"label": "FT oversampled data", "value": 2},
]

# It is used in irheo GT
DownloadSelection = dbc.Select(
    id="download-selection",
    options=downlaod_options_list,
    placeholder="Choose a type ..."
)

def download_selection_generate(prefix_app_name):
    id = prefix_app_name+"-download-selection"   
    DownloadSelection = dbc.Select(
        id=id,
        options=downlaod_options_list,
        placeholder="Choose a type ..."
    )

    return DownloadSelection