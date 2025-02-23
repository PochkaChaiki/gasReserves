from dash import html
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

from src.constants import *
from src.gas_reserves.constants import *
from src.layouts.components import *


def make_kriterias_table(values: dict,
                         kriteria_name: str,
                         hide_header: bool = False,
                         cell_data_type: str = None,
                         kriteria_cell_editable: bool = True,
                         select_cell_editor: bool = False,
                         cell_editor_params: list = None,
                         aligned_grids: list = None):
    data = values.get(f'kriteria_{kriteria_name}_table', None)
    if data is None:
        data = [{'parameter': VARNAMES_RISKS[kriteria_name],
                 'kriteria': None,
                 'value': 0,
                 'weight': 0}]

    kriteria_header = {
        'headerName': 'Критерий',
        'field': 'kriteria',
        'editable': kriteria_cell_editable,
        'cellDataType': cell_data_type,
    }

    if not kriteria_cell_editable:
        kriteria_header['cellStyle'] = {'background-color': DISABLE_CELL_COLOR}
    if cell_data_type == 'number':
        kriteria_header['valueFormatter'] = {"function": "d3.format('.3f')(params.value)"}
    if select_cell_editor:
        kriteria_header['cellEditor'] = 'agSelectCellEditor'
        kriteria_header['cellEditorParams'] = {'values': cell_editor_params}

    columns = [
        {
            'headerName': 'Показатель',
            'field': 'parameter',
            'cellStyle': {'background-color': DISABLE_CELL_COLOR}
        },
        kriteria_header,
        {
            'headerName': 'Значение',
            'field': 'value',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"},
            'cellStyle': {'background-color': DISABLE_CELL_COLOR},
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
        "stopEditingWhenCellsLoseFocus": True,
    }
    if aligned_grids:
        grid_options['alignedGrids'] = aligned_grids

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
        data = [{'parameter': VARNAMES_RISKS[key], 'value': None}
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
                                     cell_editor_params=list(SEISMIC_EXPLR_WORK_KRITERIAS.keys()),
                                     aligned_grids=[
                                         'kriteria-grid_density-table',
                                         'kriteria-core_research-table',
                                         'kriteria-c1_reserves-table',
                                         'kriteria-hydrocarbon_properties-table',
                                     ]),

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
                                     cell_editor_params=list(HYDROCARBON_PROPERTIES.keys())),

                html.Br(),
                dbc.Button('Произвести расчёты', id='risks_btn', n_clicks=None)
            ]),

        ], class_name='my-2'),
        dbc.Row([
            dbc.Col([
                make_input_group([{'parameter': VARNAMES_RISKS['study_coef'], 'value': study_coef}],
                                 id='study_coef',
                                 style={'height': '100px'},
                                 editable_value=False),
            ]),
            dbc.Col()
        ], class_name='my-2')
    ])