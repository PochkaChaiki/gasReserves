from dash import html, dcc
import dash_bootstrap_components as dbc

def make_menu() -> dbc.Offcanvas:
    return dbc.Offcanvas([
        dbc.Card([
            dbc.CardBody([
                dbc.Stack([], id='menu_nav', gap=1),
                dbc.Button(['Добавить месторождение', html.I(className='bi bi-plus-square')],
                           id='open_field_modal',
                           n_clicks=None,
                           color='success'
                           ),
                html.Br(),
                dbc.Button(['Сравнительный анализ', html.I(className='bi bi-search')],
                           id='analyze_fields',
                           n_clicks=None,
                           color='primary')
            ]),
            dbc.CardFooter([
                dbc.Button([
                    'Сохранить',
                    html.I(className='bi bi-download')
                ], id='save_btn', n_clicks=0),
                dbc.Button([
                    'Экспорт Отчёта Excel',
                    html.I(className='bi bi-file-earmark-spreadsheet')
                ], id='download_btn', n_clicks=0),
                dbc.Button(id='update_fields_btn', n_clicks=0, style={'display': 'none'}),
                dcc.Upload(dbc.Button('Загрузить', id='upload_btn', n_clicks=0), id='load_save'),
            ])
        ]),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Введите название месторождения'), close_button=True),
            dbc.ModalBody([
                dbc.Input(placeholder='Месторождение...', type='text', id='field_name', required=True),
            ]),
            dbc.ModalFooter([
                dbc.Button('Добавить', id='add_field', color='success', n_clicks=0),
            ])
        ], is_open=False, id='add_field_modal'),
        dcc.Download(id='download_save'),


    ], is_open=False, id='menu')



def make_field_item(field_name: str):
    hashed_id = str(hash(field_name))
    return dbc.Row([
        dbc.ButtonGroup([
            dbc.Button(html.I(className='bi bi-trash'),
                       id={'type': 'delete_item', 'index': f'delete_{hashed_id}'},
                       color='danger',
                       class_name='col-2'),
            dbc.Button(field_name,
                       id={'type': 'open_field', 'index': f'open_{hashed_id}'},
                       className='col-10', color='secondary', outline=True),
        ])
    ], className='row', id=hashed_id)


