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

def make_list_group_item(group_name: str, options: list[str], values: list[str], table: pd.DataFrame):
    hashed_id = str(hash(group_name))

    return dbc.ListGroupItem([
        dbc.InputGroup(
            [
                dbc.Button(html.I(className='bi bi-trash'),
                           id={'type': 'delete_list_group_item', 'index': f'delete_{hashed_id}'},
                           color='danger',
                           ),
                dbc.InputGroupText(group_name),
            ]
        ),

        dbc.Stack([
            dcc.Checklist(
                options=options,
                value=values,
                id={'type': 'checkbox_fields', 'index': hashed_id},
                inline=True,
                labelStyle={"display": "flex", "flex-flow": "row nowrap", "gap": "0.5rem"},
                style={
                    "display": "flex",
                    "flex-flow": "row wrap",
                    "gap": "1rem",
                    "justify-content": "center",
                }
            ),
            html.Div(
                make_analysis_table(table),
                id={'type': 'table_of_group', 'index': hashed_id}
            ),
            ],
            gap=3
        )

    ], id=hashed_id)

def make_fields_comparison_page(options: list[str], groups: dict | None, values: dict[str, pd.DataFrame], fig: Figure = Figure()):
    return html.Div([
        dbc.Stack([
            dbc.InputGroup(
                [
                    dbc.Button("Добавить группу", id="add_group"),
                    dbc.Input(id="group_name", placeholder="Название группы"),
                ]
            ),
            dbc.ListGroup([

                make_list_group_item(group, options, groups[group], values[group])
                for group in groups ], id="fields_checklists"),
            # html.Div([
            #     make_analysis_table(values.copy()),
            # ], id='analysis_table'),
            html.Div(
                dcc.Graph(figure=fig, id="graph_fields")
            )
        ],
        gap=3)
    ])