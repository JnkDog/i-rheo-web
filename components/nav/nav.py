import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_html_components.Div import Div

WEB_LOGO = "assets/imgs/UoG_icon.png"
BAR_ITEMS = ["MOT", "AFM", "BULK", "GT", "FT"]

"""
id (string; Must)
To the bar-itme's name, like Themes
url (string; optional)
Binds the link between the bar-item.
Otherwise, the item binds .../id
"""
def generate_navbar_item(id, url=None):
    # url is not null, modify the href
    if url:
        href = url
    else:
        href = "/" + id.lower()
    
    # TODO needs modify after the project finished
    # if href == "/GT":
    #     item = dbc.NavItem(dbc.NavLink(id, href="/", 
    #                                    className="px-2 text-white active", 
    #                                    active="exact"
    #                                    ))
    # else:
    item = dbc.NavItem(dbc.NavLink(id, href=href, 
                                className="px-2 text-white", 
                                active="partial"
                                ))
    
    return item

NavBar = html.Header(
    dbc.Container(
        dbc.Navbar([
            #  This is the web icon
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=WEB_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                # TODO Change the link later
                href="/gt",
            ),
            html.Div(
                [
                    html.Ul([generate_navbar_item(id) for id in BAR_ITEMS], 
                             className="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0"),
                ],
                className="collapse navbar-collapse"
            ),
            html.Div([dbc.Button("wiki", color="primary", className="mr-1",
                      href="/wiki")], 
                    className="text-end")],
        color="dark",
        dark=True,
        className="navbar navbar-expand-lg navbar-light bg-light nav-pills"
        )
    ),
    className="p-3 bg-dark text-white"
)



# bulma version
# just like react to create component
# NavBar = html.Nav(
#     className='navbar is-white',
#     children=html.Div([
#         html.A(
#             className="navbar-item",
#             children=[
#                 html.Img(src="assets/imgs/icon.png", style={'maxHeight': '70px'}, className="py-2 px-2"),   
#             ],
#         ),
#         html.A(
#             # mobile phone
#             className="navbar-burger",
#             id="burger",
#             children=[html.Span(),html.Span(),html.Span()]
#         ),
#         html.Div(
#             className="navbar-menu", 
#             id="nav-links",
#             children=html.Div(
#                 className="navbar-end",
#                 # children for words
#                 # every link for each app
#                 children=[  html.A(className="navbar-item", children="My Count"), 
#                             html.A(className="navbar-item", children="Shopping  Cart")
#                         ]
#             ) 
#         )
#     ],
#     className="navbar-brand")
# )








