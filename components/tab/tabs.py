import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.display.spinner import Spinner_sigma, Spinner_FT, Spinner_Gamma

Tab_Sigma_content = Spinner_sigma

Tab_FT_content = Spinner_FT

Tab_Gamma_content = Spinner_Gamma

Tabs = dbc.Tabs([
        dbc.Tab(children=Spinner_sigma, label="Sigma", tab_id="sigma"),
        dbc.Tab(children=Spinner_FT, label="FT", tab_id="FT"),
        dbc.Tab(children=Spinner_Gamma, label="Gamma", tab_id="Gamma")
], id="fig-tabs")