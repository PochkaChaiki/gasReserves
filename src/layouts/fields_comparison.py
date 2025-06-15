import pandas as pd
from dash import html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from plotly.graph_objs import Figure

from src.layouts.comparison_analysis import make_analysis_table


# def make_fields_comparison_table(df_data: pd.DataFrame) -> dag.AgGrid:
#     columns = [
#         {'headerName': 'Параметр', 'field': 'parameter'},
#     ]
#     columns.extend([
#         {'headerName': field, 'field': field, 'cellDataType': 'number',
#          'valueFormatter': {"function": "d3.format('.3f')(params.value)"}}
#         for field in df_data.columns
#     ])
#     df_data['parameter'] = df_data.index
#     return dag.AgGrid(
#         id='analysis_results',
#         columnDefs=columns,
#         rowData=df_data.to_dict('records'),
#         defaultColDef={'editable': False, 'sortable': False, 'filter': False},
#         columnSize='responsiveSizeToFit',
#         dashGridOptions={
#             'domLayout': 'autoHeight',
#         }
#     )

def make_fields_comparison_page(options: list[str], selected: list[str], values: pd.DataFrame = None, fig: Figure = None) -> html.Div:
    return html.Div([
        dbc.Stack([
            dcc.Checklist(
                options=options,
                value=selected,
                id='fields_checklist',
                inline=True,
                labelStyle={"display": "flex", "flex-flow": "row nowrap", "gap": "0.5rem"},
                style={
                    "display": "flex",
                    "flex-flow": "row wrap",
                    "gap": "1rem",
                    "justify-content": "center",
                }
            ),
            html.Div([
                make_analysis_table(values.copy()),
            ], id='analysis_table'),
            html.Div(
                dcc.Graph(figure=fig, id="graph_fields")
            )
        ])
    ])