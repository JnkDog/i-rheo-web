import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# Radioitems = html.Div(dbc.FormGroup([
#     dbc.RadioItems(
#         options=[
#             {"label": "A(t)", "value": 0},
#             {"label": "∏(t)", "value": 1},
#         ],
#         value=1,
#         id="radioitems-input",
#     )],
#     className=""
# ))

MOTRadioitems = html.Div([
    dbc.RadioItems(
        options=[
            {"label": "A(t)", "value": 0},
            {"label": "∏(t)", "value": 1},
        ],
        value=0,
        id="MOT-radioitems-input",
    )],  
    className="btn-group me-2"
)
