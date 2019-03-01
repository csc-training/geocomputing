# PDAL

## Exercise 1. Extracting smaller area from .laz file
Throughout these exercises we will ALS data fron National Land Survey. We will use a part of the L4131H3 tile that covers Otaniemi area in Espoo. Because the tiles are quite large and take some time to process for the course it is more convinient to use smaller portions of data. In the first exercise we will extract four adjacent pieces from the L4131H3 tile. The original tile is already in Taito as part of shared gis data and can be found in ```/proj/ogiir-csc/mml/laserkeilaus/2008_17/2008/L413/1/L4131H3.laz```. We a ready made script in github we will use in this exercise so the first thing to do is download the exercise scripts.


1. Copy exercise zip from your local machine to Taito.
2. Login to Taito-shell
3. Load necessary modules (module load geo-env)
4. Go to your work directory and unzip exercise zip (cd $WRKDIR & unzip pdal_exercise.zip)
5. Go to the extracted pdal_exercise folder.

In order to extract smaller pieces of it we will use PDAL's crop filter. We have two necessary files for this exercise: crop\_pipeline.json and split\_laz.sh. Crop\_pipeline.json defines a pdal pipeline for cropping a .laz file and split\_laz.sh runs the pipeline 4 times changing the crop area and output file.

_crop\_pipeline.json_
``` json
{
  "pipeline":[
    "/proj/ogiir-csc/mml/laserkeilaus/2008_17/2008/L413/1/L4131H3.laz",
    {
      "type":"filters.crop",
      "bounds":"([379591,379978],[6673858,6674143])"
    },
    {
      "type":"writers.las",
      "filename":"output.laz"
    }
  ]
}
```

_split\_laz.sh_
``` bash
#Define origin for the first piece and piece size
origin_x=379190
origin_y=6673340
piece_size=400

#Extract four 400x400m pieces arranged in 2x2 grid
for x in 0 1
do
    for y in 0 1
    do
	#Calculate minx, max, miny, maxy coordinates for the tile 
        bb=($[$origin_x+$piece_size*$x] $[$origin_x+$piece_size*($x+1)] $[$origin_y+$piece_size*$y] $[$origin_y+$piece_size*($y+1)])
        #Call pdal pipeline. Note that the bounds paramter for crop filter gets overriden for each tile as well as filename for las writer.
	pdal pipeline crop_pipeline.json --filters.crop.bounds="([${bb[0]},${bb[1]]}],[${bb[2]},${bb[3]}])" --writers.las.filename=data/part_$x$y.laz

    done
done

```

5. Run the split\_laz.sh script (./split_laz.sh)
6. Check that smaller tiles were created in the data folder with ls command. You can also take a look at the files with ccViewer


## Exercise 2. Direct PDAL usage - Ground identification using SMRF
In this exercise we'll detect ground returns using simple morphological filter (SMRF), filter outliers and construct a DEM. In the first exercise we will use PDAL directly from taito-shell using JSON pipelines. Below you will find a ready made json pipeline. The same pipeline can be found in the exercise zip as _pipeline.json_ The aim of the first thing to do is simply get it running using PDAL from command line.

 1. Run the pipeline with pdal. Syntax: ```pdal pipeline pipeline.json```
 2. Check resulting dem with qgis
 3. Run the same pipeline for different input and output files (more files in data folder). To do this it is possible to override input and outputfiles in the pipeline using --readers.las.filename --writers.gdal.filename switches with pdal pipeline command. For example `pdal pipeline --readers.las.filename=data/part_01.laz --writers.gdal.filename=outputs/part_01.tif pipeline.json`. Ability to override input and outptufiles will come handy also in the next exercise when we start processing multiple files with array jobs.

