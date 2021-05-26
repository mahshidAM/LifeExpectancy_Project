"""Visualizations(plotly/dash)"""

import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app_data import *


def get_groupedYearData(country,df):
    """
    Returns dataframe filtered by country and grouped by year (for lineCharts)
    Inputs - country=country, dataframe=df
    """
    grouped_df = df[df['country'] == country].groupby('year')['value'].sum().reset_index()
    return grouped_df


def generate_table(df):
    """
    Returns Dash dataTable   
    Inputs - dataframe=df
    """
    return dash_table.DataTable(
        id='table',
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns
        ],
        page_size=14,
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
            'lineHeight': '14px'
        },
        style_table={'height': '500px', 'overflowY': 'auto'},
        style_cell_conditional=[
            {
                'if': {'column_id': 'country'},
                'fontWeight': 'bold',
                'textAlign': 'left'
            }
        ],
        data=df.to_dict('records'),
        sort_action="native",
    )

def create_map(df):
    """
    Returns plotly map   
    Inputs - dataframe=df
    """
    #geojson=get_countries_geo(df)
    #geojson = px.data.gapminder()
    #print(geojson)
    fig = px.choropleth(df,               
              height=600,
              locations='country_code',
              color='value',
              hover_name="country",  
              animation_frame="year", 
              color_continuous_scale='Viridis'
    )
    #fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    title_text='Life Expectancy(1961 to 2018)', title_x=0.5,
    coloraxis_colorbar=dict(title="Years"),
    geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        coloraxis_colorbar_x=-0.15
    )
    
    return fig

def create_lineChart(df, selected):
    """
    Returns countries geojson for plotly map   
    Inputs - dataframe=df, countries=selected
    """
    # Create figure
    fig = go.Figure()

    for name in selected:
        data = get_groupedYearData(name,df)
        fig.add_trace(go.Scatter(x=data['year'], y=data['value'],
                    mode='lines',
                    name=name))
        
    # Set title, layouts, styles
    fig.update_layout(
        title_text="Life Expectancy "+str(df.year.min()) + " to " + str(df.year.max()),
        xaxis=dict(
            gridcolor='rgb(243, 243, 243)',
            type='linear',
            gridwidth=2,
        ),
        yaxis=dict(     #template="plotly_dark"
            gridcolor='rgb(243, 243, 243)',
            gridwidth=2,
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=700,
            hovermode='x unified'
        )
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    # style all the traces
    fig.update_traces(
        line={"width": 1.5},
        marker={"size": 6},
        mode="lines+markers"
    )
    
    return fig
    



