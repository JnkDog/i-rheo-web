import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

InputValue = html.Div([
    html.P("Input the x value"),
    dbc.Input(id="input", placeholder="Type something...", type="number")
])

def input_component_generate(id, style={"marginTop": "10px"}, 
                             placeholder="Type number ...", type="number", 
                             p_message=None):
    return  html.Div([
                # html.P(p_message) if p_message is not None else None,
                dbc.Input(id=id, placeholder=placeholder, type=type)
                ], style=style)