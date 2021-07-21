import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from algorithm.pwft import fttest

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = html.Div([
#     dcc.Graph(
#         id='ft-fig',
#         figure=fttest()
#     ),
# ], style={'margin': 100})


@app.callback(
    Output('ft-store', 'data'),

    # in upload button
    )
def store_ft_data():
    data = fttest() # fttest(factor)
    return data


def store_oversampled_data(n_clicks, content, oversamping_number):
    data = fttest(oversamping_number)
    return data 


if __name__ == '__main__':
    app.run_server(debug=True)
