import logging

import commondatamodel
import requests
import yaml
from ckanapi import RemoteCKAN  # mamba install ckanapi

LOGGER = logging.getLogger(__name__)
CKAN_API_URL = 'https://data.naturalcapitalproject.stanford.edu'


# Objective: try out working with the CKAN API on our site to get a raster
# layer and also a vector layer of watersheds that has been filtered to a
# subset.
#    --> on-the-fly clipping of both seems important.
#    --> for vectors, let's try a FlatGeoBuf of hydrobasins vector (highest
#        level, level 12.  Alternatively, use the shorelines FGB because it has
#        lots of features (just shy of a million linestrings)
#
# 1: use existing search to get datasets for a specific type (e.g. DEM).
# 2: Extend results to allow a dataset to be subsetted.
#   --> Local caching?
#   --> VRTs?
#   --> What about vectors?
#
# Additional things to consider later on:
#   * how to integrate datatypes recorded in the InVEST model spec
#   * delayed loading and/or how to handle datasets that will need to be
#     fetched from a remote source.
#   * how to handle authentication across multiple sources (or maybe GDAL does
#     this implicitly?)


# map InVEST abstract type to the search query that matches
INVEST_TYPES = {
    'DEM': 'tags=DEM',
    'K_FACTOR': 'tags=SOIL+ERODIBILITY',
    # 'PRECIP': '',  # We don't yet have precip on the data hub
}
# Sanity check: make sure the INVEST types above match the enum in the common
# data model.
assert set(INVEST_TYPES.keys()) == set(
    k for k in dir(commondatamodel.InVESTInputType) if not k.startswith('_'))
ROWS_PER_SEARCH = 10


class InVESTDataset(object):
    def __init__(self, ckan_object, spatial_filter=None):
        self._ckan_data = ckan_object

        # Assume spatial filter is in the form (xmin, ymin, xmax, ymax)
        self.spatial_filter = spatial_filter

        # locate and load the geometamaker yaml file
        gmm_data = None
        for resource in self._ckan_data['resources']:
            if resource['description'] == 'Geometamaker YML':
                yml_text = requests.get(resource['url']).text
                gmm_data = yaml.load(yml_text, Loader=yaml.CLoader)
                assert isinstance(gmm_data, dict)

        self._gmm_data = gmm_data


class InVESTRaster(InVESTDataset):
    def __init__(self, *args, **kwargs):
        InVESTDataset.__init__(self, *args, **kwargs)

    def download(block=False):
        pass


def search(invest_type, bbox=None):
    """Search CKAN for the dataset of the target InVEST type.

    Args:
        invest_type (str): The InVEST datatype to search for.
            Case-insensitive.
        bbox (tuple, list): The bounding box to use, as a 4-tuple of (minx,
            miny, maxx, maxy).  If ``None``, spatial search will not be used.

    Returns:
        ``None``

    Yields:
        TODO
    """
    LOGGER.info(
        f"Searching CKAN with invest_type:{invest_type}; bbox:{bbox}")
    with RemoteCKAN(CKAN_API_URL) as catalog:
        offset = 0
        count = None
        while True:
            query_string = INVEST_TYPES[invest_type.upper()]

            extras = {}
            if bbox:
                extras['ext_bbox'] = ','.join(
                    (str(coord) for coord in bbox))

            result = catalog.action.package_search(
                q=query_string,
                start=offset,
                extras=extras,
            )
            if not count:
                count = result['count']
            for dataset in result['results']:
                yield commondatamodel.RasterLayer(
                    source_catalog_dataset_url=(
                        f'{CKAN_API_URL}/dataset/{dataset["name"]}'),
                    source_rest_data=dataset,
                    name=dataset['title'],
                    invest_type=invest_type,
                    license={
                        'id': dataset['license_id'],
                        'title': dataset['license_title'],
                        'url': dataset['license_url'],
                    },
                    description=dataset['notes'],
                )
                offset += 1

            if offset >= count:
                break


if __name__ == '__main__':
    #with RemoteCKAN(CKAN_API_URL) as catalog:
    #    results = catalog.action.package_search(rows=ROWS_PER_SEARCH,
    #                                            q=INVEST_TYPES['DEM'])
    for dataset in search('dem'):
        print(dataset.name)



# OK, what is a facet?? clearly a solr concept.
# Actually, not strictly solr, it's more of a general search concept.
# A facet is a way to group things, sort of like tags.
# For our purposes, I'm reading this as synonymous with tags.
