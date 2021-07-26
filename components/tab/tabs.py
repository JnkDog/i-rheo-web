import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.display.spinner import Spinner_stress, Spinner_FT, Spinner_strain, spinner_generate # Spinner_eta

TABS_ID_SUFFIX_DICT = {
    "STRESS": "stress",
    "FT"   :    "FT",
    "STRAIN": "strain",
    # "ETA"  :   "eta",
    
}

# This is templates but used in irheo GT
Tab_Stress_content = Spinner_stress

Tab_FT_content = Spinner_FT

Tab_Strain_content = Spinner_strain

# Tab_Eta_content = Spinner_eta

# This is templates but used in irheo GT
Tabs = dbc.Tabs([
        dbc.Tab(children=Spinner_stress, label="Stress", tab_id="stress"),
        dbc.Tab(children=Spinner_FT, label="Elastic & Viscous", tab_id="FT"),
        dbc.Tab(children=Spinner_strain, label="Strain", tab_id="strain"),
        # dbc.Tab(children=Spinner_eta, label="Eta", tab_id="eta")
], id="fig-tabs")

def tabs_component_generate(prefix_app_name):    
    Tab_list = [dbc.Tab(spinner_generate(prefix_app_name+"-"+value), 
             label=value.capitalize(), tab_id=value) 
             for value in TABS_ID_SUFFIX_DICT.values()]
    
    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs