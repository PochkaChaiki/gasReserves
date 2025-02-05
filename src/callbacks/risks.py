from dash import callback, Output, Input, State, ALL, no_update, ctx

from src.gas_reserves.calculations.risks_and_uncertainties import prepare_values, prepare_weights, calculate_study_coef
from src.gas_reserves.constants import varnamesRisks, varnames
from src.utils import get_value, save_tab_risks_and_uncertainties

NO_DICT_UPDATE = dict(
    seismic_exploration_work = None,
    grid_density = None,
    core_research = None,
    c1_reserves = None,
    hydrocarbon_properties = None,
)

@callback(
    Output('study_coef', 'children'),
    Output('kriteria-seismic_exploration_work-table', 'rowData'),
    Output('kriteria-grid_density-table', 'rowData'),
    Output('kriteria-core_research-table', 'rowData'),
    Output('kriteria-c1_reserves-table', 'rowData'),
    Output('kriteria-hydrocarbon_properties-table', 'rowData'),
    Output('persistence_storage', 'data', allow_duplicate=True),

    Input('risks_btn', 'n_clicks'),
    State('kriteria-seismic_exploration_work-table', 'rowData'),
    State('kriteria-grid_density-table', 'rowData'),
    State('kriteria-core_research-table', 'rowData'),
    State('kriteria-c1_reserves-table', 'rowData'),
    State('kriteria-hydrocarbon_properties-table', 'rowData'),
    State('parameter-table-risks', 'rowData'),

    State('current_field', 'children'),
    State('persistence_storage', 'data'),
    prevent_initial_call = True,
)
def update_table_data(value,
                      seismic_exploration_work,
                      grid_density,
                      core_research,
                      c1_reserves,
                      hydrocarbon_properties,
                      risks_parameters_table,
                      current_field,
                      storage_data
                      ):

    if value is None:
        return tuple(no_update for _ in range(7))
    indics_calcs = get_value(storage_data=storage_data,
                                 field_name=current_field,
                                 tab='tab-reserves-calcs',
                                 prop='indics_calcs', default=None)
    if indics_calcs is None:
        return (value,seismic_exploration_work, grid_density,
                core_research, c1_reserves, hydrocarbon_properties,
                no_update)

    area = 0
    effective_thickness = 0
    for row in indics_calcs:
        if area == 0 and row['parameter'] == varnames['area']:
            area = row['P50']
        if effective_thickness == 0 and row['parameter'] == varnames['effective_thickness']:
            effective_thickness = row['P50']

    if area == 0 and effective_thickness == 0:
        return (value, seismic_exploration_work, grid_density,
                core_research, c1_reserves, hydrocarbon_properties,
                no_update)

    kriterias = dict(
        seismic_exploration_work = seismic_exploration_work[0]['kriteria'],
        grid_density = grid_density[0]['kriteria'],
        core_research = core_research[0]['kriteria'],
        c1_reserves = c1_reserves[0]['kriteria'],
        hydrocarbon_properties = hydrocarbon_properties[0]['kriteria'],
    )

    exploration_wells_amount = 0
    for row in risks_parameters_table:
        if row['parameter'] == varnamesRisks['exploration_wells_amount']:
            exploration_wells_amount = row['value']



    values = prepare_values(kriterias=kriterias,
                                area=area,
                                effective_thickness=effective_thickness,
                                exploration_wells_amount=exploration_wells_amount)

    weights = dict(
        seismic_exploration_work = seismic_exploration_work[0]['weight'],
        grid_density = grid_density[0]['weight'],
        core_research = core_research[0]['weight'],
        c1_reserves = c1_reserves[0]['weight'],
        hydrocarbon_properties = hydrocarbon_properties[0]['weight'],
    )

    prepared_weights = prepare_weights(weights)

    study_coef = calculate_study_coef(values, prepared_weights)

    seismic_exploration_work[0]['value'] = values['seismic_exploration_work']
    seismic_exploration_work[0]['weight'] = prepared_weights['seismic_exploration_work']

    grid_density[0]['value'] = values['grid_density']
    grid_density[0]['weight'] = prepared_weights['grid_density']

    core_research[0]['value'] = values['core_research']
    core_research[0]['weight'] = prepared_weights['core_research']

    c1_reserves[0]['value'] = values['c1_reserves']
    c1_reserves[0]['weight'] = prepared_weights['c1_reserves']

    hydrocarbon_properties[0]['value'] = values['hydrocarbon_properties']
    hydrocarbon_properties[0]['weight'] = prepared_weights['hydrocarbon_properties']

    save_data = save_tab_risks_and_uncertainties(
        storage_data=storage_data,
        field_name=current_field,
        parameter_table_risks=risks_parameters_table,
        kriteria_seismic_exploration_work_table=seismic_exploration_work,
        kriteria_grid_density_table=grid_density,
        kriteria_core_research_table=core_research,
        kriteria_c1_reserves_table=c1_reserves,
        kriteria_hydrocarbon_properties_table=hydrocarbon_properties,
        study_coef=study_coef,
    )

    return (study_coef, seismic_exploration_work, grid_density,
            core_research, c1_reserves, hydrocarbon_properties,
            save_data)
    # return value
