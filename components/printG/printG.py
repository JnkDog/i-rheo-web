import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from algorithm.pwft import fttest

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dcc.Graph(
        id='ft-fig',
        figure=fttest()
    ),
], style={'margin': 100})


@app.callback(
    Output('ft-fig', 'figure'),
    )
def switch_ftfigure():
    if button == on:
        return original-Figure
    else:
        return oversampled-Figure


if __name__ == '__main__':
    app.run_server(debug=True)
