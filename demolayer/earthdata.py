import commondatamodel
import earthaccess

# Until we have a better way to do this, authenticate with:
#  import earthdata; earthdata.login(persist=True)

CATALOG_DATA = {
    'HOMEPAGE': 'https://earthdata.nasa.gov',
    'API_KEY_REQUIRED': True,
}


INVEST_TYPES = {
    'DEM': 'digital elevation model',
    'K_FACTOR': 'soil erodibility',
    # 'PRECIP': '',  # We don't yet have precip on the data hub
}
# Sanity check: make sure the INVEST types above match the enum in the common
# data model.
assert set(INVEST_TYPES.keys()) == set(commondatamodel.INVEST_TYPES)


def search(invest_type, bbox=None):
    kwargs = {
        'keyword': INVEST_TYPES[invest_type],
    }
    results = earthaccess.search_datasets(**kwargs)
    for result in results:
        import pdb; pdb.set_trace()
        pass


if __name__ == '__main__':
    for dataset in search('DEM'):
        print(dataset)
