import dash_html_components as html
import dash_core_components as dcc

Upload = dcc.Upload(
    html.Button('Upload File', className="btn btn-primary"),
    id="upload",
    accept='.txt, .csv',
    # modify the upload file name
    filename="raw data"
)

# vitrtual line version
# Upload = dcc.Upload(
#     id='upload-file',
#     children=html.Div([
#         'Drag and Drop or ',
#         # className'is-uppercase',
#         html.A('Select Files', className='is-uppercase'),
#     ],
#     className='has-text-weight-bold'),
#     style={
#         'width': '100%',
#         'height': '60px',
#         'lineHeight': '60px',
#         'borderWidth': '1px',
#         'borderStyle': 'dashed',
#         'borderRadius': '5px',
#         'textAlign': 'center',
#         'margin': '10px'
#     },
#     accept='.txt,.pdf',
# )


