import base64
import json
import os

from dash import callback, Output, Input, State, ALL, ctx, no_update, clientside_callback

from src.constants import EXCEL_TEMPLATE_PATH, OUTPUT_EXCEL_PATH
from src.excel_report.prepare_data import make_data_to_excel
from src.excel_report.create import create_report
from src.layouts.menu import *
from src.utils import appropriate_name



clientside_callback(
    """
    function(n_clicks, is_open) {
        if (n_clicks !== null) {
            return !is_open;
        }
        return is_open;
    }
    """,
Output('add_field_modal', 'is_open', allow_duplicate=True),

    Input('open_field_modal', 'n_clicks'),
    State('add_field_modal', 'is_open'),
    prevent_initial_call=True
)



@callback(
    Output('add_field_modal', 'is_open', allow_duplicate=True),
    Output('menu_nav', 'children', allow_duplicate=True),
    Output('persistence_storage', 'data', allow_duplicate=True),

    Input('add_field', 'n_clicks'),
    State('field_name', 'value'),
    State('menu_nav', 'children'),
    State('persistence_storage', 'data'),

    prevent_initial_call=True
)
def add_field_modal(n_clicks, field_name: str, field_items: list[dict], storage_data: dict):
    fields_list = []
    for field in field_items:
        fields_list.append(field['props']['children'][0]['props']['children'][1]['props']['children'])

    if field_name is None:
        field_name = f'Месторождение{str(n_clicks)}'

    name_for_field = appropriate_name(field_name, fields_list)

    field_item = make_field_item(name_for_field)
    field_items.append(field_item)
    if storage_data:
        storage_data[name_for_field] = {}
    else:
        storage_data = {name_for_field: {}}
    return False, field_items, storage_data



@callback(
    Output('menu_nav', 'children'),

    Input('update_fields_btn', 'n_clicks'),
    State('persistence_storage', 'data')
)
def update_fields(n_clicks, storage_data):
    fields = []
    if storage_data:
        fields = [make_field_item(field_name) for field_name in storage_data]
    return fields



@callback(
    Output('persistence_storage', 'data', allow_duplicate=True),
    Output('update_fields_btn', 'n_clicks'),
    Output('load_save', 'contents'),

    Input('load_save', 'contents'),
    State('update_fields_btn', 'n_clicks'),
    prevent_initial_call=True
)
def load_save(contents, update_fields_btn):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        storage_data = json.loads(decoded)
        update_fields_btn = 1
        return storage_data, update_fields_btn, None
    return no_update, no_update, None



@callback(
    Output('download_save', 'data'),
    Input('save_btn', 'n_clicks'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def send_storage_data(n_clicks, storage_data):
    with open('save.json', 'w', encoding='utf-8') as file:
        json.dump(storage_data, file, ensure_ascii=False, indent=4)

    return dcc.send_file('save.json')



@callback(
    Output('menu_nav', 'children', allow_duplicate=True),
    Output('persistence_storage', 'data', allow_duplicate=True),
    Output('current_field', 'children', allow_duplicate=True),

    Input({'type': 'delete_item', 'index': ALL}, 'n_clicks'),
    State('menu_nav', 'children'),
    State('persistence_storage', 'data'),
    State('current_field', 'children'),
    prevent_initial_call=True
)
def delete_field(n_clicks:list[int], fields_list: list[dict], storage_data: dict, current_field: str):
    if ctx.triggered[0]['value']:
        field_id = ctx.triggered_id['index'][len('delete_'):]
        field_to_delete = dict()
        for field in fields_list:
            if field['props']['id'] == field_id:
                field_to_delete = field
                break

        field_to_delete_name = field_to_delete['props']['children'][0]['props']['children'][1]['props']['children']
        storage_data.pop(field_to_delete_name, None)
        if field_to_delete_name == current_field:
            current_field = ''

        fields_list.remove(field_to_delete)
        
    return fields_list, storage_data, current_field



@callback(
    Output({'type': 'open_field', 'index': ALL}, 'outline'),

    Input({'type': 'open_field', 'index': ALL}, 'n_clicks'),
    State('menu_nav', 'children'),
    prevent_initial_call=True
)
def open_field(n_clicks, fields_list):
    if ctx.triggered[0]['value']:
        field_btn = ctx.triggered_id['index']
        outline_list = [
            field['props']['children'][0]['props']['children'][1]['props']['id']['index'] != field_btn
            for field in fields_list
        ]
        return outline_list

    return no_update


@callback(
    Output('download_excel', 'data'),

    Input('excel_store_not_to_use', 'modified_timestamp'),
    State('persistence_storage', 'data'),
    prevent_initial_call = True,
)
def send_excel_report(timestamp, storage_data):
    excel_data = make_data_to_excel(storage_data=storage_data)

    create_report(excel_data=excel_data,
                  template_path=EXCEL_TEMPLATE_PATH,
                  output_path=OUTPUT_EXCEL_PATH)

    return dcc.send_file(OUTPUT_EXCEL_PATH)


@callback(

    Output('notification_store', 'data', allow_duplicate=True),
    Output('excel_store_not_to_use', 'data'),

    Input('download_btn', 'n_clicks'),
    State('persistence_storage', 'data'),
    prevent_initial_call = True,
)
def check_excel_template(n_clicks, storage_data):
    if not os.path.exists(EXCEL_TEMPLATE_PATH):
        return dict(is_open=True,
                    children='Не найден шаблон эксель отчёта. Проверьте наличие всех файлов.',
                    header='Ошибка подготовки отчёта',
                    icon='danger'), no_update

    return no_update, 1







@callback(
    Output('download_btn', 'disabled'),
    Output('save_btn', 'disabled'),

    Input('persistence_storage', 'modified_timestamp'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def disable_button(timestamp, storage_data):
    if storage_data is None or len(storage_data.keys()) == 0:
        return True, True
    return False, False

clientside_callback(
    """
    function(n_clicks, is_open) {
        if (n_clicks !== null) {
            return !is_open;
        }
        return is_open;
    }
    """,
    Output('menu', 'is_open'),
    Input('toggle_menu', 'n_clicks'),
    State('menu', 'is_open'),
    prevent_initial_call=True
)

@callback(
    Output('analyze_fields', 'disabled'),

    Input('persistence_storage', 'modified_timestamp'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def disable_comparison_button(timestamp, storage_data):
    if storage_data is None or len(storage_data.keys()) == 0:
        return True
    return False
