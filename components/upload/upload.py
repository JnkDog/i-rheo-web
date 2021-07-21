import dash_html_components as html
import dash_core_components as dcc

# This is templates but used in irheo GT
Upload = dcc.Upload(
    html.Button('Upload File', className="btn btn-primary"),
    id="upload",
    accept='.txt, .csv',
    # modify the upload file name
    filename="raw data"
)

def upload_component_generate(id):
    return dcc.Upload(    
        html.Button('Upload File', className="btn btn-primary"),
        id=id,
        accept='.txt, .csv',
        # modify the upload file name
        filename="raw data"
    )



