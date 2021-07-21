import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

div_align_style = {
    "height": "100px",
    "lineHeight": "100px",
    "textAlign": "center",
}

span_align_style = {
    "display": "inline-block",
    "verticalAlign": "middle",
    "lineHeight": "normal",
}

NotFoundPage = html.Div(
             [
              html.H1("404 NOT FOUND", className="text-danger", 
                        style=span_align_style), 
              html.H5("Click the navbar to the right place ...", className="text-danger")
              ],
              style=div_align_style
)