import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

Loading = dcc.Loading(
          children=[html.Div(html.Div(id="loading-test"))],
          id="FT-loading",
          fullscreen=True,
          type="default",
        #   debug=True,
)