# Data Hub Abstraction Layer

## Problem Statement

Although we have a perfectly functional data hub, CKAN has its own abstractions
that don't have a 1:1 mapping to InVEST concepts of data.  It would be really
helpful to create an API layer that will allow a user of InVEST to interface
with our data hub using language that is native to InVEST.  So if someone is
looking for DEMs, they should be able to use DEMs from the data hub.

## Solution

The most direct solution here is to offer an API wrapper that will behave as a
sort of pass-through interface, returning the basic attributes needed for a
cursory evaluation of the dataset, such as the layer name, spatial coverage,
license type, and a link to a location to find out more information about the
layer on its source catalog.  Because our catalog already thinks in terms of
these datasets, this layer will likely be very simple.


## Future Work

### Search other data catalogs

With an abstraction layer like this, we have a real opportunity to search more
than just our CKAN instance, provided that

1. we are willing to put in the effort to interact with different catalogs
   (including authentication if needed)
2. we are able to discern the kinds of queries necessary to search these other
   catalogs.

It's worth noting that this approach is really only useful for searching
_catalogs_ and there are very likely datasets out there (e.g.
hydrosheds/hydrobasins/hydro-etc) that are statically hosted.  This intent of
this search is not to serve as a sort of index here.  Instead, we are merely
trying to provide a meta-search functionality.

Additionally, there's likely great value in starting with preexiting protocols
and known catalogs.  So by searching our CKAN catalog, we should be fairly
close to being able to search other CKAN catalogs.  Similarly, we should be
able to search OpenDataCube and STAC sites using consistent APIs, just with
perhaps custom semantic search criteria depending on how each resource
categorizes their datasets.

This work is _not_ intended to take the place of necessary data processing and
hosting efforts that we have going into the data hub.
