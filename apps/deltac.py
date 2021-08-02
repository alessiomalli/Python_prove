# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 12:43:34 2021

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
from dash.dependencies import Input, Output, State
import dash_table
import os
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import time
from dash.exceptions import PreventUpdate
import re


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_pickle(DATA_PATH.joinpath("df.pkl"))
ind=pd.DataFrame({"Cat": ["Total", "Mannequin", "Radiators", "Wheels", "Fairing", "Ventilation", "Oil", "Water", "No"], "String": ["Tot", "MannequinC", "Rad", "whe", "Fair", "Vent","oil","wat","No"]})

layout = html.Div([
    html.H1('Delta Coefficienti', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="RUN 1", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='run-dropdown', clearable=False,
                persistence=True, persistence_type='session',

                options=[{'label': x, 'value': x}
                         for x in sorted(df["Directory"].unique())]
            )
        ],  # className='ten columns'
            style={'width': '20%'}),

        html.Div([
            html.Pre(children="Case", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='case-dropdown', clearable=False,
                persistence=True, persistence_type='session',
                # df.loc[(df['Directory']==ii),'Case']
                options=[{'label': x, 'value': x}
                         for x in sorted(df["Case"].unique())],
            )
        ],  # className='six columns'
            style={'width': '20%'}),
    ], className='row'),

    html.Div([
        html.Div([
            html.Pre(children="RUN 2", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='run-dropdown2', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x}
                         for x in sorted(df["Directory"].unique())]
            )
        ],  # className='ten columns'
            style={'width': '20%'}),

        html.Div([
            html.Pre(children="Case", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='case-dropdown2', clearable=False,
                persistence=True, persistence_type='session',
                # df.loc[(df['Directory']==ii),'Case']
                options=[{'label': x, 'value': x}
                         for x in sorted(df["Case"].unique())],
            )
        ],  # className='six columns'
            style={'width': '20%'}),
    ], className='row'),

    html.Br(),
    
    html.Div([
        html.Div([
            html.Pre(children="Coefficients", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='coeffs', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x} for x in sorted(ind["Cat"].unique())],
            )
        ],  # className='six columns'
            style={'width': '20%'}),
        
        html.Div([
            html.Pre(children="Decimals", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='decs', clearable=False,
                persistence=True, persistence_type='session',
                options=[{'label': x, 'value': x}
                         for x in range(3,10)],
                value=5
            )
        ],  # className='six columns'
            style={'width': '20%'}),
    ], className='row'),
    
    html.Br(),
    
    html.Div([html.Button('Click here to see the content', id='show-secret',n_clicks=None)]),    

    html.Br(),
    html.Br(),
    html.H4('Showing: RUN 1 - RUN 2', style={"textAlign": "center"}),
    html.Br(),
    html.Div(id="div-1"),
])

@app.callback(
    Output(component_id='div-1', component_property='children'),
     [Input(component_id='run-dropdown', component_property='value'),
     Input(component_id='case-dropdown', component_property='value'),
     Input(component_id='run-dropdown2', component_property='value'),
     Input(component_id='case-dropdown2', component_property='value'),
     Input(component_id='coeffs', component_property='value'), 
     Input(component_id='decs', component_property='value'),
     Input(component_id='show-secret', component_property='n_clicks')],[State(component_id='show-secret', component_property='n_clicks')])

def display_value(run_chosen, case_chosen, run_chosen2, case_chosen2, coeffs, decs, n_clicks, stato):
    if n_clicks is None:
        raise PreventUpdate
    else:
        #n_clicks=None
        dfg = df[(df['Case'] == case_chosen) & (df["Directory"] == run_chosen)]
        dfg2 = df[(df['Case'] == case_chosen2) & (df["Directory"] == run_chosen2)]
        string = (ind.loc[ind["Cat"] == coeffs, "String"]).to_string(index=False)
        coll = [col for col in dfg.columns if string in col]
        dfg_1 = dfg[coll]
        dfg_2 = dfg2[coll]
        dfg_1.reset_index(inplace=True, drop=True)
        dfg_2.reset_index(inplace=True, drop=True)
        deltas = dfg_1-dfg_2
        deltas = deltas.round(decimals=decs)
        data = deltas.to_dict('rows')
        columns =  [{"name": i, "id": i,} for i in (deltas.columns)]
        #return 'The button has been clicked {} times'.format(n_clicks),
        return html.Div([ html.Div(dash_table.DataTable(data=data, columns=columns)),])

    
'''
 [
        dash_table.DataTable(
            id='table2',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
                for i in deltas.columns
            ],
            data=deltas.to_dict('delta_Coefficients'),  # the tmpents of the tableNo documentation available
            editable=True,              # allow editing of data inside all cells
            # allow filtering of data by user ('native') or not ('none')
            filter_action="native",
            # enables data to be sorted per-column by user or not ('none')
            sort_action="native",
            sort_mode="single",         # sort across 'multi' or 'single' columns
            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
            # choose if user can delete a row (True) or not (False)
            row_deletable=True,
            selected_columns=[],        # ids of columns that user selects
            selected_rows=[],           # indices of rows that user selects
            page_action="native",
            page_current=0,             # page number that user is on
            page_size=10,               # number of rows visible per page
            style_cell={                # ensure adequate header width when text is shorter than cell's text
                'minWidth': 10, 'maxWidth': 300, 'width': 30, "padding": "4px"
            },
            style_data={                # overflow cells' tmpent into multiple lines
                'whiteSpace': 'normal',
                'height': 'auto'
            })]
'''