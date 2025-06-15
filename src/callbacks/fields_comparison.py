from dash import Output, Input, State, callback

from src.comparison_analysis import analyze_fields
from src.layouts.comparison_analysis import make_analysis_table
from src.layouts.fields_comparison import make_fields_comparison_page
from src.fields_comparison import compare_fields, plot_summary_charts_for_compare, take_selected_fields

import pandas as pd

@callback(
    Output('main-contents', 'children', allow_duplicate=True),
    Output('current_field', 'children', allow_duplicate=True),
    Output('for_fields_comparison', 'data'),

    Input('compare_fields', 'n_clicks'),
    State('persistence_storage', 'data'),
    State('for_fields_comparison_checkboxes', 'data'),
    prevent_initial_call=True
)
def compare_fields_callback(n_clicks, storage_data: dict, chkbxs: list[str]):

    opts = list(storage_data.keys())
    if chkbxs is None or len(chkbxs) == 0:
        chkbxs = opts

    data = compare_fields(storage_data)

    table = take_selected_fields(data, chkbxs)

    fig = plot_summary_charts_for_compare(storage_data, chkbxs)

    return make_fields_comparison_page(opts, chkbxs, table, fig), 'Сравнение месторождений', data


@callback(
    Output('analysis_table', 'children', allow_duplicate=True),
    Output('graph_fields', 'figure'),
    Output('for_fields_comparison_checkboxes', 'data', allow_duplicate=True),

    Input('fields_checklist', 'value'),
    State('for_fields_comparison', 'data'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def change_contents(selected_fields: list[str], data: dict, storage_data: dict):

    table = take_selected_fields(data, selected_fields)
    fig = plot_summary_charts_for_compare(storage_data, selected_fields)

    return make_analysis_table(table), fig, selected_fields