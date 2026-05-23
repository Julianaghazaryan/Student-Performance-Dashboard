import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


dash.register_page(__name__, path='/interactive')


try:
    df = pd.read_csv('Student_data.csv')
    df.columns = df.columns.str.strip()
except Exception as e:
    df = pd.DataFrame({
        'Study_Hours_Per_Day': [2, 4, 6, 8, 1.2, 5, 7, 3],
        'Attendance_Pct': [90, 80, 95, 70, 66.7, 85, 90, 60],
        'Final_CGPA': [2.4, 3.0, 3.6, 3.9, 3.59, 2.8, 3.4, 2.6],
        'Gender': ['Female', 'Male', 'Female', 'Male', 'Male', 'Female', 'Male', 'Female'],
        'Major': ['Engineering', 'Business', 'Engineering', 'Engineering', 'Business', 'Business', 'Engineering', 'Business']
    })

available_majors = df['Major'].unique() if 'Major' in df.columns else ['Engineering']


layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("📊 Ուսանողների Առաջադիմության Ինտերակտիվ Վերլուծություն", className="mb-4 text-center mt-3"), width=12)
    ]),
    
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.B("🕹️ Կառավարման Վահանակ")),
                dbc.CardBody([
                    html.Label("Ընտրեք Մասնագիտությունը (Major):"),
                    dcc.Dropdown(
                        id='department-dropdown',
                        options=[{'label': str(m), 'value': str(m)} for m in available_majors],
                        value=available_majors[0],
                        clearable=False,
                        className="mb-3"
                    ),
                    html.Label("Ուսման նվազագույն ժամեր (օրական):"),
                    dcc.Slider(
                        id='hours-slider',
                        min=0,
                        max=15,
                        step=0.5,
                        value=0,
                        marks={i: str(i) for i in range(0, 16, 2)},
                        className="mb-3"
                    )
                ])
            ], className="mb-3"),
            
         
            dbc.Card([
                dbc.CardHeader(html.B("📈 Ընթացիկ Վիճակագրություն")),
                dbc.CardBody([
                    html.Div([
                        html.Span("Ուսանողների քանակը: ", className="text-muted"),
                        html.B(id='student-count-display', className="text-primary float-end")
                    ], className="mb-2"),
                    
                    html.Div([
                        html.Span("Միջին CGPA: ", className="text-muted"),
                        html.B(id='avg-gpa-display', className="text-success float-end")
                    ], className="mb-2"),
                    
                    html.Hr(),
                    
                    html.Div([
                        html.Small("🔗 Կորելացիա (Ժամեր vs CGPA):", className="text-muted d-block mb-1"),
                        html.Div(id='correlation-display', className="badge bg-info text-wrap w-100 p-2")
                    ])
                ])
            ], className="mb-3")
        ], width=4),
        
        
        dbc.Col([
            
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='dynamic-scatter')
                ])
            ], className="mb-3"),
            
            
            dbc.Card([
                dbc.CardHeader(html.B("🌡️ Գործոնների Կորելացիոն Մատրից (EDA Heatmap)")),
                dbc.CardBody([
                    dcc.Graph(id='eda-heatmap')
                ])
            ])
        ], width=8)
    ])
], fluid=True)


@dash.callback(
    [Output('student-count-display', 'children'),
     Output('avg-gpa-display', 'children'),
     Output('correlation-display', 'children'),
     Output('dynamic-scatter', 'figure'),
     Output('eda-heatmap', 'figure')], 
    [Input('department-dropdown', 'value'),
     Input('hours-slider', 'value')]
)
def update_dashboard(selected_major, min_hours):
    x_col = 'Study_Hours_Per_Day'
    y_col = 'Final_CGPA'
    size_col = 'Attendance_Pct'
    color_col = 'Gender'
    major_col = 'Major'

    
    filtered_df = df[(df[major_col].astype(str) == str(selected_major)) & (df[x_col] >= min_hours)]
    
   
    if filtered_df.empty:
        empty_fig = px.scatter(title="Այս պայմաններով ուսանող չգտնվեց")
        return "0 հոգի", "0.00", "Տվյալ չկա", empty_fig, empty_fig
            
    student_count = len(filtered_df)
    avg_gpa = filtered_df[y_col].mean()
    
    
    if student_count > 1:
        corr_val = filtered_df[x_col].corr(filtered_df[y_col])
        corr_text = "Բավարար չէ" if pd.isna(corr_val) else f"r = {corr_val:.2f}"
    else:
        corr_text = "Բավարար չէ"
    
    
    fig_scatter = px.scatter(
        filtered_df, 
        x=x_col, 
        y=y_col, 
        color=color_col,
        size=size_col,
        title=f'{selected_major} Ուսանողների Առաջադիմությունը',
        labels={x_col: 'Օրական ուսման ժամեր', y_col: 'Վերջնական CGPA'},
        category_orders={color_col: ["Male", "Female"]}
    )
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20), hovermode='closest')
    
    
    numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) > 1 and student_count > 1:
        corr_matrix = filtered_df[numeric_cols].corr()
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto='.2f', 
            aspect="auto",
            color_continuous_scale='RdBu_r', 
            zmin=-1, zmax=1,
            title=f"Գործոնների փոխկապակցվածությունը {selected_major}-ում"
        )
        fig_heatmap.update_layout(margin=dict(l=40, r=20, t=40, b=40))
    else:
        fig_heatmap = px.scatter(title="Heatmap-ի համար տվյալները քիչ են")

    return f"{student_count} հոգի", f"{avg_gpa:.2f}", corr_text, fig_scatter, fig_heatmap
