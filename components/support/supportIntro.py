import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components.download.download import download_component_generate
from components.oversampling.switch import switch_component_generate

GeneralHelp = html.Div(
    dcc.Markdown('''
        # General
        Use the perscribed format of file.

        For more information on the principles and details please go to the wiki page.
    ''')
)

SupportHelp = html.Div([
    dcc.Markdown('''
        ## Upload button
        Click the "Load Example data" button to use our example data for test.

        Click the "Upload File" button to use your own data.

        ***Attention:*** The data you upload should in the format we have perscribed.
    '''),
    html.Div([
        html.Button('Upload File', className="btn btn-primary"),
        html.Button("Load Example data", className="btn btn-primary", style={"margin": "5px"}),
    ]),
    ],
)

InputHelp = html.Div([
    dcc.Markdown('''
        ## Boundary Condition & Input Parameters
        After you change your file to our prescribed format. You have to enter your own boundary values and parameterss.

        We have set some default value to make sure the app can run.

        You can change these values and do/redo the following operations.
    '''),
    html.Div([
        dbc.Input(
            type="number",
            placeholder="Input your first number, default 1"
        ),
        html.Br(),
        dbc.Input(
            type="number",
            placeholder="Input your second number, default 0"
        )
    ], style={"width": "25%"}),
    ],
)

ParameterHelp = html.Div([
    dcc.Markdown('''
        
    '''),
    html.Div([

    ]),
    ],
)

OversamplingHelp = html.Div([
    dcc.Markdown('''
        ## Oversampling
        Oversampling Times number: The number of dots you want to add between two raw datas.

        Output Points number: The number you want to show in the figure.

        Oversampling/Refresh Button: Start to do the oversampling operation with the numbers your input or default.

        ***Attention:*** The data used in this operation is your Row Data.

        Oversampling Render: Switch the figures to oversampled one and move back.
    '''),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Oversampling times number", className="mr-2"),
                dbc.Input(type="number", placeholder="default 10"),
            ],
        ),
        dbc.FormGroup(
            [
                dbc.Label("Output points number", className="mr-2"),
                dbc.Input(type="number", placeholder="default 100"),
            ],        
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(dbc.Button("Oversampling", color="primary")), 
                ),
                dbc.Col(
                    html.Div(dbc.Button("Refresh", color="secondary")),
                ),
            ],
        ),
        html.Br(),
        switch_component_generate("Index"),
    ], style={"width": "25%"}),
    ]
)

DownloadHelp = html.Div([
    dcc.Markdown('''
        ## Download
        Choose a type of file your want to download.

        Your can downlaod all.
    '''),
    html.Div(download_component_generate("Index"), style={"width": "25%"})
    ]
)

FigHelp = html.Div([
    dcc.Markdown('''
        ## Figure Tab & Axis change
        Switch between tabs to view different images.

        Use the checklist under the figres to change axis between "log-log" and "linear-log".
    '''),
    html.Div([

    ]),
    ]
)