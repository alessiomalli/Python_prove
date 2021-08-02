import dash
import dash_bootstrap_components as dbc

external_ss = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_ss , suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
