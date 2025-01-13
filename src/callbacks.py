from dash import Input, Output, State, callback, ALL, dcc
from dash.exceptions import PreventUpdate

from layout import *
from gas_reserves.plot import *
from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *

from utils import *

@callback(
    Output('parameter-table-area', 'columnDefs'),
    Input('parameter-table-area', 'cellValueChanged'),
    State('parameter-table-area', 'rowData')
)
def update_table_area(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-effective_thickness', 'columnDefs'),
    Input('parameter-table-effective_thickness', 'cellValueChanged'),
    State('parameter-table-effective_thickness', 'rowData')
)
def update_table_effective_thickness(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-porosity_coef', 'columnDefs'),
    Input('parameter-table-porosity_coef', 'cellValueChanged'),
    State('parameter-table-porosity_coef', 'rowData')
)
def update_table_porosity_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-gas_saturation_coef', 'columnDefs'),
    Input('parameter-table-gas_saturation_coef', 'cellValueChanged'),
    State('parameter-table-gas_saturation_coef', 'rowData')
)
def update_table_gas_saturation_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-permeability', 'columnDefs'),
    Input('parameter-table-permeability', 'cellValueChanged'),
    State('parameter-table-permeability', 'rowData')
)
def update_table_permeability(cell, rowData):
    return update_table_columns(cell, rowData)



@callback(
    output=[
        Output('output-table', "children"),
        Output('tornado-diagram', "children"),
        Output('ecdf-diagram', "children"),
        Output('pdf-diagram', 'children'),
        Output('parameter-table-output_calcs', 'rowData'),
        Output('persistence_storage', 'data', allow_duplicate=True),
    ],
    
    inputs=[
        Input("calculate_reserves_button", "n_clicks"),
        State('parameter-table-area', 'rowData'),
        State('parameter-table-effective_thickness', 'rowData'),
        State('parameter-table-porosity_coef', 'rowData'),
        State('parameter-table-gas_saturation_coef', 'rowData'),
        State('parameter-table-calcs', 'rowData'),
        State('parameter-table-output_calcs', 'rowData'),
        State('persistence_storage', 'data'),
    ],
    prevent_initial_call=True,
    )
