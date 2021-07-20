# os package
import datetime
import base64
from unicodedata import name

# framework package
import dash
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Navbar import Navbar
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Nav import Nav
# delay js after loading components rendered
# import dash_defer_js_import as defer_load

# import apps and components
from app import app
from apps.sigma import sigma_app
from apps.notfound import notfound_app
from components.nav.nav import NavBar

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    NavBar,
    html.Div(id="page-content")
], className="container-fluid")


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname): 
    # print("1")
    if pathname == "/app1" or pathname == "/":
        return sigma_app.Layout
    else:
        return notfound_app.NotFoundPage

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.layout = html.Article(defer_load.Import(src="./assets/js/nav-menu.js"))
