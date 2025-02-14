import os.path

from dash import Dash

from src.callbacks.production_profiles import *
from src.callbacks.reserves_calcs import *
from src.callbacks.menu import *
from src.callbacks.single_page import *
from src.callbacks.risks import *

from src.layouts.single_page import *

app = Dash(#external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           # assets_folder='assets',
           suppress_callback_exceptions=True)

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# app.config.assets_folder = 'assets'     # The path to the assets folder.
# app.config.include_asset_files = True   # Include the files in the asset folder
# app.config.assets_external_path = ""    # The external prefix if serve_locally == False
# app.config.assets_url_path = '/assets'  # the local url prefix ie `/assets/*.js`

app.layout = Layout

if __name__ == '__main__':
    if not os.path.exists('./~temp'):
        os.mkdir('./~temp')
    app.run(debug=True)