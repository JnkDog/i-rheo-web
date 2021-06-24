"""
TODO(Chen) layout for this web           ok
TODO(Chen) encryption for message   
TODO(Chen) Read txt                      ok
TODO(Chen) Change txt to render          
TODO(Chen) science represent    
TODO(Chen) how to draw line
TODO(Chen) import file and render        ok
TODO(Chen) Web Router
TODO(Chen) Data duration                 ok  
"""

# os package
from calendar import c
import datetime
import base64
from unicodedata import name

# framework package
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# delay js after loading components rendered
# import dash_defer_js_import as defer_load

# team components
from components.nav.nav import NavBar
from components.upload.upload import Upload
from components.input.input import InputValue
from components.display.spinner import Spinner

# Algorithms
from drawing import drawing

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        NavBar,
        dbc.Row([
            dbc.Col(
                [
                    html.Div([
                        html.H5("Support .txt"),
                        Upload,
                        html.Div(id="upload_message")
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Key Parameters"),
                        InputValue
                    ]),
                    html.Hr(),
                    html.Div([
                        html.H5("Commands"),
                        dbc.Button("Calculate", id="calculate", color="primary", style={"margin": "5px"})
                    ])
                ], 
            width=3
            )
        , dbc.Col([Spinner], width=True)
        ])
    ],
    className="container-fluid"
)

# Be caution about the different between [Output] and Output
# Also the Input and Output !!!
@app.callback(
    [
        Output("display", "figure"),
        Output("upload_message", "children")
    ],
    Input("calculate", "n_clicks"),
    State("upload", "contents"),
    State("input", "value"),
    State("upload", "filename"),
    # dont call the func when first loaded
    prevent_initial_call=True
)
def data_process(n_clicks, contents, input_value, name):
    # print(contents)
    # print(type(contents))
    fig = drawing(contents, input_value)
    # print(type(value))  
    if contents is None:
        name = "Please chosse a file"

    message = html.Div([
        html.H6(name)
    ])

    return [fig, message]

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.layout = html.Article(defer_load.Import(src="./assets/js/nav-menu.js"))
