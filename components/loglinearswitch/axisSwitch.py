from dash_bootstrap_components._components.RadioItems import RadioItems
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

VERTICAL_AXIS_SWITCH = "-vertical-axis-switch"


def vertical_axis_swith(prefix_app_name):
    radio_id = prefix_app_name + VERTICAL_AXIS_SWITCH
    # Switch = dbc.FormGroup(
    #         dbc.Checklist(
    #             options=[
    #                 {"label": "loglog", "value": True}
    #             ],
    #             id=switch_id,
    #             switch=True,
    #             style={"margin": "auto", "fontSize": "20px"}),
    #         style={"display": "flex", "justifyContent": "center", "alignItems": "center", "height": "1vh"},    # id="time-derivate-form",
    #         className="mt-1")
     
    VerticalRadioItems = dbc.FormGroup([
        dbc.RadioItems(
            options=[
                {"label": "log-log", "value": 0},
                {"label": "linear-log", "value": 1},
            ],
            value=0,
            id=radio_id,
            inline=True,
        ),
    ], style={"display": "flex", "justifyContent": "center", "alignItems": "center", "height": "1vh"})

    return VerticalRadioItems
