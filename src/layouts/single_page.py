from src.layouts.menu import *
import dash_bootstrap_components as dbc

def make_front_page():
    return html.Div([
        dbc.Button(['Menu ', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
        html.H1('Для выбора месторождения или добавления нового, нажмите на кнопку меню.'),
    ], style={"display": "flex", "justify-content": "center", "align-items": "center",})

def make_main_contents():
    return html.Div([
        dbc.Button(['Menu ', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
        html.Header(
            dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
                dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
                dcc.Tab(label="Показатели разработки", value="tab-production-indicators")
            ])),
        html.Div(id="tabs-content")
    ])


Layout = html.Div(
    [
        dcc.Store(id='persistence_storage', storage_type='session'),
        dcc.Download(id='download_excel'),
        dbc.Row([
            html.Span([
                make_menu(),
                html.Span(id='current_field'),
            ]),
            html.Div([
                make_front_page(),
            ], id='main-contents')
        ], style={'display': 'inline'}),

    ])


