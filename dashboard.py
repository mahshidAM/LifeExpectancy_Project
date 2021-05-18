"""Interactive Dashboard dash/plotly"""
from dash.dependencies import Output, Input

import flask
from flask import send_file, make_response, Response
from io import *

from dashboard_layouts import *
from dash_data import *

# external JavaScript files
external_scripts = [
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
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
    }
]

df = get_DataFrame() #load and clean data

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container main', children=[
                               set_header(), #dashboard header
                               html.Div(className='row main-row',  # Define the row element
                                       children=[
                                          set_tableDiv(df),  # Define the left element(table)
                                          set_mapDiv(df)  # Define the right element(map)
                                        ]),
                                html.Div(className='row main-row',  # Define the row element
                                          children = set_chartDiv(df)  # Define the bottom element(line chart)
                                        )

                            ])

@app.callback(Output('line-chart', 'figure'),[Input('countries-dropdown', 'value')])
def update_graph(selected_country):
    return create_lineChart(df,selected_country)

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