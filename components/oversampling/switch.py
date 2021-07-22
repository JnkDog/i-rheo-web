import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

SWITCH_ID_SUFFIX = "-oversampling-render-switch"

Switch = dbc.FormGroup([
    dbc.Checklist(options=[
        {"label" : "oversampling render", "value" : True}
    ],
    # value=[False], 
    id="oversampling-render-switch", 
    switch=True,
    style={"fontSize" : "20px"}
)])

def switch_component_generate(prefix_app_name):
    switch_id = prefix_app_name + SWITCH_ID_SUFFIX
    return dbc.FormGroup([
            dbc.Checklist(options=[
                {"label" : "oversampling render", "value" : True}
            ],
            # value=[False], 
            id=switch_id, 
            switch=True,
            style={"fontSize" : "20px"}
    )])