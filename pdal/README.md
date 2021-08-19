# PDAL
[PDAL](https://www.pdal.io/) is an open source command line application for point cloud translations and processing. PDAL's functionality is available via [PDAL commandline commands](https://pdal.io/apps/index.html) or [PDAL Python library](https://pdal.io/python.html#extend). 

[Puhti PDAL documentation](https://docs.csc.fi/apps/pdal/)

## Interactive working 
With `pdal info` it is often helpful to check the files, this is a light-weight task, so it can be done from login-node without interactive session.

* Load [PDAL module](https://docs.csc.fi/apps/pdal/)
```
module load geoconda
```
* Check a file with `pdal info`. 
```
pdal info /appl/data/geo/mml/laserkeilaus/2008_latest/2008/L413/1/L4131H3.laz
```

For computationally more demanding interactive working, use [interactive partition](https://docs.csc.fi/computing/running/interactive-usage/)

## Batch jobs
Often the same PDAL pipelines (=workflows) need to be applied to a lot of files, then the [batch jobs](https://docs.csc.fi/computing/running/creating-job-scripts-puhti/) should be used. Main options in Puhti for working with a lot of files in parallel are:

* GNU parallel in one node (max 40 cores), GNU parallel should be favoured if processing one file takes less than 20 minutes. See exercise 3 below.
* Array jobs, could be favoured if processing one files takes several hours. See exercise 4 below
* If thousands of files need to be processed and processing of one file is relatively slow, it is possible to combine [GNU parallel with array jobs](https://docs.csc.fi/support/tutorials/many/)
* [Python parallezation options](https://github.com/csc-training/geocomputing/tree/master/python/puhti)

## PDAL exercises from a CSC course in 2019
(Updated to Puhti in 2021)

### Exercise 1. Extracting smaller area from .laz file
Throughout these exercises we'll use lidar data from Finnish National Land Survey. We'll use a part of the L4131H3 tile that covers Otaniemi area in Espoo. Because the tiles are quite large and take some time to process for the course it is more convinient to use smaller portions of data. In the first exercise we will extract four adjacent pieces from the L4131H3 tile. The original tile is already in Puhti as part of shared GIS data and can be found in `/appl/data/geo/mml/laserkeilaus/2008_latest/2008/L413/1/L4131H3.laz`. In this exercise we'll use a ready made script to extract four smaller pieces from the tile. In order to extract smaller pieces we will use PDAL's crop filter. We have two necessary files for this exercise: 

Files:
* [01_crop_pipeline.json](01_crop_pipeline.json) - defines a PDAL pipeline for cropping a .laz file
* [01_split_laz.sh](01_split_laz.sh) - runs the pipeline 4 times changing the crop area and output file using. The processing is done in a for loop, so the work is done serial manner (= no parallelization).

1. Run the script in interactive session: 
```
module load geoconda
bash 01_split_laz.sh
```

### Exercise 2. DEM creation with ground identification using SMRF for one file
In this exercise we'll detect ground returns using simple morphological filter (SMRF) and construct a DEM from the ground points. The workflow / pipeline is in [02_pipeline.json](02_pipeline.json) 

1. Run the pipeline in an interactive session: `pdal pipeline pipeline.json`
2. Optinal, check resulting DEM with [QGIS](https://docs.csc.fi/apps/qgis/).

### Excercise 3. DEM creation for several files in parallel with GNU parallel
Run the same DEM creation pipeline for all 4 tiles. To achieve this, it is possible to override input and outputfiles in the pipeline using `--readers.las.filename` and `--writers.gdal.filename` switches with pdal pipeline command. For example:

`pdal pipeline --readers.las.filename=new_input_file --writers.gdal.filename=new_output_file pipeline.json`. 

Running the pipeline on multiple files can easily be done with GNU parallel. GNU parallel starts multiple jobs in parallel, for example for different input files. To use GNU parallel you need to submit your job through the batch job system rather than running it interactively. 

Files:
* [02_pipeline.json](02_pipeline.json) - PDAL pipeline file, same as in Exercise 2
* [03_batch_job_gnu_parallel.sh](03_batch_job_gnu_parallel.sh) - the batch job script containts two parts:
	* the instructions to the batch job system marked with `#SBATCH`, these reserve computational resources from Puhti. Each `#SBATCH` option used is explained in the example
	* the instructions for data analysis in normal shell script style, including the 'gnu parallel' for distribiuting the work to all available cores.
* [03_filelist.csv](03_filelist.csv) - list of files to be processed

1. Submit the job: `sbatch 03_batch_job_gnu_parallel.sh`
2. Check computational resources used by your arrayjob: `seff <Job ID>`
3. Verify that all DEM files were successfully created.


### Excercise 4. DEM creation for several files in parallel with array job
Run the same DEM creation pipeline for all 4 tiles with array job. Array job is alternative to running jobs in parallel with GNU parallel.

Files:
* [02_pipeline.json](02_pipeline.json) - PDAL pipeline file, same as in Exercise 2 and 3
* [04_batch_job_array.sh](04_batch_job_array.sh) - the batch job script containts two parts:
	* the instructions to the batch job system marked with `#SBATCH`, these reserve computational resources from Puhti. 
	* the instructions for data analysis in normal shell script style, including the array job style distribiuting of work.
* [03_filelist.csv](03_filelist.csv) - list of files to be processed, same as in Exercise 3

1. Submit the job: `sbatch 03_batch_job_array.sh`
2. Check computational resources used by your arrayjob: `seff <Job ID>`
3. Verify that all DEM files were successfully created.


### Exercise 5. PDAL translate, Filtering example
When performing simple tasks it's sometimes a bit cumbersome to create separate pipeline files. The ```pdal_translate``` can be used to run operations directly from command line without constructing pipeline file. In this exercise the task is to compute height above ground and extract points that are above 2m from ground.
The syntax for pdal translate is as follows: ```pdal translate input-file output-file filters options-for-filters```

1. Replace Z coordinate with height above ground. You can use following command: ```pdal translate data/part_00.laz outputs/hag_00.laz hag ferry --filters.ferry.dimensions="HeightAboveGround=Z"``` In this example ```hag``` filter is used to compute height above ground. We use ```ferry``` filter to replace Z with HeightAboveGround before saving.
2. Use ```range``` filter to extract points with height above ground value (stored in attribute Z) above 2m. The range filter takes limits option as: ```--filters.range.limits="Attribute[1:100]"``` Where Attribute is the name of the attribute used for filtering and the numbers between square brackets are lower and upper limits. If one of the limits can also be left out to leave one end of the range unlimited.
3. (Extra) It's also possible to combine multiple filters into one pdal translate command as was done with hag and ferry filters in the first step. Try to repeat the whole exercise with just one command combining hag ferry and range filters in correct order.


### Exercise 6. Index creation

Pdal provides a convinient tool tindex for creating index maps for pointcloud files. 
Usage: ```pdal tindex index.shp file_pattern options```
To reduce computation time use ```--fast_boundary``` option. Without this pdal will check location of each point individually which will take longer.
File pattern means that all files matching the pattern will be included in the index. To match multiple files use * character. This character is interperted as any filename or part of file name. For example to include all files ending in .laz in current folder use pattern ```"*.laz"```. To include all files in some other folder use pattern ```"path/to/some/folder/*"```
1. Use the ```pdal tindex``` command to create an index shapefile of the four files created under data folder.


### Exercise 7. PDAL usage from a Python script

PDAL can also be used from a Python script. The advantage is that it enables to easily do some preprocessing with PDAL and then load the data into Python for further analysis or for example plotting. In this exercise we'll do just that by first doing ground classification using PDAL, after which we'll read the result into a Pandas data frame and plot the points. 

* File: [07_pdal_ground.py](07_pdal_ground.py)

1. Run the pipeline in an interactive session: `python 07_pdal_ground.py`


