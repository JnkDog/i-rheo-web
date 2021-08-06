import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def trap_radius_generate(prefix_app_name):
    kt_id = prefix_app_name + "-kt"
    at_id = prefix_app_name + "-at"

    MOTInput = html.Div([
        dbc.Input(
            id=kt_id,
            type="number",
            placeholder="Input trap stiffness, default 1e-6"
        ),
        html.Br(),
        dbc.Input(
            id=at_id,
            type="number",
            placeholder="Input radius, default 1e1"
        )
    ]) 

    TrapAndRadius = html.Div([
        html.H5("Trap stiffness and radius"),
        MOTInput,
        html.Br()
    ])

    return TrapAndRadius
