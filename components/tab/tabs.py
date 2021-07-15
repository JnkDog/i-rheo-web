import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.display.spinner import Spinner_sigma, Spinner_FT

Tab_Sigma_content = Spinner_sigma

Tab_FT_content = Spinner_FT

Tabs = dbc.Tabs([
        dbc.Tab(children=Spinner_sigma, label="Sigma", tab_id="sigma"),
        dbc.Tab(children=Spinner_FT, label="FT", tab_id="FT")
], id="fig-tabs")