_pipeline.json_
``` json
{
    "pipeline":[
        "data/part_00.laz",
        {
            "type":"filters.smrf",
            "window":33,
            "slope":1.0,
            "threshold":0.15,
            "cell":1.0
        },
        {
            "type":"filters.range",
            "limits":"Classification[2:2]"
        },
        {
            "type":"writers.gdal",
            "filename":"outputs/exercise1.tif",
            "output_type":"min",
            "resolution":1.0
        }
    ]
}

```

## Excercise 3. Parallelising PDAL usage with array jobs

When you want to run your pipeline on multiple files it can be done easily in Taito with array jobs. Array jobs are a way of running the same task multiple times for example for different input files. To use array jobs you need to submit your job through the batch job system rather than running it interactively in Taito-shell. In the second excercise the goal is to run the json pipeline created in the first excersize on 4 different files in parallel.

 1. Connect to taito login node
 2. Change to the excercise folder.
 3. There you will have a file called arrayjob.sh (also below). Take a look at how computational resources are reserved and how files are read from a filelist.csv file and processed with pdal.
 4. Submit the array job. Syntax: sbatch my_arrayjob.sh
 5. Check computational resources used by your arrayjob with seff <Job ID>
 6. Verify that all DEM files were successfully created
 7. Modify the arrayjob.sh and filelist.csv files to only process part00.laz and part10.laz files and save the outputs in a new folder.

_arrayjob.sh_ 

A batch job script containts two parts, first are the instructions to the batch job system marked with #SBATCH. After these rest of the file is normal shell script (same commands you would write to the terminal). Each #SBATCH option used is explained in the example script below. 

``` bash

#!/bin/bash -l
#Name of the job, this makes it easier to identify your job
#SBATCH -J batch_job_array

#Outputfile. Everything that would normally be printed into to the terminal when you run a program gets printed to this file. The %j refers to job number so that you don't overwrite the same file for each job
#SBATCH -o arrayjob_output/output_%j.txt

#As above but for error messages. It's however always not so clear what messages go to errors and what to output so it's always best to check both.
#SBATCH -e arrayjob_output/error_%j.txt

#Partition you want to submit your job to. Possible values are serial, parallel, longrun, hugemem and test. In this excerecise we use test as it is for testing, but it shouldn't be used for serious work. See [Taito user guide](https://research.csc.fi/taito-constructing-a-batch-job-file) for details. 
#SBATCH -p test

#Time limit for the job in hh:mm:ss, Once this amount of time has passed the job will be terminated regardless of weather it has finished.
#SBATCH -t 00:05:00

#Tells the batch job system that this is an array job that should be run 4 times. During each run the $SLURM_ARRAY_TASK_ID variable will get different value ranging from 1 to 4. This will be used to select different input files.
#SBATCH --array=1-4

#Tells the batch job system that this is not a parallel task and only one task should be used. Note that this is one task per job, but array job will actually launch 3 simultaneous jobs.
#SBATCH --ntasks=1

#Tells the batch job sytem to reserve 1000MB (1GB) of memory for each of the 3 jobs.
#SBATCH --mem-per-cpu=1000

#As the job is not run on the login where we submit the job from, it's necessary to load necessary modules in the batch job script. Loading the modules on login node will not help.
module load geo-env
#Change to the directory where you have the files

cd $WRKDIR/pdal_exercise
#Read the file to be processed from a list of input files. This is done by getting the line corresponding to the $SLURM_ARRAY_TASK_ID from the input file list.
input=$(sed -n "$SLURM_ARRAY_TASK_ID"p filelist.csv)

#Create output name from input by exchanging .laz to .tif and changing "data" to "outputs" in path.
name=$(echo "$input" | cut -f 1 -d '.')
output=outputs/$(echo "$name" | cut -f 2 -d '/').tif


#Run the pipeline as in previous exercise. Note that it is possible to override input and output files in your pipeline json from the commandline.
pdal pipeline --readers.las.filename=$input --writers.gdal.filename=$output pipeline.json
```


## Exercise 4. Index creation

