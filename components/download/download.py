import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from components.input.input import input_component_generate

begin_line_input_cfg = {
    "id": "begin-line-number",
    "placeholder": "Type begin number ...",
    "type": "number"
}

end_line_input_cfg = {
    "id": "end-line-number",
    "placeholder": "Type end number ...",
    "type": "number"
}

BeginLineInput = input_component_generate(**begin_line_input_cfg)
EndLineInput   = input_component_generate(**end_line_input_cfg)

Download = html.Div([
         html.H5("Download Data"),
         BeginLineInput,
         EndLineInput,
         html.Button("Download File", id="download-btn", 
                     className="btn btn-primary", 
                     style={"marginTop": "10px"}), 
         dcc.Download(id="download-text"),
         html.Div(id="download-message")   
])

# TODO provides a Downlaod genereate function
def download_component_generate():
    Download = html.Div()
    return Download