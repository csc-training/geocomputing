# FORCE example & benchmarks

This is an example of using FORCE to process L1 Sentinel images to L2 using the **force-level2** command. FORCE documentation can be found here 

https://force-eo.readthedocs.io/en/latest/index.html

## Repository content

* **file_queue.txt** - the queue file that has all Sentinel images to be processed
* **LEVEL2_parameters.prm** - the parameter file which holds all processing related parameters. Remember to change the NPROC to number of CPUs you reserved
* **force_batch_job.sh** - the batch job file used to submit the job to Puhti

## Benchmarks

Processing 4 L1C Sentinel-images to L2A. Test images can be found from /appl/data/geo/sentinel/s2_example_data/L1C

relevant parameters in .prm file

**DO_TOPO = FALSE**
**NPROC = number of CPU you reserved in the batch job file**
**NTHREAD = 2**

### 4CPU

Nodes: 1
Cores per node: 4
CPU Utilized: 01:33:09
CPU Efficiency: 94.60% of 01:38:28 core-walltime
Job Wall-clock time: 00:24:37

### 8CPU

Nodes: 1
Cores per node: 8
CPU Utilized: 01:35:51
CPU Efficiency: 80.05% of 01:59:44 core-walltime
Job Wall-clock time: 00:14:58

### 16CPU

Nodes: 1
Cores per node: 16
CPU Utilized: 01:37:39
CPU Efficiency: 42.19% of 03:51:28 core-walltime
Job Wall-clock time: 00:14:28

# CONCLUSION

From the benchmark runs, it seems that **a good rule of thumb is that the optimal number of CPU cores is in maximum twice the amount of processed images.** In this example we had 4 images and 8 CPU cores produced 80% CPU efficiency, but 16 CPU cores only 42%. Maximum is one node in Puhti so 40 CPU cores. 

This example used approximately 34GB memory while processing 4 images at the same time. 

