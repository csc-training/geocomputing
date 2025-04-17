* `zonal_stats_serial.py` is the basic version, here the work is done on one core in serial mode. 
* `zonal_stats_parallel.py` is the parallel version, where processing of polygons is split to several cores. For parallelization `multiprocessing` library is used.
* `zonal-stats-stac-parallel.py`is the parallel version, where statistics is calculated for several rastes found via STAC. For parallelization `dask` delayed functions are used.

Additionally batch job scripts are provided, for running this script on CSC's Puhti supercluster. For submitting the job to Puhti:
`sbatch batch_job_XX.sh`
