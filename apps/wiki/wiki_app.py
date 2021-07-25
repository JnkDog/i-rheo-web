
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


Layout = html.Div(
    children=[
        html.Br(),
        dcc.Link(
            'Navigate to Manlio\'s LinkedIn', href="https://www.linkedin.com/in/manlio-tassieri-b94a7127/",
            refresh=True,
            style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}
        ),
        html.Br(),
        dcc.Link(
            'Navigate to Manlio\'s Twitetr', href="https://twitter.com/ManlioTassieri",
            refresh=True,
            style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}
        )
    ],
    className="bd-content ps-lg-4",
)