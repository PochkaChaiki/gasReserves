from dash import callback, Output, Input, State, ctx, no_update, dcc
import pandas as pd

from utils import *

from gas_reserves.constants import *
from gas_reserves.plot import *
from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *

from layout import *




@callback(
    output=[
        [
            Output('prod_calcs_table_P10', 'rowData'),
            Output('prod_calcs_table_P50', 'rowData'),
            Output('prod_calcs_table_P90', 'rowData'),
        ],
        Output('pressures-graph', 'children'),
        Output('prod-kig', 'children'),
        Output('persistence_storage', 'data', allow_duplicate=True),
    ],
    
    inputs=[
        Input('prod_calcs', 'n_clicks'),
        State('parameter-table-permeability', 'rowData'),
        State('parameter-table-indics', 'rowData'),
        State('parameter-table-indics_collapse', 'rowData'),
        State('parameter-table-stat_indics', 'rowData'),
        State('persistence_storage', 'data'),
    ],
    prevent_initial_call=True,
)
def calculate_production_indicators(n_clicks: int, 
                                    p_permeability: list[dict], 
                                    p_indics: list[dict], 
                                    p_indics_collapse: list[dict], 
                                    p_stat_indics: list[dict], 
                                    storage_data: dict):
    if n_clicks is None or n_clicks == 0 or ctx.triggered_id != 'prod_calcs':
        return [[no_update for _ in range(3)], no_update, no_update, no_update]

    _, permeability_params = *parse_params(dist_dict[p_permeability[0]['distribution']], p_permeability[0]),
    stat_params = {"permeability": permeability_params}
    stat_perm = generate_stats(stat_params, 3000)
    
    permeability_Pinds = st.scoreatpercentile(stat_perm['permeability'], [10, 50, 90])

    init_data = {}
    for el in p_indics:
        if el['value'] is not None:
            init_data[reversed_varnamesIndicators[el['parameter']]] = el['value']

    for el in p_indics_collapse:
        if el['value'] is not None:
            init_data[reversed_varnamesIndicators[el['parameter']]] = el['value']

    stat_indics_data = {}
    for row in p_stat_indics:
        stat_indics_data[row['parameter']] = {'P90': row['P90'], 'P50': row['P50'], 'P10': row['P10']}

    prod_kig_fig = None
    pressures_graphs = []
    results_list = []
    save_filtr_resistance_A, save_filtr_resistance_B = None, None
    for perm, name in zip(permeability_Pinds, ['P10', 'P50', 'P90']):
        init_data['permeability'] = perm
        init_data['effective_thickness'] = stat_indics_data[varnamesIndicators['effective_thickness']][name]
        init_data['geo_gas_reserves'] = stat_indics_data[varnamesIndicators['geo_gas_reserves']][name]
        init_data['porosity_coef'] = stat_indics_data[varnamesIndicators['porosity_coef']][name]
        init_data['gas_saturation_coef'] = stat_indics_data[varnamesIndicators['gas_saturation_coef']][name]

        input_data = make_init_data_for_prod_indics(pd.DataFrame(init_data, index=["value"]))

        result = calculate_indicators(input_data.to_dict('records')[0])
        result['year'] = [i for i in range(1, len(result.index)+1)]
        result['avg_production'] = result['annual_production'] / result['n_wells']

        results_list.append(result.to_dict('records'))
        pressures_df = result[['current_pressure', 'wellhead_pressure', 'ukpg_pressure']]
        pressures_df['downhole_pressure'] = result['current_pressure'] - input_data.loc['value', 'max_depression']
        pressures_graphs.append(plot_pressure_on_production_stages(pressures_df, name))
        prod_kig_fig = plot_summary_chart(prod_kig_fig, result[['annual_production', 'kig', 'n_wells']], name)

        if name == 'P50':
            save_filtr_resistance_A, save_filtr_resistance_B = input_data['filtr_resistance_A']['value'], input_data['filtr_resistance_B']['value']
    

    pressures_fig = plot_united_pressures(pressures_graphs)

    save_data = save_tab_production_indicators(storage_data=storage_data,
                                               field_name='Месторождение1',
                                               p_permeability=p_permeability,
                                               parameter_table_indics=p_indics,
                                               parameter_table_stat_indics=p_stat_indics,
                                               parameter_table_indics_collapse=p_indics_collapse,
                                               prod_calcs_table=results_list,
                                               pressures_on_stages_plot=pressures_fig,
                                               prod_kig_plot=prod_kig_fig,
                                               filtr_resistance_A=save_filtr_resistance_A,
                                               filtr_resistance_B=save_filtr_resistance_B)
    
    return [results_list, 
            dcc.Graph(figure=pressures_fig), 
            dcc.Graph(figure=prod_kig_fig), 
            save_data]





