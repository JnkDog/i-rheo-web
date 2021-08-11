import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_html_components.Div import Div

from components.support import supportIntro

Layout = html.Div([
    html.Div(html.H1("User Guide"), style={"text-align": "center"}),
    html.Br(),
    supportIntro.GeneralHelp,
    html.Br(),
    supportIntro.SupportHelp,
    html.Br(),
    supportIntro.InputHelp,
    html.Br(),
    supportIntro.OversamplingHelp,
    html.Br(),
    supportIntro.DownloadHelp,
    html.Br(),
    supportIntro.FigHelp,
    html.Br(),
    ],
    className="container"   
)