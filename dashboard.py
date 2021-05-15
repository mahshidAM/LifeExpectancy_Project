"""Interactive dash/plotly dashboard"""
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dashboard_plots import *
import flask
from flask import send_file, make_response, Response
from io import *


# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    },
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    },
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]

graph = create_chart()

df = pd.read_csv('data/API_SP_clean.csv', sep=',', encoding='utf8', engine='python')
map_graph = create_map(df)

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container main', children=[
                               html.Div(className='row main-row',  # Define the row element
                                       children=[
                                          html.Div(className='col-4',
                                                   children= [
                                                     html.Article(className='card', 
                                                                 children= [
                                                                     html.Div(className='card-header',
                                                                             children=[ 
                                                                                 html.H2('Life Expectancy'),
                                                                                 html.P(children=html.A(id='csv-button', n_clicks=0, className='fas fa-file-csv fa-2x download', href="/urlToDownload/") 
                                                                                       )]                                                 
                                                                                                
                                                                             ),
                                                                     html.Div(className='card-body text-secondary',
                                                                              children=generate_table(df)
                                                                             )
                                                                         ])
                                                   ]),  # Define the left element(table)
                                          html.Div(className='col-8',
                                                   children= [
                                                     html.Article(className='card', 
                                                                 children= [
                                                                     #html.Div(className='card-header',
                                                                     #        children=html.H2('Map')
                                                                     #        ),
                                                                     html.Div(className='card-body text-secondary',
                                                                             children=                                                                                                                                   dcc.Graph(
                                                                                      id='map',
                                                                                      figure=map_graph)
                                                                             )]
                                                                 )]
                                                  )  # Define the right element(map)
                                      ]),
                                html.Div(className='row main-row',  # Define the row element
                                       children=[
                                          html.Div(className='col-12',
                                                   children= [
                                                     html.Article(className='card', 
                                                                 children= [
                                                                     html.Div(className='card-header',
                                                                             children=html.H2('Chart')
                                                                             ),
                                                                     html.Div(className='card-body text-secondary',
                                                                               children=                                                                                                                                   dcc.Graph(
                                                                                      id='example-graph',
                                                                                      figure=graph)
                                                                             )]
                                                                 )]
                                                  ),  # Define the bottom element(chart)
                                         
                                      ])

                            ])

@app.server.route('/urlToDownload/') 
def download_csv():
    """
    Return flask make_response (download file)
    Call back from download button in html
    """
    response = make_response(df.to_csv())
    response.headers["Content-Disposition"] = f"attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
            
        
'''def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')'''

def run_app():
    app.run_server()    
    """Timer(1, open_browser).start();
    app.logger.setLevel(logging.DEBUG)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=2000)"""