# Alternatives

- OpenDAP: https://en.wikipedia.org/wiki/OPeNDAP (python client: https://github.com/pydap/pydap)
    - this looks to me to be a useful backend for accessing some well-known datasets, but it's still something we'd want to wrap due to its complexity.
    - What if we returned details of the steps needed to access the data and then we had a local download mechanism?
        - So the data returned from the layer is lazy
        - Download happens locally.
- pooch: https://www.fatiando.org/#pooch
    - this looks like it's great for downloading data with a number of different protocols (at least in python)


OK so there are clearly at least 2 practical pieces of this puzzle we need to think about:
- finding the dataset we are interested in
- Downloading the dataset (possibly processing if needed)

Some datasets have already been processed for distribution on the data hub, and
so the API should probably have an understanding of priority.  If a USGS
dataset, for example is already on the data hub, then we should procure from
that rather than reassemble the dataset from USGS from tiles (unless the data
hub is down or something)

So, given that, maybe I've been thinking about this API all wrong.  I've been
thinking about it as being a wrapper around other data catalogs, but it's
really dataset-centric and the sources, while important, are not what's really important.

The MVP of this service will be to return options, even if the same dataset is represented multiple times.

A later version of the service will have a single layer and multiple ways to procure it.
Getting to this point will require some work to avoid discrepancies in titles, citations, etc

Are there any other open source projects that do this?
Awesome lists, maybe
Nothing is really standing out, probably because doing this really well across multiple providers would take a lot of effort and isn't strictly necessary for the data to be useful.

Would it make sense to translate everything to STAC?


## 2025-08-15
I came across this article about a newish API for earthdata access: https://www.earthdata.nasa.gov/news/blog/earthaccess-earth-science-data-simplified
    - github page: https://github.com/nsidc

This to me feels like another example of an API that we should be able to interface with.
Depending on what this API returns (e.g. a stitched layer), we may need to do the stitching on our end and returning a stitched layer.

At this time, it does seem like intake might be helpful for the specific catalogs it supports, but it only supports 3 or 4 different catalogs.
- [ ] can we use intake to just get the raw files?  Or is it required to convert to xarray objects?




# Entities

A sketch doc of entities that we will use to interact with the API.

Data Hub constraints
- datasets may have several layers associated with them (e.g. year, different scenarios)

OpenTopography constraints
- DEMs only
- [ ] how much processing will be needed?
- [ ] Will they need to provide an API key?

Earthaccess/Earthdata:
- [ ] what InVEST-type datasets do they have that might be interesting?
    There are a whole lot of datasets there ... we'll need to figure out what will qualify as InVEST datasets
- [ ] how much processing will be needed on these relevant layers?

I'm running their demo featured in the earthaccess package docs to see how it works.
BOY is search slow.

OK maybe it's a little faster now.
Jupyter widgets built in are really pretty nice.
The demo layer (ATL08) resulted in a few H5 files downloaded.

Looks like their docs can use a little work, too.  Basic functionality is there, but even the earthdata.search_data() entrypoint isn't described.

If we use this in an abstraction layer, we will need to map different `short_name`s of datasets on EarthData to the various InVEST-centric data types that we have.

Looks like the `search_data()` function expects that you already know the dataset you want.  This is incongruous with the basic premise of InVEST that you will want to look for _some_ dataset of a type (e.g. LULC), but might not know what to use or look for.

Therefore, the `search_data()` function is useful when you already know what you want and you just need to download it from EarthData.

So what are our options here?
* Required: we need to decide which datasets on EarthData map to data we want people to be able to use through the abstraction layer.
* Choice: how to handle search
    * Option: we use EarthData's search, authenticated with the user's API key
    * Option: we preprocess all tiles from EarthData so that we know which bboxes map to which tiles so that we can implement our own search.
* Choice: how to provide data
    * Option: We use their EarthData API key to access the datasets where they are hosted
        * Depending on the data formats a tile/layer is stored in, we may need to help tile the layer appropriately.
    * Option: Since NASA data is generally open-access, we could just reprocess and host all the layers ourself on our data hub


VARIOUS STAC
To me, STAC feels like it's got all the spatial information needed to process data, but not all of the information needed about what datasets are in the location.
I guess I'm assuming that a single STAC catalog will have information about only one dataset, but that there might be a whole lot of tiles (e.g. for LANDSAT).
If that's the case, then we would be wise to point to the STAC itself and support operations for tiling the layer.


Use cases:

--> Searching for data for InVEST when you don't really know what to use
    --> We want to be able to offer a range of available datasets from various providers.
    --> We already know what the type of dataset we're looking for is going to be
    --> We already know how to transform (if needed) the dataset into a form that can be consumed by InVEST
        --> There may be some tiling/processing needed, along the lines of assembling local DEM from SRTM tiles.

--> Searching for data when you know exactly what you want to use, you just don't have it available locally.
    --> We should be able to use a specific dataset from one of these providers, even if it doesn't obviously match a known type or has not been verified as compatible by NatCappers
        --> maybe we provide a warning or something that veracity is up to the user




Obvious one: dataset
Attributes:
- abstract type (e.g. raster, vector, etc.)
- projection
- datatype (e.g. int32)
- filetype (e.g. geotiff)
- spatial bbox (in wgs84 or in requested coordinate system)
- url, obviously
- license string
- description?
- citation
- catalog page URL
- filesize
- procurement steps
    - Is a direct URL available?
    - Are further steps required/available, e.g. OpenDAP?
- [ ] how to do year/date of publication?
LATER: auth

What about aspatial tables?
Could work as a type of dataset, just without the spatial information (null in JS, None in python)


Credentials
Not required for all data portals, but definitely for some
- token (required for OpenTopography, token is free)





VERBS
/search (with params)
