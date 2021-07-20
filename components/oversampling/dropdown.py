import dash_bootstrap_components as dbc

items_list = [
    dbc.DropdownMenuItem("linear"),
    dbc.DropdownMenuItem("Item 2"),
    dbc.DropdownMenuItem("Item 3"),
]

Dropdown = dbc.DropdownMenu(
    id="oversampling-dropdown",
    label="oversampling choice",
    color="primary",
    className="m-1",
    children=items_list
)

