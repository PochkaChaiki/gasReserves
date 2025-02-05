from dash import html
from src.layouts.components import *
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

def make_kriterias_table(values: dict,
                         kriteria_name: str,
                         hide_header: bool = False,
                         cellDataType: str = None,
                         select_cell_editor: bool = False,
                         cell_editor_params: list = None,
                         ):
    data = values.get(f'kriteria_{kriteria_name}_table', None)
    if data is None:
        data = [{'parameter': varnamesRisks[kriteria_name],
                 'kriteria': None,
                 'value': 0,
                 'weight': 0}]


    columns = [{'headerName': 'Показатель', 'field': 'parameter'}]
    if select_cell_editor:
        columns.append(
            {
                'headerName': 'Критерий',
                'field': 'kriteria',
                'editable': True,
                'cellEditor': 'agSelectCellEditor',
                'cellDataType': cellDataType,
                # 'cellEditorPopup': True,
                'cellEditorParams': {
                    'values': cell_editor_params
                },
            },
        )
    else:
        columns.append({'headerName': 'Критерий', 'field': 'kriteria', 'editable': True, 'cellDataType': cellDataType})

    columns.extend([
        {'headerName': 'Значение', 'field': 'value', 'cellDataType': 'number'},
        {'headerName': 'Вес', 'field': 'weight', 'editable': True, 'cellDataType': 'number'},
    ])


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
                                     cellDataType='string',
                                     select_cell_editor=True,
                                     cell_editor_params=list(seismic_exploration_work_kriterias.keys())),

                make_kriterias_table(values=data,
                                     kriteria_name='grid_density',
                                     cellDataType='number',
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='core_research',
                                     cellDataType='number',
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='c1_reserves',
                                     cellDataType='number',
                                     hide_header=True),

                make_kriterias_table(values=data,
                                     kriteria_name='hydrocarbon_properties',
                                     cellDataType='string',
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