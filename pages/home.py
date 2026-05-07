import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H2("EduDash Նախագիծ")),
                dbc.CardBody([
                    html.P("Բարի գալուստ ուսանողների առաջադիմության վերլուծության հարթակ:"),
                    html.P("Այս dashboard-ը ստեղծվել է Assignment 3-ի շրջանակներում:"),
                    dbc.Button("Անցնել Վերլուծությանը", href="/analysis", color="primary")
                ])
            ], className="mt-4")
        ], width=12)
    ])
])