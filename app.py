import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


# app = Dash(__name__, suppress_callback_exceptions=True)
# server = app.server

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True
                )

server = app.server