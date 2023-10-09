# Dask examples

These are Python examples using the Dask library to parallelize the workload.

In these examples we use three Sentinel-2 satellite images as the dataset. They can be found from Puhti in the location

__/appl/data/geo/sentinel/s2_example_data/L2A__

NDVI (The normalized difference vegetation index) will be calculated for each of the 3 satellite images 

### Single node example

This example uses [delayed functions](https://docs.dask.org/en/latest/delayed.html) from Dask to parallelize the workload.

It can only utilize a single node in Puhti so the maximum number of workers/cpu cores is 40

You need to set your project to the batch job file, otherwise this example works out of the box.

### Multi-node example

This example uses the same delayed functions inside one node but also spreads the workload to several nodes through the [Dask-Jobqueue library](https://jobqueue.dask.org/en/latest/).

The batch job file launches basically a master job that does not require much resources. It then launches the worker jobs that do the actual computing. The worker jobs are defined inside the multiple_nodes.py file. Note that they have to queue individually for resources so it is good idea to reserve enough time for the master job so it's not cancelled before the workers finish.

When the worker jobs finish, they will be displayd as CANCELLED on Puhti which is intended, the master job cancels them.

### Dask arrays in STAC example
[STAC example](../../STAC) shows how to use Dask arrays via xarray.


