# Dask geopandas example
> Dask-GeoPandas is a project merging the geospatial capabilities of GeoPandas and scalability of Dask. GeoPandas is an open source project designed to make working with geospatial data in Python easier. GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types. Dask provides advanced parallelism and distributed out-of-core computation with a dask.dataframe module designed to scale pandas.

In this example, we will use finnish addresses (osoitteet), and based on post codes data, we will assign each address its post code. To do that, we will load two shapefiles from allas storage into GeoDataFrames and perform spatial join. In the end, we compare execution times of both dask-geopandas and plain geopandas.

Dask-geopandas documentation can be found [here](https://dask-geopandas.readthedocs.io/en/stable/).
