# PDAL

This folder includes example scripts for running PDAL on Roihu supercomputer. In Roihu, PDAL is included to 2 modules: [python-geo](https://docs.csc.fi/apps/python-geo/) and [qgis](https://docs.csc.fi/apps/qgis/). Exact versions and other details in [Roihu PDAL documentation](https://docs.csc.fi/apps/pdal/).

[PDAL](https://www.pdal.io/) is an open source command line application for point cloud translations and processing. PDAL's functionality is available via [PDAL commandline commands](https://pdal.io/apps/index.html) or [PDAL Python library](https://pdal.io/python.html#extend). 

The example show five options for working with PDAL

* Interactive
	* On login-node, mainly for `pdal info` and other quick and light commands.
	* On compute-node, as interactive job
* Simple batch job, suitable if calculation can not be parallized.
* Parallel batch jobs:
	* **xargs** parallel for one node (max 386 cores). If you need more than one node to process the files, it can be done with combining [xargs with array jobs](https://docs.csc.fi/support/tutorials/many/).
	* **Python**, for example with `multiprocessing` package for one node (max 386 cores). Python has also other [parallelization options](https://github.com/csc-training/geocomputing/tree/master/python/roihu). See Dask for multi-node example.
* (Another option could be pdal-wrench, which is available in qgis module. But it would require creation of Virtual Point Clouds from the input files. And the current PDAL installations do not have the tools for creating Virtual Point Clouds. If you need such installation, ask via servicedesk@csc.fi.)

The example detects ground returns using simple morphological filter (SMRF) and constructs a DEM from the ground points. 

Common files
* [pipeline.json](pipeline.json) - pdal pipeline/workflow to be run
* [filelist.txt](filelist.txt) - list of files to be processed
* data-folder with 4 .laz files created in the serial job.


## Interactive working on login-node
With `pdal info` it is often helpful to check the files, this is a light-weight task, so it can be done from login-node.

* Make PDAL commands available with [python-geo module](https://docs.csc.fi/apps/python-geo/)
```
module load python-geo
```
* Check a file with `pdal info`. 
```
pdal info /dataset/project_2019680/mml/laserkeilaus/2008_latest/2008/L413/1/L4131H3.laz
```

## Interactive working on compute-node
For computationally more demanding interactive working, use [interactive partition](https://docs.csc.fi/computing/running/interactive-usage/)

After the interactive job has started, load `python-geo` or `qgis`-module and then run `pdal`-commands.

## Batch jobs
Often the same PDAL pipelines (=workflows) need to be applied to a lot of files, then [batch jobs](https://docs.csc.fi/computing/running/creating-job-scripts-roihu/) should be used. 

## Serial batch job

In this script we prepare data (4 files) for the parallel examples. It runs the pipeline 4 times changing the crop area and output file using. The processing is done in a for loop, so the work is done serial manner (= no parallelization).

Files:
* [01_crop_pipeline.json](01_serial/01_crop_pipeline.json) - defines a PDAL pipeline for cropping a .laz file
* [01_split_laz.sh](01_serial/01_split_laz.sh) - 
* [01_serial_batch_job.sh](01_serial/01_serial_batch_job.sh) - 

1. Run the script in interactive session: 
```
module load python-geo
cd 01_serial
sbatch 01_serial_batch_job.sh
```

It creates new `data`-folder to the pdal folder, which the parallel exercises use as input.

## Parallel batch jobs
The parallel jobs below achieve the same result, but using different techinques. The Python set up is slightly more complicated, but gives the options to do something additional with Python.

### Parallel job with xargs

The goal is to run the DEM creation pipeline for 4 tiles. To achieve this, it is possible to override input and outputfiles in the pipeline using `--readers.las.filename` and `--writers.gdal.filename` switches with pdal pipeline command. For example:

`pdal pipeline --readers.las.filename=new_input_file --writers.gdal.filename=new_output_file pipeline.json`. 

Running the pipeline on multiple files can easily be done with xargs. xargs starts multiple calculation in parallel. 

Files:
* The common files: [pipeline.json](pipeline.json) and [filelist.txt](filelist.txt)
* [02_batch_job_xargs_parallel.sh](02_xargs_parallel/02_batch_job_xargs_parallel.sh) - the batch job script containts two parts:
	* The instructions to the batch job system marked with `#SBATCH`, these reserve computational resources from Roihu. Each `#SBATCH` option used is explained in the example
	* The instructions for data analysis in normal shell script style, including the 'xargs' for distribiuting the work to all available cores.

1. Submit the job: 

```
cd ../02_xargs_parallel
sbatch 02_batch_job_xargs_parallel.sh
```

2. Check computational resources used by your arrayjob: `seff <Job ID>`
3. Verify that all DEM files were successfully created.

2. Optinal, check resulting DEM with [QGIS](https://docs.csc.fi/apps/qgis/).


### Parallel job with Python multiprocessing

PDAL can also be used from a Python script. The advantage is that it enables to easily do some preprocessing with PDAL and then load the data into Python for further analysis or for example plotting.  

The script processes 4 files in parallel, with Python `multiprocessing` library.

Files: 
* The common files: [pipeline.json](pipeline.json) and [filelist.txt](filelist.txt)
* [03_python_pipeline_multiprocessing.py](03_python_multiprocessing_parallel/03_python_pipeline_multiprocessing.py)
* [03_batch_job_python.sh](03_python_multiprocessing_parallel/03_batch_job_python.sh)

1. Run the pipeline with batch job: 
```
cd 03_python_multiprocessing_parallel
sbatch 03_batch_job_python.sh`
```

2. Check computational resources used by your job: `seff <Job ID>`
3. Verify that all DEM files were successfully created.