Pdal provides a convinient tool tindex for creating index maps for pointcloud files. 
Usage: ```pdal tindex index.shp file\_pattern options```
To reduce computation time use ```--fast_boundary``` option. Without this pdal will check location of each point individually which will take longer.
File pattern means that all files matching the pattern will be included in the index. To match multiple files use * character. This character is interperted as any filename or part of file name. For example to include all files ending in .laz in current folder use pattern ```"*.laz"```. To include all files in some other folder use pattern ```"path/to/some/folder/*"```
1. Connect to taito-shell
2. Use the ```pdal tindex``` command to create an index shapefile of the four files created under data folder.


## Exercise 5. PDAL translate, Filtering example

When performing simple tasks it's sometimes a bit cumbersome to create separate pipeline files. The ```pdal_translate``` can be used to run operations directly from command line without constructing pipeline file. In this exercise the task is to compute height above ground and extract points that are above 2m from ground.
The syntax for pdal translate is as follows: ```pdal translate input-file output-file filters options-for-filters```

1. Replace Z coordinate with height above ground. You can use following command: ```pdal translate data/part_00.laz outputs/hag_00.laz hag ferry --filters.ferry.dimensions="HeightAboveGround=Z"``` In this example ```hag``` filter is used to compute height above ground. Because .laz files can't store custom attributes we use ```ferry``` filter to replace Z with HeightAboveGround before saving.
2. Use ```range``` filter to extract points with height above ground value (stored in Z) above 2m. The range filter takes limits option as: ```--filters.range.limits="Attribute[1:100]"``` Where Attribute is the name of the attribute used for filtering and the numbers between square brackets are lower and upper limits. If one of the limits can also be left out to leave one end of the range unlimited.
3. Check the resulting pointcloud with ccViewer
4. (Extra) It's also possible to combine multiple filters into one pdal translate command as was done with hag and ferry filters in the first step. Try to repeat the whole exercise with just one command combining hag ferry and range filters in correct order.


## Exercise 6. PDAL usage from a Python script

PDAL can also be used from inside a Python script. The advantage here is that it enables you to easily do some preprocessing with PDAL and then load the data into Python for further analysis or for example plotting. In third exercise we'll do just that by first doing ground classification using PDAL, after which we'll read the result into a Pandas data frame and plot the points. In taito Python support for PDAL has been installed with PDAL 1.5 version found in geo-env module.

1. Connect to Taito-shell
2. Load necessary modules (geo-env)
3. Run pdal\_ground.py script using python (python pdal\_ground.py)
4. Take a look at the plot you created (for example copy the plot to your local computer)


``` python
# -*- coding: utf-8 -*-
import pdal
import pandas as pd
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def pdal2df(pipelineJson):
    """
    Feed me a JSON pipeline, get back a Pandas dataframe with points in it.
    """
    jd = json.dumps(pipelineJson)
    pipeline = pdal.Pipeline(jd.decode('utf-8'))
    pipeline.validate() # check if our JSON and options were good
    pipeline.loglevel = 8 #really noisy
    count = pipeline.execute()
    arrays = pipeline.arrays
    arr = pipeline.arrays[0]
    description = arr.dtype.descr
    cols = [col for col, __ in description]
    df = pd.DataFrame({col: arr[col] for col in cols})
    
    return df
        

input_file="data/part_00.laz"

pipe_json={
    "pipeline":[
        input_file,
        {
            "type":"filters.smrf",
            "window":33,
            "slope":1.0,
            "threshold":0.15,
            "cell":1.0
        },
    ]
}

df = pdal2df(pipe_json)
print df

#Plot as 3d plot, green if ground red if not.
colors=['green' if c==2 else 'red' for c in df.Classification.tolist()]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df.X.tolist(),df.Y.tolist(),df.Z.tolist(), c=colors)
plt.savefig(inputfile.replace('data', 'plots').replace('laz','png'))
```
