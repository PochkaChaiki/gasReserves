import scipy.stats as st
import pandas as pd

DISTRIBUTIONS = {
    "norm": st.norm,
    "uniform": st.uniform,
    "triang": st.triang,
    "truncnorm": st.truncnorm,
}

'''
-------------------------------------------------------------------------------------------------------------------------|
    STAT_PARAM EXAMPLE:
        stat_params={
            'column': {
                'distribution': 'var', 
                'params': {
                    'loc': <value>, 
                    'scale': <value>
                    }, 
                'adds': {'param1': <value>}
            }
        }
-------------------------------------------------------------------------------------------------------------------------|
'''

def generate_stats(stat_params:dict, num_of_vars: int) -> pd.DataFrame:
    stat_data = pd.DataFrame(columns=list(stat_params.keys()))
    for var in stat_data.columns:
        generator = DISTRIBUTIONS[stat_params[var]['distribution']]
        loc, scale = tuple(stat_params[var]['params'].values())
        stat_data[var] = generator.rvs(*(stat_params[var]['adds'].values()), loc=loc, scale=scale, size=num_of_vars)

    return stat_data
