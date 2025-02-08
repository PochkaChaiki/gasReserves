from src.layouts.menu import *
import dash_bootstrap_components as dbc


def make_front_page():
    return dbc.Container([
        dbc.Row(
            dbc.Col(html.H1('Для выбора месторождения или добавления нового, нажмите на кнопку меню.')),
            align='center',
        )
    ])

def make_main_contents():
    return html.Div([
        html.Header(
            dcc.Tabs(id="tabs-calcs", value="tab-reserves-calcs", children=[
                dcc.Tab(label="Подсчёт запасов", value="tab-reserves-calcs"),
                dcc.Tab(label="Показатели разработки", value="tab-production-indicators"),
                dcc.Tab(label="Риски и неопределённости", value="tab-risks-and-uncertainties")
            ])),
        html.Div(id="tabs-content")
    ])



Layout = html.Div(
    [
        dcc.Store(id='persistence_storage', storage_type='session'),
        dcc.Download(id='download_excel'),
        html.Div([
            dbc.Row([

                html.Div([
                    dbc.Button(['Menu ', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
                    html.Span([
                        make_menu(),
                        html.Span(id='current_field'),
                    ]),
                    html.Div([
                        make_front_page(),
                    ], id='main-contents')
                ], style={'display': 'inline'})

            ], style={'display': 'inline'}),
        ])

    ])


