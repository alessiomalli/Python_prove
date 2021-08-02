# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 11:57:17 2021

@author: mallia
"""

import dash  #(version 1.12.0)
from dash.dependencies import Input, Output
import dash_table
import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from pages import deltac
from pages import index
from pages import tabella
import re

# -------------------------------------------------------------------------------------
# Import the cleaned data (importing csv into pandas)


directory_all=os.listdir()
directory=[]

j=-1
for i in directory_all:
    #print(i[0:1])
    if i[0:3]=="RUN":
        j=j+1
        directory.append(i)
       # print(j,temp[j])
       
df=pd.DataFrame(directory, columns =['Directory']) #, 'Report', 'Loads']
df['Case R0_Y0']=""
df['Case R55_Y1.5']=""
df['Case R55_Y-10']=""
df['Case']=""

#SCRIVE TUTTE LE SOTTO-DIRECTORY PER OGNI CARTELLA DEL TIPO RUN_*
for i in df['Directory']:
    l=os.listdir(i)
    tmp =0
    for f in l:
        if f.startswith('R0_Y0'):
            tmp=tmp+1
            df.loc[df['Directory']==i,'Case' ]=f
            df.loc[df['Directory']==i,'Case R0_Y0' ]=f
            #df['Case R0_Y0'][df['Directory']==i]=f
            #df['Case'][df['Directory']==i]=fs
        elif f.startswith('R55_Y1.5'):
            tmp=tmp+1
            df.loc[df['Directory']==i,'Case R55_Y1.5' ]=f
            df.loc[df['Directory']==i,'Case' ]=f
            #df['Case R55_Y1.5'][df['Directory']==i]=f
            #df['Case'][df['Directory']==i]=f
        elif f.startswith('R55_Y-10'):
            tmp=tmp+1
            df.loc[df['Directory']==i,'Case' ]=f
            df.loc[df['Directory']==i,'Case R55_Y-10' ]=f
            #df['Case R55_Y-10'][df['Directory']==i]=f
            #df['Case'][df['Directory']==i]=f
    if tmp>1:
        if tmp==2:
            df_mod=pd.concat([df[df['Directory']==i], df[df['Directory']==i]],ignore_index=True)
            if df_mod.loc[0,'Case R55_Y1.5'] and df_mod.loc[0,'Case R0_Y0']:
                df_mod.loc[0,'Case R55_Y1.5']=""
                df_mod.loc[1,'Case R0_Y0']=""
                df_mod.loc[0,'Case']=df_mod.loc[0,'Case R0_Y0']
                df_mod.loc[1,'Case']=df_mod.loc[1,'Case R55_Y1.5']
            if df_mod.loc[0,'Case R55_Y1.5'] and df_mod.loc[0,'Case R55_Y-10']:
                df_mod.loc[1,'Case R55_Y1.5']=""
                df_mod.loc[0,'Case R55_Y-10']=""
                df_mod.loc[0,'Case']=df_mod.loc[0,'Case R55_Y1.5']
                df_mod.loc[1,'Case']=df_mod.loc[1,'Case R55_Y-10']
            if df_mod.loc[0,'Case R0_Y0'] and df_mod.loc[0,'Case R55_Y-10']:
                df_mod.loc[1,'Case R0_Y0']=""
                df_mod.loc[0,'Case R55_Y-10']=""
                df_mod.loc[0,'Case']=df_mod.loc[0,'Case R0_Y0']
                df_mod.loc[1,'Case']=df_mod.loc[1,'Case R55_Y-10']
            
        elif tmp==3:
            df_mod=pd.concat([df[df['Directory']==i], df[df['Directory']==i], df[df['Directory']==i]],ignore_index=True)
            df_mod.loc[0,'Case R55_Y1.5']=""
            df_mod.loc[0,'Case R55_Y-10']=""
            df_mod.loc[1,'Case R55_Y-10']="" 
            df_mod.loc[1,'Case R0_Y0']=""
            df_mod.loc[2,'Case R55_Y1.5']="" 
            df_mod.loc[2,'Case R0_Y0']=""
            df_mod.loc[0,'Case']=df_mod.loc[0,'Case R0_Y0'] 
            df_mod.loc[1,'Case']=df_mod.loc[1,'Case R55_Y1.5']
            df_mod.loc[2,'Case']=df_mod.loc[2,'Case R55_Y-10']

        df=pd.concat([df[df['Directory']<i], df_mod ,df[df['Directory']>i]],ignore_index=True)
        
df.drop(['Case R0_Y0', 'Case R55_Y1.5', 'Case R55_Y-10'], axis = 1, inplace=True)
    
#SCRIVO I PUNTI MAPPA (MP)
df['Roll']=-100
df['Yaw']=-100
df['Umag']=-100
df['Description']="NO"
df['frh']=-100
df['rrh']=-100
df['Steer']=-100
df['Model']="NO"
df['Mannequin']="NO"
df['Simulation']="NO"
df['Reference']="NO"
df['Report']=""
#numbers=[]
for ii in df['Directory']:
    l=os.listdir(ii)
    for ll in l:
        k=os.listdir(ii+'/'+ll)
        for kk in k:
            if kk.startswith('MP'):
                fname=ii+'/'+ll+'/'+kk
                with open(fname) as f:
                    lines = f.readlines()
                    numbers=[]
                    '''
                    for a in lines:
                        tmp = re.findall(r'\d+', a)
                        res = list(map(int, tmp))
                        numbers.append(res)
                    '''
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'frh']=int(lines[0].replace('frh=','' ))
                    #df['frh'][(df['Directory']==ii) & (df['Case']==ll)]=int(lines[0].replace('frh=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'rrh']=int(lines[1].replace('rrh=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Roll']=int(lines[2].replace('roll=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Yaw']=int(lines[3].replace('yaw=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Steer']=int(lines[4].replace('steer=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Umag']=int(lines[5].replace('Umag=','' ))
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Description']=re.findall('"([^"]*)"',lines[13])
                    if "DES=true" in lines[14]:
                        df.loc[(df['Directory']==ii) & (df['Case']==ll),'Simulation']="DES"
                    #elif MANCA CASO CHT e DES TERMICA 
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Model']=lines[11].replace('model=','' )
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Mannequin']=lines[10].replace('mannequin=','' )
                    df.loc[(df['Directory']==ii) & (df['Case']==ll),'Reference']=lines[12].replace('refCase=','' )
            elif kk.startswith('DES'):
                p=os.listdir(ii+'/'+ll+'/'+kk)
                for pp in p:
                    if pp.startswith('report_'):
                        df.loc[(df['Directory']==ii) & (df['Case']==ll),'Report']="C:/Users/MalliA/Desktop/Python_prove/"+ii+'/'+ll+'/'+kk+'/'+pp

def display_report(df):
        links = df['Report'].to_list()
        rows = []
        for x in links:
            link=""
            if x:
                link = '[X](' +str(x) + ')'
            else:
                link= 'O'
            rows.append(link)
        return rows
    
df['Report'] = display_report(df)

dati=df.to_dict('records')


# -------------------------------------------------------------------------------------
# App layout


external_ss = ['css/dash-uber-ride-demo.css']
external_ss = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_ss ) #prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Br() ])
'''
    html.Br(),
    html.Div([
    html.Img(src=app.get_asset_url('logo.png'),style={"padding": "0px","height": "5%", "width": "5%", 'display': 'inline-block'}),
    html.H1('Ducati Corse Aero Team',style={'display': 'inline-block', 'margin':'20px'}),
    ]),
    html.Br(),
    dcc.Link('LOADS', href='/page1', style={"padding": "0px"}),
    html.Br(),
    
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True, 'presentation':'markdown'}
            if i == "Report"
            else {"name": i, "id": i, "deletable": False, "selectable": True ,"hideable": True}
            for i in df.columns
        ],
        data=dati,  # the tmpents of the tableNo documentation available 
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=10,               # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 10, 'maxWidth': 95, 'width': 10
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={                # overflow cells' tmpent into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    )
], style={"padding": "20px"})

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page1(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page1.page_1_layout
    else:
        return '404'
'''

# Page 1 callback
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

# Index Page callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/deltac':
        return deltac.page_1_layout
    elif pathname == '/':
        return index.index_page
    elif pathname == '/tabella':
        return tabella.tab_layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False,port=8050)
