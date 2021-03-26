# Dask examples

These are Python examples using the Dask library to parallelize the workload.

In these examples we use three Sentinel-2 satellite images as the dataset. They can be found in Puhti from location

/appl/data/geo/sentinel/s2_example_data/L2A

### Single node example

This example uses [delayed functions](https://docs.dask.org/en/latest/delayed.html) from Dask to parallelize the workload.

It can only utilize a single node in Puhti so the maximum number of workers/cpu cores is 40

You need to set your project to the batch job file, otherwise this example works out of the box.

### Multi-node example

This example uses the same delayed functions inside one node but also spreads the workload to several nodes through the [Dask-Jobqueue library](https://jobqueue.dask.org/en/latest/). The batch job file launches basically a master job that does not require much resources which then launches the worker jobs that queue for resources like any other work in Puhti.

