from dash import html
from src.layouts.components import *
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

def make_kriterias_table(values: dict,
                         kriteria_name: str,
                         hide_header: bool = False,
                         cell_data_type: str = None,
                         kriteria_cell_editable: bool = True,
                         select_cell_editor: bool = False,
                         cell_editor_params: list = None,
                         ):
    data = values.get(f'kriteria_{kriteria_name}_table', None)
    if data is None:
        data = [{'parameter': varnamesRisks[kriteria_name],
                 'kriteria': None,
                 'value': 0,
                 'weight': 0}]

    kriteria_header = {
        'headerName': 'Критерий',
        'field': 'kriteria',
        'editable': kriteria_cell_editable,
        'cellDataType': cell_data_type
    }

    if cell_data_type == 'number':
        kriteria_header['valueFormatter'] = {"function": "d3.format('.3f')(params.value)"}
    if select_cell_editor:
        kriteria_header['cellEditor'] = 'agSelectCellEditor'
        kriteria_header['cellEditorParams'] = {'values': cell_editor_params}

    columns = [
        {'headerName': 'Показатель', 'field': 'parameter'},
        kriteria_header,
        {
            'headerName': 'Значение',
            'field': 'value',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"},
        },
        {
            'headerName': 'Вес',
            'field': 'weight',
            'editable': True,
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"},
        },
    ]


    grid_options = {
        'rowSelection': 'single',
        "stopEditingWhenCellsLoseFocus": True,
    }

    table_style = {
        'height': '95px'
    }
    if hide_header:
        grid_options['headerHeight'] = 0
        table_style['height'] = '45px'

    return dag.AgGrid(
        id=f'kriteria-{kriteria_name}-table',
        columnDefs=columns,
        rowData=data,
        defaultColDef={'editable': False, 'sortable': False, 'filter': False},
        dashGridOptions=grid_options,
        columnSize='responsiveSizeToFit',
        style=table_style
    )


def make_input_params_table(values: dict):
    data = values.get('parameter_table_risks', None)
    if data is None:
        data = [{'parameter': varnamesRisks[key], 'value': None}
                for key in ('exploration_wells_amount', 'distance_from_infra')]
    return dbc.Col(
        make_input_group(data, 'risks', style={'height': '135px'})
    )


def render_risks_and_uncertainties(data):
    study_coef = data.get('study_coef', '')

    return html.Div([
        dbc.Row([
            dbc.Col([
                make_input_params_table(data),
            ]),
            dbc.Col([
                make_kriterias_table(values=data,
                                     kriteria_name='seismic_exploration_work',
                                     cell_data_type='string',
                                     select_cell_editor=True,
                                     cell_editor_params=list(seismic_exploration_work_kriterias.keys())),

                make_kriterias_table(values=data,
                                     kriteria_name='grid_density',
                                     cell_data_type='string',
                                     kriteria_cell_editable=False,
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='core_research',
                                     cell_data_type='number',
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='c1_reserves',
                                     cell_data_type='number',
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='hydrocarbon_properties',
                                     cell_data_type='string',
                                     hide_header=True,
                                     select_cell_editor=True,
                                     cell_editor_params=list(hydrocarbon_properties.keys())),

                html.Br(),
                dbc.Button('Произвести расчёты', id='risks_btn', n_clicks=None)
            ]),

        ]),
        dbc.Row([
            html.Span([
                html.H3('Критерий изученности, д.е.: '),
                html.H3(study_coef, id='study_coef')
            ])
        ])
    ])