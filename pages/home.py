from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pathlib
import base64


# image_filename = 'levana.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#https://secureservercdn.net/50.62.88.172/5xn.794.myftpupload.com/wp-content/uploads/2022/02/levana-logo-white-800x260.png

layout = html.Div([
    # dbc.Row(dbc.Col(html.H1("HOME PAGE", style={'textAlign': 'center'}))),
    # html.Br(),
    html.Div(dbc.Col(dbc.Row(
        html.Img(src='https://media-exp1.licdn.com/dms/image/C4D1BAQFc_flaS1UIww/company-background_10000/0/1630320107555?e=2147483647&v=beta&t=5oLIP2aWhYHJq26Q993TYILD0Gkdkab96WkjqGMJYt8', alt='levana')
    ))),
    #dbc.Row(dbc.Col(html.H4("Select from the directory below.", style={'textAlign': 'center'}))),
    #dbc.Row(dcc.Markdown("""---""")),
    dcc.Markdown("""# *currently in beta* """, style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row(html.H3('Sales Stats', style={'textAlign': 'center'})),
    html.Div(id='page-2-display-value'),
    html.Div(
    children=[
        dbc.Row([
            dcc.Link('Raw Table - All Sales - RandomEarth, Knowhere, LuArt', href='/total_raw', style={'textAlign': 'center'}),
            dcc.Link('Daily Sales - RandomEarth, Knowhere, LuArt', href='/daily_sales_stats', style={'textAlign': 'center'}),
            html.Br(),
            html.Br(),
            dcc.Markdown("""Old Dashboards (Streamlit)""", style={'textAlign': 'center'}),
            dcc.Link('RandomEarth', refresh = True, href='https://share.streamlit.io/kmonee/randomearth-sales-dash/main/sales_app.py', style={'textAlign': 'center'}),
            dcc.Link('Knowhere', refresh = True, href='https://share.streamlit.io/kmonee/knowhere-sales-dash/main/kw_app.py', style={'textAlign': 'center'})

            ], align="center"),        
        ],
    style=dict(display='flex', justifyContent='center'))
], style={"overflow-x": "hidden"})