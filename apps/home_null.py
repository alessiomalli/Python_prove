# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:21:40 2021

@author: mallia
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pathlib
from app import app
import plotly.express as px
import dash  #(version 1.12.0)
from dash.dependencies import Input, Output
import dash_table
import os
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import re


layout = html.Div([
    #html.Img(src=app.get_asset_url('logo.png'),style={"padding": "0px","height": "5%", "width": "5%", 'display': 'inline-block'}),
    html.H1('READY TO RACE'),
    ], style={ 'position': 'absolute', 'top': '50%', 'left': '50%', 'margin-right': '-50%', 'transform': 'translate(-50%, -50%)' })


