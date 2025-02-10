import pandas as pd
import plotly.graph_objects as go

from src.utils import get_value
from src.gas_reserves.constants import varnamesAnalysis, varnamesRisks, varnamesIndicators


def analyze_fields(storage_data: dict) -> pd.DataFrame:
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

    return df_values.copy()


def make_bubble_charts(values: pd.DataFrame,
                       y: str) -> go.Figure:

    fig = go.Figure()
    for field in values.columns:
        fig.add_trace(
            go.Scatter(
                x=[values.loc[varnamesAnalysis['area'], field]],
                y=[values.loc[varnamesAnalysis[y], field]],
                mode='markers',
                name=field,
                marker_size=values.loc[varnamesAnalysis['accumulated_production'], field] / 100,
            )
        )

    fig.update_layout(
        xaxis=dict(
            tickformat=".0f",  # Full Format
            title=dict(text=varnamesAnalysis['area'])
        ),
        yaxis=dict(
            title=varnamesAnalysis[y]
        )
    )

    return fig