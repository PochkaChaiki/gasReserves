from dash import Output, Input, State, callback, ALL, MATCH, ctx, no_update
from plotly.graph_objs import Figure

from src.comparison_analysis import analyze_fields
from src.layouts.comparison_analysis import make_analysis_table
from src.layouts.fields_comparison import make_fields_comparison_page, make_list_group_item
from src.fields_comparison import compare_fields, plot_summary_charts_for_compare, take_selected_fields

from src.utils import appropriate_name


import pdb

@callback(
    Output('main-contents', 'children', allow_duplicate=True),
    Output('current_field', 'children', allow_duplicate=True),
    Output('for_fields_comparison', 'data'),

    Input('compare_fields', 'n_clicks'),
    State('persistence_storage', 'data'),
    State('for_fields_comparison_checkboxes', 'data'),
    prevent_initial_call=True
)
def compare_fields_callback(n_clicks, storage_data: dict, chkbxs: dict):
    # pdb.set_trace()
    opts = list(storage_data.keys())

    data = compare_fields(storage_data)
    fig: Figure = Figure()
    tables = dict()

    if chkbxs is None or isinstance(chkbxs, type(list())) or len(chkbxs.keys()) == 0:
        return make_fields_comparison_page(opts, dict(), tables, fig), 'Сравнение месторождений', data


    for group in chkbxs:
        table = take_selected_fields(data, chkbxs[group])
        tables[group] = table

    fig = plot_summary_charts_for_compare(storage_data, chkbxs)


    return make_fields_comparison_page(opts, chkbxs, tables, fig), 'Сравнение месторождений', data


@callback(
    Output('fields_checklists', 'children', allow_duplicate=True),
    Output('for_fields_comparison_checkboxes', 'data', allow_duplicate=True),

    Input({'type': 'delete_list_group_item', 'index': ALL}, 'n_clicks'),
    State('fields_checklists', 'children'),
    State('for_fields_comparison_checkboxes', 'data'),
    prevent_initial_call=True
)
def delete_group(n_clicks: list[int], groups_list: list[dict], groups_data: dict):

    if ctx.triggered[0]['value'] is not None:
        group_id = ctx.triggered_id['index'][len('delete_'):]
        group_to_delete = dict()
        for group in groups_list:
            if group['props']['id'] == group_id:
                group_to_delete = group
                break

        group_to_delete_name = group_to_delete['props']['children'][0]['props']['children'][1]['props']['children']
        groups_data.pop(group_to_delete_name, None)

        groups_list.remove(group_to_delete)

        return groups_list, groups_data
    return no_update, no_update


@callback(
    Output('fields_checklists', 'children', allow_duplicate=True),
    Output('for_fields_comparison_checkboxes', 'data', allow_duplicate=True),

    Input('add_group', 'n_clicks'),
    State('group_name', 'value'),
    State('fields_checklists', 'children'),
    State('for_fields_comparison_checkboxes', 'data'),
    State('persistence_storage', 'data'),

    prevent_initial_call=True
)
def add_group(n_clicks, group_name: str, groups_items: list[dict], groups_data: dict, storage_data: dict):
    if not ctx.triggered[0]['value']:
        return no_update, no_update

    groups_list = []
    for group in groups_items:
        groups_list.append(group['props']['children'][0]['props']['children'][1]['props']['children'])

    if group_name is None:
        group_name = f'Группа {str(n_clicks)}'

    name_for_group = appropriate_name(group_name, groups_list)

    group_item = make_list_group_item(name_for_group,
                                      list(storage_data.keys()),
                                      [],
                                      take_selected_fields({}, []))
    groups_items.append(group_item)
    if groups_data:
        groups_data[name_for_group] = []
    else:
        groups_data = {name_for_group: []}
    return groups_items, groups_data


@callback(
    Output('for_fields_comparison_checkboxes', 'data', allow_duplicate=True),

    Input({'type': 'checkbox_fields', 'index': ALL}, 'value'),
    Input('fields_checklists', 'children'),
    State('for_fields_comparison_checkboxes', 'data'),
    prevent_initial_call=True
)
def change_contents(selected_fields: list[str], groups_list: list, groups_data: dict):
    # print(f'change_contents: tr_id: {ctx.triggered_id}\n\ttr: {ctx.triggered}')

    if ctx.triggered[0]['value'] is not None and ctx.triggered_id != 'fields_checklists':
        group_id = ctx.triggered_id['index']
        group_element = dict()
        for group in groups_list:
            if group['props']['id'] == group_id:
                group_element = group
                break

        group_name = group_element['props']['children'][0]['props']['children'][1]['props']['children']
        groups_data[group_name] = ctx.triggered[0]['value']

        return groups_data

    return no_update


@callback(
    Output({'type': 'table_of_group', 'index': MATCH}, 'children', allow_duplicate=True),

    Input({'type': 'checkbox_fields', 'index': MATCH}, 'value'),
    State('for_fields_comparison', 'data'),
    prevent_initial_call=True
)
def change_contents_of_table(selected_fields: list[str], data: dict):
    # pdb.set_trace()
    table = take_selected_fields(data, selected_fields)

    return make_analysis_table(table)

@callback(
    Output('graph_fields', 'figure'),

    Input('for_fields_comparison_checkboxes', 'modified_timestamp'),
    State('for_fields_comparison_checkboxes', 'data'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def update_graph(t, groups_data, storage_data):
    # print(f"Trigger update_graph.\n\ttimestamp:{t} \n\tgroups_data:{groups_data}")
    fig = plot_summary_charts_for_compare(storage_data, groups_data)
    return fig