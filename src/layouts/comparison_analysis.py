from dash import html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

import pandas as pd
from plotly import graph_objects as go
from src.gas_reserves.constants import *



def make_analysis_table(df_data: pd.DataFrame):
    columns = [
        {'headerName': 'Параметр', 'field': 'parameter'},
    ]
    columns.extend([
        {'headerName': field, 'field': field, 'cellDataType': 'number',
         'valueFormatter': {"function": "d3.format('.3f')(params.value)"}}
        for field in df_data.columns
    ])
    df_data['parameter'] = df_data.index
    return dag.AgGrid(
        id='analysis_results',
        columnDefs=columns,
        rowData=df_data.to_dict('records'),
        defaultColDef={'editable': False, 'sortable': False, 'filter': False},
        columnSize='responsiveSizeToFit',
        dashGridOptions={
            'domLayout': 'autoHeight',
        }
    )

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

def make_comparison_analysis_page(values: pd.DataFrame = None):

    return html.Div([
        dbc.Container([
            make_analysis_table(values.copy())
        ], id='analysis_table'),
        dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=make_bubble_charts(values, 'study_coef'),
                    id='study_coef')),
                dbc.Col(dcc.Graph(
                    figure=make_bubble_charts(values, 'uncertainty_coef'),
                    id='uncertainty_coef')),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=make_bubble_charts(values, 'annual_production'),
                    id='annual_production')),
                dbc.Col(dcc.Graph(
                    figure=make_bubble_charts(values, 'distance_from_infra'),
                    id='distance_from_infra')),
            ])
        ], id='charts', fluid=True)
    ])