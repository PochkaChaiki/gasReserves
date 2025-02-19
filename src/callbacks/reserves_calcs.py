from dash import callback, Output, Input, State, ctx, no_update, dcc

from src.gas_reserves.process_input import *
from src.gas_reserves.stats import *
from src.constants import VARNAMES
from src.plot import *
from src.gas_reserves.calculations.reserves_calculations import *
from src.gas_reserves.calculations.prod_indicators import *

from src.layouts.components import make_indics_table, update_table_columns
from src.utils import *




# noinspection PyTupleAssignmentBalance
def _prepare_inputs(p_area: list[dict],
                   p_effective_thickness: list[dict],
                   p_porosity_coef: list[dict],
                   p_gas_saturation_coef: list[dict],
                   params: list[dict],
                   add_params: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    

    area_value, area = *parse_params(DIST_DICT[p_area[0]['distribution']],
                                     p_area[0]),
    et_value, effective_thickness = *parse_params(DIST_DICT[p_effective_thickness[0]['distribution']],
                                                  p_effective_thickness[0]),
    pc_value, porosity_coef = *parse_params(DIST_DICT[p_porosity_coef[0]['distribution']],
                                            p_porosity_coef[0]),
    gsc_value, gas_saturation_coef = *parse_params(DIST_DICT[p_gas_saturation_coef[0]['distribution']],
                                                   p_gas_saturation_coef[0]),

    stat_params={
        "area": area,
        "effective_thickness": effective_thickness,
        "porosity_coef": porosity_coef,
        "gas_saturation_coef": gas_saturation_coef
    }
    params_df = pd.DataFrame(params).set_index(['parameter'])

    init_data={
        "area": area_value,
        "effective_thickness": et_value,
        "porosity_coef": pc_value,
        "gas_saturation_coef": gsc_value,
        "init_reservoir_pressure": params_df.loc[VARNAMES['init_reservoir_pressure'], 'value'],
        "relative_density": params_df.loc[VARNAMES['relative_density'], 'value'],
        "reservoir_temp": params_df.loc[VARNAMES['reservoir_temp'], 'value'],
        "num_of_vars": params_df.loc[VARNAMES['num_of_vars'], 'value']
    }

    for el in add_params:
        var = el.get('parameter', None)
        val = el.get('value', None)
        if var is not None and val is not None:
            init_data[REVERSED_VARNAMES[var]] = val

    input_data = make_input_data(pd.DataFrame(init_data, index=["value"], dtype=np.float64))
    stat_data = generate_stats(stat_params, np.int64(init_data['num_of_vars']))

    return input_data, stat_data


def _calculate_reserves(input_data: pd.DataFrame,
              stat_data: pd.DataFrame
              ) -> tuple[pd.DataFrame, go.Figure, go.Figure, go.Figure]:
    reserves = calculate_reserves(stat_data, input_data)
    df_affection = calculate_sensitivity(stat_data, input_data, reserves)
    df_affection.rename(index=VARNAMES, inplace=True)
    tornado_fig = plot_tornado(df_affection)
    ecdf_fig = plot_ecdf_indicators(reserves, VARNAMES['geo_gas_reserves'])
    pdf_fig = plot_pdf_indicators(reserves, VARNAMES['geo_gas_reserves'])

    stat_data['geo_gas_reserves'] = reserves
    result_df = pd.DataFrame(
        columns=['P90', 'P50', 'P10'], 
        index=[
            VARNAMES['geo_gas_reserves'], 
            VARNAMES['area'], 
            VARNAMES['effective_thickness'], 
            VARNAMES['porosity_coef'], 
            VARNAMES['gas_saturation_coef']
        ]
    )
    for var in ('geo_gas_reserves', 'area', 'effective_thickness',
                'porosity_coef', 'gas_saturation_coef'):
        result_df.loc[VARNAMES[var], 'P90'] = st.scoreatpercentile(stat_data[var], 10)
        result_df.loc[VARNAMES[var], 'P50'] = st.scoreatpercentile(stat_data[var], 50)
        result_df.loc[VARNAMES[var], 'P10'] = st.scoreatpercentile(stat_data[var], 90)
    
    return result_df, tornado_fig, ecdf_fig, pdf_fig


def _save_data_to_profiles_tab(storage_data: dict,
                              field_name: str,
                              result_df: pd.DataFrame,
                              input_data: pd.DataFrame,
                              ) -> dict:

    pass_df = result_df.copy()
    pass_df = pass_df.drop(VARNAMES['area'])
    pass_data = [
        {'parameter': var,
         'P90': result_df.loc[var, 'P90'],
         'P50': result_df.loc[var, 'P50'],
         'P10': result_df.loc[var, 'P10']}
        for var in pass_df.index
    ]
    save_data = save_to_storage(storage_data=storage_data, 
                                field_name=field_name, 
                                tab='tab-production-indicators', 
                                prop='parameter_table_stat_indics',
                                data=pass_data)


    keys = dict(
        keys_input = ['init_reservoir_pressure', 'reservoir_temp', 'relative_density', 'init_overcompress_coef'],
        keys_input_hide = ['critical_temp', 'critical_pressure']
    )
    for prop, keys_to_add in zip(['parameter_table_indics', 'parameter_table_indics_collapse'],
                                 ['keys_input', 'keys_input_hide']):
        data: list[dict] = get_value(storage_data=storage_data,
                                     field_name=field_name,
                                     tab='tab-production-indicators',
                                     prop=prop,
                                     default=[])
        
        if len(data) == 0 or data == [{}]:
            data = []
            for var in keys[keys_to_add]:
                data.append({'parameter': VARNAMES_INDICATORS[var], 'value': input_data.loc['value', var]})
        else:
            for row in data:
                if REVERSED_VARNAMES_INDICATORS[row['parameter']] in set(keys[keys_to_add]):
                    row['value'] = input_data.loc['value', REVERSED_VARNAMES_INDICATORS[row['parameter']]]
        
        save_data = save_to_storage(storage_data=storage_data, 
                                    field_name=field_name, 
                                    tab='tab-production-indicators',
                                    prop=prop,
                                    data=data)
    return save_data



@callback(
    output=[
        Output('output-table', "children"),
        Output('tornado-diagram', "children"),
        Output('ecdf-diagram', "children"),
        Output('pdf-diagram', 'children'),
        Output('parameter-table-output_calcs', 'rowData', allow_duplicate=True),
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
        State('current_field', 'children'),
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
                           storage_data: dict,
                           current_field: str):
    
    if n_clicks is None or n_clicks == 0 or ctx.triggered_id != 'calculate_reserves_button':
        return [no_update for _ in range(6)]

# Processing input values to pass them to gas_reserves lib later ------------------------------------------------------------------------------------
    input_data, stat_data = _prepare_inputs(p_area=p_area,
                                           p_effective_thickness=p_effective_thickness,
                                           p_porosity_coef=p_porosity_coef,
                                           p_gas_saturation_coef=p_gas_saturation_coef,
                                           params=params,
                                           add_params=add_params)

# Making calculations -------------------------------------------------------------------------------------------------------------------------------
    result_df, tornado_fig, ecdf_fig, pdf_fig = _calculate_reserves(input_data=input_data,
                                                          stat_data=stat_data)


    res_table = [
        {'parameter': var,
         'P90': result_df.loc[var, 'P90'],
         'P50': result_df.loc[var, 'P50'],
         'P10': result_df.loc[var, 'P10']}
        for var in result_df.index
    ]

    output_data_columns = ['area_volume', 'pore_volume', 'temp_correction', 'critical_pressure',
                           'critical_temp', 'init_overcompress_coef', 'fin_overcompress_coef',
                           'geo_gas_reserves', 'dry_gas_init_reserves']

    output_data_calcs = [
        {'parameter': VARNAMES[var], 'value': input_data.loc['value', var]}
        for var in output_data_columns
    ]

# Save data for tab persistence ---------------------------------------------------------------------------------------------------------------------
    save_data = save_tab_reserves_calcs(storage_data=storage_data,
                                        field_name=current_field,
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

# Adding calculated earlier in reserves' calculation tab values to inputs of production indicators tab ----------------------------------------------
    save_data = _save_data_to_profiles_tab(storage_data=save_data,
                                          field_name=current_field,
                                          result_df=result_df,
                                          input_data=input_data)

    return [make_indics_table('Параметры', res_table, 'indics'), 
            dcc.Graph(figure=tornado_fig), 
            dcc.Graph(figure=ecdf_fig), 
            dcc.Graph(figure=pdf_fig), 
            output_data_calcs,
            save_data,
        ]


@callback(
    Output('parameter-table-area', 'columnDefs'),
    Input('parameter-table-area', 'cellValueChanged'),
    State('parameter-table-area', 'rowData'),
    prevent_initial_call = True
)
def update_table_area(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-effective_thickness', 'columnDefs'),
    Input('parameter-table-effective_thickness', 'cellValueChanged'),
    State('parameter-table-effective_thickness', 'rowData'),
    prevent_initial_call = True
)
def update_table_effective_thickness(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-porosity_coef', 'columnDefs'),
    Input('parameter-table-porosity_coef', 'cellValueChanged'),
    State('parameter-table-porosity_coef', 'rowData'),
    prevent_initial_call = True
)
def update_table_porosity_coef(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-gas_saturation_coef', 'columnDefs'),
    Input('parameter-table-gas_saturation_coef', 'cellValueChanged'),
    State('parameter-table-gas_saturation_coef', 'rowData'),
    prevent_initial_call = True
)
def update_table_gas_saturation_coef(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-permeability', 'columnDefs'),
    Input('parameter-table-permeability', 'cellValueChanged'),
    State('parameter-table-permeability', 'rowData'),
    prevent_initial_call = True
)
def update_table_permeability(cell, rowData):
    return update_table_columns(cell, rowData)


@callback(
    Output('parameter-table-output_calcs', 'rowData', allow_duplicate=True),
    Input('clear_main_output', 'n_clicks'),
    State('parameter-table-output_calcs', 'rowData'),
    prevent_initial_call=True
)
def clear_main_output(n_clicks, rowData):
    if rowData is None or rowData == []:
        return rowData

    for row in rowData:
        row['value'] = None
    return rowData