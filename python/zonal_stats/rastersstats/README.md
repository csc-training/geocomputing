`zonal_stats_serial.py` is the more basic version, here the work is done on one core. 

`zonal_stats_parallel.py` is the more advanced version, here the work is done on 4 cores. To make processing multiple polygons faster we divide the calculation into parts and process them in parallel using `multiprocessing` library. 

Additionally a batch job scripts are provided, for running this script on CSC's Puhti supercluster. For submitting the job to Puhti:
`sbatch batch_job_XX.sh`