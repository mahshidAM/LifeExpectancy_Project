"""Dashboard Layouts"""
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash_plots import *


def set_header():
    return html.Div(className="header",
                children=[
                    html.H1(
                        children="Life Expectancy", className="header-title"
                    ),
                    html.P(
                        children="Analyze the behavior of avocado prices"
                        " and the number of avocados sold in the US"
                        " between 2015 and 2018",
                        className="header-description",
                    ),
                ],

        )

def set_tableDiv(df):
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
    return html.Div(className='col-8',
                        children= html.Div(                                                                                                                    dcc.Graph(
                                  id='map',
                                  figure=create_map(df)
                                             )
                             ))

def set_chartDiv(df):
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
    