def calculate_gas_reserves(n_clicks: int,
                           p_area: list[dict],
                           p_effective_thickness: list[dict],
                           p_porosity_coef: list[dict],
                           p_gas_saturation_coef: list[dict],
                           params: list[dict],
                           add_params: list[dict],
                           storage_data: dict):
    if p_area is None or p_area[0]['distribution'] == 'Площадь':
        raise PreventUpdate
    area_value, area = *parse_params(dist_dict[p_area[0]['distribution']], p_area[0]),
    et_value, effective_thickness = *parse_params(dist_dict[p_effective_thickness[0]['distribution']], p_effective_thickness[0]),
    pc_value, porosity_coef = *parse_params(dist_dict[p_porosity_coef[0]['distribution']], p_porosity_coef[0]),
    gsc_value, gas_saturation_coef = *parse_params(dist_dict[p_gas_saturation_coef[0]['distribution']], p_gas_saturation_coef[0]),
    


    stat_params={
        "area": area,
        "effective_thickness": effective_thickness,
        "porosity_coef": porosity_coef,
        "gas_saturation_coef": gas_saturation_coef
    }
    params_df = pd.DataFrame(params)
    params_df = params_df.set_index(['parameter'])

    init_data={
        "area": area_value,
        "effective_thickness": et_value,
        "porosity_coef": pc_value,
        "gas_saturation_coef": gsc_value,
        "init_reservoir_pressure": params_df.loc[varnames['init_reservoir_pressure'], 'value'],
        "relative_density": params_df.loc[varnames['relative_density'], 'value'],
        "reservoir_temp": params_df.loc[varnames['reservoir_temp'], 'value'],
        "num_of_vars": params_df.loc[varnames['num_of_vars'], 'value']
    }

    for el in add_params:
        var = el.get('parameter', None)
        val = el.get('value', None)
        if var is not None and val is not None:
            init_data[reversed_varnames[var]] = val

    
    input_data = make_input_data(pd.DataFrame(init_data, index=["value"], dtype=np.float64))
    stat_data = generate_stats(stat_params, np.int64(init_data['num_of_vars']))
    reserves = calculate_reserves(stat_data, input_data)
    df_affection = calculate_sensitivity(stat_data, input_data, reserves)
    df_affection.rename(index=varnames, inplace=True)
    tornado_fig = plot_tornado(df_affection)
    ecdf_fig = plot_ecdf_indicators(reserves, varnames['reserves'])
    pdf_fig = plot_pdf_indicators(reserves, varnames['reserves'])

    stat_data['geo_gas_reserves'] = reserves
    result_df = pd.DataFrame(
        columns=['P90', 'P50', 'P10'], 
        index=[
            varnames['geo_gas_reserves'], 
            varnames['area'], 
            varnames['effective_thickness'], 
            varnames['porosity_coef'], 
            varnames['gas_saturation_coef']
        ]
    )
    for var in result_df.index:
        result_df.loc[var, 'P90'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 10)
        result_df.loc[var, 'P50'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 50)
        result_df.loc[var, 'P10'] = st.scoreatpercentile(stat_data[reversed_varnames[var]], 90)


    res_table = [{'parameter': var, 'P90': result_df.loc[var, 'P90'], 'P50': result_df.loc[var, 'P50'], 'P10': result_df.loc[var, 'P10']} for var in result_df.index]

    output_data_columns = ['area_volume', 'pore_volume', 'temp_correction', 'critical_pressure',
                           'critical_temp', 'init_overcompress_coef', 'fin_overcompress_coef',
                           'geo_gas_reserves', 'dry_gas_init_reserves']

    output_data_calcs = [{'parameter': varnames[var], 'value': input_data.loc['value', var]} for var in output_data_columns]



    save_data = save_tab_reserves_calcs(storage_data=storage_data,
                                        field_name='Месторождение1',
                                        p_area=p_area,
                                        p_effective_thickness=p_effective_thickness,
                                        p_porosity_coef=p_porosity_coef,
                                        p_gas_saturation_coef=p_gas_saturation_coef,
                                        parameter_table_calcs=params,
                                        parameter_table_output_calcs=output_data_calcs,
                                        indics_calcs=res_table,
                                        tornado_diagram=tornado_fig,
                                        ecdf_plot=ecdf_fig,
                                        pdf_plot=pdf_fig)
    
    save_data = save_to_storage(storage_data=save_data, 
                                field_name='Месторождение1', 
                                tab='tab-production-indicators', 
                                prop='parameter_table_effective_thickness_indics',
                                data=[{
                                    'parameter': varnames['effective_thickness'],
                                    'P90': result_df.loc[varnames['effective_thickness'], 'P90'],
                                    'P50': result_df.loc[varnames['effective_thickness'], 'P50'],
                                    'P10': result_df.loc[varnames['effective_thickness'], 'P10'],
                                }])

    save_data = save_to_storage(storage_data=save_data, 
                                field_name='Месторождение1', 
                                tab='tab-production-indicators', 
                                prop='parameter_table_geo_gas_reserves_indics',
                                data=[{
                                    'parameter': varnames['geo_gas_reserves'],
                                    'P90': result_df.loc[varnames['geo_gas_reserves'], 'P90'],
                                    'P50': result_df.loc[varnames['geo_gas_reserves'], 'P50'],
                                    'P10': result_df.loc[varnames['geo_gas_reserves'], 'P10'],
                                }])
    

    prod_indics_data = get_value(storage_data=save_data,
                                 field_name='Месторождение1',
                                 tab='tab-production-indicators',
                                 prop='parameter_table_indics',
                                 default=None)
    
    keys = set(varnamesIndicators.keys()).intersection(varnames.keys())
    keys_input = ['init_reservoir_pressure', 'reservoir_temp', 'relative_density', 'init_overcompress_coef']
    keys_input_hide = ['critical_temp', 'critical_pressure']
    if prod_indics_data is None:
        prod_indics_data = []
        for var in keys_input:
            prod_indics_data.append({'parameter': varnamesIndicators[var], 'value': input_data.loc['value', var]})
    else:
        for row in prod_indics_data:
            if reversed_varnamesIndicators[row['parameter']] in set(keys_input):
                row['value'] = input_data.loc['value', reversed_varnamesIndicators[row['parameter']]]
            
    save_data = save_to_storage(storage_data=save_data, 
                                field_name='Месторождение1', 
                                tab='tab-production-indicators',
                                prop='parameter_table_indics',
                                data=prod_indics_data)
    
    prod_collapse_indics_data = get_value(storage_data=save_data,
                                 field_name='Месторождение1',
                                 tab='tab-production-indicators',
                                 prop='parameter_table_indics_collapse',
                                 default=None)
    
    if prod_collapse_indics_data is None:
        prod_collapse_indics_data = []
        for var in keys_input_hide:
            prod_collapse_indics_data.append({'parameter': varnamesIndicators[var], 'value': input_data.loc['value', var]})
    else:
        for row in prod_collapse_indics_data:
            if reversed_varnamesIndicators[row['parameter']] in set(keys_input_hide):
                row['value'] = input_data.loc['value', reversed_varnamesIndicators[row['parameter']]]
    
    save_data = save_to_storage(storage_data=save_data, 
                                field_name='Месторождение1', 
                                tab='tab-production-indicators',
                                prop='parameter_table_indics_collapse',
                                data=prod_collapse_indics_data)
        
    return [make_indics_table('Параметры', res_table, 'indics'), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=ecdf_fig), 
            dcc.Graph(figure=pdf_fig), 
            output_data_calcs,
            save_data,
        ]


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
        State('parameter-table-effective_thickness_indics', 'rowData'),
        State('parameter-table-geo_gas_reserves_indics', 'rowData'),     
        State('persistence_storage', 'data'),
    ],
    prevent_initial_call=True,
)
def calculate_production_indicators(n_clicks: int, 
                                    p_permeability: list[dict], 
                                    p_indics: list[dict], 
                                    p_indics_collapse: list[dict], 
                                    p_et: list[dict], 
                                    p_ggr: list[dict],
                                    storage_data: dict):
    
    if p_permeability is None or p_permeability[0]['distribution'] == 'Проницаемость':
        raise PreventUpdate

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


    effective_thickness_Pinds = [p_et[0]['P90'], p_et[0]['P50'], p_et[0]['P10']]
    geo_gas_reserves_Pinds = [p_ggr[0]['P90'], p_ggr[0]['P50'], p_ggr[0]['P10']]
    

    prod_kig_fig = None
    pressures_graphs = []
    results_list = []
    for eft, ggr, perm, name in zip(effective_thickness_Pinds, geo_gas_reserves_Pinds, permeability_Pinds, ['P10', 'P50', 'P90']):
        init_data['permeability'] = perm
        init_data['effective_thickness'] = eft
        init_data['geo_gas_reserves'] = ggr

        input_data = make_init_data_for_prod_indics(pd.DataFrame(init_data, index=["value"]))
        result = calculate_indicators(input_data.to_dict('records')[0])
        results_list.append(result.to_dict('records'))
        pressures_df = result[['current_pressure', 'wellhead_pressure', 'ukpg_pressure']]
        pressures_df['downhole_pressure'] = result['current_pressure'] - input_data.loc['value', 'max_depression']
        pressures_graphs.append(plot_pressure_on_production_stages(pressures_df, name))
        prod_kig_fig = plot_summary_chart(prod_kig_fig, result[['annual_production', 'kig', 'n_wells']], name)
    

    pressures_fig = plot_united_pressures(pressures_graphs)

    save_data = save_tab_production_indicators(storage_data=storage_data,
                                               field_name='Месторождение1',
                                               p_permeability=p_permeability,
                                               parameter_table_indics=p_indics,
                                               parameter_table_effective_thickness_indics=p_et,
                                               parameter_table_geo_gas_reserves_indics=p_ggr,
                                               parameter_table_indics_collapse=p_indics_collapse,
                                               prod_calcs_table=results_list,
                                               pressures_on_stages_plot=pressures_fig,
                                               prod_kig_plot=prod_kig_fig)
    return [results_list, 
            dcc.Graph(figure=pressures_fig), 
            dcc.Graph(figure=prod_kig_fig), 
            save_data]