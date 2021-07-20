import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

Switch = dbc.FormGroup([
    dbc.Checklist(options=[
        {"label" : "oversampling render", "value" : True}
    ],
    # value=[False], 
    id="oversampling-render-switch", 
    switch=True,
    style={"fontSize" : "20px"}
)])