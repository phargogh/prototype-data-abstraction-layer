# run this script after the flask server is running.
import pprint

import requests

params = {
    'invest_type': 'dem',
    'bbox': [
        -126.56250000000001,
        25.190029755362676,
        -92.10937500000001,
        45.60250901510299,
    ],
}
resp = requests.get(
    'http://127.0.0.1:5000/search', params=params)
resp.raise_for_status()
data = resp.json()
print(data['catalogs_searched'])
for dataset in data['datasets']:
    print(dataset['name'], dataset['wgs84_extent'])
