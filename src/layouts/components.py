from dash import html, dcc

from src.constants import disable_cell_color
from src.gas_reserves.constants import *
import dash_ag_grid as dag



def update_table_columns(cell, rowData):
    if cell and cell[0]['colId'] == 'distribution':
        base_columns = [
            {'headerName': 'Параметр', 'field': 'parameter', 'editable': True},
            {'headerName': 'Распределение', 'field': 'distribution', 'editable': True,
             'cellEditor': 'agSelectCellEditor',
             'cellEditorParams': {
                 'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
             },
            }
        ]

        additional_columns = []
        for row in rowData:
            distribution = row.get('distribution', 'Нормальное')
            if distribution == 'Нормальное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    
                ]
            elif distribution == 'Треугольное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                ]
            elif distribution == 'Равномерное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                ]
            elif distribution == 'Усечённое нормальное':
                additional_columns = [
                    {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Стандартное отклонение', 'field': 'std_dev', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True,
                     'hide': False, 'cellDataType': 'number'},
                    {'headerName': 'Мода', 'field': 'mode', 'editable': True,
                     'hide': True, 'cellDataType': 'number'},
                ]

        return base_columns + additional_columns


def distribution_input(name, id, placeholder, initial_data=None):
    initial_columns = []
    if initial_data is None or initial_data == []:
        initial_data = [
            {'parameter': name, 'distribution': placeholder}
        ]
        initial_columns = [
            {'headerName': 'Параметр', 'field': 'parameter', 'editable': False,
             'cellStyle': {'background-color': disable_cell_color}},
            {'headerName': 'Распределение', 'field': 'distribution', 'editable': True,
             'cellEditor': 'agSelectCellEditor',
             'cellEditorParams': {
                 'values': ['Нормальное', 'Равномерное', 'Треугольное', 'Усечённое нормальное']
             },
            },
            {'headerName': 'Мат. ожидание', 'field': 'mean', 'editable': True,
             'hide': True, 'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Ст. отклонение', 'field': 'std_dev', 'editable': True,
             'hide': True, 'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Мин. значение', 'field': 'min_value', 'editable': True,
             'hide': True, 'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Макс. значение', 'field': 'max_value', 'editable': True,
             'hide': True, 'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
            {'headerName': 'Мода', 'field': 'mode', 'editable': True, 'hide': True,
             'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
        ]
    else:
        initial_columns = update_table_columns([{'colId': 'distribution'}], initial_data)

    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=initial_columns,
        rowData=initial_data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "rowSelection": "single",
            "stopEditingWhenCellsLoseFocus": True,
        },
        columnSize='responsiveSizeToFit',
        style={'height': '108px'}
    )
    

def make_indics_table(name: str | None, data: list[dict], id: str, editable: bool = False):
    if data is None or len(data) == 0:
        data = [
            {'parameter': name, 'P90': None, 'P50': None, 'P10': None}
        ]
    columns = [
        {'headerName': 'Параметр', 'field': 'parameter', 'cellStyle': {'background-color': disable_cell_color}},
        {'headerName': 'P90', 'field': 'P90', 'cellDataType': 'number', 
            'editable': editable,
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"},
            'cellStyle': {'background-color': disable_cell_color if not editable else '#FFFFFF'},
        },
        {'headerName': 'P50', 'field': 'P50', 'cellDataType': 'number', 
            'editable': editable,
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"},
            'cellStyle': {'background-color': disable_cell_color if not editable else '#FFFFFF'},
        },
        {'headerName': 'P10', 'field': 'P10', 'cellDataType': 'number', 
            'editable': editable,
            'valueFormatter': {"function": f"{locale}.format(',.2f')(params.value)"},
            'cellStyle': {'background-color': disable_cell_color if not editable else '#FFFFFF'},
        },
    ]
    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=columns,
        rowData=data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions={
            "domLayout": "autoHeight",
            "rowSelection": "single",
        },
        columnSize='responsiveSizeToFit',
    )


def make_input_group(initial_data: list[dict], id: str, style: dict = None, editable_value: bool = True):
    
    initial_columns = [
        {'headerName': 'Параметр', 'field': 'parameter', 'cellStyle': {'background-color': disable_cell_color}},
        {'headerName': 'Значение', 'field': 'value', 'editable': editable_value, 'cellDataType': 'number',
            'valueFormatter': {"function": "d3.format('.3f')(params.value)"}},
    ]
    grid_options = {
        "rowSelection": "single",
        "stopEditingWhenCellsLoseFocus": True,
        "domLayout": "autoHeight"
    }

    if style:
        grid_options.pop('domLayout', None)

    return dag.AgGrid(
        id='parameter-table-'+id,
        columnDefs=initial_columns,
        rowData=initial_data,
        defaultColDef={"editable": False, "sortable": False, "filter": False},
        dashGridOptions=grid_options,
        columnSize='responsiveSizeToFit',
        style=style,
    )



