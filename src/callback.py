from dash import Input, Output, State, callback

from src.layouts.components import *
from src.layouts.menu import make_field_item
from src.gas_reserves.excel_report import *

from src.excel_report import make_data_to_excel




@callback(
    Output('download_excel', 'data', allow_duplicate=True),
    Input('download_btn', 'n_clicks'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def send_excel_report(n_clicks, storage_data):
    excel_data = make_data_to_excel(storage_data=storage_data)
    create_report(data=excel_data,
                  template_path='Шаблон отчета.xlsx',
                  output_path='Отчёт.xlsx')
    
    return dcc.send_file('Отчёт.xlsx')


@callback(
    Output('menu', 'is_open'),

    Input('toggle_menu', 'n_clicks'),
    State('menu', 'is_open'),
)
def toggle_menu(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

