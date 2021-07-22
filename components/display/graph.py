import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# import components
from components.tab.tabs import Tabs
from components.display.spinner import Spinner

Graph = html.Div([
    Tabs
], id="right-colum-layout")