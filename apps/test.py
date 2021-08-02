# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 10:54:01 2021

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

ind=pd.DataFrame({"Cat": ["Total", "Mannequin", "Radiators", "Wheels", "Fairing", "Ventilation", "Oil and Water", "No"], "String": ["Tot", "Mann", "Rad", "whe", "Fair", "Vent","oil","No"]})
coeffs="Mannequin"

string=(ind.loc[ind["Cat"]==coeffs,"String"]).to_string(index=False)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_pickle(DATA_PATH.joinpath("df.pkl"))

case_chosen=df['Case'][0]
run_chosen=df['Directory'][0]
case_chosen2=df['Case'][1]
run_chosen2=df['Directory'][1]

dfg = df[(df['Case'] == case_chosen) & (df["Directory"] == run_chosen)]
dfg2 = df[(df['Case'] == case_chosen2) & (df["Directory"] == run_chosen2)]

string = (ind.loc[ind["Cat"] == coeffs, "String"]).to_string(index=False)



coll = [col for col in dfg.columns if string in col]
dfg_1 = dfg[coll]
dfg_2 = dfg2[coll]
dfg_1.reset_index(inplace = True,drop=True)
dfg_2.reset_index(inplace = True,drop=True)
dfg_2=dfg_2.round(1)

