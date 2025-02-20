import dash_bootstrap_components as dbc

def make_new_notification(data: dict):
    return dbc.Toast(children=data.get('children', ""),
                     id="notification",
                     header=data.get('header', ''),
                     icon=data.get('icon', ''),
                     duration=10000,
                     dismissable=True,
                     is_open=data.get('is_open', False),
                     style={"position": "fixed", "top": '40px', "right": '10px', "width": '350px', 'z-index': '99'},
              ),