from src.layouts.components import *
from src.constants import *

import dash_bootstrap_components as dbc
from dash import html, dcc

def make_filtr_resistance_indics(frs_A: list, frs_B: list):
    data = [{'parameter': VARNAMES_INDICATORS['filtr_resistance_A'],
             'P10': frs_A[0], 'P50': frs_A[1], 'P90': frs_A[2]},
            {'parameter': VARNAMES_INDICATORS['filtr_resistance_B'],
             'P10': frs_B[0], 'P50': frs_B[1], 'P90': frs_B[2]}]
    return make_indics_table('Полученные коэффициенты сопротивления',
                             data,
                             'filtr_resistance',
                             editable=False, digits=7)

def make_production_indicators_inputs(values: dict):
    keys_with_indics = ['effective_thickness', 'geo_gas_reserves']
    keys_to_collapse = ['filtr_resistance_A','filtr_resistance_B',
                        'critical_temp', 'critical_pressure']

    keys_to_omit = {'permeability', 'annual_production', 'PIPE_ROUGHNESS',
                    'init_num_wells', 'COEF_K', 'ADIABATIC_INDEX', 'lambda_trail',
                    'lambda_fontain', 'macro_roughness_l', 'density_athmospheric',
                    'porosity_coef', 'gas_saturation_coef', 'trail_roughness'}

    data: list[dict] = values.get('parameter_table_indics', [])
    keys_not_to_include = set(keys_to_collapse) | set(keys_with_indics) | keys_to_omit
    if len(data) == 0:
        for key in list(VARNAMES_INDICATORS.keys()):
            if key not in keys_not_to_include:
                data.append({'parameter': VARNAMES_INDICATORS[key], 'value': None})
    else:
        keys = [row['parameter'] for row in data]
        keys_to_add = REVERSED_VARNAMES_INDICATORS.keys() - set(keys)
        for key in list(REVERSED_VARNAMES_INDICATORS.keys()):
            if (REVERSED_VARNAMES_INDICATORS[key] not in keys_not_to_include
                    and key in keys_to_add):
                data.append({'parameter': key, 'value': None})

    stat_indics_data = values.get('parameter_table_stat_indics', None)
    if stat_indics_data is None:
        stat_indics_data = [
            {'parameter': VARNAMES_INDICATORS[key], 'value': None} for key in
                ('effective_thickness', 'geo_gas_reserves',
                 'porosity_coef', 'gas_saturation_coef')
        ]

    data_to_collapse: list[dict] = values.get('parameter_table_indics_collapse', [])
    if len(data_to_collapse) == 0:
        data_to_collapse = [
            {'parameter': VARNAMES_INDICATORS[key], 'value': None}
            for key in keys_to_collapse
        ]
    else:
        keys = [
            REVERSED_VARNAMES_INDICATORS[row['parameter']]
            for row in data_to_collapse
        ]

        keys_to_add = set(keys_to_collapse) - set(keys)
        for key in keys_to_collapse:
            if key in keys_to_add:
                data_to_collapse.append(
                    {'parameter': VARNAMES_INDICATORS[key], 'value': None}
                )

    return dbc.Col([
        distribution_input(VARNAMES_INDICATORS['permeability'],
                           "permeability",
                           "Проницаемость",
                           values.get('p_permeability', None)),

        html.Div(make_input_group(data, 'indics'), className='my-2'),
        dbc.Accordion([
            dbc.AccordionItem([
                html.Div(make_indics_table(None,
                                  stat_indics_data,
                                  'stat_indics',
                                  True), className='my-2'),
                html.Div(make_input_group(data_to_collapse, 'indics_collapse'), className='my-2'),
                html.A('Показать рассчитанные значения', n_clicks=None,
                       className='m-2 link-secondary link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover',
                       id='filtr_resistance_link'),
                dbc.Collapse([
                    make_filtr_resistance_indics(values.get('filtr_resistance_A', [None, None, None]),
                                                 values.get('filtr_resistance_B', [None, None, None]))
                ],
                    id='filtr_resistance_indics', is_open=False, class_name='m-2')

            ], title='Дополнительные параметры')
        ],
            start_collapsed=True,
            always_open=True,
            class_name='my-2'
        ),
        dbc.Button('Произвести расчёт', id='prod_calcs', n_clicks=0, class_name='my-2')
    ])


def make_prod_calcs_table(values: dict = None):
    data = values.get('prod_calcs_table', None)
    if data is None:
        data = [
            [{
                'year': '',
                'avg_production': '',
                'kig': '',
                'annual_production': '',
                'current_pressure': '',
                'wellhead_pressure': '',
                'n_wells': '',
                'ukpg_pressure': '',
                'cs_power': '',
            }] for _ in range(3)
        ]
    columns = [
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['year'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['year'],
            'field': 'year',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['avg_production'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['avg_production'],
            'field': 'avg_production',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['kig'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['kig'],
            'field': 'kig',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['annual_production'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['annual_production'],
            'field': 'annual_production',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['current_pressure'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['current_pressure'],
            'field': 'current_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['wellhead_pressure'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['wellhead_pressure'],
            'field': 'wellhead_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['downhole_pressure'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['downhole_pressure'],
            'field': 'downhole_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['n_wells'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['n_wells'],
            'field': 'n_wells',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['ukpg_pressure'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['ukpg_pressure'],
            'field': 'ukpg_pressure',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
        {
            'headerName': SHORTNAMES_VARNAMES_INDICATORS['cs_power'],
            'headerTooltip': DISPLAY_VARNAMES_INDICATORS['cs_power'],
            'field': 'cs_power',
            'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.2f')(params.value)"}
        },
    ]
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dag.AgGrid(
                    id = f'prod_calcs_table_{profile_id}',
                    columnDefs = columns,
                    rowData = data[i],
                    defaultColDef = {
                        "editable": False,
                        "sortable": False,
                        "filter": False
                    },
                    dashGridOptions = {
                        "stopEditingWhenCellsLoseFocus": True,
                        # "domLayout": "autoHeight"
                    },
                    columnSize = 'responsiveSizeToFit',
                    style={'height': '400px'},
                ),
                title = f'{profile_id} таблица'
            ) for profile_id, i in zip(('P10', 'P50', 'P90'), range(3))
        ],
        start_collapsed=True,
        always_open=True
    )


def make_prod_indics_plots(values: dict):
    pressures_fig = values.get('pressures_on_stages_plot', None)
    pressures_diagram = html.Div(id='pressures-graph')
    if pressures_fig is not None:
        pressures_diagram.children = [
            dcc.Graph(figure=pressures_fig),
        ]

    prod_kig_fig = values.get('prod_kig_plot', None)
    prod_kig_diagram = html.Div(id='prod-kig')
    if prod_kig_fig is not None:
        prod_kig_diagram.children = [
            dcc.Graph(figure=prod_kig_fig),
        ]

    return dbc.Row([
        pressures_diagram,
        prod_kig_diagram
    ])


def render_production_indicators(data):
    return html.Div([
        dbc.Row([
            dbc.Col(make_production_indicators_inputs(data)),
            dbc.Col(make_prod_calcs_table(data)),
        ], class_name='my-2'),
        dbc.Row([
            make_prod_indics_plots(data)
        ], class_name='my-2')
    ])
