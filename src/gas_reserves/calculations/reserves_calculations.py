from src.gas_reserves.constants import PRES_STD_COND
from src.gas_reserves.process_input import *



def calculate_reserves(stat_data: pd.DataFrame, input_data: pd.DataFrame) -> pd.DataFrame:
    return (stat_data[['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef']].prod(axis=1)
            * 1e3 * input_data['init_reservoir_pressure']['value']
            * input_data['temp_correction']['value']
            / input_data['init_overcompress_coef']['value']
            / PRES_STD_COND)
    

def calculate_sensitivity(stat_data: pd.DataFrame, input_data: pd.DataFrame, reserves: pd.DataFrame) -> pd.DataFrame:
    df_sens = pd.DataFrame(dict(min=stat_data.min(), mean=stat_data.mean(), max=stat_data.max()))
    const_multiplier = (input_data['init_reservoir_pressure']['value']
                        * input_data['temp_correction']['value']
                        / input_data['init_overcompress_coef']['value']
                        / PRES_STD_COND)
    df_reserves_affection = pd.DataFrame(columns=['min', 'max'], index=df_sens.index)
    
    for var in df_sens.index:
        df_reserves_affection.loc[var, 'min'] = (reserves.mean()
                                                 - df_sens['min'][var]
                                                    * df_sens.loc[df_sens.index != var]['mean'].prod()
                                                    * const_multiplier
                                                    * 1e3)
        df_reserves_affection.loc[var, 'max'] = (df_sens['max'][var]
                                                 * df_sens.loc[df_sens.index != var]['mean'].prod()
                                                 * const_multiplier
                                                 * 1e3 - reserves.mean())
    
    df_affection = pd.DataFrame(dict(
        kmin=df_reserves_affection['min']/df_reserves_affection['min'].sum(),
        kmax=abs(df_reserves_affection['max'])/df_reserves_affection['max'].sum()
    )) 
    return df_affection

#|------------------------------------------------
#| init_data = {
#|     'area': <value>,
#|     'effective_thickness': <value>,
#|     'porosity_coef': <value>,
#|     'gas_saturation_coef': <value>,
#|     'init_reservoir_pressure': <value>,
#|     'relative_density': <value>,
#|     'reservoir_temp': <value>,
#|     'permeability': <value>,
#| }
#|
#| stat_data = {
#|     'area': dict,
#|     'effective_thickness': dict,
#|     'porosity_coef': dict,
#|     'gas_saturation_coef': dict
#| }
#|------------------------------------------------

