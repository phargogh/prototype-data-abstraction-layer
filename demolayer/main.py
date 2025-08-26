import dataclasses
import json

import ckan
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/search', methods=['get'])
def search():
    # TODO: can we sort by InVEST-applicability?  E.g. layer can be directly
    # ingested vs requires preprocessing, etc.
    # pass in relevant search parameters, for example:
    #   Allowed catalogs (assume a default list)
    #   InVEST dataset type (e.g. DEM, watersheds)
    #   spatial extent in WGS84 # probably ignore until we fix on ckan

    invest_type = request.args['invest_type']

    found_data = [dataclasses.asdict(d) for d in ckan.search(invest_type)]
    return json.dumps({
        'catalogs_searched': [ckan.CKAN_API_URL],
        'datasets': found_data,
    })


@app.route('/download/<ds_id>')
def download(ds_id):
    pass

# How to run this flask server:
# python -m flask --app main run
