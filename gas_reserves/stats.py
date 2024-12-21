from gas_reserves.constants import *
import scipy.stats as st
import pandas as pd


#|-------------------------------------------------------------------------------------------------------------------------|
#| STAT_PARAM EXAMPLE:
#|   stat_params={'distribution': 'var', 'params': {'loc': <value>, 'scale': <value>}, 'adds': {'param1': <value>}}
#|-------------------------------------------------------------------------------------------------------------------------|


def generate_stats(stat_params:dict) -> pd.DataFrame:
    stat_data = pd.DataFrame(columns=['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef', 'permeability'])
    for var in stat_data.columns:
        generator = distributions[stat_params[var]['distribution']]
        loc, scale = tuple(stat_params[var]['params'].values())
        stat_data = generator.rvs(*(stat_params[var]['adds'].values()), loc=loc, scale=scale, size=amount_of_vars)

    stat_data['permeability'] = abs(stat_data['permeability'])
    return stat_data


def calculate_indicators(var: pd.DataFrame, stat_params:dict) -> list:
    generator = distributions[stat_params[var.columns[0]]['distribution']]

    var_p10 = generator.ppf(0.9, loc=var.mean(), scale=var.std())
    var_p50 = generator.ppf(0.5, loc=var.mean(), scale=var.std())
    var_p90 = generator.ppf(0.1, loc=var.mean(), scale=var.std())
    return [var_p10, var_p50, var_p90]