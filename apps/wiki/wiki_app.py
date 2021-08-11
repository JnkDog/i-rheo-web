
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components.paper.reference import AllPapers, PaperMarkDown

NavDiv = html.Div([
    dcc.Link(
        'Navigate to Manlio\'s LinkedIn', href="https://www.linkedin.com/in/manlio-tassieri-b94a7127/",
        refresh=True,
        style={'fontFamily': 'Times New Roman, Times, serif', 'fontWeight': 'bold'},
        className="mr-5"
    ),
    dcc.Link(
        'Navigate to Manlio\'s Twitetr', href="https://twitter.com/ManlioTassieri",
        refresh=True,
        style={'fontFamily': 'Times New Roman, Times, serif', 'fontWeight': 'bold'},
        # className="center-block"
    ),
], className="text-center")

PaperList = html.Div([
    html.H2("Related articles", className="text-center"),
    html.Div(PaperMarkDown)
])

Layout = html.Div(
    children=[
        NavDiv,
        PaperList
    ],
    # className="container"
)