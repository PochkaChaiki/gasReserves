from src.layouts.menu import *
import dash_bootstrap_components as dbc


def make_front_page():
    return dbc.Container([
        dbc.Row(
            [
                html.Div([
                    html.Div([
                        html.H1('ВЕРОЯТНОСТНАЯ ОЦЕНКА ПЕРСПЕКТИВНОСТИ РАЗРАБОТКИ МЕСТОРОЖДЕНИЙ УГЛЕВОДОРОДОВ',
                                className='text-center', style={
                                'color': 'white',
                                'font-family': 'Verdana',
                                'font-size': '4.4vh',
                                'text-shadow': '1px 1px 10px black',
                            }),
                    ], style={
                        'padding': '12px',
                        'background-color': 'rgba(0, 38, 84, 0.5)',
                        'border-radius': '25px',
                        'width': '75%',
                        'max-width': '1344px',
                    }),
                ], style={
                    'display': 'flex',
                    'justify-content': 'center',
                    'position': 'absolute',
                    'left': '0px', 'bottom': '15%',
                }),

                html.Img(src='/assets/background.jpg',
                         style={
                             'padding': '0px',
                             'object-fit': 'cover',
                             'position': 'absolute',
                             'top': '0px', 'left': '0px',
                             'min-height': '100vh', 'max-height': '100vh',
                             'min-width': '100vw', 'max-width': '100vw',
                             'z-index': '-2'
                         }),
                html.Div([
                    html.Img(src='/assets/logos.png',
                             width='638px',
                             height='140px',
                             ),
                ], style={
                    'display': 'flex',
                    'position': 'absolute',
                    'justify-content': 'center',
                    'left': '0px', 'top': '0px',
                })
            ],
            align='center', class_name='my-auto'
        )
    ], style={'display': 'flex', 'flex-grow': '1', 'align-contents': 'center', 'z-index': '-1'})

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
        dcc.Store(id='notification_store', storage_type='memory'),
        dcc.Store(id='excel_store_not_to_use', storage_type='memory'),
        dcc.Store(id='for_fields_comparison', storage_type='memory'),
        dcc.Store(id='for_fields_comparison_checkboxes', storage_type='session'),
        html.Div(id='notifications'),
        dbc.Container([
            html.Div([
                dbc.Button(['Меню ', html.I(className="bi bi-list")], id='toggle_menu', n_clicks=0),
                html.Span([
                    make_menu(),
                    html.Span(id='current_tab', style={'display': 'none'}),
                    html.Span(id='current_field', style={'float': 'right'}, className='pe-3 my-2'),
                ]),
            ], className='px-3'),
            html.Div([
                make_front_page(),
            ], id='main-contents', className='p-3', style={'display': 'flex', 'flex-grow': '1', 'flex-direction': 'column'}),
        ], class_name='py-3', fluid=True, style={'min-height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'z-index': '1'})

    ])


