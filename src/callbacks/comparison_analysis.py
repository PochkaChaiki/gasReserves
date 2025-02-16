from dash import callback, Output, Input, State

from src.constants import *
from src.utils import *

from src.layouts.comparison_analysis import make_comparison_analysis_page
from src.comparison_analysis import analyze_fields




@callback(
    Output('main-contents', 'children', allow_duplicate=True),
    Output('current_field', 'children', allow_duplicate=True),

    Input('analyze_fields', 'n_clicks'),
    State('persistence_storage', 'data'),
    prevent_initial_call=True
)
def analyze_fields_callback(n_clicks, storage_data):
    df_values = analyze_fields(storage_data)

    return make_comparison_analysis_page(df_values), 'Сравнительный анализ'


