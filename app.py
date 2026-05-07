import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
   
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Գլխավոր", href="/")),
            dbc.NavItem(dbc.NavLink("Վերլուծություն", href="/analysis")),
            dbc.NavItem(dbc.NavLink("Ինտերակտիվ", href="/interactive")),
        ],
        brand="Student Performance Dashboard",
        color="primary",
        dark=True,
        className="mb-4"
    ),

    
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)