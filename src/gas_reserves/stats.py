from src.gas_reserves.constants import *
import scipy.stats as st
import pandas as pd


#|-------------------------------------------------------------------------------------------------------------------------|
#| STAT_PARAM EXAMPLE:
#|   stat_params={'column: {'distribution': 'var', 'params': {'loc': <value>, 'scale': <value>}, 'adds': {'param1': <value>}}}
#|-------------------------------------------------------------------------------------------------------------------------|


def generate_stats(stat_params:dict, num_of_vars: int) -> pd.DataFrame:
    stat_data = pd.DataFrame(columns=stat_params.keys())
    for var in stat_data.columns:
        generator = distributions[stat_params[var]['distribution']]
        loc, scale = tuple(stat_params[var]['params'].values())
        stat_data[var] = generator.rvs(*(stat_params[var]['adds'].values()), loc=loc, scale=scale, size=num_of_vars)

    return stat_data


# def calculate_indicators(stat_params:dict) -> list[float]:
#     generator = distributions[stat_params['distribution']]

#     var_p10 = generator.ppf(0.9, *(stat_params['adds'].values()) ,loc=stat_params['params']['loc'], scale=stat_params['params']['scale'])
#     var_p50 = generator.ppf(0.5, *(stat_params['adds'].values()) ,loc=stat_params['params']['loc'], scale=stat_params['params']['scale'])
#     var_p90 = generator.ppf(0.1, *(stat_params['adds'].values()) ,loc=stat_params['params']['loc'], scale=stat_params['params']['scale'])
#     return [var_p10, var_p50, var_p90]

def calculate_percentiles(vars: pd.DataFrame) -> list:
    return st.scoreatpercentile(vars, [90, 50, 10])