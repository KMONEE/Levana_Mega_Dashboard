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
grouping_1 = ['DAY', 'MARKET', 'NFT_TYPE', 'RARITY']
grouping_2 = grouping_1 + ['NFT_LUNA_PRICE', 'NFT_UST_PRICE_AT_PURCHASE']

def daily(df_master, group_master):
    df = pd.read_json('http://165.22.125.123/total_raw.json', lines=True).fillna(value='N/A') #THE FILE NAME
    daily_df = df[df_master].groupby(group_master).aggregate(
        TOTAL_TRANSACTIONS_MADE=('NFT_LUNA_PRICE', 'count'),
        MAX_LUNA_PRICE=('NFT_LUNA_PRICE','min'),
        MIN_LUNA_PRICE=('NFT_LUNA_PRICE','max'),
        MEDIAN_LUNA_PRICE=('NFT_LUNA_PRICE','median'),
        AVERAGE_LUNA_PRICE=('NFT_LUNA_PRICE','mean'),
        TOTAL_LUNA_TRADED=('NFT_LUNA_PRICE','sum'),
        MAX_UST_PRICE=('NFT_UST_PRICE_AT_PURCHASE','min'),
        MIN_UST_PRICE=('NFT_UST_PRICE_AT_PURCHASE','max'),
        MEDIAN_UST_PRICE=('NFT_UST_PRICE_AT_PURCHASE','median'),
        AVERAGE_UST_PRICE=('NFT_UST_PRICE_AT_PURCHASE','mean'),
        TOTAL_UST_TRADED=('NFT_UST_PRICE_AT_PURCHASE','sum'),
        TOTAL_LUNA_CUMULATIVE=('NFT_LUNA_PRICE','sum'),
        TOTAL_UST_CUMULATIVE=('NFT_UST_PRICE_AT_PURCHASE','sum')).reset_index()
    return daily_df

daily_df = daily(grouping_2, grouping_1)

layout = html.Div(
    dbc.Container([
        dbc.Row(dbc.Col(html.H1("CSV BUILDER - DAILY SALES STATS", style={'textAlign': 'center'}))),
        dbc.Row(dbc.Col(html.H4("Tracking sales from all 3 marketplaces", style={'textAlign': 'center'}))),
        dbc.Row(dcc.Markdown("""---""")),

        #Tab 1
        dcc.Tabs([
        dcc.Tab(label='DataFrame', children=[
            dbc.Row(dbc.Col()),
            html.Br(),
            dbc.Row(html.H3('Daily Stats Table', style={'textAlign': 'center'})),
            html.Br(),
            
            #table building - start
            dbc.Row(dbc.Col([
            dbc.Container([
            dash_table.DataTable(
                id='daily_tbl',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in daily_df.columns
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
            html.Br(),
            html.Div([
                html.Button("Download Table as CSV", id="btn_daily_csv"),
                dcc.Download(id="download-daily-csv")], style=dict(display='flex', justifyContent='center'))
            ]),

        #Tab 2
        dcc.Tab(label='Table Builder', children=[
            html.P(id='subgroup_select'),
            html.Br(),
            html.H3('DataTable Builder', style={'textAlign': 'center'}),
            html.P('Select row values to INCLUDE in the datatable', style={'textAlign': 'center'}),
            html.Br(),
            dbc.Row([
                html.P('Columns'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(['DAY', 'MARKET', 'NFT_TYPE', 'RARITY'], id='column_select_0', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.P('Marketplace'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(daily_df['MARKET'].unique()), id='column_select_1', multi=True, placeholder='None')
                ], style={'padding': 20, 'flex': 1})
                ))),
                html.P('NFT Type'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(daily_df['NFT_TYPE'].unique()), id='column_select_2', multi=True, placeholder='None'),
                ], style={'padding': 20, 'flex': 10})
                ))),
                html.P('Rarity'),
                    html.Div(dbc.Col(dbc.Container(
                html.Div([
                    dcc.Dropdown(list(daily_df['RARITY'].unique()), id='column_select_3', multi=True, placeholder='None')
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
    Output('daily_tbl', 'data'),
    [Input('column_select_0', 'value'),
    Input('column_select_1', 'value'),
    Input('column_select_2', 'value'),
    Input('column_select_3', 'value')]
    
)

def selective_filter_column(zero, one, two, three):

    global daily_df


    if zero == None:
        zero = ['DAY', 'MARKET', 'NFT_TYPE', 'RARITY']
    
    grouping_2 = zero + ['NFT_LUNA_PRICE', 'NFT_UST_PRICE_AT_PURCHASE']
    daily_df = daily(grouping_2, zero)
    data = daily_df.to_dict('records')
        

    column_select_dict = {}
    for key, value in {'MARKET':one, 'NFT_TYPE':two, 'RARITY':three}.items():
        if key in zero:
            column_select_dict[key] = value


    for key, value in column_select_dict.items():
        if value != [] and value != None:
            daily_df = daily_df[daily_df[key].isin(value)]
            data = daily_df[daily_df[key].isin(value)].to_dict('records')
    return data

@callback(
    Output("download-daily-csv", "data"),
    Input("btn_daily_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(daily_df.to_csv, "daily_sales.csv")
            


    