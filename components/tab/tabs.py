import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.display.spinner import Spinner_sigma, Spinner_FT, Spinner_gamma, Spinner_eta, spinner_generate

TABS_ID_SUFFIX_DICT = {
    "SIGMA": "sigma",
    "FT"   :    "FT",
    "GAMMA": "gamma",
    "ETA"  :   "eta",
    
}

# This is templates but used in irheo GT
Tab_Sigma_content = Spinner_sigma

Tab_FT_content = Spinner_FT

Tab_Gamma_content = Spinner_gamma

Tab_Eta_content = Spinner_eta

# This is templates but used in irheo GT
Tabs = dbc.Tabs([
        dbc.Tab(children=Spinner_sigma, label="Sigma", tab_id="sigma"),
        dbc.Tab(children=Spinner_FT, label="FT", tab_id="FT"),
        dbc.Tab(children=Spinner_gamma, label="Gamma", tab_id="gamma"),
        dbc.Tab(children=Spinner_eta, label="Eta", tab_id="eta")
], id="fig-tabs")

def tabs_component_generate(prefix_app_name):
    # Spinner_list = [spinner_generate(prefix_app_name
    #                                  +"-"
    #                                  +value) 
    #                 for value in TABS_ID_SUFFIX_DICT.values()]
    
    Tab_list = [dbc.Tab(spinner_generate(prefix_app_name+"-"+value), 
             label=value.capitalize(), tab_id=value) 
             for value in TABS_ID_SUFFIX_DICT.values()]
    
    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs