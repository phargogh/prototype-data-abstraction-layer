from flask import Flask

from . import ckan

app = Flask(__name__)


@app.route('/search')
def search():
    # pass in relevant search parameters, for example:
    #   Allowed catalogs (assume a default list)
    #   InVEST dataset type (e.g. DEM, watersheds)
    #   spatial extent in WGS84 # probably ignore until we fix on ckan
    pass

# Each dataset entity should have at least the following attributes:
#  * Source catalog
#  * the original catalog's REST data (for reference)
#  * Dataset name
#  * InVEST type
#  * License string/identifier
#  * Dataset description
#  * Source catalog page, for more information


@app.route('/download/<ds_id>')
def download(ds_id):
    pass

# How to run this flask server:
# TODO
