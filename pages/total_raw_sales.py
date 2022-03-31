from types import NoneType
from dash import dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve() #FILE LOCATION

#global df
df = pd.read_json('http://165.22.125.123/total_raw.json', lines=True).fillna(value='N/A') #THE FILE NAME


layout = html.Div(
    dbc.Container([
        dbc.Row(dbc.Col(html.H1("CSV BUILDER - SALES", style={'textAlign': 'center'}))),
        dbc.Row(dbc.Col(html.H4("Tracking sales from all 3 marketplaces", style={'textAlign': 'center'}))),
        dbc.Row(dcc.Markdown("""---""")),

        #Tab 1
        dcc.Tabs([
        dcc.Tab(label='DataFrame', children=[
            dbc.Row(dbc.Col()),
            html.Br(),
            dbc.Row(html.H3('Raw Table', style={'textAlign': 'center'})),
            html.Br(),
            
            #table building - start
            dbc.Row(dbc.Col([
            dbc.Container([
            dash_table.DataTable(
                id='tbl',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                ],
                #data=df.to_dict('records'), #passing the dataframe as dictionary format
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 25,
                style_table={'height':'500px', 'overflowY': 'auto', 'minWidth': '10%', 'width': '100%', 'maxWidth': '100%'})
            #dbc.Alert(id='tbl_out', color='secondary'),
            ])
            ])),
            html.Div([
                html.Button("Download Table as CSV", id="btn_csv"),
                dcc.Download(id="download-dataframe-csv")], style=dict(display='flex', justifyContent='center'))
            ]),

        #Tab 2
        dcc.Tab(label='Table Builder', children=[
            html.P(id='subgroup_select'),
            html.Br(),
            html.H3('DataTable Builder', style={'textAlign': 'center'}),
            html.P('Select row values to INCLUDE in the datatable', style={'textAlign': 'center'}),
            html.Br(),
            dbc.Row([ 
                html.P('Marketplace'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(df['MARKET'].unique()), id='column_select_1', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.P('NFT Type'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(df['NFT_TYPE'].unique()), id='column_select_2', multi=True, placeholder='None'),
                ], style={'padding': 20, 'flex': 10})
                ))),
                html.P('Rarity'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(df['RARITY'].unique()), id='column_select_3', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.P('Faction'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(df['FACTION'].unique()), id='column_select_4', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.P('Loot Type'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(df['LOOT_TYPE'].unique()), id='column_select_5', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.Div(style={'padding': 50, 'flex': 1})
            ])
        ])

        #end tab
        
        ]),

    #table building - end

    dbc.Row(dcc.Markdown("""---""")),
    html.Div(
    children=[dcc.Link('Go to Home', href='/home', style={'textAlign': 'center'})],  # fill out your Input however you need
    style=dict(display='flex', justifyContent='center')),
    html.Div(style={'padding': 25, 'flex': 1})
    
], fluid=False))

# @callback(
#     Output('tbl', 'data'), 
#     Input('tbl', 'active_cell')
# )
# def update_graphs(active_cell):
#     return str(active_cell) if active_cell else "Click the table"

@callback(
    Output('tbl', 'data'),
    [Input('column_select_1', 'value'),
    Input('column_select_2', 'value'),
    Input('column_select_3', 'value'),
    Input('column_select_4', 'value'),
    Input('column_select_5', 'value')]
    
)

def selective_filter_column(one, two, three, four, five):

    global df
    df = pd.read_json('http://165.22.125.123/total_raw.json', lines=True).fillna(value='N/A')
    data = df.to_dict('records')
    for key, value in {'MARKET':one, 'NFT_TYPE':two, 'RARITY':three, 'FACTION':four, 'LOOT_TYPE':five}.items():
        if value != [] and value != None:
            df = df[df[key].isin(value)]
            data = df[df[key].isin(value)].to_dict('records')
    return data

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, "raw_data_manipulated.csv")
            


    