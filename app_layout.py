"""Dashboard Layouts"""
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from app_plot import *


def set_header():
    """
    Returns header layout   
    """
    return html.Div(className="header",
                children=[
                    html.H1(
                        children="Life Expectancy", className="header-title"
                    ),
                    html.P(
                        children=["Life expectancy (at birth) indicates the number of years a newborn infant would live if prevailing patterns of mortality at the time of its birth were to stay the same throughout its life."
                        " The data is published by the ",
                                  html.A('THE WORD BANK', target='_blank', href='https://data.worldbank.org/indicator/SP.DYN.LE00.IN?end=2019&most_recent_year_desc=false&start=1960&view=map&year=2019')
                                ],
                        className="header-description",
                    ),
                ],

        )

def set_tableDiv(df):
    """
    Returns table layout   
    Inputs - dataframe=df
    """
    return html.Div(className='col-4 lifeExptable',
       children= [
         html.Article(className='card',children= [
                         html.Div(className='card-header',
                                     children= html.A(id='csv-button', n_clicks=0, className='fas fa-file-csv fa-2x download', href="/urlToDownload/")                                                 
                                 ),
                         html.Div(className='card-body text-secondary',
                                  children=generate_table(df)
                                 )
                 ])
           ])

def set_mapDiv(df):
    """
    Returns map layout  
    Inputs - dataframe=df
    """
    return html.Div(className='col-8',
                        children= html.Div(                                                                                                                    dcc.Graph(
                                  id='map',
                                  figure=create_map(df)
                                             )
                             ))

def set_chartDiv(df):
    """
    Returns lineChart layout   
    Inputs - dataframe=df
    """
    countries = df.country.unique()
    return html.Div(className='col-12',
                   children= [
                     html.Article(className='card', 
                                 children= [
                                     html.Div(className='card-header',#html.H2('Life Expectancy,'),
                                             children=[
                                                        html.Div([
                                                            dcc.Dropdown(
                                                                id='countries-dropdown',
                                                                options=[{'label': c, 'value': c} for c in countries],
                                                                multi=True,
                                                                value=['United States','France','Japan'],
                                                                placeholder="Add a Country" 
                                                                
                                                            )
                                                        ])
                                                      ]),
                                     html.Div(className='card-body text-secondary',
                                               children=                                                                                                                 dcc.Graph(
                                                      id='line-chart',
                                                      figure=create_lineChart(df,['United States','France','Japan']))
                                             )]
                                 )]
                  )
    

