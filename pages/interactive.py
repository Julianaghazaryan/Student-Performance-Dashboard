import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/interactive')

df = pd.read_csv('Student_data.csv')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("Ուսանողների բաշխումն ըստ տարիքի"),
            dcc.Input(id="age-input", type="number", placeholder="Մուտքագրիր տարիքը", className="mb-3"),
            dcc.Graph(id='age-hist')
        ])
    ])
])

@callback(
    Output('age-hist', 'figure'),
    Input('age-input', 'value')
)
def update_hist(age_val):
    data = df if age_val is None else df[df['Age'] >= age_val]
    return px.histogram(data, x="Final_CGPA", title="GPA-ի բաշխումը", color_discrete_sequence=['indianred'])