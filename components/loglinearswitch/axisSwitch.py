import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

VERTICAL_AXIS_SWITCH = "-vertical-axis-switch"


def vertical_axis_swith(prefix_app_name):
    switch_id = prefix_app_name + VERTICAL_AXIS_SWITCH
    Switch = dbc.FormGroup(
            dbc.Checklist(
                options=[
                    {"label": "vertical axis switch", "value": True}
                ],
                id=switch_id,
                switch=True,
                style={"margin": "auto", "fontSize": "20px"}),
            style={"display": "flex", "justifyContent": "center", "alignItems": "center", "height": "1vh"},    # id="time-derivate-form",
            className="mt-1")
             
    return Switch
