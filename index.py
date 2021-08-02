import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import tabella,deltac,home_null


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
    html.Img(src=app.get_asset_url('logo.png'),style={"padding": "0px","height": "5%", "width": "5%", 'display': 'inline-block'}),
    html.H1('Ducati Corse Aero Team',style={'display': 'inline-block', 'margin':'20px'}),
    ]),
    html.Div([
        dcc.Link('Tabella|', href='/apps/tabella'),
        dcc.Link('Delta Coefficienti', href='/apps/deltac'),
    ], className="row"),
    html.Div(id='page-content', children=[])
], style={"padding": "20px"})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/deltac':
        return deltac.layout
    elif pathname == '/apps/tabella':
        return tabella.layout
    elif pathname == '/':
        return home_null.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
