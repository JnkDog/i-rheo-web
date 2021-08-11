# os package
import datetime
import base64
from os import path
from unicodedata import name

# framework package
import dash
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Navbar import Navbar
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Center import Center
from dash_html_components.Nav import Nav
# delay js after loading components rendered
# import dash_defer_js_import as defer_load

# import apps and components
from app import app

from apps.mot import mot_app
from apps.afm import afm_app
from apps.irheoGT import irheoGT_app
from apps.irheoFT import irheoFT_app
from apps.bulk import bulk_app
from apps.notfound import notfound_app
from apps.wiki import wiki_app
# from apps.bulk import bulk_app
from components.nav.nav import NavBar
from components.support import supportIntro

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    NavBar,
    html.Div(id="page-content")
], className="container-fluid")

IndexLayout = html.Div([
    html.Div(html.H1("Support to Use the Website"), style={"text-align": "center"}),
    html.Br(),
    supportIntro.GeneralHelp,
    html.Br(),
    supportIntro.SupportHelp,
    html.Br(),
    supportIntro.InputHelp,
    html.Br(),
    supportIntro.OversamplingHelp,
    html.Br(),
    supportIntro.DownloadHelp,
    html.Br(),
    supportIntro.FigHelp,
    html.Br(),
    ]   
)

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname): 
    pathname = pathname.lower()
    
    # TODO need to modify
    if pathname == "/" or pathname == "/index":
        return IndexLayout
    if pathname == "/bulk":
        bulk_app.Layout
    if pathname == "/afm":
        # return afm_app.Layout
        return afm_app.Layout
    if pathname == "/mot":
        return mot_app.Layout
    if pathname == "/ft":
        return irheoFT_app.Layout
    elif pathname == "/bulk":
        return bulk_app.Layout
    elif pathname == "/wiki":
        return wiki_app.Layout
    elif pathname == "/gt":  # or pathname == "/":
        return irheoGT_app.Layout
    else:
        return notfound_app.NotFoundPage

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.layout = html.Article(defer_load.Import(src="./assets/js/nav-menu.js"))
