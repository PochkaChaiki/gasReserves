from dash import callback, Output, Input, State, ALL, ctx, no_update

from src.layouts.risks import render_risks_and_uncertainties
from src.layouts.single_page import *
from src.layouts.reserves_calcs import render_reserves_calcs
from src.layouts.production_profiles import render_production_indicators
from src.utils import *


@callback(
    Output('main-contents', 'children', allow_duplicate=True),
    Output('current_field', 'children', allow_duplicate=True),

    Input({'type': 'open_field', 'index': ALL}, 'n_clicks'),
    State('menu_nav', 'children'),
    Input('current_field', 'children'),
    prevent_initial_call=True
)
def show_main_contents(n_clicks, field_items, current_field):
    if len(ctx.triggered) == 1 and ctx.triggered_id and ctx.triggered[0]['value'] and isinstance(ctx.triggered_id, dict):
        field_name = ''
        hashed_id = ctx.triggered_id['index'][len('open_'):]
        for field in field_items:
            if field['props']['id'] == hashed_id:
                field_name = field['props']['children'][0]['props']['children'][1]['props']['children']
                break

        return make_main_contents(), field_name
    elif current_field and len(current_field) > 0:
            return no_update, no_update
    else:
        return make_front_page(), ''




@callback(
    Output('tabs-content', 'children'),
    Output('current_tab', 'children'),

    Input('tabs-calcs', 'value'),
    State('persistence_storage', 'data'),
    State('current_field', 'children'),
)
def render_content(tab, data, field_name):
    if tab == 'tab-reserves-calcs':
        values = get_tab(data, field_name, tab)
        return render_reserves_calcs(values), 'tab-reserves-calcs'
    elif tab == 'tab-production-indicators':
        values = get_tab(data, field_name, tab)
        return render_production_indicators(values), 'tab-production-indicators'

    elif tab == 'tab-risks-and-uncertainties':
        values = get_tab(data, field_name, tab)
        return render_risks_and_uncertainties(values), 'tab-risks-and-uncertainties'


# @callback(
#     Output('persistence_storage', 'data', allow_duplicate=True),

#     Input('tabs-calcs', 'value'),
#     State('persistence_storage', 'data'),
#     State('current_field', 'children'),
#     State('current_tab', 'children'),

#     State('kriteria-seismic_exploration_work-table', 'rowData'),
#     State('kriteria-grid_density-table', 'rowData'),
#     State('kriteria-core_research-table', 'rowData'),
#     State('kriteria-c1_reserves-table', 'rowData'),
#     State('kriteria-hydrocarbon_properties-table', 'rowData'),
#     State('parameter-table-risks', 'rowData'),
#     State('parameter-study_coef', 'rowData'),


#     State('parameter-table-area', 'rowData'),
#     State('parameter-table-effective_thickness', 'rowData'),
#     State('parameter-table-porosity_coef', 'rowData'),
#     State('parameter-table-gas_saturation_coef', 'rowData'),

#     State('parameter-table-calcs', 'rowData'),
#     State('parameter-table-output_calcs', 'rowData'),

#     State('parameter-table-permeability', 'rowData'),
#     State('parameter-table-indics', 'rowData'),
#     State('parameter-table-indics_collapse', 'rowData'),
#     State('parameter-table-stat_indics', 'rowData'),
#     prevent_initial_call=True
# )
# def keep_contents(tab: str, 
#                   storage_data: dict,
#                   current_field: str,
#                   current_tab: str,
#                   seismic_exploration_work,
#                   grid_density,
#                   core_research,
#                   c1_reserves,
#                   hydrocarbon_properties,
#                   risks_parameters_table,
#                   study_coef, 
#                   p_area: list[dict],
#                   p_effective_thickness: list[dict],
#                   p_porosity_coef: list[dict],
#                   p_gas_saturation_coef: list[dict],
#                   params: list[dict],
#                   add_params: list[dict],
#                   p_permeability: list[dict],
#                   p_indics: list[dict],
#                   p_indics_collapse: list[dict],
#                   p_stat_indics: list[dict],
#                   ):
#     if current_tab == 'tab-risks-and-uncertainties':
#         save_data = save_tab_risks_and_uncertainties(
#             storage_data=storage_data,
#             field_name=current_field,
#             parameter_table_risks=risks_parameters_table,
#             kriteria_seismic_exploration_work_table=seismic_exploration_work,
#             kriteria_grid_density_table=grid_density,
#             kriteria_core_research_table=core_research,
#             kriteria_c1_reserves_table=c1_reserves,
#             kriteria_hydrocarbon_properties_table=hydrocarbon_properties,
#             study_coef=study_coef,
#         )
#         return save_data
    
#     if current_tab == 'tab-reserves-calcs':
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'p_area',
#                                        p_area)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'p_effective_thickness',
#                                        p_effective_thickness)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'p_porosity_coef',
#                                        p_porosity_coef)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'p_gas_saturation_coef',
#                                        p_gas_saturation_coef)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'parameter_table_calcs',
#                                        params)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'parameter_table_output_calcs',
#                                        add_params)
#         return storage_data
    
#     if current_tab == 'tab-production-indicators':
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'p_permeability',
#                                        p_permeability)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'parameter_table_indics',
#                                        p_indics)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'parameter_table_stat_indics',
#                                        p_stat_indics)
#         storage_data = save_to_storage(storage_data, current_field, tab,
#                                        'parameter_table_indics_collapse',
#                                        p_indics_collapse)
#         return storage_data
    
#     return no_update