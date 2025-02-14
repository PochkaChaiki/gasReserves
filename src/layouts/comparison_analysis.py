from dash import html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd

from src.comparison_analysis import make_bubble_charts


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



def make_comparison_analysis_page(values: pd.DataFrame = None):

    return html.Div([
        html.Div([
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