from dash import Input, Output, State, callback, ALL, dcc, ctx, no_update

from layout import *
from gas_reserves.plot import *
from gas_reserves.calculations.reserves_calculations import *
from gas_reserves.calculations.prod_indicators import *

from utils import *

from callbacks import *

@callback(
    Output('parameter-table-area', 'columnDefs'),
    Input('parameter-table-area', 'cellValueChanged'),
    State('parameter-table-area', 'rowData')
)
def update_table_area(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-effective_thickness', 'columnDefs'),
    Input('parameter-table-effective_thickness', 'cellValueChanged'),
    State('parameter-table-effective_thickness', 'rowData')
)
def update_table_effective_thickness(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-porosity_coef', 'columnDefs'),
    Input('parameter-table-porosity_coef', 'cellValueChanged'),
    State('parameter-table-porosity_coef', 'rowData')
)
def update_table_porosity_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-gas_saturation_coef', 'columnDefs'),
    Input('parameter-table-gas_saturation_coef', 'cellValueChanged'),
    State('parameter-table-gas_saturation_coef', 'rowData')
)
def update_table_gas_saturation_coef(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-permeability', 'columnDefs'),
    Input('parameter-table-permeability', 'cellValueChanged'),
    State('parameter-table-permeability', 'rowData')
)
def update_table_permeability(cell, rowData):
    return update_table_columns(cell, rowData)

@callback(
    Output('parameter-table-output_calcs', 'rowData', allow_duplicate=True),
    Input('clear_main_output', 'n_clicks'),
    State('parameter-table-output_calcs', 'rowData'),
    prevent_initial_call=True
)
def clear_main_output(n_clicks, rowData):
    if rowData is None or rowData == []:
        return rowData
    
    for row in rowData:
        row['value'] = None
    return rowData




