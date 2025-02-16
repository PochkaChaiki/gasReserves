from src.layouts.menu import *
import dash_bootstrap_components as dbc


def make_front_page():
    return dbc.Container([
        dbc.Row(
            dbc.Col([html.H1('Вероятностная оценка перспективности разработки месторождения газа.', className='text-center'),
                     html.Img(src='/assets/main_logo.png')]),
            align='center', class_name='my-auto align-middle'
        )
    ], style={'display': 'flex', 'flex-grow': '1', 'align-contents': 'center'})

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
        dbc.Container([
            html.Div([
                dbc.Button(['Меню ', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
                html.Span([
                    make_menu(),
                    html.Span(id='current_field', style={'float': 'right'}, className='pe-3 my-2'),
                ]),
            ], className='px-3'),
            html.Div([
                make_front_page(),
            ], id='main-contents', className='p-3', style={'display': 'flex', 'flex-grow': '1', 'flex-direction': 'column'}),
        ], class_name='py-3', fluid=True, style={'min-height': '100vh', 'display': 'flex', 'flex-direction': 'column'})

    ])


