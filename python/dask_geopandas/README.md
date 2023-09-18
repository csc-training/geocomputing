# Dask geopandas example
> Dask-GeoPandas is a project merging the geospatial capabilities of GeoPandas and the scalability of Dask. GeoPandas is an open source project designed to make working with geospatial data in Python easier. GeoPandas extends the datatypes used by pandas to allow spatial operations on geometric types. Dask provides advanced parallelism and distributed out-of-core computation with a dask.dataframe module designed to scale pandas. 

In general, one can work with Dask-GeoDataFrames as they are regular GeoDataFrames. A good approach would be to start solving a problem using plain GeoPandas, because for small data problems, Dask-GeoPandas generates a significant overhead. Only after one would run into memory or performance issues with GeoPandas, they should switch to Dask-GeoPandas with one partition having less than 1GB of data in it.

Unfortunately, Dask-GeoPandas provides only a limited number of operations. Before using dask-geopandas, check if the method that you need is available in [Dask-GeoPandas](https://dask-geopandas.readthedocs.io/en/stable/api.html).

In this example, we will use Finnish addresses (osoitteet), and based on post code data, we will assign each address its post code. To do that, we will load two shapefiles into GeoDataFrames and perform a spatial join. In the end, we compare the execution times of both dask-geopandas and plain geopandas.

To launch this notebook in Puhti, you need JupyterLab with at least 5GB of memory and 4 cores.

### Documentation
- [Dask-geopandas documentation](https://dask-geopandas.readthedocs.io/en/stable/)
- [CSC Dask tutorial](https://docs.csc.fi/support/tutorials/dask-python/)
- [Jupyter in Puhti supercomputer](https://docs.csc.fi/computing/webinterface/jupyter/)
