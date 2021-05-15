"""Visualizations(plotly) for dash."""

import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def generate_table(df):
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
        ],
        page_size=15,
        style_cell={'padding': '5px',#'textAlign': 'right',
                   'fontSize':12,'whiteSpace': 'normal',
                   'height': 'auto'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=df.to_dict('records'),
        sort_action="native",
    )

def create_map(df):
    df1 = df.query("year == 2007")
    print(df1)
    '''data = df.query("year == 2007")
    #fig = go.Figure(go.Scattergeo())
    fig = px.choropleth(data, locations='code',
                    color="value", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)'''
    fig = px.choropleth(df1,  # Input Pandas DataFrame
                    locations="code",  # DataFrame column with locations
                    color="value",  # DataFrame column with color values
                    hover_name="country") # DataFrame column hover info) # Set 


    
    return fig

def create_chart():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    
    return fig



