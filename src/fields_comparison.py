import numpy as np
import pandas as pd
from plotly.graph_objs import Figure

from src.comparison_analysis import analyze_fields
from src.plot import plot_summary_chart
from src.utils import get_value
from src.constants import VARNAMES_ANALYSIS, VARNAMES_RISKS, VARNAMES_INDICATORS, VARNAMES

def compare_fields(storage_data: dict) -> dict:

    cols = ['P10', 'P50', 'P90']

    values = dict()

    for field in storage_data:
        df_values = pd.DataFrame(index=[VARNAMES_ANALYSIS['study_coef'],
                                        VARNAMES_ANALYSIS['uncertainty_coef'],
                                        VARNAMES_ANALYSIS['annual_production'],
                                        VARNAMES_ANALYSIS['accumulated_production'],
                                        VARNAMES_ANALYSIS['geo_gas_reserves']
                                        ],
                                 columns=cols)

        indics_calcs = get_value(storage_data,
                                 field_name=field,
                                 tab='tab-reserves-calcs',
                                 prop='indics_calcs',
                                 default=[])

        study_coef = get_value(storage_data,
                               field_name=field,
                               tab='tab-risks-and-uncertainties',
                               prop='study_coef',
                               default=None)

        parameter_table_indics = get_value(storage_data,
                                           field_name=field,
                                           tab='tab-production-indicators',
                                           prop='parameter_table_indics',
                                           default=[])

        prod_calcs_table = get_value(storage_data,
                                     field_name=field,
                                     tab='tab-production-indicators',
                                     prop='prod_calcs_table',
                                     default=[])


        for row in indics_calcs:
            if row['parameter'] == VARNAMES_ANALYSIS['area']:
                for index in cols:
                    df_values.loc[VARNAMES_ANALYSIS['uncertainty_coef'], index] = round(row['P90'] / row['P10'], 3)
            if row['parameter'] == VARNAMES['geo_gas_reserves']:
                for index in cols:
                    df_values.loc[VARNAMES['geo_gas_reserves'], index] = round(row[index], 3)

        study_coef = round(study_coef, 3) if study_coef is not None else study_coef
        for index in cols:
            df_values.loc[VARNAMES_ANALYSIS['study_coef'], index] = study_coef

        prod_rate = 0

        for row in parameter_table_indics:
            if row['parameter'] == VARNAMES_INDICATORS['prod_rate']:
                prod_rate = row['value']
                break

        for index in cols:
            df_values.loc[VARNAMES_ANALYSIS['annual_production'], index] = round(
                prod_rate * df_values.loc[VARNAMES_ANALYSIS['geo_gas_reserves'], index], 3)

        if len(prod_calcs_table):
            for i, index in enumerate(cols):
                accumulated_production = 0
                for row in prod_calcs_table[i]:
                    accumulated_production += row['annual_production']
                df_values.loc[VARNAMES_ANALYSIS['accumulated_production'], index] = round(accumulated_production, 3)

        values[field] = df_values.to_dict()
    return values


def take_selected_fields(values: dict, selected_fields: list[str]) -> pd.DataFrame:
    cols = ['P10', 'P50', 'P90']
    inds = [VARNAMES_ANALYSIS['study_coef'],
            VARNAMES_ANALYSIS['uncertainty_coef'],
            VARNAMES_ANALYSIS['annual_production'],
            VARNAMES_ANALYSIS['accumulated_production'],
            VARNAMES_ANALYSIS['geo_gas_reserves']]

    df_values = pd.DataFrame(data=[[1.0, 1.0, 1.0],
                                   [1.0, 1.0, 1.0],
                                   [0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0]],
                             index=inds,
                             columns=cols)

    if len(values.keys()) == 0:
        return df_values

    for field in selected_fields:
        df_field = pd.DataFrame.from_dict(values[field])  # YOU DID NOT CHECK IF FIELD IS PRESENT AT THIS MOMENT!
        for index in cols:
            field_study_coef = df_field.loc[VARNAMES_ANALYSIS['study_coef'], index]
            if pd.isnull(field_study_coef):
                field_study_coef = 0
            vals_study_coef = df_values.loc[VARNAMES_ANALYSIS['study_coef'], index]
            df_values.loc[VARNAMES_ANALYSIS['study_coef'], index] = field_study_coef \
                if field_study_coef < vals_study_coef else vals_study_coef

            field_uncertainty_coef = df_field.loc[VARNAMES_ANALYSIS['uncertainty_coef'], index]
            if pd.isnull(field_uncertainty_coef):
                field_uncertainty_coef = 1
            vals_uncertainty_coef = df_values.loc[VARNAMES_ANALYSIS['uncertainty_coef'], index]
            df_values.loc[VARNAMES_ANALYSIS['uncertainty_coef'], index] = field_uncertainty_coef \
                if field_uncertainty_coef < vals_uncertainty_coef else vals_uncertainty_coef

            geo_gas_reserves = df_field.loc[VARNAMES_ANALYSIS['geo_gas_reserves'], index]
            annual_production = df_field.loc[VARNAMES_ANALYSIS['annual_production'], index]
            accumulated_production = df_field.loc[VARNAMES_ANALYSIS['accumulated_production'], index]
            df_values.loc[VARNAMES_ANALYSIS['geo_gas_reserves'], index] += geo_gas_reserves if not pd.isnull(geo_gas_reserves) else 0
            df_values.loc[VARNAMES_ANALYSIS['annual_production'], index] += annual_production if not pd.isnull(annual_production) else 0
            df_values.loc[VARNAMES_ANALYSIS['accumulated_production'], index] += accumulated_production if not pd.isnull(accumulated_production) else 0

    return df_values


def plot_summary_charts_for_compare(storage_data: dict, groups: dict[str, list[str]]) -> Figure:
    if len(groups.keys()) == 0:
        return Figure()

    cols = ['annual_production', 'kig', 'n_wells']

    prod_kig_fig = None

    for i, (group_name, selected_fields) in enumerate(groups.items()):
        p90 = None
        for ind, field in enumerate(selected_fields):
            calcs_list = get_value(storage_data,
                                   field_name=field,
                                   tab='tab-production-indicators',
                                   prop='prod_calcs_table',
                                   default = [])

            if len(calcs_list) == 0:
                continue

            temp_p90 = pd.DataFrame.from_records(calcs_list[2])

            if p90 is None:
                p90 = temp_p90[cols]
            else:
                p90 = p90.add(temp_p90[['annual_production', 'n_wells']], fill_value=0)
                p90['kig'] = p90['kig'].add(temp_p90['kig'].reindex(p90.index, fill_value=1), fill_value=ind)

        if p90 is None:
            continue

        p90['kig'] = p90['kig'] / len(selected_fields)

        prod_kig_fig = plot_summary_chart(prod_kig_fig, p90, group_name, chart_colors_num=i, lines_full_name=True)

    return prod_kig_fig if prod_kig_fig else Figure()

