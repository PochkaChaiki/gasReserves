from dash import callback, Output, Input, State

from src.gas_reserves.constants import *
from src.utils import *

from src.layouts.comparison_analysis import make_comparison_analysis_page

import pandas as pd



@callback(
    Output('main-contents', 'children', allow_duplicate=True),

    Input('analyze_fields', 'n_clicks'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def analyze_fields(n_clicks, storage_data):
    df_values = pd.DataFrame(index=[ varnamesAnalysis['area'],
                                    varnamesAnalysis['study_coef'],
                                    varnamesAnalysis['uncertainty_coef'],
                                    varnamesAnalysis['annual_production'],
                                    varnamesAnalysis['distance_from_infra'],
                                    varnamesAnalysis['accumulated_production']
                                    ],
                             columns=list(storage_data.keys()))
    for field in storage_data:
        indics_calcs = get_value(storage_data,
                                 field_name=field,
                                 tab='tab-reserves-calcs',
                                 prop='indics_calcs',
                                 default=[])

        for row in indics_calcs:
            if row['parameter'] == varnamesAnalysis['area']:
                df_values.loc[varnamesAnalysis['area'], field] = row['P50']
                df_values.loc[varnamesAnalysis['uncertainty_coef'], field] = row['P90'] / row['P10']
                break

        study_coef = get_value(storage_data,
                               field_name=field,
                               tab='tab-risks-and-uncertainties',
                               prop='study_coef',
                               default=None)
        df_values.loc[varnamesAnalysis['study_coef'], field] = study_coef

        parameter_table_output_calcs = get_value(storage_data,
                                                  field_name=field,
                                                  tab='tab-reserves-calcs',
                                                  prop='parameter_table_output_calcs',
                                                  default=[])

        geo_gas_reserves = 0
        for row in parameter_table_output_calcs:
            if row['parameter'] == varnamesIndicators['geo_gas_reserves']:
                geo_gas_reserves = row['value']
                break

        prod_rate = 0
        parameter_table_indics = get_value(storage_data,
                                           field_name=field,
                                           tab='tab-production-indicators',
                                           prop='parameter_table_indics',
                                           default=[])
        for row in parameter_table_indics:
            if row['parameter'] == varnamesIndicators['prod_rate']:
                prod_rate = row['value']
                break

        df_values.loc[varnamesAnalysis['annual_production'], field] = prod_rate * geo_gas_reserves

        prod_calcs_table = get_value(storage_data,
                                     field_name=field,
                                     tab='tab-production-indicators',
                                     prop='prod_calcs_table',
                                     default=[])
        accumulated_production = 0
        for row in prod_calcs_table[1]:
            accumulated_production += row['annual_production']

        df_values.loc[varnamesAnalysis['accumulated_production'], field] = accumulated_production

        parameter_table_risks = get_value(storage_data,
                                          field_name=field,
                                          tab='tab-risks-and-uncertainties',
                                          prop='parameter_table_risks',
                                          default=[])
        distance_from_infra = 0
        for row in parameter_table_risks:
            if row['parameter'] == varnamesRisks['distance_from_infra']:
                distance_from_infra = row['value']
                break

        df_values.loc[varnamesAnalysis['distance_from_infra'], field] = distance_from_infra



    return make_comparison_analysis_page(df_values)
