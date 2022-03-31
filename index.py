import dash
from dash import Dash, dcc, html, Input, Output, callback
#import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages; the following two are the only things you adjust in this file if you add new pages
from pages import home, total_raw_sales, daily_sales_stats
pages_dict = {'home':home, 'total_raw_sales':total_raw_sales, 'daily_sales_stats':daily_sales_stats}


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if str(pathname).replace('/', '') not in pages_dict.keys(): #use this first to check if the page exists or not
        return '404! This page does not exist.'
    else:
        for key, value in pages_dict.items(): #then return the page
            if pathname == f'/{key}':
                return value.layout

if __name__ == '__main__':
    app.run_server(debug=True)