
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


Layout = html.Div(
    [html.H2("Overview"), html.P("This is a i-rheo web")],
    className="bd-content ps-lg-4"
)