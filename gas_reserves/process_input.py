import pandas as pd
import numpy as np
from gas_reserves.constants import *

#|-------------------------------------------------------------------------------------------------------------------------|
#| DATA EXAMPLE:
#|     init_data = {
#|         'area': 38_556 * 1e3,
#|         'effective_thickness': 11.10,
#|         'porosity_coef': 0.091,
#|         'gas_saturation_coef': 0.7,
#|         'init_reservoir_pressure': 32.30 * 1e6,
#|         'relative_density': 0.6348,
#|         'reservoir_temp': 320.49,
#|         'permeability': 0.75,
#|     }
#|-------------------------------------------------------------------------------------------------------------------------|


def make_input_data(init_data: pd.DataFrame) -> pd.DataFrame:
    mid_data = pd.DataFrame(columns=['area_volume', 'pore_volume', 'temp_correction', 'fin_reservoir_pressure', 'critical_pressure', 'critical_temp', 'init_overcompress_coef',
                                              'fin_overcompress_coef', 'geo_gas_reserves', 'dry_gas_init_reserves'])
    
    mid_data['area_volume']            = init_data['area'] * init_data['effective_thickness']
    mid_data['pore_volume']            = mid_data['area_volume'] * init_data['porosity_coef']
    mid_data['temp_correction']        = (zero_c_to_k * 2 + norm_temp_c) / (zero_c_to_k + init_data['reservoir_temp'] )
    mid_data['fin_reservoir_pressure'] = np.exp(1293 * 1e-9 * 2700 * init_data['relative_density']) / 1e6
    mid_data['critical_pressure']      = (4.892 - 0.4048 * init_data['relative_density'])
    mid_data['critical_temp']          = 94.717 + 170.8 * init_data['relative_density'] 
    mid_data['init_overcompress_coef'] = (0.4 * np.log10(init_data['reservoir_temp'] / mid_data['critical_temp']) + 0.73)**(init_data['init_reservoir_pressure'] / mid_data['critical_pressure']) + 0.1 * init_data['init_reservoir_pressure'] / mid_data['critical_pressure'] # Same question
    mid_data['fin_overcompress_coef']  = (0.4 * np.log10(init_data['reservoir_temp'] / mid_data['critical_temp']) + 0.73)**(mid_data['fin_reservoir_pressure'] / mid_data['critical_pressure']) + 0.1 * mid_data['fin_reservoir_pressure'] / mid_data['critical_pressure'] # Same question
    mid_data['geo_gas_reserves']       = init_data['area'] * init_data['effective_thickness'] * init_data['porosity_coef'] * init_data['gas_saturation_coef'] * init_data['init_reservoir_pressure'] / mid_data['init_overcompress_coef'] / pres_std_cond * mid_data['temp_correction']
    mid_data['dry_gas_init_reserves']  = mid_data['geo_gas_reserves'] * (100 - 0.012 - 0.003 - 0.012) / 100

    input_data = init_data.join(mid_data[np.setdiff1d(mid_data.columns, init_data.columns)])
    return input_data


