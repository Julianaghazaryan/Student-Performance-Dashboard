import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/analysis')

df = pd.read_csv('Student_data.csv')
df.columns = df.columns.str.strip()

layout = dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.Label("Ընտրիր Մասնագիտությունը:"),
                dcc.Dropdown(
                    id='major-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Major'].unique()],
                    value=df['Major'].unique()[0],
                    clearable=False,
                    className="mb-3"
                ),
                html.Label("Ուսման ժամերի Slider:"),
                dcc.Slider(
                    id='analysis-hours-slider',  # ⬅️ Փոխվեց
                    min=df['Study_Hours_Per_Day'].min(),
                    max=df['Study_Hours_Per_Day'].max(),
                    value=df['Study_Hours_Per_Day'].min(),
                    marks={i: str(i) for i in range(int(df['Study_Hours_Per_Day'].max()) + 1)},
                    step=0.5
                ),
            ])
        ], className="p-3")
    ], width=4),

    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H4("Միջին Final CGPA", className="card-title"),
                html.H2(id="analysis-avg-gpa-display", className="text-success")  # ⬅️ Փոխվեց
            ])
        ], className="mb-4 text-center"),
        dcc.Graph(id='success-scatter')
    ], width=8)
])

@callback(
    [Output('success-scatter', 'figure'),
     Output('analysis-avg-gpa-display', 'children')],  # ⬅️ Փոխվեց
    [Input('major-dropdown', 'value'),
     Input('analysis-hours-slider', 'value')]  # ⬅️ Փոխվեց
)
def update_analysis(selected_major, min_hours):
    filtered_df = df[(df['Major'] == selected_major) & (df['Study_Hours_Per_Day'] >= min_hours)]
    fig = px.scatter(
        filtered_df, x="Study_Hours_Per_Day", y="Final_CGPA",
        color="Gender", size="Attendance_Pct",
        title=f"GPA vs Study Hours ({selected_major})",
        template="plotly_white"
    )
    avg_gpa = filtered_df['Final_CGPA'].mean()
    return fig, f"{avg_gpa:.2f}" if not pd.isna(avg_gpa) else "N/A"
