from numpy import index_exp
from dash_bootstrap_components._components.Tab import Tab
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.display.spinner import Spinner, Spinner_stress, Spinner_FT, Spinner_strain, spinner_generate # Spinner_eta

TABS_LABEL_DICT = {
    "STRESS": "Stress",
    "E & V" : "Elastic & Viscous",
    "STRAIN": "Strain",
    # "ETA"  :   "eta",
}

TABS_ID_SUFFIX_DICT = {
    "SIGMA": "sigma",
    "FT"   :    "FT",
    "GAMMA": "gamma",
    # "ETA"  :   "eta",
}

MOT_TABS_DICT = {
    "1": "Input",
    "2": "Viscoelastic moduli"
}

FT_TABS_DICT = {
    "1": "Input",
    "2": "Re & Im",
}

AFM_TABS_DICT = {
    "1": "Force",
    "2": "Indentation",
    "3": "Classic-Moduli"
}

AFM_TABS_LABEL_DICT = {
    "1": "Force",
    "2": "Indentation",
    "3": "Viscoelastic moduli"
}

# This is templates but used in irheo GT
Tab_Stress_content = Spinner_stress

Tab_FT_content = Spinner_FT

Tab_Strain_content = Spinner_strain

# Tab_Eta_content = Spinner_eta

# This is templates but used in irheo GT
Tabs = dbc.Tabs([
        dbc.Tab(children=Spinner_stress, label="Stress", tab_id="stress"),
        dbc.Tab(children=Spinner_FT, label="Elastic & Viscous", tab_id="elastic & viscous"),
        # dbc.Tab(children=Spinner_strain, label="Strain", tab_id="strain"),
        # dbc.Tab(children=Spinner_eta, label="Eta", tab_id="eta")
], id="fig-tabs")

def tabs_component_generate(prefix_app_name):
    Spinner_list = [spinner_generate(prefix_app_name+"-"+value)
                    for value in TABS_ID_SUFFIX_DICT.values()]
    
    Tab_list = [dbc.Tab(item, label=list(TABS_LABEL_DICT.values())[idx], 
                        tab_id=list(TABS_LABEL_DICT.values())[idx].lower()) 
                        for idx, item in enumerate(Spinner_list)]

    # Tab_list = [dbc.Tab(spinner_generate(prefix_app_name+"-"+value), 
    #          label=value.capitalize(), tab_id=value) 
    #          for value in TABS_ID_SUFFIX_DICT.values()]
    
    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs

def mot_tabs_generate(prefix_app_name):
    Spinner_list = [
        spinner_generate(prefix_app_name+"-"+value) for value in ["A(t)", "Mot"]
    ]
    
    Tab_list = [dbc.Tab(item, label=list(MOT_TABS_DICT.values())[idx],
                        tab_id=list(MOT_TABS_DICT.values())[idx])
                        for idx, item in enumerate(Spinner_list)]
    
    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs

def afm_tabs_generate(prefix_app_name):
    Spinner_list = [spinner_generate(prefix_app_name+"-"+value)
                    for value in AFM_TABS_DICT.values()]

    Tab_list = [dbc.Tab(item, label=list(AFM_TABS_LABEL_DICT.values())[idx],
                        tab_id=list(AFM_TABS_DICT.values())[idx])
                        for idx, item in enumerate(Spinner_list)]

    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs

def ft_tabs_generate(prefix_app_name):
    Spinner = [spinner_generate(prefix_app_name+"-"+value)
               for value in ["sigma", "FT"]]
    
    Tab_list = [dbc.Tab(item, label=list(FT_TABS_DICT.values())[idx],
                        tab_id=list(FT_TABS_DICT.values())[idx])
                        for idx, item in enumerate(Spinner)]
    
    Tabs = dbc.Tabs(children=Tab_list)

    return Tabs

