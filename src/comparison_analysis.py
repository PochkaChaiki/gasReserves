import pandas as pd

from src.utils import get_value
from src.constants import VARNAMES_ANALYSIS, VARNAMES_RISKS, VARNAMES_INDICATORS, VARNAMES


def analyze_fields(storage_data: dict) -> pd.DataFrame:
    df_values = pd.DataFrame(index=[VARNAMES_ANALYSIS['study_coef'],
                                    VARNAMES_ANALYSIS['uncertainty_coef'],
                                    VARNAMES_ANALYSIS['annual_production'],
                                    VARNAMES_ANALYSIS['distance_from_infra'],
                                    VARNAMES_ANALYSIS['accumulated_production'],
                                    VARNAMES_ANALYSIS['geo_gas_reserves']
                                    ],
                             columns=list(storage_data.keys()))
    for field in storage_data:
        indics_calcs = get_value(storage_data,
                                 field_name=field,
                                 tab='tab-reserves-calcs',
                                 prop='indics_calcs',
                                 default=[])

        for row in indics_calcs:
            if row['parameter'] == VARNAMES_ANALYSIS['area']:
                df_values.loc[VARNAMES_ANALYSIS['uncertainty_coef'], field] = round(row['P90'] / row['P10'], 3)
            if row['parameter'] == VARNAMES['geo_gas_reserves']:
                df_values.loc[VARNAMES['geo_gas_reserves'], field] = round(row['P50'], 3)
        study_coef = get_value(storage_data,
                               field_name=field,
                               tab='tab-risks-and-uncertainties',
                               prop='study_coef',
                               default=None)
        df_values.loc[VARNAMES_ANALYSIS['study_coef'], field] = round(study_coef, 3)


        prod_rate = 0
        parameter_table_indics = get_value(storage_data,
                                           field_name=field,
                                           tab='tab-production-indicators',
                                           prop='parameter_table_indics',
                                           default=[])
        for row in parameter_table_indics:
            if row['parameter'] == VARNAMES_INDICATORS['prod_rate']:
                prod_rate = row['value']
                break

        df_values.loc[VARNAMES_ANALYSIS['annual_production'], field] = round(
            prod_rate * df_values.loc[VARNAMES_ANALYSIS['geo_gas_reserves'], field], 3)

        prod_calcs_table = get_value(storage_data,
                                     field_name=field,
                                     tab='tab-production-indicators',
                                     prop='prod_calcs_table',
                                     default=[])
        accumulated_production = 0
        if len(prod_calcs_table):
            for row in prod_calcs_table[1]:
                accumulated_production += row['annual_production']

        df_values.loc[VARNAMES_ANALYSIS['accumulated_production'], field] = round(accumulated_production, 3)

        parameter_table_risks = get_value(storage_data,
                                          field_name=field,
                                          tab='tab-risks-and-uncertainties',
                                          prop='parameter_table_risks',
                                          default=[])
        distance_from_infra = 0
        for row in parameter_table_risks:
            if row['parameter'] == VARNAMES_RISKS['distance_from_infra']:
                distance_from_infra = row['value']
                break

        df_values.loc[VARNAMES_ANALYSIS['distance_from_infra'], field] = distance_from_infra


    return df_values.copy()


