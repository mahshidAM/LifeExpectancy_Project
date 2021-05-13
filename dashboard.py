"""Interactive flask/plotly dashboard"""
from flask import Flask, render_template,request , send_file, send_from_directory, make_response, Response, redirect,jsonify
import os
import io
import pandas as pd
import numpy as np
import webbrowser
from threading import Timer
import logging
#from dashboard_plots import *
#from dashboardDB import *


db = DashboardDB()

app = Flask(__name__)

            
def open_browser():
    webbrowser.open_new('http://127.0.0.1:2000/')

def run_app():
    Timer(1, open_browser).start();
    app.logger.setLevel(logging.DEBUG)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=2000)