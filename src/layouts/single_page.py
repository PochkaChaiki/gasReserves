from src.layouts.menu import *
import dash_bootstrap_components as dbc

Layout = html.Div(
    [
        dcc.Store(id='persistence_storage', storage_type='session'),
        dcc.Download(id='download_excel'),
        dbc.Row([
            make_menu(),
            html.Div([
                dbc.Button(['Menu', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
                html.Header(
                    dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
                        dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
                        dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
                    ])),
                html.Div(id="tabs-content")
            ])
        ], style={'display': 'inline'}),

    ])