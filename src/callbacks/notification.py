from dash import callback, Input, Output, State, no_update

from src.layouts.notification import make_new_notification


@callback(
    Output('notifications', 'children'),
    Output('notification_store', 'clear_data'),

    Input('notification_store', 'modified_timestamp'),
    State('notification_store', 'data'),

    prevent_initial_call=True
)
def push_notification(timestamp, data):
    if data is None:
        return no_update, no_update

    return make_new_notification(data), True