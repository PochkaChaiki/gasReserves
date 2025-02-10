import src.gas_reserves as gr
from pytest import *
import pytest
import pandas as pd
import plotly.graph_objects as go
import kaleido

class TestExcelReport:
    def test_create_report(self):
        data = {
            'Месторождение 1': {
                'stat_params': {
                    'area': {
                        'distribution': 'Нормальное',
                        'params': 'M = 12, s = 13',
                    },
                    'effective_thickness': {
                        'distribution': 'Треугольное',
                        'params': 'a = 12, b = 13, c = 0.4',
                    },
                    'porosity_coef': {
                        'distribution': 'Равномерное',
                        'params': 'a = 12, b = 13',
                    },
                    'gas_saturation_coef': {
                        'distribution': 'Нормальное усечённое',
                        'params': 'M = 12, s = 13, a = 10, b = 16',
                    },
                    'permeability': {
                        'distribution': 'Нормальное',
                        'params': 'M = 12, s = 13',
                    },
                },
                'init_data': {
                    'relative_density': 0.6348,
                    'reservoir_temp': 320.49,
                    'init_reservoir_pressure': 32.3,
                    'temp_correction': 92,
                    'init_overcompress_coef': 0.93,
                    'num_of_vars': 3000,
                },
                'prod_profile_init_data': {
                    'prod_rate': 5,
                    'operations_ratio': 1.05,
                    'reserve_ratio': 0.98,
                    'machines_num': 1,
                    'time_to_build': 6,
                    'well_height': 2700,
                    'pipe_diameter': 0.168,
                    'main_gas_pipeline_pressure': 4,
                    'abandon_pressure': 1.615,
                    'filtr_resistance_A': 0.000952,
                    'filtr_resistance_B': 0.000013,
                    'hydraulic_resistance': 0.019,
                    'trail_length': 2500,
                    'input_cs_temp': 310,
                },
                'profiles_report': pd.DataFrame(
                    {
                        'P10': {
                            'geo_gas_reserves': 12,
                            'effective_thickness': 12,
                            'porosity_coef': 12,
                            'gas_saturation_coef': 12,
                            'relative_density': 12,
                            'reservoir_temp': 12,
                            'init_reservoir_pressure': 12,
                            'temp_correction': 12,
                            'init_overcompress_coef': 12,
                            'annual_production': 12,
                            'accumulated_production': 12,
                            'kig': 12,
                            'num_of_wells': 12,
                            'years': 12,
                        },
                        'P50': {
                            'geo_gas_reserves': 13,
                            'effective_thickness': 13,
                            'porosity_coef': 13,
                            'gas_saturation_coef': 13,
                            'relative_density': 13,
                            'reservoir_temp': 13,
                            'init_reservoir_pressure': 13,
                            'temp_correction': 13,
                            'init_overcompress_coef': 13,
                            'annual_production': 13,
                            'accumulated_production': 13,
                            'kig': 13,
                            'num_of_wells': 13,
                            'years': 13,
                        },
                        'P90': {
                            'geo_gas_reserves': 14,
                            'effective_thickness': 14,
                            'porosity_coef': 14,
                            'gas_saturation_coef': 14,
                            'relative_density': 14,
                            'reservoir_temp': 14,
                            'init_reservoir_pressure': 14,
                            'temp_correction': 14,
                            'init_overcompress_coef': 14,
                            'annual_production': 14,
                            'accumulated_production': 14,
                            'kig': 14,
                            'num_of_wells': 14,
                            'years': 14,
                        },
                    }
                ),
                "images": {
                    "hist": go.Figure([go.Scatter(x=[1], y=[2])]).to_image(format='png'),
                    "tornado": go.Figure([go.Scatter(x=[1], y=[2])]).to_image(format='png'),
                    "profile": go.Figure([go.Scatter(x=[1], y=[2])]).to_image(format='png'),
                }
            }
        }
        gr.excel_report.create_report(data, 'Шаблон отчета.xlsx', 'Отчёт.xlsx')
        assert 1 == 1