# run this script after the flask server is running.
import pprint

import requests

resp = requests.get(
    'http://127.0.0.1:5000/search', params={'invest_type': 'dem'})
resp.raise_for_status()
pprint.pprint(resp.json())
